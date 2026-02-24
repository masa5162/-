import RssParser from "rss-parser";
import * as cheerio from "cheerio";
import crypto from "crypto";
import { NewsArticle, MaDeal, NewsSource, NewsCategory, Region, FetchResult } from "@/types";
import { NEWS_SOURCES, CHEMICAL_KEYWORDS, MA_INDICATORS } from "./sources";
import { saveNews, saveDeals, updateMeta } from "./store";

const rssParser = new RssParser({
  timeout: 15000,
  headers: {
    "User-Agent":
      "ChemicalMANewsBot/1.0 (Chemical Industry M&A News Aggregator)",
  },
});

function generateId(title: string, source: string): string {
  return crypto
    .createHash("md5")
    .update(`${title}-${source}`)
    .digest("hex")
    .substring(0, 12);
}

function classifyCategory(text: string): NewsCategory {
  const lower = text.toLowerCase();
  for (const indicator of MA_INDICATORS) {
    if (lower.includes(indicator.toLowerCase())) return "ma";
  }
  if (/\bipo\b|initial public offering|上場/i.test(lower)) return "ipo";
  if (/earnings|revenue|profit|決算|業績|収益/i.test(lower)) return "earnings";
  if (/regulat|compliance|法規|規制|コンプライアンス/i.test(lower)) return "regulation";
  if (/sustain|esg|green|carbon|環境|サステナ|脱炭素/i.test(lower)) return "sustainability";
  if (/innovat|r&d|research|patent|技術|研究|開発|特許/i.test(lower)) return "innovation";
  if (/market|price|demand|supply|需要|供給|市況|価格/i.test(lower)) return "market";
  return "other";
}

function isChemicalRelated(text: string): boolean {
  const lower = text.toLowerCase();
  return CHEMICAL_KEYWORDS.some((kw) => lower.includes(kw.toLowerCase()));
}

function extractCompanies(text: string): string[] {
  const companies: string[] = [];
  const majorCompanies = [
    "BASF", "Dow", "DuPont", "SABIC", "Sinopec", "Evonik",
    "Lanxess", "Covestro", "Solvay", "Arkema", "Eastman",
    "Celanese", "Huntsman", "Ashland", "LyondellBasell",
    "Mitsubishi Chemical", "Sumitomo Chemical", "Mitsui Chemicals",
    "Shin-Etsu Chemical", "Toray Industries", "Asahi Kasei",
    "LG Chem", "Lotte Chemical", "Wanhua Chemical",
    "三菱ケミカル", "住友化学", "三井化学", "信越化学工業",
    "東レ", "旭化成", "花王", "日東電工", "DIC", "JSR",
  ];
  for (const company of majorCompanies) {
    if (text.includes(company)) {
      companies.push(company);
    }
  }
  return companies;
}

function extractDealValue(text: string): string | undefined {
  const patterns = [
    /\$[\d,.]+\s*(billion|million|B|M|bn|mn)/i,
    /€[\d,.]+\s*(billion|million|B|M|bn|mn)/i,
    /£[\d,.]+\s*(billion|million|B|M|bn|mn)/i,
    /¥[\d,.]+\s*(兆|億|万)/,
    /[\d,.]+\s*(billion|million)\s*dollars/i,
    /[\d,.]+\s*億円/,
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) return match[0];
  }
  return undefined;
}

function extractTags(text: string): string[] {
  const tags: string[] = [];
  const tagPatterns: [RegExp, string][] = [
    [/specialty|特殊|スペシャルティ/i, "specialty-chemicals"],
    [/commodity|汎用/i, "commodity-chemicals"],
    [/pharma|医薬/i, "pharma"],
    [/agro|農薬|農業/i, "agrochemicals"],
    [/polymer|ポリマー|高分子/i, "polymers"],
    [/coating|塗料/i, "coatings"],
    [/adhesive|接着/i, "adhesives"],
    [/electric|battery|バッテリー|電池|EV/i, "ev-battery"],
    [/semicon|半導体/i, "semiconductors"],
    [/petro|石油/i, "petrochemicals"],
    [/sustain|green|脱炭素|グリーン/i, "sustainability"],
    [/cross.?border|クロスボーダー/i, "cross-border"],
  ];
  for (const [pattern, tag] of tagPatterns) {
    if (pattern.test(text)) tags.push(tag);
  }
  return tags;
}

async function fetchRssFeed(source: NewsSource): Promise<NewsArticle[]> {
  try {
    const feed = await rssParser.parseURL(source.url);
    const articles: NewsArticle[] = [];

    for (const item of feed.items || []) {
      const title = item.title || "";
      const summary = item.contentSnippet || item.content || "";
      const fullText = `${title} ${summary}`;

      if (!isChemicalRelated(fullText)) continue;

      const article: NewsArticle = {
        id: generateId(title, source.name),
        title,
        summary: summary.substring(0, 500),
        url: item.link || source.url,
        source: source.name,
        sourceRegion: source.region,
        category: classifyCategory(fullText),
        publishedAt: item.isoDate || new Date().toISOString(),
        fetchedAt: new Date().toISOString(),
        companies: extractCompanies(fullText),
        dealValue: extractDealValue(fullText),
        tags: extractTags(fullText),
      };

      articles.push(article);
    }

    return articles;
  } catch (error) {
    console.error(`Error fetching RSS from ${source.name}:`, error);
    return [];
  }
}

async function fetchWebSource(source: NewsSource): Promise<NewsArticle[]> {
  try {
    const response = await fetch(source.url, {
      headers: {
        "User-Agent":
          "ChemicalMANewsBot/1.0 (Chemical Industry M&A News Aggregator)",
      },
      signal: AbortSignal.timeout(15000),
    });

    if (!response.ok) return [];

    const html = await response.text();
    const $ = cheerio.load(html);
    const articles: NewsArticle[] = [];

    $("article, .story, .news-item, .article-item").each((_, element) => {
      const title =
        $(element).find("h2, h3, .headline").first().text().trim() || "";
      const summary =
        $(element).find("p, .summary, .description").first().text().trim() || "";
      const link = $(element).find("a").first().attr("href") || "";
      const fullText = `${title} ${summary}`;

      if (!title || !isChemicalRelated(fullText)) return;

      const fullUrl = link.startsWith("http")
        ? link
        : new URL(link, source.url).toString();

      articles.push({
        id: generateId(title, source.name),
        title,
        summary: summary.substring(0, 500),
        url: fullUrl,
        source: source.name,
        sourceRegion: source.region,
        category: classifyCategory(fullText),
        publishedAt: new Date().toISOString(),
        fetchedAt: new Date().toISOString(),
        companies: extractCompanies(fullText),
        dealValue: extractDealValue(fullText),
        tags: extractTags(fullText),
      });
    });

    return articles;
  } catch (error) {
    console.error(`Error fetching web source ${source.name}:`, error);
    return [];
  }
}

function articlesToDeal(article: NewsArticle): MaDeal | null {
  if (article.category !== "ma") return null;

  const text = `${article.title} ${article.summary}`;
  const companies = article.companies || [];

  return {
    id: `deal-${article.id}`,
    title: article.title,
    acquirer: companies[0] || "Unknown",
    acquirerCountry: regionToCountry(article.sourceRegion),
    target: companies[1] || "Unknown",
    targetCountry: regionToCountry(article.sourceRegion),
    dealValue: article.dealValue,
    status: inferDealStatus(text),
    announcedDate: article.publishedAt,
    sector: "Chemicals",
    subsector: inferSubsector(text),
    summary: article.summary,
    url: article.url,
    source: article.source,
    tags: article.tags,
  };
}

function regionToCountry(region: Region): string {
  const map: Record<Region, string> = {
    "north-america": "US",
    europe: "EU",
    "asia-pacific": "JP",
    "middle-east": "AE",
    "latin-america": "BR",
    africa: "ZA",
    global: "Global",
  };
  return map[region] || "Unknown";
}

function inferDealStatus(text: string): MaDeal["status"] {
  const lower = text.toLowerCase();
  if (/complet|clos|finaliz|完了|成立/i.test(lower)) return "completed";
  if (/pending|await|review|審査|承認待/i.test(lower)) return "pending";
  if (/withdraw|cancel|撤回|中止/i.test(lower)) return "withdrawn";
  if (/rumor|report|考え|検討/i.test(lower)) return "rumored";
  return "announced";
}

function inferSubsector(text: string): string {
  const lower = text.toLowerCase();
  if (/specialty|特殊/i.test(lower)) return "Specialty Chemicals";
  if (/agro|crop|農/i.test(lower)) return "Agrochemicals";
  if (/pharma|医薬/i.test(lower)) return "Pharmaceuticals";
  if (/polymer|plastic|樹脂|高分子/i.test(lower)) return "Polymers & Plastics";
  if (/petro|石油化学/i.test(lower)) return "Petrochemicals";
  if (/coating|paint|塗料/i.test(lower)) return "Coatings";
  if (/catalyst|触媒/i.test(lower)) return "Catalysts";
  if (/electronic|半導体/i.test(lower)) return "Electronic Chemicals";
  return "General Chemicals";
}

export async function fetchAllSources(): Promise<FetchResult> {
  const errors: string[] = [];
  const allArticles: NewsArticle[] = [];
  const allDeals: MaDeal[] = [];

  const fetchPromises = NEWS_SOURCES.map(async (source) => {
    try {
      const articles =
        source.type === "rss"
          ? await fetchRssFeed(source)
          : await fetchWebSource(source);
      return { source: source.name, articles };
    } catch (error) {
      const msg = `Failed to fetch ${source.name}: ${error}`;
      console.error(msg);
      errors.push(msg);
      return { source: source.name, articles: [] };
    }
  });

  const results = await Promise.allSettled(fetchPromises);

  for (const result of results) {
    if (result.status === "fulfilled") {
      allArticles.push(...result.value.articles);
      for (const article of result.value.articles) {
        const deal = articlesToDeal(article);
        if (deal) allDeals.push(deal);
      }
    }
  }

  await saveNews(allArticles);
  await saveDeals(allDeals);
  await updateMeta();

  return {
    success: errors.length === 0,
    articlesCount: allArticles.length,
    dealsCount: allDeals.length,
    lastFetched: new Date().toISOString(),
    errors,
  };
}

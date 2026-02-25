import { promises as fs } from "fs";
import path from "path";
import { NewsArticle, MaDeal, DashboardStats, Region, NewsCategory } from "@/types";

const DATA_DIR = path.join(process.cwd(), "src", "data");
const NEWS_FILE = path.join(DATA_DIR, "news.json");
const DEALS_FILE = path.join(DATA_DIR, "deals.json");
const META_FILE = path.join(DATA_DIR, "meta.json");

async function ensureDataDir(): Promise<void> {
  try {
    await fs.access(DATA_DIR);
  } catch {
    await fs.mkdir(DATA_DIR, { recursive: true });
  }
}

async function readJson<T>(filePath: string, defaultValue: T): Promise<T> {
  try {
    const content = await fs.readFile(filePath, "utf-8");
    return JSON.parse(content) as T;
  } catch {
    return defaultValue;
  }
}

async function writeJson<T>(filePath: string, data: T): Promise<void> {
  await ensureDataDir();
  await fs.writeFile(filePath, JSON.stringify(data, null, 2), "utf-8");
}

export async function getNews(): Promise<NewsArticle[]> {
  return readJson<NewsArticle[]>(NEWS_FILE, []);
}

export async function getDeals(): Promise<MaDeal[]> {
  return readJson<MaDeal[]>(DEALS_FILE, []);
}

export async function saveNews(articles: NewsArticle[]): Promise<void> {
  const existing = await getNews();
  const existingIds = new Set(existing.map((a) => a.id));
  const newArticles = articles.filter((a) => !existingIds.has(a.id));
  const merged = [...newArticles, ...existing].sort(
    (a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime()
  );
  // Keep last 90 days of articles
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 90);
  const filtered = merged.filter((a) => new Date(a.publishedAt) >= cutoff);
  await writeJson(NEWS_FILE, filtered);
}

export async function saveDeals(deals: MaDeal[]): Promise<void> {
  const existing = await getDeals();
  const existingIds = new Set(existing.map((d) => d.id));
  const newDeals = deals.filter((d) => !existingIds.has(d.id));
  const merged = [...newDeals, ...existing].sort(
    (a, b) => new Date(b.announcedDate).getTime() - new Date(a.announcedDate).getTime()
  );
  await writeJson(DEALS_FILE, merged);
}

export async function getStats(): Promise<DashboardStats> {
  const news = await getNews();
  const deals = await getDeals();
  const today = new Date().toISOString().split("T")[0];

  const regionBreakdown: Record<Region, number> = {
    "north-america": 0,
    europe: 0,
    "asia-pacific": 0,
    "middle-east": 0,
    "latin-america": 0,
    africa: 0,
    global: 0,
  };

  const categoryBreakdown: Record<NewsCategory, number> = {
    ma: 0,
    ipo: 0,
    earnings: 0,
    regulation: 0,
    sustainability: 0,
    innovation: 0,
    market: 0,
    other: 0,
  };

  news.forEach((article) => {
    regionBreakdown[article.sourceRegion]++;
    categoryBreakdown[article.category]++;
  });

  let totalDealValueUsd = 0;
  deals.forEach((deal) => {
    if (deal.dealValue) {
      const num = parseFloat(deal.dealValue.replace(/[^0-9.]/g, ""));
      if (!isNaN(num)) {
        totalDealValueUsd += num;
      }
    }
  });

  return {
    totalNews: news.length,
    totalDeals: deals.length,
    todayNews: news.filter((a) => a.publishedAt.startsWith(today)).length,
    todayDeals: deals.filter((d) => d.announcedDate.startsWith(today)).length,
    totalDealValue: `$${(totalDealValueUsd / 1e9).toFixed(1)}B`,
    regionBreakdown,
    categoryBreakdown,
  };
}

export async function getMeta(): Promise<{ lastFetched: string | null }> {
  return readJson(META_FILE, { lastFetched: null });
}

export async function updateMeta(): Promise<void> {
  await writeJson(META_FILE, { lastFetched: new Date().toISOString() });
}

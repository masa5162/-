import { NewsSource } from "@/types";

export const NEWS_SOURCES: NewsSource[] = [
  // === Global Chemical Industry News ===
  {
    name: "Chemical & Engineering News (C&EN)",
    url: "https://cen.acs.org/rss/feed.html",
    type: "rss",
    region: "global",
    category: ["ma", "innovation", "market"],
    language: "en",
  },
  {
    name: "ICIS News",
    url: "https://www.icis.com/explore/resources/news/rss/",
    type: "rss",
    region: "global",
    category: ["ma", "market"],
    language: "en",
  },
  {
    name: "Chemical Week",
    url: "https://chemweek.com/rss",
    type: "rss",
    region: "global",
    category: ["ma", "market", "earnings"],
    language: "en",
  },

  // === North America ===
  {
    name: "Reuters Chemicals",
    url: "https://www.reuters.com/news/archive/chemical-news?view=page&page=1&pageSize=10",
    type: "web",
    region: "north-america",
    category: ["ma", "market", "earnings"],
    language: "en",
  },
  {
    name: "Chemistry World",
    url: "https://www.chemistryworld.com/rss/news.xml",
    type: "rss",
    region: "north-america",
    category: ["innovation", "regulation"],
    language: "en",
  },

  // === Europe ===
  {
    name: "European Chemical Industry Council (CEFIC)",
    url: "https://cefic.org/media-corner/newsroom/feed/",
    type: "rss",
    region: "europe",
    category: ["regulation", "sustainability", "market"],
    language: "en",
  },
  {
    name: "CHEManager",
    url: "https://www.chemanager-online.com/en/rss.xml",
    type: "rss",
    region: "europe",
    category: ["ma", "market", "innovation"],
    language: "en",
  },

  // === Asia-Pacific ===
  {
    name: "化学工業日報",
    url: "https://www.chemicaldaily.co.jp/feed/",
    type: "rss",
    region: "asia-pacific",
    category: ["ma", "market", "innovation"],
    language: "ja",
  },
  {
    name: "日本経済新聞 化学",
    url: "https://www.nikkei.com/news/category/rss/chemical",
    type: "rss",
    region: "asia-pacific",
    category: ["ma", "earnings", "market"],
    language: "ja",
  },
  {
    name: "Asian Chemical News",
    url: "https://www.acnnewswire.com/rss/chemicals.xml",
    type: "rss",
    region: "asia-pacific",
    category: ["ma", "market"],
    language: "en",
  },

  // === M&A Specific ===
  {
    name: "Mergermarket Chemical",
    url: "https://www.mergermarket.com/intelligence/rss",
    type: "rss",
    region: "global",
    category: ["ma"],
    language: "en",
  },
  {
    name: "Bloomberg Chemical M&A",
    url: "https://www.bloomberg.com/feed/chemical",
    type: "rss",
    region: "global",
    category: ["ma", "market"],
    language: "en",
  },

  // === Sustainability & ESG ===
  {
    name: "Chemical Watch (ENHESA)",
    url: "https://www.enhesa.com/feed/",
    type: "rss",
    region: "global",
    category: ["regulation", "sustainability"],
    language: "en",
  },

  // === Industry Research ===
  {
    name: "Kline & Company",
    url: "https://klinegroup.com/feed/",
    type: "rss",
    region: "global",
    category: ["market", "ma"],
    language: "en",
  },
];

export const CHEMICAL_KEYWORDS = [
  // General Chemical
  "chemical", "chemicals", "petrochemical", "specialty chemical",
  "commodity chemical", "agrochemical", "pharmaceutical",
  "polymer", "plastics", "resin", "catalyst", "coating",
  "adhesive", "surfactant", "solvent", "pigment", "dye",
  "fertilizer", "pesticide", "herbicide", "insecticide",

  // Japanese
  "化学", "化学品", "化成品", "石油化学", "機能化学",
  "高分子", "樹脂", "触媒", "塗料", "接着剤",
  "界面活性剤", "溶剤", "顔料", "染料", "肥料",
  "農薬",

  // M&A Terms
  "acquisition", "merger", "takeover", "buyout",
  "divestiture", "joint venture", "strategic partnership",
  "買収", "合併", "統合", "売却", "M&A",
  "提携", "出資", "TOB", "MBO",

  // Major Chemical Companies
  "BASF", "Dow", "DuPont", "SABIC", "Sinopec",
  "Mitsubishi Chemical", "Sumitomo Chemical", "Mitsui Chemicals",
  "Shin-Etsu", "Toray", "LG Chem", "Lotte Chemical",
  "Evonik", "Lanxess", "Covestro", "Solvay", "Arkema",
  "Eastman", "Celanese", "Huntsman", "Ashland",
  "三菱ケミカル", "住友化学", "三井化学", "信越化学",
  "東レ", "旭化成", "花王", "日東電工",
];

export const MA_INDICATORS = [
  "acquire", "acquisition", "merger", "merge",
  "takeover", "buy", "buyout", "purchase",
  "divest", "divestiture", "sell", "sale",
  "joint venture", "JV", "partnership",
  "stake", "equity", "share purchase",
  "tender offer", "bid", "offer",
  "買収", "合併", "統合", "売却", "取得",
  "出資", "譲渡", "TOB", "MBO", "LBO",
];

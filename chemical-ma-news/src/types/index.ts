export interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  url: string;
  source: string;
  sourceRegion: Region;
  category: NewsCategory;
  publishedAt: string;
  fetchedAt: string;
  imageUrl?: string;
  companies?: string[];
  dealValue?: string;
  tags: string[];
}

export interface MaDeal {
  id: string;
  title: string;
  acquirer: string;
  acquirerCountry: string;
  target: string;
  targetCountry: string;
  dealValue?: string;
  currency?: string;
  status: DealStatus;
  announcedDate: string;
  closedDate?: string;
  sector: string;
  subsector?: string;
  summary: string;
  url: string;
  source: string;
  advisors?: string[];
  tags: string[];
}

export type Region =
  | "north-america"
  | "europe"
  | "asia-pacific"
  | "middle-east"
  | "latin-america"
  | "africa"
  | "global";

export type NewsCategory =
  | "ma"
  | "ipo"
  | "earnings"
  | "regulation"
  | "sustainability"
  | "innovation"
  | "market"
  | "other";

export type DealStatus =
  | "announced"
  | "pending"
  | "completed"
  | "withdrawn"
  | "rumored";

export interface NewsSource {
  name: string;
  url: string;
  type: "rss" | "web";
  region: Region;
  category: NewsCategory[];
  language: string;
}

export interface DashboardStats {
  totalNews: number;
  totalDeals: number;
  todayNews: number;
  todayDeals: number;
  totalDealValue: string;
  regionBreakdown: Record<Region, number>;
  categoryBreakdown: Record<NewsCategory, number>;
}

export interface FetchResult {
  success: boolean;
  articlesCount: number;
  dealsCount: number;
  lastFetched: string;
  errors: string[];
}

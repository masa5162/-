import { NextRequest, NextResponse } from "next/server";
import { getNews } from "@/lib/store";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const region = searchParams.get("region");
  const category = searchParams.get("category");
  const search = searchParams.get("q");
  const page = parseInt(searchParams.get("page") || "1");
  const limit = parseInt(searchParams.get("limit") || "20");

  let articles = await getNews();

  if (region && region !== "all") {
    articles = articles.filter((a) => a.sourceRegion === region);
  }
  if (category && category !== "all") {
    articles = articles.filter((a) => a.category === category);
  }
  if (search) {
    const q = search.toLowerCase();
    articles = articles.filter(
      (a) =>
        a.title.toLowerCase().includes(q) ||
        a.summary.toLowerCase().includes(q) ||
        a.companies?.some((c) => c.toLowerCase().includes(q)) ||
        a.tags.some((t) => t.toLowerCase().includes(q))
    );
  }

  const total = articles.length;
  const start = (page - 1) * limit;
  const paginated = articles.slice(start, start + limit);

  return NextResponse.json({
    articles: paginated,
    total,
    page,
    totalPages: Math.ceil(total / limit),
  });
}

import { NextRequest, NextResponse } from "next/server";
import { getDeals } from "@/lib/store";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const status = searchParams.get("status");
  const search = searchParams.get("q");
  const page = parseInt(searchParams.get("page") || "1");
  const limit = parseInt(searchParams.get("limit") || "20");

  let deals = await getDeals();

  if (status && status !== "all") {
    deals = deals.filter((d) => d.status === status);
  }
  if (search) {
    const q = search.toLowerCase();
    deals = deals.filter(
      (d) =>
        d.title.toLowerCase().includes(q) ||
        d.acquirer.toLowerCase().includes(q) ||
        d.target.toLowerCase().includes(q) ||
        d.summary.toLowerCase().includes(q) ||
        d.subsector?.toLowerCase().includes(q) ||
        d.tags.some((t) => t.toLowerCase().includes(q))
    );
  }

  const total = deals.length;
  const start = (page - 1) * limit;
  const paginated = deals.slice(start, start + limit);

  return NextResponse.json({
    deals: paginated,
    total,
    page,
    totalPages: Math.ceil(total / limit),
  });
}

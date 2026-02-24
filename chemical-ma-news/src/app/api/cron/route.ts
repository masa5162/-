import { NextResponse } from "next/server";
import { fetchAllSources } from "@/lib/fetcher";
import { getMeta } from "@/lib/store";

export async function POST() {
  try {
    const result = await fetchAllSources();
    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { success: false, error: String(error) },
      { status: 500 }
    );
  }
}

export async function GET() {
  const meta = await getMeta();
  return NextResponse.json(meta);
}

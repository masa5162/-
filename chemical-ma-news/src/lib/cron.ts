/**
 * Daily cron job for fetching chemical industry M&A news
 * 化学業界M&Aニュースの日次取得ジョブ
 *
 * Usage:
 *   npx tsx src/lib/cron.ts         # Run once
 *   npx tsx src/lib/cron.ts --watch  # Run with scheduler (every 6 hours)
 *
 * Can also be triggered via:
 *   - POST /api/cron (from the dashboard UI)
 *   - External cron scheduler (e.g., Vercel Cron, GitHub Actions)
 *   - System crontab: 0 0,6,12,18 * * * cd /path/to/app && npx tsx src/lib/cron.ts
 */

import { fetchAllSources } from "./fetcher";

async function run() {
  console.log(`[${new Date().toISOString()}] Starting news fetch...`);
  console.log("化学業界M&Aニュース取得開始...\n");

  try {
    const result = await fetchAllSources();

    console.log("\n=== Fetch Results / 取得結果 ===");
    console.log(`Articles fetched: ${result.articlesCount}`);
    console.log(`Deals identified: ${result.dealsCount}`);
    console.log(`Timestamp: ${result.lastFetched}`);

    if (result.errors.length > 0) {
      console.log(`\nErrors (${result.errors.length}):`);
      result.errors.forEach((err) => console.log(`  - ${err}`));
    }

    console.log(`\nStatus: ${result.success ? "SUCCESS" : "PARTIAL"}`);
  } catch (error) {
    console.error("Fatal error during fetch:", error);
    process.exit(1);
  }
}

const isWatch = process.argv.includes("--watch");

if (isWatch) {
  // Run immediately, then every 6 hours
  run();
  const SIX_HOURS = 6 * 60 * 60 * 1000;
  setInterval(run, SIX_HOURS);
  console.log("Scheduler started: running every 6 hours");
} else {
  run().then(() => process.exit(0));
}

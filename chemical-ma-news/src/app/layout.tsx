import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Chemical M&A Advisory | 化学業界M&Aアドバイザリ",
  description: "化学業界のM&A動向・バリュエーション分析・アドバイザリレポート",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className="bg-gray-50 text-gray-900">
        <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <div className="flex items-center gap-8">
                <a href="/" className="font-bold text-lg text-blue-900">
                  Chemical M&A Advisory
                </a>
                <div className="hidden md:flex gap-6 text-sm">
                  <a href="/deals" className="text-gray-600 hover:text-blue-700 font-medium">
                    M&Aディール
                  </a>
                  <a href="/valuation" className="text-gray-600 hover:text-blue-700 font-medium">
                    バリュエーション
                  </a>
                  <a href="/reports" className="text-gray-600 hover:text-blue-700 font-medium">
                    レポート
                  </a>
                </div>
              </div>
              <span className="text-xs text-gray-400">化学業界M&Aアドバイザリプラットフォーム</span>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="border-t border-gray-200 mt-16 py-8 text-center text-xs text-gray-400">
          <p>本サービスは公開情報に基づく分析であり、投資助言ではありません。</p>
          <p className="mt-1">© 2026 Chemical M&A Advisory. All rights reserved.</p>
        </footer>
      </body>
    </html>
  );
}

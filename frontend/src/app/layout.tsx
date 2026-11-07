import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SARTA - Semantic Adaptive Technical Assessment",
  description: "Resume-Driven Skill Extraction, Role-Specific MCQ & Coding Assessment with Adaptive Difficulty",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col font-sans bg-[#0f1117] text-white">
        {children}
      </body>
    </html>
  );
}

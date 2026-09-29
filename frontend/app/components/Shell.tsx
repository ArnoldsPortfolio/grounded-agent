"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
const LINKS = [["/ask", "Ask"], ["/docs", "Documents"], ["/evals", "Evals"]];
export default function Shell({ title, children }: { title: string; children: React.ReactNode }) {
  const path = usePathname();
  return (
    <div className="shell">
      <nav>
        <p><strong>Grounded Agent</strong></p>
        {LINKS.map(([href, label]) => <Link className={path === href ? "on" : ""} href={href} key={href}>{label}</Link>)}
      </nav>
      <main><h1>{title}</h1>{children}</main>
    </div>
  );
}

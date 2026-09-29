"use client";
import { useEffect, useState } from "react";
import Shell from "../components/Shell";
import { api } from "@/lib/api";
type Doc = { id: string; title: string };
const SAMPLE = "Refund policy. Customers may request a refund within 14 days of purchase. After 14 days the sale is final.";
export default function DocsPage() {
  const [docs, setDocs] = useState<Doc[]>([]);
  const [title, setTitle] = useState("policy.txt");
  const [text, setText] = useState(SAMPLE);
  const [error, setError] = useState("");
  async function load() { setDocs(await api<Doc[]>("/documents")); }
  useEffect(() => { load().catch((err: Error) => setError(err.message)); }, []);
  async function save() {
    await api("/documents/text", { method: "POST", body: JSON.stringify({ title, text }) });
    await load();
  }
  return (
    <Shell title="Documents">
      {error ? <p className="err">{error}</p> : null}
      <div className="card">
        <input value={title} onChange={(e) => setTitle(e.target.value)} />
        <textarea value={text} onChange={(e) => setText(e.target.value)} />
        <button type="button" onClick={() => save().catch((err: Error) => setError(err.message))}>Index text</button>
      </div>
      {docs.map((doc) => <p className="card" key={doc.id}>{doc.title}</p>)}
    </Shell>
  );
}

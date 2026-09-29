"use client";
import { useState } from "react";
import Shell from "../components/Shell";
import { api } from "@/lib/api";
type Citation = { document_id: string; chunk_id: string; title: string; quote: string; score: number };
type Answer = { grounded: boolean; answer: string; refusal?: string | null; citations: Citation[]; run_id: string };
export default function AskPage() {
  const [question, setQuestion] = useState("What is the refund window?");
  const [agent, setAgent] = useState(false);
  const [result, setResult] = useState<Answer | null>(null);
  const [error, setError] = useState("");
  async function submit() {
    if (agent) {
      const run = await api<{ final: Answer }>("/agent/run", { method: "POST", body: JSON.stringify({ question }) });
      setResult(run.final);
      return;
    }
    setResult(await api<Answer>("/ask", { method: "POST", body: JSON.stringify({ question }) }));
  }
  return (
    <Shell title="Ask">
      <p className="muted">The model may only answer from indexed documents.</p>
      {error ? <p className="err">{error}</p> : null}
      <textarea value={question} onChange={(e) => setQuestion(e.target.value)} />
      <p><label><input type="checkbox" checked={agent} onChange={(e) => setAgent(e.target.checked)} /> Use agent</label></p>
      <button type="button" onClick={() => submit().catch((err: Error) => setError(err.message))}>Ask</button>
      {result ? (
        <article className="card">
          <p><strong>{result.grounded ? "Grounded" : "Refused"}</strong></p>
          <p>{result.grounded ? result.answer : result.refusal}</p>
          {result.citations.map((c) => <p className="cite" key={c.chunk_id}><strong>{c.title}</strong> ({c.score.toFixed(2)})<br />{c.quote}</p>)}
        </article>
      ) : null}
    </Shell>
  );
}

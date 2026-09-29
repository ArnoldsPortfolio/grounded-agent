"use client";
import { useState } from "react";
import Shell from "../components/Shell";
import { api } from "@/lib/api";
type Score = { case_id: string; question: string; passed: boolean; reason: string };
export default function EvalsPage() {
  const [rows, setRows] = useState<Score[]>([]);
  const [error, setError] = useState("");
  return (
    <Shell title="Evals">
      <p className="muted">Refund question should cite 14 days. Pizza question should refuse.</p>
      {error ? <p className="err">{error}</p> : null}
      <button type="button" onClick={() => api<Score[]>("/evals/run", { method: "POST" }).then(setRows).catch((err: Error) => setError(err.message))}>Run suite</button>
      {rows.map((row) => (
        <article className="card" key={row.case_id}>
          <strong>{row.passed ? "Pass" : "Fail"}</strong> — {row.question}
          <p className="muted">{row.reason}</p>
        </article>
      ))}
    </Shell>
  );
}

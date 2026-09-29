# Grounded Agent architecture

Answer only from tenant documents. Cite or refuse. Trace every run.

Ports: DocumentStore, VectorIndex, LanguageModel, ToolRegistry, TraceSink, ObjectBlobStore.

Local adapters (no paid LLM required): hash embedding + cosine retrieve, extractive answerer, SQLite traces.

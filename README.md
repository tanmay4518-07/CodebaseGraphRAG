# PageRank-Enriched GraphRAG for Codebase Intelligence

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph_Database-008CC1?logo=neo4j)
![LangChain](https://img.shields.io/badge/LangChain-Framework-white?logo=langchain)
![Gemini](https://img.shields.io/badge/Gemini_3.5_Flash-LLM-8E75B2?logo=google)

## 📌 Overview
Standard Retrieval-Augmented Generation (RAG) is fundamentally flawed for complex codebase reasoning. By splitting source code into arbitrary text chunks and relying solely on semantic vector embeddings, standard RAG destroys the logical topology of software architecture. 

This project solves codebase intelligence from first principles. It bypasses semantic shortcuts by engineering a **PageRank-Enriched GraphRAG system**. It extracts deterministic execution flows, maps them as a mathematical topology in Neo4j, calculates structural bottlenecks using Graph Data Science (GDS), and leverages Google's Gemini 3.5 Flash to synthesize absolute downstream impact analysis.


## 🏗️ Architecture: The 4-Step Pipeline

This system rejects LLM guesswork in favor of rigorous, deterministic data extraction prior to generative reasoning.

1. **Deterministic Extraction (AST Parser):** A custom Python Abstract Syntax Tree (`ast`) visitor traverses `.py` files. It programmatically isolates function definitions, docstrings, and explicit `CALLS` dependencies (Caller → Callee) without probabilistic failure.
2. **Topological Indexing (Neo4j):** Extracted nodes and edges are indexed into a local Neo4j database using strict transactional Cypher routines, converting the codebase into an immutable relational graph.
3. **Graph Analytics (GDS PageRank):** The Neo4j Graph Data Science (GDS) library projects the codebase into in-memory RAM and executes a PageRank algorithm. This mathematically calculates the eigenvector centrality of every function, inherently tagging high-risk architectural bottlenecks.
4. **Hybrid Reasoning (LangChain):** The topological schema is unified with `gemini-embedding-2-preview` vectors. A `GraphCypherQAChain` dynamically evaluates the database schema and mathematical `pagerank_score` properties to synthesize Cypher traversal queries, ensuring the LLM's final impact analysis is structurally grounded.


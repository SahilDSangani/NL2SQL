# StatGenie: A Learning Journey into Local NL2SQL ⚾

StatGenie is an experimental **Text-to-SQL (NL2SQL)** data agent built to explore the challenges of on-device AI and natural language interfaces for structured data. 

This project started as a way to apply what I learned about local LLMs in class, using a familiar MLB batting dataset as a testing ground. It is less about being a "perfect tool" and more about the architectural decisions and roadblocks encountered while building it.

## 💡 Inspiration: The "Genie" 
This project is inspired by **Databricks Genie**, an AI/BI feature that allows users to chat with their data. Genie works by:
- **Semantic Mapping:** Using metadata and a "Knowledge Store" to translate business terms into technical columns.
- **Trust & Verification:** Providing the underlying SQL so users can trust the answer.
- **Feedback Loops:** Allowing analysts to "teach" the agent through instructions and example queries.

StatGenie is my attempt to build a "miniature," local version of this—one that is agnostic enough to eventually work with any dataset (batting, fielding, or even non-sports data) just by swapping the schema and database.

## 🚀 Technical Setup
- **Model:** Liquid AI LFM2-8B (LFM2-8B-A1B-Q4_K_M)
- **Engine:** llama.cpp (`llama-server`) on Port 8080
- **Orchestration:** LangChain (Modular Chain approach)
- **Database:** SQLite

## 🚧 Roadblocks & Design Goals
The goal of this project is to intentionally encounter and solve common NL2SQL problems:
- **The "Schema Gap":** How do I help an 8B model understand that `hr` means Home Runs? (Solution: Hardcoded Data Dictionary).
- **Subjectivity Handling:** When asked "Who is the best player?", a standard SQL query fails. I am working on a "Clarification Loop" where the LLM questions the user back: *"Do you mean by home runs, batting average, or defensive value?"*
- **Agnostic Architecture:** Designing the system so the logic remains the same even if the data changes from baseball to something entirely different.

## 🗺️ Learning Roadmap
- [ ] **Dynamic Data Dictionary:** Finalize the column descriptions for the MLB dataset.
- [ ] **Clarification Logic:** Implement a system where the LLM flags ambiguous/subjective questions instead of guessing.
- [ ] **Scaling:** Add fielding/pitching stats and verify cross-table reasoning.
- [ ] **Streamlit Interface:** Build a frontend for easier interaction and database updates.

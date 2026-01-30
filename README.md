# StatGenie: Local NL2SQL Sports Analytics ⚾

StatGenie is a local-first **Text-to-SQL (NL2SQL)** data agent designed for sports analytics. Inspired by **Databricks Genie**, this project allows users to query sports databases using plain English. 

This is a learning-focused project ("Work-in-Progress") exploring the intersection of statistics, LLM orchestration, and on-device AI.

## 🚀 The Brain: Liquid AI LFM2-8B
This project runs on the **LFM2-8B-A1B-Q4_K_M** model using **llama.cpp**. 
- **Hybrid Architecture:** Uses a mix of convolutions and attention.
- **Efficient MoE:** Although it has 8.3B parameters, only **1.5B are active** during inference, making it incredibly fast on a MacBook.
- **Privacy First:** No data ever leaves your device.

## 🧠 Project Architecture
StatGenie uses a **Modular Chain** approach for high reliability on local hardware:
1. **Schema Injection:** Hardcoded table metadata prevents the LLM from hallucinating column names.
2. **SQL Generation:** Translates English questions into precise SQLite queries.
3. **Synthesis:** Python executes the query and returns a conversational answer.

## 🗺️ Roadmap & Future Goals
- [ ] **Data Dictionary:** Finalize schema descriptions so the LLM knows `hr` = Home Runs.
- [ ] **Data Scaling:** Expand beyond batting to include fielding and pitching stats.
- [ ] **Streamlit UI:** Build a front-end "chat" interface for a seamless experience.
- [ ] **Database Management:** Add tools to update or refresh the database via the UI.

## 📄 License
This is an open-source project created for educational purposes.

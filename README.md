# 🛡️ Aegis: Adversarial Voice Agent Test Lab

> **Status:** 🧪 **MVP (Minimum Viable Product)**  
> This repository contains the functional, interactive Streamlit MVP demonstrating the core multi-agent adversarial simulation loop, real-time live transcript streaming, and automated LLM-as-a-Judge evaluation. The planned enterprise production stack and architecture roadmap are detailed below.

---

## 📌 Product Overview

**Aegis** is an automated, pre-deployment testing simulator (LLMOps) designed specifically for enterprise Voice AI agencies. Before deploying a voice agent to a real client, Aegis generates synthetic callers (using LLM personas like "angry customer", "scammer", or "confused caller") to interact with the target agent. It uses an automated "LLM-as-a-Judge" system to score the target agent on task completion, hallucination rates, and strict guardrail violations. 

The full open-source target stack utilizes LangGraph for multi-agent adversarial orchestration, Llama-3 8B (hosted locally) to generate the synthetic personas and judge outputs, FastAPI for the backend evaluation engine, and Coqui TTS / Whisper STT to simulate real-time voice latency and audio interference during regression testing.

---

## 💡 Why Aegis?

I chose this because automated LLMOps and AI safety are the biggest unsolved bottlenecks in enterprise Generative AI. Agencies deploy AI rapidly but have no systematic way to regression-test their models against unpredictable human behavior. By automating adversarial edge-case testing, we protect the agency from massive liability and ensure enterprise-grade reliability before the client ever sees the product.

---

## 🏗️ Target Production Architecture

The diagram below illustrates the end-to-end architecture planned for the complete open-source enterprise voice testing suite:

```mermaid
graph TD
    %% Styling
    classDef target fill:#43AA8B,stroke:#fff,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef adversary fill:#F24236,stroke:#fff,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef judge fill:#F5F749,stroke:#333,stroke-width:2px,color:#333,rx:5px,ry:5px;
    classDef infra fill:#2E86AB,stroke:#fff,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    classDef data fill:#8A4F7D,stroke:#fff,stroke-width:2px,color:#fff,rx:5px,ry:5px;
    %% Components
    UI[FastAPI / React Dashboard <br/> Test Configurator]:::infra
    
    subgraph Multi-Agent Orchestration
        AG[Synthetic Caller Agent <br/> Persona Generator]:::adversary
        TGT[Target Voice Agent <br/> Under Test]:::target
        JUDGE[LLM-as-a-Judge <br/> Evaluator Agent]:::judge
    end
    subgraph Open-Source Voice Stack
        TTS[Coqui TTS <br/> Text-to-Speech]:::infra
        STT[Whisper STT <br/> Speech-to-Text]:::infra
    end
    subgraph Evaluation Data
        DB[(PostgreSQL <br/> Test Logs & Scores)]:::data
        DASH[Regression Test <br/> Analytics Dashboard]:::data
    end
    %% Flow
    UI -- Defines Personas & Guardrails --> AG
    AG -- Generates Text Persona --> TTS
    TTS -- Synthesizes Hostile Audio --> TGT
    TGT -- Responds with Audio --> STT
    STT -- Transcribes Response --> AG
    
    AG -. "Interaction Loop N turns" .- TGT
    
    AG -- Sends Full Transcript --> JUDGE
    TGT -- Sends System Logs --> JUDGE
    
    JUDGE -- Scores Hallucinations & Guardrails --> DB
    DB -- Streams Live Metrics --> DASH
```

---

## 🚀 Current MVP Implementation

The current working MVP validates the multi-agent testing concept with a lightweight, zero-overhead architecture:

- **Target Agent**: Bank customer service representative under strict guardrails (strictly prohibits refunds over $50, profanity, and prompt leakage).
- **Adversarial Agent**: Dynamic synthetic caller driven by specialized adversarial system prompts. Uses conversation role-swapping to engage naturally as a customer.
- **LLM-as-a-Judge Evaluator**: Analytical agent scoring the full transcript on a 1–10 scale, validating guardrails, hallucination risk, and prompt injection resistance with JSON enforcement and automatic retry recovery.
- **Streaming Live Simulation**: Python generator-based simulation loop rendering live turn-by-turn chat updates in Streamlit before scoring.
- **Evaluation Dashboard**: Dark-mode report card with circular SVG score gauge, violation badges, and behavioral breakdown.

### Tech Stack (MVP)
- **Frontend / Dashboard**: Streamlit (Python) with custom CSS & dark mode
- **LLM Engine**: OpenAI API (`gpt-4o-mini` for conversational agents, `gpt-4o` for evaluation)
- **Dependencies**: Only `streamlit>=1.38.0` and `openai>=1.40.0`

---

## 🎭 Adversarial Personas (Included in MVP)

| Persona | Difficulty | Attack Strategy & Failure Modes Tested |
|---|---|---|
| 😡 **Angry Customer** | Hard | Demands $100 refund, escalates profanity, threatens legal action to force policy violation. |
| 👴 **Confused Elderly** | Medium | Misunderstands answers, rambles off-topic, tests agent patience and clarity. |
| 🕵️ **Social Engineer / Hacker** | Hard | Prompt injection (`"Ignore previous instructions"`), authority impersonation, prompt extraction. |
| 🙂 **Polite but Persistent** | Medium | Emotional manipulation, gentle boundary erosion, probing for exceptions. |
| ⚡ **Rapid-Fire Caller** | Easy | Stacks multiple unrelated questions per turn to induce hallucinations and loss of focus. |

---

## 🗺️ Planned Features & Roadmap

The MVP will evolve into the full production platform through the following milestones:

- [ ] **LangGraph Multi-Agent Orchestration**: Migrate the conversational loop to stateful LangGraph workflows with branching edge conditions.
- [ ] **Local Llama-3 8B Integration**: Support local inference (vLLM / Ollama) to run personas and judge evaluations cost-free on local GPUs.
- [ ] **Voice Stack (Audio-in-the-Loop)**: Integrate **Coqui TTS** for synthetic speech synthesis and **Whisper STT** for speech-to-text to measure real-time latency and audio interference.
- [ ] **FastAPI Backend & Custom Target Config**: Decouple the simulation engine into a standalone REST API allowing users to test any custom voice agent webhook or system prompt.
- [ ] **PostgreSQL Evaluation Logs & Regression Dashboard**: Store all test transcripts, violation logs, and historical scores to detect safety regressions across model updates.
- [ ] **Automated Batch Test Suites**: Run exhaustive test matrices across multiple personas and parameter sweeps in a single click.

---

## 🛠️ Quick Start (Running the MVP)

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/i220893/Aegis-Voice-Test-Lab.git
cd Aegis-Voice-Test-Lab
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
streamlit run app.py
```

### 3. Run a Simulation
1. Enter your **OpenAI API Key** in the sidebar.
2. Select an **Adversarial Persona** and set the number of turns.
3. Click **🚀 Run Simulation**.
4. Observe the automated multi-turn confrontation in the live chat window.
5. Review the final **Evaluation Report** with the judge's score and reasoning.

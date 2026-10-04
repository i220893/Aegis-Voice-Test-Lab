# 🛡️ Aegis: Voice Agent Test Lab

**Adversarial multi-agent simulator for stress-testing enterprise voice AI agents.**

Aegis generates synthetic hostile callers to attack your AI agent and automatically evaluates its performance on guardrail compliance, hallucination detection, and prompt injection resistance.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

### 3. Configure and test

1. Enter your **OpenAI API Key** in the sidebar
2. Select an **adversarial persona** (e.g., "Angry Customer", "Social Engineer")
3. Click **Run Simulation**
4. Watch the adversarial conversation unfold in real-time
5. Review the **Evaluation Report** with score and analysis

---

## Architecture

```
🔴 Adversarial Caller ──▶ 🟢 Target Agent (Bank CS Bot)
        ◀──────────────────────
              × 3 turns
                  │
                  ▼
         🟡 LLM-as-a-Judge
                  │
                  ▼
          📊 Score & Report
```

- **Target Agent** — A bank customer service bot with strict guardrails (no refunds > $50, no profanity, no prompt leaks)
- **Adversarial Agent** — Persona-driven attacker (angry customer, hacker, confused caller, etc.)
- **Judge Agent** — Evaluates the transcript and returns a structured score (1-10)

## Personas

| Persona | Difficulty | Attack Strategy |
|---|---|---|
| 😡 Angry Customer | Hard | Demands $100 refund, uses profanity |
| 👴 Confused Elderly | Medium | Rambles, misunderstands, tests patience |
| 🕵️ Social Engineer | Hard | Prompt injection, impersonation |
| 🙂 Polite but Persistent | Medium | Emotional manipulation, boundary pushing |
| ⚡ Rapid-Fire Caller | Easy | Multiple questions, tries to cause hallucination |

---

## Tech Stack

- **Frontend**: Streamlit (Python)
- **LLM**: OpenAI API (`gpt-4o-mini` for agents, `gpt-4o` for judge)
- **No external dependencies** beyond `streamlit` and `openai`

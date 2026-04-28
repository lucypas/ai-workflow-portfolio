# AI Workflow Portfolio

This repository showcases practical AI workflows designed for enterprise data, product, and technical program environments.

The focus is not just on using AI models, but on building complete, production-style workflows that support real business operations, including:

- dataset onboarding and validation
- data quality review and issue detection
- AI-assisted executive reporting and status summaries
- retrieval-augmented knowledge assistants
- workflow governance and validation logic

Each workflow is implemented using Python with structured inputs, validation rules, and test coverage to simulate real-world delivery scenarios.

## Workflows Included

1. **Dataset Onboarding Reviewer**  
   Validates dataset readiness against required columns, null-rate thresholds, and freshness requirements.

2. **Executive Status Summary Generator**  
   Converts structured delivery metrics into an executive-ready program health summary.

3. **RAG-Style Knowledge Assistant**  
   Demonstrates a lightweight retrieval workflow using a mocked internal knowledge base.

## How to Run

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run all tests:

```bash
pytest
```

Run each workflow:

```bash
python workflows/01_dataset_onboarding_reviewer/src/reviewer.py
python workflows/02_exec_status_summary/src/status_summary.py
python workflows/03_rag_knowledge_assistant/src/rag_assistant.py
```

## Data Privacy Notice

All data in this repository is mock data. No client, employer, customer, or proprietary information is included.

## Purpose

This portfolio demonstrates how AI can be applied beyond experimentation into structured, scalable workflows that support enterprise delivery, decision-making, and operational efficiency.

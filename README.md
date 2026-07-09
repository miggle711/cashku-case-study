# Cashku Case Study: Fund Data Challenge

## Context

Cashku is an AI-native digital wealth management platform. A core part of our engineering work involves ingesting, cleaning, and analysing Malaysian unit trust fund data to power our investor-facing features.

You have been given a dataset of **20 fictional Malaysian unit trust funds** with 12 months of daily NAV (Net Asset Value) history. The data is messy — it reflects the kind of real-world data quality issues we deal with regularly.

## Your Task

You have been assigned **one or both tracks** below. Check with your recruiter which track(s) apply to you.

**Time limit: 3 days from when you receive this repo.**

You may use AI tools (Claude, Copilot, ChatGPT, etc.) freely. We encourage it — it reflects how we work. **However, you must include a short note in your README on how you used AI tools and where.** We will assess your judgment in using them, not penalise you for it.

---

## Track A: Development

**Goal:** Build a working data pipeline and API that cleans the fund data and makes it queryable.

### Requirements

1. **Data Cleaning & Ingestion**
   - Parse and clean `data/nav_history.csv` (handle date format inconsistencies, missing/invalid NAV values, duplicate rows, malformed fund IDs)
   - Load the cleaned data into a SQLite database with a schema you design
   - Join with `data/fund_metadata.csv` for fund details

2. **API Endpoints**
   - Implement the functions defined in `track-a/starter.py`
   - `get_fund_performance(fund_id, start_date, end_date)` — return NAV series and total return
   - `compare_funds(fund_ids, start_date, end_date)` — return comparative performance
   - `get_portfolio_return(holdings, start_date, end_date)` — given a list of (fund_id, units) pairs, return weighted portfolio return and allocation breakdown

3. **Tests**
   - Make the provided tests in `tests/test_pipeline.py` pass
   - Add at least 2 additional edge case tests of your own

### Deliverables

- Your completed code in `track-a/`
- A `track-a/README.md` explaining your schema design choices and any assumptions
- All tests passing

---

## Track B: Data Analytics

**Goal:** Analyse the fund dataset and deliver actionable insights.

### Requirements

Answer the questions in `track-b/questions.md` using Python (pandas, matplotlib/seaborn, or any libraries you prefer). Deliver your work as a Jupyter notebook or a Python script with printed outputs and saved charts.

### Deliverables

- Your notebook or script in `track-b/`
- Charts saved as images in `track-b/charts/`
- A `track-b/README.md` with a brief executive summary of your findings

---

## Both Tracks

If assigned both tracks, your Track A pipeline should feed your Track B analysis. We value integration — show us that the cleaned data from your pipeline is what powers your analytics.

---

## Submission

1. Clone this repo and complete your work locally
2. Zip your completed project folder, excluding generated/junk files:

   ```bash
   cd cashku-case-study
   zip -r submission-<your-name>.zip . \
     -x "*.pyc" -x "__pycache__/*" -x "*/__pycache__/*" \
     -x "*.db" -x ".venv/*" -x ".env" -x "*.egg-info/*" \
     -x ".ipynb_checkpoints/*" -x "*/.ipynb_checkpoints/*" \
     -x ".git/*" -x ".DS_Store"
   ```

3. Email the zip file to your recruiter/HR contact, with your full name and the track(s) you completed in the subject line (e.g. `Cashku Case Study — Jane Tan — Track A`)

---

## Dataset

| File | Description |
|---|---|
| `data/nav_history.csv` | ~5,300 rows of daily NAV prices. Contains intentional data quality issues. |
| `data/fund_metadata.csv` | 20 funds with name, category, provider, currency, risk level. This file is clean. |

---

## Rules

- You may use any Python libraries
- You may use AI tools — just document your usage
- Do not modify the test file signatures (you may add tests)
- Ask clarifying questions via email if needed — this is encouraged, not penalised

# Track B: Data Analytics Questions

Use the data in `data/nav_history.csv` and `data/fund_metadata.csv` to answer the following questions. You will need to clean the data first (see the README for known data quality issues).

Deliver your work as a Jupyter notebook or Python script. Include charts where indicated, saved to `track-b/charts/`.

---

## Question 1: Data Quality Report

Before any analysis, assess the quality of `nav_history.csv`.

- How many rows have invalid or missing NAV values?
- How many duplicate (same fund + same date) entries exist?
- How many rows have malformed fund IDs or inconsistent date formats?
- Which funds have the most missing trading days, and what might explain the gaps?

Produce a summary table of data quality issues by fund.

**Chart:** A heatmap showing data completeness (date on x-axis, fund on y-axis, colour = data present/missing).

---

## Question 2: Performance Comparison Across Categories

After cleaning the data:

- Calculate the total return and annualised return for each fund over the full 12-month period.
- Group funds by category (Equity, Bond, Balanced, Money Market, REIT, Shariah variants). Which category performed best on average? Which had the widest spread?
- Identify the top 3 and bottom 3 individual funds by total return.

**Chart:** A grouped bar chart of average return by category, with individual fund returns shown as scatter points overlaid.

---

## Question 3: Risk-Adjusted Returns

For each fund, calculate:

- Daily return volatility (standard deviation of daily percentage changes)
- Sharpe ratio (assume a risk-free rate of 3.0% per annum)
- Maximum drawdown over the 12-month period

Which funds offer the best risk-adjusted returns? Does the risk level label in the metadata (High/Medium/Low) align with the actual observed volatility?

**Chart:** A scatter plot of annualised return vs. volatility, with points coloured by risk level label and sized by AUM (you may use a proxy like average NAV if actual AUM is not available).

---

## Question 4: Anomaly Detection

Identify NAV entries that appear anomalous:

- Flag any single-day NAV changes greater than 10% (up or down) for any fund.
- For each flagged entry, assess whether it looks like a genuine market move or a data error. Explain your reasoning.
- Recommend a rule or threshold that Cashku could apply automatically to catch data errors without flagging legitimate moves.

**Chart:** A time series of one or two funds with the most anomalies, with flagged points highlighted.

---

## Bonus (Optional)

If you had access to benchmark index data (e.g., FTSE Bursa Malaysia KLCI), what additional analyses would you run? Describe 2-3 analyses and why they would be valuable to Cashku's investors. You do not need to implement these, just explain them clearly.

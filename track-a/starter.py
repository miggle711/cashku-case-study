"""
Cashku Fund Data Pipeline — Starter Code

Complete the functions below. You may add helper functions, modules, and classes
as needed. Do not change the function signatures.
"""

import sqlite3
import csv
import os
from datetime import datetime
from typing import Optional


DB_PATH = os.path.join(os.path.dirname(__file__), "cashku.db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# =============================================================================
# PART 1: Data Cleaning & Ingestion
# =============================================================================

def clean_fund_id(raw_id: str) -> str:
    """
    Normalise a fund ID to the canonical format 'FNDXXX' (e.g., 'FND001').

    The raw data contains inconsistencies:
    - Extra whitespace ('FND 001', ' FND001')
    - Lowercase ('fnd001')
    - Missing leading zeros ('FND1')

    Args:
        raw_id: The raw fund_id string from the CSV.

    Returns:
        A cleaned fund_id string in the format 'FNDXXX'.
    """
    # TODO: Implement
    pass


def parse_date(raw_date: str) -> Optional[datetime]:
    """
    Parse a date string into a datetime object.

    The raw data uses multiple formats:
    - '2025-07-01' (ISO, most common)
    - '01/07/2025' (DD/MM/YYYY)
    - '07-01-2025' (MM-DD-YYYY)
    - '01 Jul 2025' (DD Mon YYYY)
    - '2025/07/01' (YYYY/MM/DD)

    Args:
        raw_date: The raw date string from the CSV.

    Returns:
        A datetime object, or None if the date cannot be parsed.
    """
    # TODO: Implement
    pass


def parse_nav(raw_nav: str) -> Optional[float]:
    """
    Parse a NAV value into a float.

    The raw data contains:
    - Normal floats ('1.4523')
    - Currency prefixed ('RM 1.4523')
    - Invalid markers ('N/A', 'null', '-', '')

    Args:
        raw_nav: The raw NAV string from the CSV.

    Returns:
        A float NAV value, or None if the value is invalid/missing.
    """
    # TODO: Implement
    pass


def create_schema(conn: sqlite3.Connection) -> None:
    """
    Create the database schema.

    Design your own schema. At minimum, you need:
    - A table for fund metadata
    - A table for daily NAV prices (cleaned, deduplicated)

    Consider: indexing, data types, constraints, and how you would
    query for performance calculations efficiently.

    Args:
        conn: An open SQLite connection.
    """
    # TODO: Implement
    pass


def ingest_data(conn: sqlite3.Connection) -> dict:
    """
    Read the raw CSVs, clean the data, and insert into the database.

    This function should:
    1. Read and insert fund_metadata.csv
    2. Read nav_history.csv, clean each row using the functions above
    3. Deduplicate (same fund_id + date = keep one)
    4. Skip rows with unparseable dates or invalid NAVs
    5. Return a summary dict with counts

    Args:
        conn: An open SQLite connection (schema already created).

    Returns:
        A dict like:
        {
            "total_raw_rows": int,
            "rows_inserted": int,
            "rows_skipped": int,
            "duplicates_removed": int,
        }
    """
    # TODO: Implement
    pass


# =============================================================================
# PART 2: API / Query Functions
# =============================================================================

def get_fund_performance(
    conn: sqlite3.Connection,
    fund_id: str,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Get a fund's performance over a date range.

    Args:
        conn: An open SQLite connection with ingested data.
        fund_id: The fund ID (e.g., 'FND001').
        start_date: Start date as 'YYYY-MM-DD'.
        end_date: End date as 'YYYY-MM-DD'.

    Returns:
        A dict like:
        {
            "fund_id": "FND001",
            "fund_name": "Cahaya Equity Growth Fund",
            "start_nav": 1.45,
            "end_nav": 1.62,
            "total_return_pct": 11.72,
            "data_points": 250,
        }

    Raises:
        ValueError: If the fund_id is not found or no data exists in the range.
    """
    # TODO: Implement
    pass


def compare_funds(
    conn: sqlite3.Connection,
    fund_ids: list[str],
    start_date: str,
    end_date: str,
) -> list[dict]:
    """
    Compare performance of multiple funds over a date range.

    Args:
        conn: An open SQLite connection with ingested data.
        fund_ids: List of fund IDs to compare.
        start_date: Start date as 'YYYY-MM-DD'.
        end_date: End date as 'YYYY-MM-DD'.

    Returns:
        A list of dicts (same format as get_fund_performance), sorted by
        total_return_pct descending.
    """
    # TODO: Implement
    pass


def get_portfolio_return(
    conn: sqlite3.Connection,
    holdings: list[tuple[str, float]],
    start_date: str,
    end_date: str,
) -> dict:
    """
    Calculate the weighted return of a portfolio.

    Args:
        conn: An open SQLite connection with ingested data.
        holdings: List of (fund_id, units_held) tuples.
            Example: [("FND001", 1000), ("FND003", 5000)]
        start_date: Start date as 'YYYY-MM-DD'.
        end_date: End date as 'YYYY-MM-DD'.

    Returns:
        A dict like:
        {
            "total_start_value": 6250.00,
            "total_end_value": 6890.00,
            "total_return_pct": 10.24,
            "allocation": [
                {
                    "fund_id": "FND001",
                    "weight_pct": 23.2,
                    "return_pct": 11.72,
                },
                ...
            ],
        }

    Raises:
        ValueError: If holdings list is empty or contains unknown fund IDs.
    """
    # TODO: Implement
    pass


# =============================================================================
# Main (for manual testing)
# =============================================================================

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)
    summary = ingest_data(conn)
    print("Ingestion summary:", summary)

    # Quick test
    perf = get_fund_performance(conn, "FND001", "2025-07-01", "2026-06-30")
    print("FND001 performance:", perf)

    conn.close()

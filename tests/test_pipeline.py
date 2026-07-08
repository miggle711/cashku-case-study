"""
Cashku Case Study — Test Suite

Run with: pytest tests/test_pipeline.py -v

Do not modify existing tests. You may add your own at the bottom.
"""

import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "track-a"))
from starter import (
    clean_fund_id,
    parse_date,
    parse_nav,
    create_schema,
    ingest_data,
    get_fund_performance,
    compare_funds,
    get_portfolio_return,
)


# =============================================================================
# Unit tests: cleaning functions
# =============================================================================

class TestCleanFundId:
    def test_normal(self):
        assert clean_fund_id("FND001") == "FND001"

    def test_lowercase(self):
        assert clean_fund_id("fnd001") == "FND001"

    def test_extra_space(self):
        assert clean_fund_id("FND 001") == "FND001"

    def test_leading_space(self):
        assert clean_fund_id(" FND001") == "FND001"

    def test_missing_leading_zero(self):
        assert clean_fund_id("FND1") == "FND001"

    def test_missing_two_leading_zeros(self):
        assert clean_fund_id("FND1") == "FND001"


class TestParseDate:
    def test_iso_format(self):
        result = parse_date("2025-07-01")
        assert result is not None
        assert result.year == 2025
        assert result.month == 7
        assert result.day == 1

    def test_dd_mm_yyyy(self):
        result = parse_date("15/08/2025")
        assert result is not None
        assert result.month == 8
        assert result.day == 15

    def test_mm_dd_yyyy(self):
        result = parse_date("08-15-2025")
        assert result is not None
        assert result.month == 8
        assert result.day == 15

    def test_dd_mon_yyyy(self):
        result = parse_date("15 Aug 2025")
        assert result is not None
        assert result.month == 8
        assert result.day == 15

    def test_yyyy_mm_dd_slash(self):
        result = parse_date("2025/08/15")
        assert result is not None
        assert result.month == 8
        assert result.day == 15

    def test_invalid_returns_none(self):
        assert parse_date("not-a-date") is None

    def test_empty_returns_none(self):
        assert parse_date("") is None


class TestParseNav:
    def test_normal_float(self):
        assert parse_nav("1.4523") == pytest.approx(1.4523)

    def test_currency_prefix(self):
        assert parse_nav("RM 1.4523") == pytest.approx(1.4523)

    def test_na(self):
        assert parse_nav("N/A") is None

    def test_null(self):
        assert parse_nav("null") is None

    def test_dash(self):
        assert parse_nav("-") is None

    def test_empty(self):
        assert parse_nav("") is None


# =============================================================================
# Integration tests: pipeline
# =============================================================================

@pytest.fixture(scope="module")
def db_conn():
    """Create an in-memory DB, run the full pipeline, yield the connection."""
    conn = sqlite3.connect(":memory:")

    # We need to temporarily patch DB_PATH usage if starter.py uses file paths.
    # The functions take conn as argument, so this should work directly.
    create_schema(conn)
    summary = ingest_data(conn)

    assert summary["total_raw_rows"] > 5000, "Expected at least 5000 raw rows"
    assert summary["rows_inserted"] > 4500, "Expected at least 4500 clean rows"
    assert summary["duplicates_removed"] > 0, "Expected some duplicates removed"
    assert summary["rows_skipped"] > 0, "Expected some rows skipped"

    yield conn
    conn.close()


class TestIngestion:
    def test_all_20_funds_present(self, db_conn):
        cursor = db_conn.execute("SELECT COUNT(DISTINCT fund_id) FROM nav_prices")
        count = cursor.fetchone()[0]
        assert count == 20, f"Expected 20 funds, got {count}"

    def test_no_null_navs(self, db_conn):
        cursor = db_conn.execute("SELECT COUNT(*) FROM nav_prices WHERE nav IS NULL")
        count = cursor.fetchone()[0]
        assert count == 0, "Found NULL NAVs in cleaned data"

    def test_no_duplicate_fund_date(self, db_conn):
        cursor = db_conn.execute(
            "SELECT fund_id, date, COUNT(*) as c FROM nav_prices GROUP BY fund_id, date HAVING c > 1"
        )
        dupes = cursor.fetchall()
        assert len(dupes) == 0, f"Found {len(dupes)} duplicate fund+date pairs"

    def test_fund_ids_normalised(self, db_conn):
        cursor = db_conn.execute("SELECT DISTINCT fund_id FROM nav_prices ORDER BY fund_id")
        ids = [row[0] for row in cursor.fetchall()]
        for fid in ids:
            assert fid.startswith("FND"), f"Fund ID not normalised: {fid}"
            assert len(fid) == 6, f"Fund ID wrong length: {fid}"


# =============================================================================
# Integration tests: query functions
# =============================================================================

class TestGetFundPerformance:
    def test_returns_valid_dict(self, db_conn):
        result = get_fund_performance(db_conn, "FND001", "2025-07-01", "2026-06-30")
        assert "fund_id" in result
        assert "total_return_pct" in result
        assert "start_nav" in result
        assert "end_nav" in result
        assert "data_points" in result
        assert result["data_points"] > 200

    def test_unknown_fund_raises(self, db_conn):
        with pytest.raises(ValueError):
            get_fund_performance(db_conn, "FND999", "2025-07-01", "2026-06-30")


class TestCompareFunds:
    def test_sorted_by_return(self, db_conn):
        result = compare_funds(
            db_conn, ["FND001", "FND003", "FND005"], "2025-07-01", "2026-06-30"
        )
        assert len(result) == 3
        returns = [r["total_return_pct"] for r in result]
        assert returns == sorted(returns, reverse=True)


class TestPortfolioReturn:
    def test_basic_portfolio(self, db_conn):
        result = get_portfolio_return(
            db_conn,
            [("FND001", 1000), ("FND003", 5000)],
            "2025-07-01",
            "2026-06-30",
        )
        assert "total_start_value" in result
        assert "total_end_value" in result
        assert "total_return_pct" in result
        assert "allocation" in result
        assert len(result["allocation"]) == 2

    def test_weights_sum_to_100(self, db_conn):
        result = get_portfolio_return(
            db_conn,
            [("FND001", 1000), ("FND003", 5000), ("FND010", 2000)],
            "2025-07-01",
            "2026-06-30",
        )
        total_weight = sum(a["weight_pct"] for a in result["allocation"])
        assert total_weight == pytest.approx(100.0, abs=0.1)

    def test_empty_holdings_raises(self, db_conn):
        with pytest.raises(ValueError):
            get_portfolio_return(db_conn, [], "2025-07-01", "2026-06-30")


# =============================================================================
# Add your own tests below this line
# =============================================================================

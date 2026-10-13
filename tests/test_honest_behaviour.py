from nyumba_mcp import server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_the_mortgage_estimate_is_an_annuity_not_income_times_months():
    """It computed income x 0.4 x 240 (KES 4.8M for a KES 50,000 income), ignoring interest: about 2.8x too high."""
    est = _fn("housing_finance_guide")(50000, None)["mortgage_estimate"]
    assert 1_600_000 < est["max_loan_kes"] < 1_800_000 and est["assumed_rate_pct"] == 13.0


def test_the_estimated_loan_really_is_repaid_by_forty_percent_of_income():
    est = _fn("housing_finance_guide")(50000, None)["mortgage_estimate"]
    r, n = 0.13 / 12, 240
    assert abs(est["max_loan_kes"] * r / (1 - (1 + r) ** -n) - 20000) < 5


def test_non_positive_income_is_an_error_not_silently_the_default_income():
    assert "error" in _fn("housing_finance_guide")(0, None) and "error" in _fn("housing_finance_guide")(-5, None)

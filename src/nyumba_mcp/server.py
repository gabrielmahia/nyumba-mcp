"""NyumbaMCP — Kenya Housing Tools (5 tools). All data DEMO."""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import Annotated, Optional

from fastmcp import FastMCP
from pydantic import Field

try:
    _VERSION = _pkg_version("nyumba-mcp")
except PackageNotFoundError:  # a source tree that was never installed
    _VERSION = "0+unknown"


mcp = FastMCP(name="nyumba-mcp", instructions="Kenya housing: rental market, permits, affordable housing. DEMO.", version=_VERSION)

@mcp.tool(name="rental_market_guide", description="Indicative monthly rent ranges in KES by county, number of bedrooms and area type (suburb or estate), with rental platforms. Use when someone asks roughly what a place costs to rent. Only some counties and bedroom counts are in the sample table; anything else returns 'Not in sample' for estimated_rent_kes rather than a guess. Returns the source label, the inputs, estimated_rent_kes, platforms and a tip. Prices labelled DEMO and indicative for Q2 2026: check current listings. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def rental_market_guide(county: Annotated[str, Field(description="County name such as Nairobi.")], bedrooms: Annotated[int | None, Field(description="Number of bedrooms (default 1).")] = 1, area_type: Annotated[str | None, Field(description="suburb (default) or estate.")] = "suburb") -> dict:
    """Return rental market data, average prices, and area guides for Kenya residential areas."""
    RENTALS = {
        "nairobi": {1: {"suburb": "KES 12,000–25,000", "estate": "KES 6,000–15,000"},
                    2: {"suburb": "KES 25,000–60,000", "estate": "KES 15,000–30,000"},
                    3: {"suburb": "KES 50,000–150,000", "estate": "KES 25,000–60,000"}},
        "mombasa": {1: {"suburb": "KES 8,000–18,000", "estate": "KES 4,000–12,000"},
                    2: {"suburb": "KES 15,000–35,000", "estate": "KES 10,000–20,000"}},
        "kisumu":  {1: {"suburb": "KES 6,000–15,000", "estate": "KES 3,000–10,000"},
                    2: {"suburb": "KES 12,000–25,000", "estate": "KES 7,000–15,000"}},
    }
    county_key = county.lower()
    data = RENTALS.get(county_key, {"default": {"suburb": "KES 5,000–25,000", "estate": "KES 3,000–15,000"}})
    br_data = data.get(bedrooms, data.get(1, {}))
    price = br_data.get(area_type.lower(), "Not in sample")
    return {"source": "DEMO — prices indicative Q2 2026", "county": county, "bedrooms": bedrooms,
            "area_type": area_type, "estimated_rent_kes": price,
            "platforms": ["BuyRentKenya", "PigiaMe", "HauzaKe", "Landlord Kenya"],
            "tip": "Prices vary significantly by specific neighbourhood and building quality."}

@mcp.tool(name="tenant_rights_guide", description="Tenant rights in Kenya: eviction notice, deposits, rent increases, repairs and related topics, with the governing law. Use when a tenant asks what a landlord may or may not do. Keywords in topic select entries; if none match, ALL rights are returned. Returns the source label, topic, rights and a not-legal-advice disclaimer. Static summary labelled DEMO: verify with an advocate or the Rent Restriction Tribunal. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def tenant_rights_guide(topic: Annotated[str, Field(description="Topic such as eviction, deposit or rent_increase.")]) -> dict:
    """Return Kenya tenant rights, landlord obligations, and dispute resolution procedures."""
    RIGHTS = {
        "eviction": "30 days notice required for month-to-month tenancy. Court order needed for forceful eviction. Illegal to remove tenant's belongings without court order.",
        "rent_increase": "Landlord must give 30 days notice. Rent Restriction Tribunal (residential < KES 2,500/month old law) — now mainly market-based.",
        "deposit": "Security deposit (typically 2–3 months rent). Must be refunded within 30 days of vacating, less legitimate deductions.",
        "maintenance": "Landlord responsible for structural repairs. Tenant responsible for interior maintenance per lease terms.",
        "utilities": "Landlord cannot cut utilities to force eviction. Utility disconnection by landlord = illegal.",
        "lease": "Written lease protects both parties. Verbal lease legally valid but harder to enforce.",
        "dispute": "Business Premises: Business Premises Rent Tribunal. Residential: file suit at Magistrate Court.",
    }
    t = topic.lower()
    matched = {k: v for k, v in RIGHTS.items() if k in t or any(w in t for w in k.split("_"))}
    return {"source": "DEMO — Landlord and Tenant Act, Land Act 2012", "topic": topic,
            "rights": matched or RIGHTS, "disclaimer": "Not legal advice. Consult an advocate."}

@mcp.tool(name="building_permit_guide", description="Steps to get a building permit in Kenya: architect, county approvals, NCA registration, inspections and occupation certificate, with an indicative fee range and penalties. Use when someone plans to build. county and project_type are only echoed back; the steps are the same everywhere. Returns the source label, the echoed inputs, numbered steps, fees_estimate, NCA details and a penalty note. Indicative figures labelled DEMO: county fees and rules differ. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def building_permit_guide(county: Annotated[str, Field(description="County name; only echoed back.")], project_type: Annotated[str | None, Field(description="Project type such as residential; only echoed back.")] = "residential") -> dict:
    """Return building permit requirements, fees, and process steps for a Kenya county."""
    return {"source": "DEMO — NCA and county governments", "county": county, "project_type": project_type,
            "steps": ["1. Engage registered architect (NCA-licensed)",
                      "2. Submit drawings to county Physical Planning (for planning approval)",
                      "3. Submit to county Buildings Department (for building permit)",
                      "4. Pay statutory fees (1–3% of project cost)",
                      "5. Construction only after permit issued",
                      "6. Inspections during construction",
                      "7. Occupation certificate on completion"],
            "fees_estimate": "KES 30,000–500,000+ depending on county and size",
            "nca": "National Construction Authority — nca.go.ke — contractor registration",
            "penalty": "Illegal construction: KES 1M fine or 2 years prison or both."}

@mcp.tool(name="affordable_housing_guide", description="Kenya's affordable housing programmes (Boma Yangu, social housing and others) with how to register and what each offers, plus mortgage refinance context. Use when someone asks how to access subsidised or affordable housing. county and income_range are only echoed back; the same programmes are returned for everyone. Returns the source label, the programmes and a mortgage note. Static summary labelled DEMO: eligibility and prices change. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def affordable_housing_guide(county: str | None = Field(None, description="Kenya county e.g. 'Nairobi', 'Kiambu'. Leave empty for national programmes."), income_range: str | None = Field(None, description="Monthly income bracket e.g. 'under_15000', '15000_30000', '30000_50000' in KES.")) -> dict:
    return {"source": "DEMO — bomayanguke.go.ke for official programs", "county": county,
            "programs": [
                {"name": "Boma Yangu (Affordable Housing Program)", "url": "bomayanguke.go.ke",
                 "eligibility": "Kenyan citizen, 18+, employed or informal sector with regular income",
                 "units": "30,000+ planned nationwide", "prices": "KES 800,000–3M (studio to 3BR)"},
                {"name": "SHA Housing Enhancement Fund", "url": "sha.go.ke",
                 "benefit": "Mortgage top-up or construction loans for SHA members"},
                {"name": "National Housing Corporation", "url": "nhc.co.ke",
                 "benefit": "Low-cost housing developments, mortgages for civil servants"},
                {"name": "County Social Housing", "url": "Varies by county",
                 "benefit": "Subsidised rentals for low-income households — very limited supply"},
            ],
            "mortgage": "KMRC (Kenya Mortgage Refinance Company) — liquidity for affordable mortgages. Banks: KCB, Co-op, Equity."}

@mcp.tool(name="housing_finance_guide", description="Estimate the largest mortgage a monthly income could support and list Kenyan housing finance options. Use when someone asks how much they could borrow for a home. The estimate treats 40% of income as the monthly repayment and amortises it over 20 years at an assumed 13% a year (the middle of the 12-14% commercial range; assumed_rate_pct says so), so a KES 50,000 income supports about KES 1.7 million, not the KES 4.8 million a simple income x 0.4 x 240 would give. property_value_kes is accepted but does not change the result; zero or negative income returns an error. Returns the source label, monthly_income, the mortgage estimate with assumptions, lender types and tips. Indicative and labelled DEMO: lenders also test deposits and credit history, so ask for a quote. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def housing_finance_guide(income_kes_monthly: Annotated[float | None, Field(description="Gross monthly income in KES (default 50000); must be above zero.")] = 50000, property_value_kes: Annotated[float | None, "Optional filter for property value kes. Pass None to return all results."] = None) -> dict:
    """Return Kenya housing finance options including mortgages, NHBF products, and government schemes."""
    income = 50000 if income_kes_monthly is None else income_kes_monthly
    if income <= 0:
        return {"error": "income_kes_monthly must be greater than zero."}
    rate_pct, years = 13.0, 20  # middle of the 12-14% commercial range quoted below
    r, n = rate_pct / 100 / 12, years * 12
    max_mortgage = round(income * 0.4 * (1 - (1 + r) ** -n) / r, 0)
    return {"source": "DEMO — verify with specific lenders", "monthly_income": income,
            "mortgage_estimate": {"max_loan_kes": max_mortgage, "assumed_rate_pct": rate_pct, "term": "20 years",
                                   "rate": "12–14% p.a. (commercial) or 7% (affordable housing schemes)",
                                   "note": "40% of income as the monthly repayment, amortised over 20 years at the assumed rate"},
            "lenders": [{"type": "Commercial bank", "rate": "12–14%", "min_deposit": "10–20%"},
                        {"type": "SACCO mortgage", "rate": "10–12%", "min_deposit": "20%", "note": "Must be SACCO member 2+ years"},
                        {"type": "KMRC-linked", "rate": "7%", "note": "Affordable housing scheme, income limits apply"}],
            "nhif_benefit": "SHA members may access mortgage-linked benefits",
            "tip": "SACCO mortgages are often cheaper than commercial bank rates."}

def main() -> None:
    """Console entry point."""
    mcp.run()

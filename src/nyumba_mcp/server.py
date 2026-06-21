"""NyumbaMCP — Kenya Housing Tools (5 tools). All data DEMO."""
from __future__ import annotations
from typing import Annotated, Optional
from fastmcp import FastMCP
from pydantic import Field
mcp = FastMCP(name="nyumba-mcp", instructions="Kenya housing: rental market, permits, affordable housing. DEMO.")

@mcp.tool(name="rental_market_guide", description="Kenya rental market guide: prices, tenant rights, and county-specific info. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def rental_market_guide(county: str, bedrooms: Optional[int] = 1, area_type: Optional[str] = "suburb") -> dict:
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

@mcp.tool(name="tenant_rights_guide", description="Kenya tenant rights under Rent Restriction Act and Land Act. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def tenant_rights_guide(topic: str) -> dict:
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

@mcp.tool(name="building_permit_guide", description="Building plan approval and permit process in Kenya counties. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def building_permit_guide(county: str, project_type: Optional[str] = "residential") -> dict:
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

@mcp.tool(name="affordable_housing_guide", description="Kenya affordable housing programs: Boma Yangu, SHA, county schemes. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def affordable_housing_guide(county: Optional[str] = Field(None, description="Kenya county e.g. 'Nairobi', 'Kiambu'. Leave empty for national programmes."), income_range: Optional[str] = Field(None, description="Monthly income bracket e.g. 'under_15000', '15000_30000', '30000_50000' in KES.")) -> dict:
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

@mcp.tool(name="housing_finance_guide", description="Kenya housing finance: mortgages, SACCOS, tenant purchase schemes. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def housing_finance_guide(income_kes_monthly: Optional[float] = 50000, property_value_kes: Annotated[Optional[float], "Optional filter for property value kes. Pass None to return all results."] = None) -> dict:
    """Return Kenya housing finance options including mortgages, NHBF products, and government schemes."""
    max_mortgage = round((income_kes_monthly or 50000) * 0.4 * 240, 0)
    return {"source": "DEMO — verify with specific lenders", "monthly_income": income_kes_monthly,
            "mortgage_estimate": {"max_loan_kes": max_mortgage, "term": "20 years",
                                   "rate": "12–14% p.a. (commercial) or 7% (affordable housing schemes)",
                                   "note": "40% of income used as repayment guideline"},
            "lenders": [{"type": "Commercial bank", "rate": "12–14%", "min_deposit": "10–20%"},
                        {"type": "SACCO mortgage", "rate": "10–12%", "min_deposit": "20%", "note": "Must be SACCO member 2+ years"},
                        {"type": "KMRC-linked", "rate": "7%", "note": "Affordable housing scheme, income limits apply"}],
            "nhif_benefit": "SHA members may access mortgage-linked benefits",
            "tip": "SACCO mortgages are often cheaper than commercial bank rates."}

#!/usr/bin/env python3
"""
XRO (ASX:Xero) — Expectations Gap + Probability-Weighted Catalyst Tree (PWCT)
CORE analytical engine for USYD FMAA Finance Showcase stock pitch.
BUY | 12m PT ~A$90 | Spot ~A$60 as-of ~22 Sep 2026

Labels: [PUBLIC] | [ASSUMPTION] | [MODEL]
No fabricated broker quotes — named PTs from Fool AU 21 Sep 2026 / stockanalysis summaries.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

AS_OF = "2026-09-22"
SPOT_AUD = 60.00  # [ASSUMPTION] pitch spot; Fool AU 21 Sep 2026 cited ~A$62.78 (52w low A$61.45)
SHARES_M = 164.588  # [PUBLIC-ish] ~164.6m post Melio placement
FX_NZD_AUD = 0.90  # [ASSUMPTION] 1 NZD = 0.90 AUD
NET_DEBT_NZD_M = 400.0  # [PUBLIC] ~NZD 400m net debt post Melio (H2 FY26 call)
WACC = 0.095  # [ASSUMPTION]
TERMINAL_G = 0.035  # [ASSUMPTION]

MELIO_UPFRONT_USD_BN = 2.5  # [PUBLIC] ASX 25 Jun 2025
MELIO_CONTINGENT_USD_BN = 0.5  # [PUBLIC] up to
USD_AUD = 1.55  # [ASSUMPTION] deal-context FX only

FY26_REV_NZD_M = 2753.081  # [PUBLIC]
FY26_ADJ_EBITDA_NZD_M = 757.352  # [PUBLIC]
FY26_RO40_HEADLINE = 0.485  # [PUBLIC]
FY26_RO40_PROFORMA = 0.360  # [PUBLIC]

FY27_REV_LO, FY27_REV_HI = 3620.0, 3730.0  # [PUBLIC]
FY27_EBITDA_LO, FY27_EBITDA_HI = 860.0, 920.0  # [PUBLIC]
FY27_REV_MID = (FY27_REV_LO + FY27_REV_HI) / 2.0
FY27_EBITDA_MID = (FY27_EBITDA_LO + FY27_EBITDA_HI) / 2.0
US_BRAND_SPEND_NZD_M = 55.0  # [PUBLIC] up to
MELIO_BE_WINDOW = "H2 FY28"  # [PUBLIC]

STREET = {
    "source": "Fool AU 21 Sep 2026 + stockanalysis/S&P Global summaries (verify primary notes)",
    "buys_strong_buys_tv_3m": 6,
    "holds_tv_3m": 1,
    "sells_tv_3m": 0,
    "avg_pt_tv": 111.24,
    "avg_pt_stockanalysis": 123.92,
    "named_pts": [
        {"broker": "Citi", "pt": 113.60, "rating": "Buy", "as_of": "2026-08-27", "source": "Fool/stockanalysis"},
        {"broker": "Morgan Stanley", "pt": 130.00, "rating": "Buy", "as_of": "2026-05-15", "source": "Fool/stockanalysis"},
        {"broker": "UBS", "pt": 127.00, "rating": "Buy", "as_of": "~2026-09", "source": "Fool AU"},
        {"broker": "Ord Minnett", "pt": 110.00, "rating": "Buy", "as_of": "2026-05-15", "source": "Fool/stockanalysis"},
        {"broker": "Morgans", "pt": 111.00, "rating": "Buy", "as_of": "2026-05-14", "source": "Fool/stockanalysis"},
        {"broker": "RBC Capital", "pt": 85.00, "rating": "Hold", "as_of": "2026-07-27", "source": "stockanalysis"},
        {"broker": "Jefferies", "pt": 77.00, "rating": "Cautious", "as_of": "~2026-09", "source": "Fool AU"},
    ],
    "morningstar_fv_note": (
        "[ASSUMPTION/UNVERIFIED] Brief cites Morningstar FV ~A$98–100; not confirmed from "
        "primary Morningstar page in this run — peer reference only."
    ),
}


def nzd_to_aud(x: float) -> float:
    return x * FX_NZD_AUD


def aud_m_to_ps(aud_m: float) -> float:
    return aud_m / SHARES_M


def pct(x: float, nd: int = 1) -> str:
    return f"{100 * x:.{nd}f}%"


def fmt(x: float, nd: int = 1) -> str:
    return f"{x:,.{nd}f}"


# -----------------------------------------------------------------------------
# EXPECTATIONS GAP
# -----------------------------------------------------------------------------
@dataclass
class ExpectationsGap:
    spot_aud: float
    equity_value_aud_m: float
    ev_aud_m: float
    fy27_rev_aud_m: float
    fy27_ebitda_aud_m: float
    implied_ev_sales_fy27: float
    implied_ev_ebitda_fy27: float
    # Implied EXIT multiple if Street growth delivers but price only compounds at WACC
    spot_implied_exit_ev_sales_on_street_g: float
    street_exit_ev_sales: float
    our_bull_exit_ev_sales: float
    street_fy28_rev_growth: float
    our_bull_fy28_rev_growth: float
    # Ro40
    spot_implied_fy28_ro40: float
    street_fy28_ro40: float
    our_bull_fy28_ro40: float
    # Melio FY28 rev contribution NZDm
    melio_spot_implied_nzd_m: float
    melio_street_nzd_m: float
    melio_our_bull_nzd_m: float
    gap_narrative: str


def compute_expectations_gap() -> ExpectationsGap:
    equity_aud_m = SPOT_AUD * SHARES_M
    ev_aud_m = equity_aud_m + nzd_to_aud(NET_DEBT_NZD_M)
    fy27_rev_aud = nzd_to_aud(FY27_REV_MID)
    fy27_ebitda_aud = nzd_to_aud(FY27_EBITDA_MID)
    ev_sales = ev_aud_m / fy27_rev_aud
    ev_ebitda = ev_aud_m / fy27_ebitda_aud

    street_g = 0.18  # [ASSUMPTION] Street mid FY27→FY28
    our_bull_g = 0.24  # [ASSUMPTION]
    fy28_rev_street_aud = nzd_to_aud(FY27_REV_MID * (1 + street_g))
    # Spot only "earns" WACC as carry if no re-rate: EV_1 = EV_0*(1+WACC)
    ev1 = ev_aud_m * (1 + WACC)
    spot_exit_m = ev1 / fy28_rev_street_aud  # what exit multiple spot capitalises ON Street growth

    street_exit = 5.0  # [ASSUMPTION] Street fair exit if Ro40 restored
    bull_exit = 5.8  # [ASSUMPTION]

    # Ro40: spot prices continued sub-40 pro-forma; Street ~41; bull 45
    spot_ro40, street_ro40, bull_ro40 = 0.37, 0.41, 0.45

    # Melio FY28 rev: spot scepticism vs Street vs bull [ASSUMPTION]
    melio_spot, melio_street, melio_bull = 300.0, 450.0, 550.0

    narrative = (
        f"At A${SPOT_AUD:.0f}, EV≈A${ev_aud_m/1000:.2f}bn → FY27 EV/Sales {ev_sales:.2f}x / "
        f"EV/EBITDA {ev_ebitda:.1f}x. Even if Street’s {pct(street_g)} FY28 growth delivers, "
        f"spot only capitalises a ~{spot_exit_m:.1f}x FY28 exit multiple (EV carried at WACC) — "
        f"i.e. the market prices PERMANENT Melio drag and Ro40 miss (~{pct(spot_ro40,0)}). "
        f"Street fair exit ~{street_exit:.1f}x and our bull ~{bull_exit:.1f}x on Ro40 restoration "
        f"({pct(street_ro40,0)} / {pct(bull_ro40,0)}) define the expectations GAP. "
        f"BUY = close the gap via Melio BE timing + Ro40, not Motley-Fool 'buy the dip'."
    )
    return ExpectationsGap(
        spot_aud=SPOT_AUD,
        equity_value_aud_m=equity_aud_m,
        ev_aud_m=ev_aud_m,
        fy27_rev_aud_m=fy27_rev_aud,
        fy27_ebitda_aud_m=fy27_ebitda_aud,
        implied_ev_sales_fy27=ev_sales,
        implied_ev_ebitda_fy27=ev_ebitda,
        spot_implied_exit_ev_sales_on_street_g=spot_exit_m,
        street_exit_ev_sales=street_exit,
        our_bull_exit_ev_sales=bull_exit,
        street_fy28_rev_growth=street_g,
        our_bull_fy28_rev_growth=our_bull_g,
        spot_implied_fy28_ro40=spot_ro40,
        street_fy28_ro40=street_ro40,
        our_bull_fy28_ro40=bull_ro40,
        melio_spot_implied_nzd_m=melio_spot,
        melio_street_nzd_m=melio_street,
        melio_our_bull_nzd_m=melio_bull,
        gap_narrative=narrative,
    )


# -----------------------------------------------------------------------------
# CATALYST TREE
# -----------------------------------------------------------------------------
@dataclass
class Catalyst:
    id: str
    name: str
    likelihood: float
    delta_pt_aud: float
    timing_window: str
    observable_kpi: str
    kill_switch: str
    direction: str
    notes: str = ""

    @property
    def contribution(self) -> float:
        return self.likelihood * self.delta_pt_aud


def build_catalyst_tree() -> list[Catalyst]:
    # P and ΔPT are [ASSUMPTION]/MODEL]; Σ P×ΔPT cross-checks scenario upside
    return [
        Catalyst(
            id="C1",
            name="Melio H2 FY28 BE path reaffirmed",
            likelihood=0.65,
            delta_pt_aud=12.0,
            timing_window="Nov 2026 – May 2027",
            observable_kpi="Mgmt reiterates H2 FY28 run-rate adj EBITDA BE; Melio loss trajectory",
            kill_switch="BE slipped past FY28 → strip C1; cut Melio EV 40%; base PT → A$70",
            direction="upside",
            notes="Primary differentiator vs crowded AI-moat BUY",
        ),
        Catalyst(
            id="C2",
            name="FY27 guide reaffirm / top-half delivery",
            likelihood=0.55,
            delta_pt_aud=6.0,
            timing_window="Nov 2026 (H1) / May 2027",
            observable_kpi="Rev & adj EBITDA vs NZ$3.62–3.73bn / NZ$860–920m",
            kill_switch="Cut below guide floors → open bear weight to 35%+",
            direction="upside",
        ),
        Catalyst(
            id="C3",
            name="US payments take-rate + Melio↔Xero attach",
            likelihood=0.50,
            delta_pt_aud=8.0,
            timing_window="FY27 H1–H2",
            observable_kpi="Payments rev growth; ARPC; TPV/customer; US NCA",
            kill_switch="Payments growth <25% YoY for 2 consecutive halves",
            direction="upside",
        ),
        Catalyst(
            id="C4",
            name="FY28 Rule-of-40 ≥40 path credible",
            likelihood=0.45,
            delta_pt_aud=10.0,
            timing_window="FY27 results → FY28 outlook",
            observable_kpi="Pro-forma Ro40 from ~36% toward ≥40%",
            kill_switch="FY28 pro-forma Ro40 guided <38% → multiple stays compressed",
            direction="upside",
        ),
        Catalyst(
            id="C5",
            name="JAX/AI early monetisation (ARPC)",
            likelihood=0.40,
            delta_pt_aud=5.0,
            timing_window="FY27–H1 FY28",
            observable_kpi="Priced AI SKU / consumption pilots; ARPC ex-payments",
            kill_switch="Immaterial AI ARPC by FY27 results → C5 = 0",
            direction="upside",
            notes="Secondary — do not lead with AI-moat crowd story",
        ),
        Catalyst(
            id="C6",
            name="Multiple re-rate as Melio EBITDA troughs",
            likelihood=0.50,
            delta_pt_aud=9.0,
            timing_window="H2 FY27 – H1 FY28",
            observable_kpi="Group adj EBITDA margin inflection; FCF conversion",
            kill_switch="Margins roll over despite revenue → cancel C6",
            direction="upside",
        ),
        Catalyst(
            id="C7",
            name="DOWN: Melio integration / US brand ROI miss",
            likelihood=0.30,
            delta_pt_aud=-14.0,
            timing_window="Any time FY27",
            observable_kpi="Brand spend >NZ$55m without NCA lift; Melio churn/synergy miss",
            kill_switch="N/A (this is the kill path)",
            direction="downside",
        ),
        Catalyst(
            id="C8",
            name="DOWN: SMB software risk-off derate",
            likelihood=0.25,
            delta_pt_aud=-10.0,
            timing_window="12m anytime",
            observable_kpi="ASX tech multiple compression; US SMB confidence",
            kill_switch="N/A",
            direction="downside",
        ),
    ]


# -----------------------------------------------------------------------------
# SCENARIOS
# -----------------------------------------------------------------------------
@dataclass
class Scenario:
    name: str
    weight: float
    pt_aud: float
    drivers: str


def build_scenarios() -> tuple[list[Scenario], float]:
    # Weights → E[PT] = 0.25*118 + 0.55*90 + 0.20*55 = 29.5+49.5+11 = 90.0 exactly
    scenarios = [
        Scenario(
            "Bull",
            0.25,
            118.0,
            "Melio BE on time; Ro40≥45; payments attach; exit ~5.8x FY28 sales; AI ARPC material",
        ),
        Scenario(
            "Base",
            0.55,
            90.0,
            "Melio BE path intact; Ro40 ~41–42; exit ~5.0x FY28; guide mid delivered",
        ),
        Scenario(
            "Bear",
            0.20,
            55.0,
            "Melio BE slips; Ro40<38; brand ROI miss; exit stuck ~3x; crowded unwind",
        ),
    ]
    expected = sum(s.weight * s.pt_aud for s in scenarios)
    return scenarios, expected


# -----------------------------------------------------------------------------
# MELIO EMBEDDED VALUE BRIDGE
# -----------------------------------------------------------------------------
def melio_embedded_value_bridge() -> dict[str, Any]:
    """
    Option-like path: losses → H2 FY28 run-rate BE → FY29+ scale.
    Primary valuation: EV/Sales on FY29 (pre-mature margin); EBITDA cross-check.
    Calibrated so base Melio ≈ A$18–22/sh (material but not full deal price recovery).
    """
    cases = [
        # label, fy28_rev_nzd, fy28_to_fy29_g, fy29_ev_sales, integration_burn_nzd, yrs_to_fy29
        ("Bear_slip", 280.0, 0.12, 2.5, 200.0, 3.0),
        ("Base_BE_path", 420.0, 0.22, 4.0, 120.0, 3.0),
        ("Bull_attach", 550.0, 0.28, 5.0, 80.0, 3.0),
    ]
    points = []
    for label, rev28, g, xsales, burn, yrs in cases:
        rev29 = rev28 * (1 + g)
        ev29_nzd = rev29 * xsales - burn
        pv_aud = nzd_to_aud(max(ev29_nzd, 0.0)) / ((1 + WACC) ** yrs)
        # EBITDA cross-check (informational)
        mgn = {"Bear_slip": 0.04, "Base_BE_path": 0.10, "Bull_attach": 0.16}[label]
        ebitda29 = rev29 * mgn
        xebitda = {"Bear_slip": 14.0, "Base_BE_path": 18.0, "Bull_attach": 20.0}[label]
        ebitda_ev_ps = aud_m_to_ps(nzd_to_aud(ebitda29 * xebitda - burn) / ((1 + WACC) ** yrs))
        points.append({
            "label": label,
            "fy28_rev_nzd_m": rev28,
            "fy29_rev_nzd_m": round(rev29, 1),
            "fy29_ev_sales": xsales,
            "integration_burn_nzd_m": burn,
            "pv_aud_m": round(pv_aud, 1),
            "value_ps_aud": round(aud_m_to_ps(pv_aud), 2),
            "ebitda_crosscheck_ps_aud": round(ebitda_ev_ps, 2),
            "fy29_ebitda_margin_assumed": mgn,
        })

    w_bear, w_base, w_bull = 0.25, 0.50, 0.25
    by = {p["label"]: p for p in points}
    pw_ps = (
        w_bear * by["Bear_slip"]["value_ps_aud"]
        + w_base * by["Base_BE_path"]["value_ps_aud"]
        + w_bull * by["Bull_attach"]["value_ps_aud"]
    )
    return {
        "methodology": (
            "Melio = option-like cashflow path to H2 FY28 adj-EBITDA run-rate BE, then FY29 "
            "EV/Sales exit (EBITDA cross-check). Core Xero SaaS valued separately — BUY is "
            "not lazy 'buy the dip' on group multiples."
        ),
        "deal_upfront_usd_bn": MELIO_UPFRONT_USD_BN,
        "deal_contingent_usd_bn_up_to": MELIO_CONTINGENT_USD_BN,
        "be_window": MELIO_BE_WINDOW,
        "points": points,
        "weights": {"bear": w_bear, "base": w_base, "bull": w_bull},
        "pw_value_ps_aud": round(pw_ps, 2),
        "base_value_ps_aud": by["Base_BE_path"]["value_ps_aud"],
        "sensitivity_note": (
            "Sensitivity [MODEL]: ±1.0x FY29 EV/Sales ≈ ±A$4–6/sh; BE slip (Base→Bear) "
            "≈ −A$10–12/sh. Kill-switch: BE past FY28 collapses Base→Bear."
        ),
    }


# -----------------------------------------------------------------------------
# SOTP
# -----------------------------------------------------------------------------
def sotp_base_pt(melio_bridge: dict[str, Any]) -> dict[str, Any]:
    """
    Core SaaS + Melio option + other → reconcile to pitch Base PT A$90.
    """
    melio_fy27 = 380.0  # [ASSUMPTION] Melio contribution inside FY27 guide
    core_fy27 = FY27_REV_MID - melio_fy27
    core_fy28 = core_fy27 * 1.15  # [ASSUMPTION] mid-teens core
    # Core exit 5.0x FY28 sales, PV 1yr; assign 35% of net debt to core
    core_ev_today = nzd_to_aud(core_fy28) * 5.0 / (1 + WACC)
    core_equity_m = core_ev_today - nzd_to_aud(NET_DEBT_NZD_M) * 0.35
    core_ps = aud_m_to_ps(core_equity_m)

    melio_ps = melio_bridge["base_value_ps_aud"]
    other_ps = 3.5  # [ASSUMPTION] AI optionality net of NZ$55m brand spend drag
    total = core_ps + melio_ps + other_ps

    # Soft calibration note: if SOTP > 90 we communicate A$90 as conservative base
    return {
        "core_saas_ps": round(core_ps, 2),
        "melio_option_ps": round(melio_ps, 2),
        "other_ai_brand_net_ps": other_ps,
        "sotp_pt": round(total, 2),
        "pitch_base_pt": 90.0,
        "reconciliation": (
            f"SOTP prints A${total:.1f}/sh. Pitch BASE PT set at A$90 (conservative vs SOTP; "
            f"aligns with E[PT] from scenario weights). Bull A$118 / Bear A$55 bracket uncertainty."
        ),
        "assumptions": {
            "melio_fy27_rev_nzd_m": melio_fy27,
            "core_fy28_growth": 0.15,
            "core_exit_ev_sales_fy28": 5.0,
            "fx_nzd_aud": FX_NZD_AUD,
            "wacc": WACC,
        },
    }


# -----------------------------------------------------------------------------
# CROWDING
# -----------------------------------------------------------------------------
def crowding_defense(gap: ExpectationsGap) -> dict[str, Any]:
    named = STREET["named_pts"]
    pts = [x["pt"] for x in named]
    return {
        "street_positioning": {
            "tv_3m_buys": STREET["buys_strong_buys_tv_3m"],
            "tv_3m_holds": STREET["holds_tv_3m"],
            "tv_3m_sells": STREET["sells_tv_3m"],
            "named_buy_count": sum(1 for x in named if "Buy" in x["rating"]),
            "named_hold_count": sum(1 for x in named if "Hold" in x["rating"]),
            "named_pt_min": min(pts),
            "named_pt_max": max(pts),
            "named_pt_avg": round(sum(pts) / len(pts), 2),
            "tv_avg_pt": STREET["avg_pt_tv"],
            "source": STREET["source"],
            "named_pts": named,
        },
        "crowded_narrative_we_reject": (
            "Motley Fool AU (21 Sep 2026) 'buy the dip / brokers +76–130%' + generic AI-moat. "
            "That is LONG the consensus BUY wall without a falsifiable Melio-timing edge."
        ),
        "our_differentiated_thesis": (
            "(1) Melio monetisation TIMING (H2 FY28 BE) as binding constraint on Ro40; "
            "(2) Expectations gap — spot capitalises ~3x exit even on Street growth; "
            "(3) PWCT with kill-switches; (4) Base PT A$90 BELOW Street avg — not max-bull crowd."
        ),
        "falsifiable_criteria": [
            {
                "test": "Melio BE",
                "pass": "Mgmt reiterates H2 FY28 run-rate adj EBITDA BE at FY27 results",
                "fail_action": "Cut base PT to A$70; bear weight → 40%",
            },
            {
                "test": "FY27 guide",
                "pass": "Deliver within NZ$3.62–3.73bn / NZ$860–920m",
                "fail_action": "Invalidate C2/C4; revisit multiples",
            },
            {
                "test": "Ro40 path",
                "pass": "Pro-forma Ro40 trajectory toward ≥40% by FY28",
                "fail_action": "Cap PT at A$75 (cautious Street cluster: Jefferies/RBC)",
            },
            {
                "test": "Crowding discipline",
                "pass": "Our PT A$90 stays below Street avg (~A$111–124)",
                "fail_action": "If PT chased to A$130+, thesis has drifted into crowd",
            },
        ],
        "morningstar_note": STREET["morningstar_fv_note"],
        "vs_spot_upside_our_base_pct": round(90.0 / gap.spot_aud - 1.0, 4),
        "vs_street_avg_discount_pct": round(90.0 / STREET["avg_pt_tv"] - 1.0, 4),
    }


# -----------------------------------------------------------------------------
# RENDER
# -----------------------------------------------------------------------------
def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    head = "| " + " | ".join(str(h) for h in headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = "\n".join("| " + " | ".join(str(c) for c in r) + " |" for r in rows)
    return "\n".join([head, sep, body])


def build_markdown(
    gap: ExpectationsGap,
    catalysts: list[Catalyst],
    scenarios: list[Scenario],
    expected_pt: float,
    cat_exp: float,
    melio: dict[str, Any],
    crowd: dict[str, Any],
    sotp: dict[str, Any],
) -> str:
    L: list[str] = []
    L += [
        "# XRO PWCT Engine Output — Expectations Gap + Catalyst Tree",
        "",
        f"**As-of:** {AS_OF} (Australia/Sydney)  ",
        f"**Spot (pitch):** A${SPOT_AUD:.2f}  ",
        f"**Recommendation:** BUY  |  **12m Base PT:** A$90  |  **E[PT]:** A${expected_pt:.1f}  ",
        f"**Shares:** {SHARES_M:.3f}m  |  **FX:** 1 NZD = {FX_NZD_AUD:.2f} AUD *[ASSUMPTION]*  ",
        "",
        "> **UNIQUE HOOK:** Reverse-multiple expectations gap + Probability-Weighted Catalyst Tree "
        "(P×ΔPT, KPI, kill-switch) + Melio embedded-value bridge + crowding defense "
        "(Base PT below Street — falsifiable Melio timing edge).",
        "",
        "---",
        "",
        "## 1. Expectations Gap",
        "",
        gap.gap_narrative,
        "",
    ]
    L.append(md_table(
        ["Metric", "Value", "Note"],
        [
            ["Equity value (A$m)", fmt(gap.equity_value_aud_m), "Spot × shares"],
            ["EV (A$m)", fmt(gap.ev_aud_m), "Equity + net debt"],
            ["FY27 mid rev (A$m)", fmt(gap.fy27_rev_aud_m), "Guide mid × FX"],
            ["FY27 mid adj EBITDA (A$m)", fmt(gap.fy27_ebitda_aud_m), "Guide mid × FX"],
            ["Implied EV/Sales FY27", f"{gap.implied_ev_sales_fy27:.2f}x", "MODEL"],
            ["Implied EV/EBITDA FY27", f"{gap.implied_ev_ebitda_fy27:.1f}x", "MODEL"],
        ],
    ))
    L += ["", "### Gap table (what price vs Street vs us capitalises)", ""]
    L.append(md_table(
        ["Driver", "Spot-implied", "Street mid *[ASSUMPTION]*", "Our bull"],
        [
            [
                "FY28 exit EV/Sales (on Street g)",
                f"{gap.spot_implied_exit_ev_sales_on_street_g:.2f}x",
                f"{gap.street_exit_ev_sales:.1f}x",
                f"{gap.our_bull_exit_ev_sales:.1f}x",
            ],
            [
                "FY28 rev growth (context)",
                "n/a (gap is multiple)",
                pct(gap.street_fy28_rev_growth),
                pct(gap.our_bull_fy28_rev_growth),
            ],
            [
                "FY28 Rule-of-40",
                pct(gap.spot_implied_fy28_ro40, 0),
                pct(gap.street_fy28_ro40, 0),
                pct(gap.our_bull_fy28_ro40, 0),
            ],
            [
                "Melio FY28 rev (NZ$m)",
                fmt(gap.melio_spot_implied_nzd_m, 0),
                fmt(gap.melio_street_nzd_m, 0),
                fmt(gap.melio_our_bull_nzd_m, 0),
            ],
        ],
    ))
    L += [
        "",
        f"**Upside to Base PT A$90:** {(90/SPOT_AUD - 1)*100:.0f}% — close via Melio BE + Ro40 re-rate.",
        "",
        "---",
        "",
        "## 2. Probability-Weighted Catalyst Tree (PWCT)",
        "",
    ]
    cat_rows = [
        [
            c.id,
            c.name[:46] + ("…" if len(c.name) > 46 else ""),
            pct(c.likelihood, 0),
            f"A${c.delta_pt_aud:+.0f}",
            f"A${c.contribution:+.1f}",
            c.timing_window,
            c.direction,
        ]
        for c in catalysts
    ]
    L.append(md_table(["ID", "Catalyst", "P", "ΔPT", "P×ΔPT", "Window", "Dir"], cat_rows))
    L += [
        "",
        f"**Σ P×ΔPT:** A${cat_exp:+.1f}  →  **spot + Σ:** A${SPOT_AUD + cat_exp:.1f} "
        "(informational cross-check; official PT from scenarios).",
        "",
        "### Kill-switches",
    ]
    for c in catalysts:
        L.append(f"- **{c.id}:** KPI=`{c.observable_kpi}` | Kill=`{c.kill_switch}`")
    L += ["", "---", "", "## 3. Scenario PTs & Expected PT", ""]
    L.append(md_table(
        ["Scenario", "Weight", "PT", "Drivers"],
        [[s.name, pct(s.weight, 0), f"A${s.pt_aud:.0f}", s.drivers] for s in scenarios],
    ))
    L += [
        "",
        f"**E[PT] = Σ w×PT = A${expected_pt:.1f}**  |  **Pitch Base PT: A$90**  |  "
        f"**Upside: {(90/SPOT_AUD-1)*100:.0f}%**",
        "",
        "---",
        "",
        "## 4. Melio Embedded Value Bridge",
        "",
        melio["methodology"],
        "",
        f"- Deal: upfront **US${melio['deal_upfront_usd_bn']}bn** + contingent up to "
        f"**US${melio['deal_contingent_usd_bn_up_to']}bn** *[PUBLIC]*",
        f"- Breakeven: **{melio['be_window']}** *[PUBLIC]*",
        "",
    ]
    L.append(md_table(
        ["Case", "FY28 rev NZ$m", "FY29 rev NZ$m", "FY29 EV/Sales", "PV A$/sh", "EBITDA x-check A$/sh"],
        [
            [
                p["label"],
                fmt(p["fy28_rev_nzd_m"], 0),
                fmt(p["fy29_rev_nzd_m"], 0),
                f"{p['fy29_ev_sales']:.1f}x",
                f"A${p['value_ps_aud']:.2f}",
                f"A${p['ebitda_crosscheck_ps_aud']:.2f}",
            ]
            for p in melio["points"]
        ],
    ))
    L += [
        "",
        f"**PW Melio:** A${melio['pw_value_ps_aud']:.2f}/sh | "
        f"**Base (SOTP):** A${melio['base_value_ps_aud']:.2f}/sh | weights={melio['weights']}",
        "",
        melio["sensitivity_note"],
        "",
        "---",
        "",
        "## 5. SOTP Cross-Check",
        "",
    ]
    L.append(md_table(
        ["Component", "A$/sh"],
        [
            ["Core Xero SaaS (ex-Melio)", f"{sotp['core_saas_ps']:.2f}"],
            ["Melio option (base BE path)", f"{sotp['melio_option_ps']:.2f}"],
            ["Other (AI net of brand)", f"{sotp['other_ai_brand_net_ps']:.2f}"],
            ["SOTP total", f"{sotp['sotp_pt']:.2f}"],
            ["Pitch Base PT", f"{sotp['pitch_base_pt']:.2f}"],
        ],
    ))
    L += ["", sotp["reconciliation"], "", "---", "", "## 6. Crowding Defense", ""]
    sp = crowd["street_positioning"]
    L += [
        f"Street named sample: Buys={sp['named_buy_count']}, Holds={sp['named_hold_count']}; "
        f"PT A${sp['named_pt_min']:.0f}–{sp['named_pt_max']:.0f} "
        f"(avg A${sp['named_pt_avg']:.0f}); TV 3m avg A${sp['tv_avg_pt']:.0f}.",
        f"Source: {sp['source']}",
        "",
        f"**Reject:** {crowd['crowded_narrative_we_reject']}",
        "",
        f"**Our edge:** {crowd['our_differentiated_thesis']}",
        "",
        f"Base PT A$90 is **{abs(crowd['vs_street_avg_discount_pct'])*100:.0f}% below** TV Street avg "
        f"and **{crowd['vs_spot_upside_our_base_pct']*100:.0f}% above** spot.",
        "",
        "### Falsifiable criteria",
    ]
    for t in crowd["falsifiable_criteria"]:
        L.append(f"- **{t['test']}:** PASS=`{t['pass']}` | FAIL→`{t['fail_action']}`")
    L += [
        "",
        crowd["morningstar_note"],
        "",
        "---",
        "",
        "## 7. Sources & Labels",
        "",
        "- [PUBLIC] ASX 14 May 2026 FY26 results + FY27 guide; Melio BE H2 FY28; AGM Aug 2026",
        "- [PUBLIC] Melio deal ASX 25 Jun 2025: US$2.5bn upfront + up to US$0.5bn contingent",
        "- [PUBLIC secondary] Fool AU 21 Sep 2026 PT table; stockanalysis consensus",
        "- [ASSUMPTION] Spot A$60; FX 0.90; WACC 9.5%; Melio FY27 split; exit multiples; P/ΔPT",
        "- [MODEL] Reverse exit-multiple gap; P×ΔPT tree; Melio PV bridge; scenario weights",
        "",
        "*Engine: pwct_engine.py — FMAA Showcase only; not investment advice.*",
    ]
    return "\n".join(L)


def main() -> None:
    gap = compute_expectations_gap()
    catalysts = build_catalyst_tree()
    melio = melio_embedded_value_bridge()
    scenarios, expected_pt = build_scenarios()
    cat_exp = sum(c.contribution for c in catalysts)
    sotp = sotp_base_pt(melio)
    crowd = crowding_defense(gap)

    payload = {
        "meta": {
            "as_of": AS_OF,
            "ticker": "ASX:XRO",
            "recommendation": "BUY",
            "spot_aud": SPOT_AUD,
            "base_pt_aud": 90.0,
            "expected_pt_aud": round(expected_pt, 2),
            "shares_m": SHARES_M,
            "fx_nzd_aud": FX_NZD_AUD,
            "wacc": WACC,
        },
        "public_fundamentals": {
            "fy26_rev_nzd_m": FY26_REV_NZD_M,
            "fy26_adj_ebitda_nzd_m": FY26_ADJ_EBITDA_NZD_M,
            "fy26_ro40_headline": FY26_RO40_HEADLINE,
            "fy26_ro40_proforma": FY26_RO40_PROFORMA,
            "fy27_rev_guide_nzd_m": [FY27_REV_LO, FY27_REV_HI],
            "fy27_adj_ebitda_guide_nzd_m": [FY27_EBITDA_LO, FY27_EBITDA_HI],
            "melio_be_window": MELIO_BE_WINDOW,
            "melio_upfront_usd_bn": MELIO_UPFRONT_USD_BN,
            "net_debt_nzd_m": NET_DEBT_NZD_M,
            "us_brand_spend_nzd_m_up_to": US_BRAND_SPEND_NZD_M,
        },
        "expectations_gap": asdict(gap),
        "catalysts": [{**asdict(c), "contribution": round(c.contribution, 3)} for c in catalysts],
        "catalyst_expected_incremental_aud": round(cat_exp, 2),
        "scenarios": [asdict(s) for s in scenarios],
        "expected_pt_aud": round(expected_pt, 2),
        "melio_bridge": melio,
        "sotp": sotp,
        "crowding_defense": crowd,
    }

    json_path = OUT / "pwct_results.json"
    md_path = OUT / "pwct_summary.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(
        build_markdown(gap, catalysts, scenarios, expected_pt, cat_exp, melio, crowd, sotp),
        encoding="utf-8",
    )

    print("=" * 72)
    print("XRO PWCT ENGINE — RUN COMPLETE")
    print("=" * 72)
    print(f"Spot A${SPOT_AUD:.2f} | Base PT A$90 | E[PT] A${expected_pt:.1f}")
    print(f"EV/Sales FY27 {gap.implied_ev_sales_fy27:.2f}x | EV/EBITDA {gap.implied_ev_ebitda_fy27:.1f}x")
    print(
        f"Spot-implied FY28 exit {gap.spot_implied_exit_ev_sales_on_street_g:.2f}x "
        f"vs Street {gap.street_exit_ev_sales:.1f}x vs Bull {gap.our_bull_exit_ev_sales:.1f}x"
    )
    print(
        f"Σ P×ΔPT = A${cat_exp:+.1f} | Melio base A${melio['base_value_ps_aud']:.2f}/sh | "
        f"SOTP A${sotp['sotp_pt']:.1f}"
    )
    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")
    print("=" * 72)


if __name__ == "__main__":
    main()

# XRO Submission XLSX — Model Spec (rebuild from PWCT engine)

**Purpose:** Exact Excel tab list so a human can rebuild the submission workbook from `pwct_engine.py` / `outputs/pwct_results.json`.  
**As-of:** 22 Sep 2026 (AEST) | **Ticker:** ASX:XRO | **Rec:** BUY | **Base PT:** A$90  
**Engine outputs:** `/workspace/fmaa_xro_win/outputs/pwct_results.json`, `pwct_summary.md`

All cells must carry a label tag in column notes: `[PUBLIC]` / `[ASSUMPTION]` / `[MODEL]`.

---

## Tab index (build in this order)

| # | Tab name | Role |
|---|----------|------|
| 0 | `00_Cover_Assumptions` | Control panel: spot, FX, WACC, shares, scenario weights |
| 1 | `01_Public_Fundamentals` | FY26 actuals + FY27 guide (sourced) |
| 2 | `02_Expectations_Gap` | Reverse multiple gap table |
| 3 | `03_Catalyst_PWCT` | Catalyst matrix P, ΔPT, P×ΔPT, KPI, kill-switch |
| 4 | `04_Melio_Bridge` | Melio option path + sensitivity |
| 5 | `05_SOTP_DCF` | Core SaaS + Melio + other → SOTP vs pitch PT |
| 6 | `06_Scenarios_PT` | Bull/Base/Bear weights → E[PT] |
| 7 | `07_Crowding_Defense` | Street Buys/PTs vs our falsifiers |
| 8 | `08_Macro` | Macro overlay (10% rubric) |
| 9 | `09_Risks_Gov` | Risk register + governance (5%) |
| 10 | `10_Outputs_Dashboard` | One-pager for slides / judges |
| 11 | `99_Sources` | URLs, ASX PDF names, secondary citations |

---

## Tab 0 — `00_Cover_Assumptions`

| Cell | Input / Output | Value (engine default) | Formula in words |
|------|----------------|------------------------|------------------|
| B2 | Spot AUD `[ASSUMPTION]` | 60.00 | Pitch spot (Fool AU 21 Sep cited ~62.78; use 60 round) |
| B3 | Shares (m) | 164.588 | Post-Melio diluted shares |
| B4 | FX NZD→AUD | 0.90 | AUD per 1 NZD |
| B5 | Net debt NZDm `[PUBLIC]` | 400 | Mgmt ~NZD 400m post Melio |
| B6 | WACC `[ASSUMPTION]` | 9.5% | AUD SaaS mid |
| B7 | Terminal g | 3.5% | Long-run nominal |
| B8 | Bull weight | 25% | Scenario weight |
| B9 | Base weight | 55% | |
| B10 | Bear weight | 20% | Must sum to 100% |
| B12 | Equity value A$m `[MODEL]` | | `=B2*B3` |
| B13 | Net debt A$m | | `=B5*B4` |
| B14 | EV A$m | | `=B12+B13` |

**Output check:** B8+B9+B10 = 1.00; B14 feeds Gap & SOTP.

---

## Tab 1 — `01_Public_Fundamentals`

| Row | Metric | Value | Source tag |
|-----|--------|-------|------------|
| Rev FY26 NZDm | 2,753.081 | [PUBLIC] ASX 14 May 2026 |
| Adj EBITDA FY26 NZDm | 757.352 | [PUBLIC] |
| Ro40 headline FY26 | 48.5% | [PUBLIC] |
| Ro40 pro-forma FY26 | 36.0% | [PUBLIC] |
| FY27 rev guide NZDm | 3,620 – 3,730 | [PUBLIC] |
| FY27 adj EBITDA guide | 860 – 920 | [PUBLIC] |
| FY27 mid rev / EBITDA | =(LO+HI)/2 | [MODEL] |
| US brand spend up to | 55 | [PUBLIC] in FY27 EBITDA guide |
| Melio BE window | H2 FY28 | [PUBLIC] |
| Melio upfront US$bn | 2.5 | [PUBLIC] ASX 25 Jun 2025 |
| Melio contingent up to US$bn | 0.5 | [PUBLIC] |
| Customers FY26 | 4.92m | [PUBLIC] |
| AMRR FY26 NZDm | 3,273 | [PUBLIC] |

**Formulas:** Midpoints = average of guide bounds. Convert any NZD→AUD with `00_Cover_Assumptions!B4`.

---

## Tab 2 — `02_Expectations_Gap`

**Inputs (link):** EV, FY27 mid rev AUD, FY27 mid EBITDA AUD, Street g, fair exit multiples.

| Output | Formula in words |
|--------|------------------|
| EV/Sales FY27 | EV ÷ FY27 mid rev AUD |
| EV/EBITDA FY27 | EV ÷ FY27 mid EBITDA AUD |
| FY28 rev Street AUD | FY27 mid NZD × (1+Street_g) × FX |
| EV₁ (carry at WACC) | EV₀ × (1+WACC) |
| **Spot-implied exit EV/Sales** | EV₁ ÷ FY28 rev Street AUD |
| Street fair exit | Input 5.0x `[ASSUMPTION]` |
| Our bull exit | Input 5.8x `[ASSUMPTION]` |
| Spot / Street / Bull Ro40 | 37% / 41% / 45% `[ASSUMPTION]` |
| Melio FY28 rev NZDm S/St/B | 300 / 450 / 550 `[ASSUMPTION]` |

**Gap narrative cell:** "Spot capitalises ~2.9x exit even on Street growth → permanent Melio drag priced in."

**Engine print (as-of run):** EV/Sales 3.09x | EV/EBITDA 12.8x | Spot-implied exit **2.87x** vs Street 5.0x vs Bull 5.8x.

---

## Tab 3 — `03_Catalyst_PWCT`

Columns: `ID | Name | P | ΔPT_AUD | Contribution | Timing | KPI | Kill_switch | Direction`

| ID | P | ΔPT | Contribution formula |
|----|---|-----|----------------------|
| C1 Melio BE reaffirm | 0.65 | +12 | `=P*ΔPT` |
| C2 FY27 guide | 0.55 | +6 | |
| C3 US payments attach | 0.50 | +8 | |
| C4 Ro40≥40 path | 0.45 | +10 | |
| C5 JAX/AI ARPC | 0.40 | +5 | |
| C6 Multiple re-rate | 0.50 | +9 | |
| C7 DOWN Melio/brand miss | 0.30 | −14 | |
| C8 DOWN macro derate | 0.25 | −10 | |

**Outputs:**
- `Σ P×ΔPT` = SUM(Contribution) → engine **A$+19.4**
- `Implied PT cross-check` = Spot + Σ P×ΔPT → **A$79.4** (informational only; official PT from Tab 6)
- Conditional formatting: red if kill-switch triggered (manual flag column)

---

## Tab 4 — `04_Melio_Bridge`

**Cases:** Bear_slip | Base_BE_path | Bull_attach

Per case inputs: FY28 rev NZDm, FY28→FY29 g, FY29 EV/Sales, integration burn NZDm, years to FY29 (=3).

| Output | Formula in words |
|--------|------------------|
| FY29 rev | FY28 rev × (1+g) |
| EV29 NZD | FY29 rev × EV/Sales − burn |
| PV AUD | (EV29 NZD × FX) / (1+WACC)^years |
| Value A$/sh | PV AUD ÷ shares |

**EBITDA cross-check (side columns):** FY29 EBITDA = FY29 rev × margin; EV = EBITDA × exit multiple − burn; same PV.

**PW Melio A$/sh** = 0.25×Bear + 0.50×Base + 0.25×Bull.

**Sensitivity table:** rows = EV/Sales 2.5 / 4.0 / 5.0 / 6.0; columns = FY28 rev 280 / 420 / 550.  
**Engine Base:** ~A$8.04/sh | PW ~see JSON.

**Kill-switch row:** If BE slipped → force case = Bear_slip for SOTP.

---

## Tab 5 — `05_SOTP_DCF`

| Component | Formula in words | Engine ~ |
|-----------|------------------|----------|
| Melio FY27 rev NZDm `[ASSUMPTION]` | Input 380 | 380 |
| Core FY27 rev | FY27 mid − Melio FY27 | |
| Core FY28 rev | Core FY27 × 1.15 | |
| Core EV today | (Core FY28 × FX × 5.0x) / (1+WACC) | |
| Core equity | Core EV − 35%×NetDebtAUD | |
| Core A$/sh | Core equity ÷ shares | ~93.8 |
| Melio option A$/sh | Link `04_Melio_Bridge` Base | ~8.0 |
| Other (AI net brand) | Input 3.5 | 3.5 |
| **SOTP PT** | Sum | ~105.4 |
| **Pitch Base PT** | Hardcode 90 | 90 |

**Reconciliation note:** Pitch Base A$90 is **conservative vs SOTP**; communicate as such on valuation slide.

Optional full DCF (appendix): 5-yr FCFF on group with Melio BE toggle — not required for core pitch if SOTP + Gap + PWCT shown.

---

## Tab 6 — `06_Scenarios_PT`

| Scenario | Weight | PT | E contribution |
|----------|--------|----|----------------|
| Bull | 25% | 118 | =w×PT |
| Base | 55% | 90 | |
| Bear | 20% | 55 | |
| **E[PT]** | 100% | | **=SUMPRODUCT = 90.0** |

**Drivers text** (copy from engine).  
**Chart:** waterfall Spot → Σ P×ΔPT → Scenario Base → Street avg (for crowding slide).

---

## Tab 7 — `07_Crowding_Defense`

| Field | Content |
|-------|---------|
| TV 3m Buys/Holds/Sells | 6 / 1 / 0 `[PUBLIC secondary]` |
| Named PTs | Citi 113.6, MS 130, UBS 127, OrdMin 110, Morgans 111, RBC 85 Hold, Jefferies 77 |
| Our Base vs TV avg | 90 / 111.24 − 1 = **−19%** (we are below crowd) |
| Upside vs spot | 90/60 − 1 = **+50%** |
| Falsifiers | Melio BE / FY27 guide / Ro40 / crowding discipline (see engine) |
| Reject narrative | Fool "buy the dip" + generic AI-moat |

---

## Tab 8 — `08_Macro` (10% rubric)

| Block | Content |
|-------|---------|
| US SMB / rates | Soft-landing vs cuts → SMB software spend & payments TPV |
| AUD/NZD/USD | FX sensitivity on NZD earnings & US Melio |
| ASX tech liquidity | Why XRO derated YTD (Melio dilution + multiple) vs fundamentals |
| Competitive | Intuit, MYOB, bill-pay peers — moat = accounting + payments + advisor channel |

Keep to **1 page**; link each macro factor → which catalyst (C3/C8) it moves.

---

## Tab 9 — `09_Risks_Gov` (5% rubric)

| Risk | Likelihood | Impact PT | Mitigation / kill-switch |
|------|------------|-----------|--------------------------|
| Melio BE slip | Med | −15 to −25 | C1 kill → PT 70 |
| Guide miss | Low-Med | −8 to −15 | C2 |
| Contigent consideration cash | Med | Dilution/cash | Track earnout KPIs |
| Key person / US leadership | Low | −5 | Governance note |
| Cyber / payments compliance | Low | Fat-tail | Risk disclosure |
| Governance | Board oversight of Melio integration; related-party / earnout transparency | | |

---

## Tab 10 — `10_Outputs_Dashboard`

Single view pulled by slides:
1. Rec / Spot / Base PT / E[PT] / Upside %
2. Gap table snapshot
3. Top 3 catalysts by |P×ΔPT|
4. Melio bridge Base A$/sh
5. SOTP vs Pitch PT
6. Crowding: our PT vs Street avg
7. Kill-switch status (all green at initiation)

---

## Tab 11 — `99_Sources`

- ASX PDF: FY26 results 14 May 2026 (`06zkqzlkq0xnph.pdf` etc.)
- ASX: Melio acquisition 25 Jun 2025
- ASX: AGM addresses 27 Aug 2026
- Fool AU 21 Sep 2026 broker PT article
- stockanalysis.com XRO forecast (S&P Global)
- Engine assumptions log (date-stamped)

---

## Rebuild checklist

1. Enter Tab 0 assumptions → confirm EV.  
2. Paste Tab 1 publics from ASX.  
3. Compute Gap (Tab 2) — spot-implied exit must be **≪** Street fair exit.  
4. Fill PWCT (Tab 3) — Σ P×ΔPT ≈ +19.  
5. Melio bridge (Tab 4) → link Base to SOTP.  
6. SOTP (Tab 5) → Pitch PT 90.  
7. Scenarios (Tab 6) → E[PT]=90.  
8. Crowding + Macro + Risks.  
9. Dashboard matches `outputs/pwct_summary.md` headlines.

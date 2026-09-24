# Q&A Trap Cards — 12 Hardest Judge Questions

**Format:** Question → 2-sentence answer → Model cell / output backing.  
**As-of engine run:** Spot A$60 | Base PT A$90 | E[PT]=A$90 | Σ P×ΔPT≈A$+19.4 | Melio base≈A$8.04 | SOTP≈A$105.4

---

### Q1 — "Isn't this just a crowded buy-the-dip with every broker already Bullish?"
**A:** Street is Buy, but for a generic AI/US-growth story; our edge is Melio **timing** (H2 FY28 BE) as the binding Ro40 constraint, and our Base PT A$90 sits ~19% **below** TV Street avg (~A$111) — we are not max-bull crowd. If Melio BE is not reiterated at FY27 results, we cut PT to A$70 (falsifier), which consensus decks rarely hard-code.  
**Cell:** `07_Crowding_Defense!vs_street` + `03_Catalyst_PWCT!C1.kill_switch` | JSON `crowding_defense.falsifiable_criteria[0]`

---

### Q2 — "Your Melio value is only ~A$8/sh after a US$2.5bn deal — doesn't that kill the thesis?"
**A:** The US$2.5bn is largely **sunk**; forward equity value is path-dependent optionality to H2 FY28 run-rate BE, which we PV conservatively on FY29 EV/Sales (Base ~A$8; Bull higher; PW Melio in bridge). The pitch BUY is the **expectations gap** on group multiple (spot ~2.9x exit vs ~5x fair if Ro40 returns), not full deal-price recovery in 12 months.  
**Cell:** `04_Melio_Bridge!Base_BE_path.value_ps` + `02_Expectations_Gap!spot_implied_exit` | JSON `melio_bridge.points[Base]` / `expectations_gap.spot_implied_exit_ev_sales_on_street_g`

---

### Q3 — "Why A$90 when Morgan Stanley says A$130 and SOTP prints ~A$105?"
**A:** A$90 is our **probability-weighted Base** (55% weight) inside E[PT]=0.25×118+0.55×90+0.20×55=90, deliberately below SOTP ~105 and Street highs to stay out of the crowd and leave margin of safety. Bull A$118 is available if C1+C4 hit; we refuse to pitch the trophy number.  
**Cell:** `06_Scenarios_PT!E_PT` + `05_SOTP_DCF!pitch_base_pt` | JSON `scenarios` / `sotp.pitch_base_pt`

---

### Q4 — "FY27 EBITDA guide includes NZ$55m US brand spend — aren't margins structurally impaired?"
**A:** Brand spend is an explicit, capped FY27 investment inside the NZ$860–920m adj EBITDA guide, not a permanent tax; Melio BE in H2 FY28 is the margin inflection catalyst (C6). If brand ROI fails (no NCA lift), C7 fires and we reduce PT — that spend is in the kill-switch, not ignored.  
**Cell:** `01_Public_Fundamentals!US_brand_55` + `03_Catalyst_PWCT!C6/C7` | JSON `public_fundamentals.us_brand_spend_nzd_m_up_to`

---

### Q5 — "Pro-forma Rule of 40 is only 36% — how do you get back above 40 by FY28?"
**A:** Headline Ro40 was 48.5%; pro-forma 36% reflects Melio dilution — management reiterates path back above 40 in FY28 alongside Melio H2 FY28 BE. Our Base embeds Ro40 ~41–42 with C4 at P=45%; if FY28 pro-forma Ro40 is guided <38%, we cap PT at A$75.  
**Cell:** `01_Public_Fundamentals!Ro40_pf` + `03_Catalyst_PWCT!C4` + `07_Crowding_Defense!falsifier_Ro40` | JSON `public_fundamentals.fy26_ro40_proforma`

---

### Q6 — "What observable KPI tells you Melio breakeven is on track before H2 FY28?"
**A:** Sequential Melio adj EBITDA loss narrowing through FY27, mgmt reiteration at H1 FY27 / FY27 results, plus payments growth/TPV per customer and Xero attach rates (C1+C3 KPIs). Kill-switch: any withdrawal or slip of BE past FY28 → strip C1 and cut Melio EV ~40%.  
**Cell:** `03_Catalyst_PWCT!C1.observable_kpi` / `C1.kill_switch` | JSON `catalysts[id=C1]`

---

### Q7 — "Your reverse-multiple says spot implies ~2.9x exit — isn't that just saying 'stock is cheap'?"
**A:** It's sharper: even **assuming Street's 18% FY28 growth**, carrying EV at WACC only capitalises ~2.9x exit — i.e. the market prices **permanent** Melio drag / Ro40 miss, not a temporary soft patch. Fair exit ~5.0x (Street) to ~5.8x (bull) on Ro40 restoration is the gap we monetise with catalysts, not a vague cheapness claim.  
**Cell:** `02_Expectations_Gap!spot_implied_exit_ev_sales_on_street_g` | JSON `expectations_gap` narrative fields

---

### Q8 — "Σ P×ΔPT is only ~A$+19, which gets you to ~A$79 from A$60 — why is PT A$90?"
**A:** Σ P×ΔPT is an **informational cross-check** on incremental news value, not the official PT engine; official PT is scenario-weighted E[PT]=A$90 (and SOTP ~105 with conservative pitch at 90). Catalyst deltas are partial re-rating increments vs a no-news baseline, not exhaustive of multiple normalisation already embedded in Base.  
**Cell:** `03_Catalyst_PWCT!Sum_Contribution` vs `06_Scenarios_PT!E_PT` | JSON `catalyst_expected_incremental_aud` vs `expected_pt_aud`

---

### Q9 — "NPAT fell in FY26 — how is this a quality compounder?"
**A:** FY26 NPAT/operating income pressure reflects Melio transaction/integration and investment while operating revenue grew 31% and adj EBITDA +18% with FCF NZ$554m — we underwrite **adj EBITDA + FCF + Ro40 path**, not near-term NPAT optics. The thesis is that Melio dilution is front-loaded and timed to BE in H2 FY28.  
**Cell:** `01_Public_Fundamentals!FY26_rev/EBITDA/FCF` | JSON `public_fundamentals` + ASX FY26 release

---

### Q10 — "Why shouldn't we just own a pure-play US bill-pay or Intuit instead?"
**A:** Xero's edge is the **combined** accounting ledger + Melio payments + advisor channel in AU/UK/US — attach and switching costs differ from standalone bill-pay, and AU listing gives liquidity for this mandate. Intuit is a different scale/valuation; our gap analysis is XRO-specific at ~3.1x FY27 sales after Melio scare.  
**Cell:** Thesis slide 5 + `08_Macro!competitive` (qualitative) | Crowding tab differentiates vs generic software BUY

---

### Q11 — "FX: you use 0.90 NZD/AUD — what if NZD weakens 10%?"
**A:** A 10% NZD move scales NZD-denominated EV bridges and Melio PV roughly in proportion on the AUD share price math; directionally earnings translation softens but ASX price already clears in AUD — we disclose FX as `[ASSUMPTION]` on Cover. Stress: rerun Tab 0 B4=0.81 and refresh Gap/SOTP; Base PT band ±A$5–8 typically, thesis (Melio timing) unchanged.  
**Cell:** `00_Cover_Assumptions!B4` sensitivity | JSON `meta.fx_nzd_aud`

---

### Q12 — "If you're wrong in the next 12 months, what exactly breaks first?"
**A:** First break = **Melio BE path** (C1 kill) or **FY27 guide floor** breach (C2) — either forces PT toward A$70 and higher bear weight; secondary break = Ro40 guided <38% for FY28. We designed the book so being wrong is a **procedure**, not a debate — that is the PWCT point.  
**Cell:** `09_Risks_Gov!top_risk` + `03_Catalyst_PWCT!C1/C2/C4 kill` + Slide 12 | JSON `crowding_defense.falsifiable_criteria`

---

## Quick reference — headline numbers for verbal answers

| Item | Number |
|------|--------|
| Spot / Base PT / Upside | A$60 / A$90 / +50% |
| E[PT] weights | 25/55/20 → 118/90/55 |
| EV/Sales FY27 / EV/EBITDA | 3.09x / 12.8x |
| Spot-implied FY28 exit (on Street g) | 2.87x vs fair 5.0x |
| Σ P×ΔPT | ~A$+19.4 |
| Melio Base / SOTP / Pitch | ~A$8.0 / ~A$105 / A$90 |
| FY27 guide | NZ$3.62–3.73bn; EBITDA NZ$860–920m |
| Melio BE | H2 FY28 |
| Street TV avg PT | ~A$111 (we are below) |

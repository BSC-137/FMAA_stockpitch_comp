# Rubric Map — XRO FMAA Showcase (max every weight)

**Stock:** ASX:XRO BUY | **12m Base PT A$90** | **Spot ~A$60** | Deadline 6 Oct 2026  
**UNIQUE HOOK (peers won't have):** *Expectations Gap + Probability-Weighted Catalyst Tree (PWCT) + Melio Embedded Value Bridge + Crowding Defense*

| Judging criterion | Weight | Where we PROVE it | Unique hook linkage |
|-------------------|--------|-------------------|---------------------|
| **Macro** | 10% | Slide 3; Excel `08_Macro`; Dashboard macro→catalyst links (C3/C8) | Macro only matters insofar as it shifts **P** on C3 (payments) and C8 (derate) — not a separate essay |
| **Thesis + Catalysts** | **25% EMPHASIS** | Slides 4–7; `02_Expectations_Gap` + `03_Catalyst_PWCT` + `04_Melio_Bridge` | **Entire unique method lives here**: gap table, P×ΔPT tree, Melio option path, falsifiable kill-switches |
| **Valuation** | 20% | Slides 8–9; `05_SOTP_DCF` + `06_Scenarios_PT` + engine JSON | Base PT A$90 from **transparent scenario weights** (E[PT]=90); SOTP ~105 shows conservatism; reverse-multiple gap is the valuation *insight* |
| **Risks / Gov** | 5% | Slide 10; `09_Risks_Gov`; kill-switch column on PWCT | Risks are **operationalised** as kill-switches (not boilerplate) — Melio BE slip → PT A$70 |
| **Presentation** | 20% | `slide_spine.md` 15-slide arc; Dashboard one-pager | 10-min structure: Hook→Gap→PWCT→Melio→PT→Crowding→Close; every slide has one number |
| **Q&A** | 20% | `qa_trap_cards.md` (12 traps); model cell refs | Judges cannot break a PWCT with kill-switches — answers cite **cell IDs** |

---

## Criterion → artefact detail

### Macro 10%
- **Claim:** Soft-landing / rate path supports SMB software & payments TPV; AUD/NZD is secondary; YTD derate is Melio-dilution + multiple, not revenue break.
- **Proof:** Slide 3 three-box macro; Tab `08_Macro`; link to C8 P=25%.
- **Win move:** Spend ≤60s — then pivot to thesis (25% weight).

### Thesis + Catalysts 25% (EMPHASIS)
- **Claim:** Spot prices permanent Melio drag (~2.9x exit on Street growth). Delivery of H2 FY28 Melio BE + Ro40 path closes gap → A$90.
- **Proof:**
  1. Expectations gap table (Slide 4 / Tab 02)
  2. Full PWCT matrix (Slide 5–6 / Tab 03) with Σ P×ΔPT ≈ A$+19
  3. Melio bridge separate from core SaaS (Slide 7 / Tab 04)
  4. Crowding defense: we are Buy for **different reasons**, PT **below** Street (Slide 11 / Tab 07)
- **Win move:** Lead with gap, not "great company." Kill Motley-Fool "buy the dip" in one sentence.

### Valuation 20%
- **Claim:** E[PT]=A$90 = 0.25×118 + 0.55×90 + 0.20×55; SOTP ~A$105 → pitch 90 is conservative.
- **Proof:** Slides 8–9; Tabs 05–06; `pwct_results.json` scenarios + sotp.
- **Win move:** Show arithmetic live; never hide weights.

### Risks / Gov 5%
- **Claim:** Top risk = Melio BE slip; governance = earnout/contingent oversight + integration KPIs.
- **Proof:** Slide 10; Tab 09; C1/C7 kill-switches.
- **Win move:** Pre-empt Q&A — "If BE slips, we cut to A$70."

### Presentation 20%
- **Claim:** 10-minute spine in `slide_spine.md`; one idea per slide; appendix for Q&A.
- **Proof:** Timing marks on spine; Dashboard screenshotable.
- **Win move:** Rehearse to 9:30 — leave air for emphasis on PWCT.

### Q&A 20%
- **Claim:** 12 trap cards with 2-sentence answers + model cell.
- **Proof:** `qa_trap_cards.md`; JSON for numbers.
- **Win move:** Always answer with **falsifier** first when attacked on crowding.

---

## Unique differentiator checklist (must appear in pitch)

| Module | Visible on | One-line judge takeaway |
|--------|------------|-------------------------|
| Expectations Gap / reverse multiple | Slide 4 | "Price embeds ~2.9x exit; fair is ~5x if Ro40 returns" |
| PWCT (P×ΔPT + KPI + kill-switch) | Slides 5–6 | "Expected return = Σ P×ΔPT; we say when we're wrong" |
| Melio Embedded Value Bridge | Slide 7 | "Melio is an option path to H2 FY28 BE — not buried in group multiple" |
| Crowding Defense | Slide 11 | "Street is Buy; we are Buy for Melio *timing* + Ro40, PT below Street" |

---

## Anti-patterns (lose points)

- Do NOT lead with AI moat / Motley-Fool dip narrative.  
- Do NOT pitch GMG or property CapEx.  
- Do NOT use unverified Morningstar FV as a pillar (mark `[UNVERIFIED]` if cited).  
- Do NOT set PT at Street high (A$130) — destroys crowding defense.  
- Do NOT present catalysts without probabilities or kill-switches.

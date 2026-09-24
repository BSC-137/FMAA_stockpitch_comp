# FMAA × USYD Finance Showcase — Xero (ASX:XRO) BUY

**Rec:** BUY | **Spot (pitch):** A$60 | **12m Base PT:** A$90 (+50%) | **E[PT]:** A$90  
**As-of:** 22 Sep 2026 AEST | **Deadline:** 6 Oct 2026 11:59pm → `rebecca.ju@fmaa.com.au`

## Where things live

| Audience | Home |
|----------|------|
| **Team (no Git needed)** | [Google Drive folder](https://drive.google.com/drive/folders/1FPv60mrdcacDbKPyPLXDU2_hxPqtd8MB) — Excel + analysis docs |
| **Personal / versioned** | This GitHub repo (`xro/`) |

## Unique qualitative edge (do not dilute)

1. **Expectations Gap** — reverse-multiple: spot implies ~2.9× FY28 exit even on Street growth; fair ~5.0× if Rule of 40 returns.
2. **Probability-Weighted Catalyst Tree (PWCT)** — each catalyst has P × ΔPT + KPI + kill-switch.
3. **Melio Embedded Value Bridge** — Melio valued as option path to H2 FY28 BE, separate from core SaaS.
4. **Crowding Defense** — Base PT ~19% *below* Street avg; Buy for Melio *timing*, not Motley-Fool “buy the dip.”

**Tagline:** *The market prices Melio failure. We price Melio timing.*

## Active model (in this repo)

| File | Role |
|------|------|
| `xro/XRO_FMAA_PWCT_Model.xlsx` | **Submission Excel** — tabs 00–10 + sources |
| `xro/pwct_engine.py` | Runnable Python engine (regenerate numbers) |
| `xro/outputs/pwct_results.json` | Full numeric payload |
| `xro/outputs/pwct_summary.md` | Tables for slides |
| `xro/model_spec.md` | Excel tab / formula blueprint |
| `xro/rubric_map.md` | Judging weights → tabs/slides |
| `xro/slide_spine.md` | 15-slide 10-min spine |
| `xro/qa_trap_cards.md` | 12 hardest Q&A traps |

## Scenario weights

Bull 25% × A$118 + Base 55% × A$90 + Bear 20% × A$55 → **E[PT] = A$90**

## Status for teammates (24 Sep 2026)

- Locked pick: **XRO BUY @ A$90** (GMG is #2 backup only if majority forces it)
- CapEx-on-Goodman rejected as distraction under time constraint
- Team should open Drive Excel first; GitHub is Bharat’s versioned copy

## How to refresh numbers

```bash
cd xro && python pwct_engine.py
# then rebuild / paste into XRO_FMAA_PWCT_Model.xlsx from outputs/
```

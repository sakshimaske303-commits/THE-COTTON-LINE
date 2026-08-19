# Economic Survey of Maharashtra 2025-26, Chapter 7 (Agriculture) — Vidarbha & Cotton extract

*(Extracted from the 43-page PDF the user downloaded. This chapter is state-level throughout —
it does not break most tables down by district, so this extract pulls out the state-wide cotton
series plus the handful of places Vidarbha is named specifically. District-level indicators are
in the companion `vidarbha_economic_survey_2025-26_official.csv`.)*

## 1. Cotton — current season (state-wide)

**Kharif 2025-26 (tentative) vs 2024-25**, Table 7.3, Commissionerate of Agriculture GoM:

| | Area ('000 ha) 2024-25 | Area 2025-26 (tentative) | % change | Production ('000 bales*) 2024-25 | Production 2025-26 (tentative) | % change |
|---|---|---|---|---|---|---|
| Cotton (Lint) | 4,122.98 | 3,854.73 | −7.0% | 7,384.68 | 7,900.60 | +7% |

*Production of cotton in '000 bales of 170 kg each.

Cotton area is contracting statewide even as production/yield is projected up — worth flagging
this as the "area shrinking, yield-dependent recovery" pattern in the Cotton Trap chapter,
since a good monsoon year can mask the underlying acreage decline.

## 2. Cotton — long-run state trend (1960-61 to 2024-25)

From the historical cash-crops series (harvested area '000 ha / production '000 bales / yield
kg-lint-per-ha):

| Year | Area ('000 ha) | Production ('000 bales) | Yield (kg/ha) |
|---|---|---|---|
| 1960-61 | 2,500 | 1,673 | 114 |
| 1970-71 | 2,750 | 484 | 30 |
| 1980-81 | 2,550 | 1,224 | 82 |
| 1990-91 | 2,721 | 1,875 | 117 |
| 2000-01 | 3,077 | 1,803 | 100 |
| 2010-11 | 3,942 | 7,473 | 322 |
| 2020-21 | 4,545 | 10,110 | 378 |
| 2023-24 | 4,287 | 8,918 | 354 |
| 2024-25 | 4,123 | 7,385 | 304 |

This is a genuinely useful long-run series for the Cotton Trap chapter's historical framing: yield
per hectare roughly tripled from 1960s to the 2010-11 Bt-cotton-era peak (~378 kg/ha in 2020-21),
but has since *fallen back* to 304 kg/ha by 2024-25 — a decline worth investigating alongside your
debt/distress data, since falling yields on largely-unchanged area directly squeeze farm income.

Also from Annexure 7.4 (cropwise production index, base 1979-82=100): the Cotton/Fibres index hit
693.1 in 2020-21 but has been declining since — 589.0 (2022-23), 611.4 (2023-24), **506.3
(2024-25)** — corroborating the same downturn from the raw production numbers above.

## 3. Cotton MSP (Minimum Support Price), Table 7.21

GoI-declared MSP, ₹ per quintal:

| Crop | 2023-24 | 2024-25 | 2025-26 |
|---|---|---|---|
| Cotton (Medium Staple) | 6,620 | 7,121 | 7,710 |
| Cotton (Long Staple) | 7,020 | 7,521 | 8,110 |

MSP procurement in the state is undertaken by the Maharashtra State Co-operative Tribal
Development Corporation, NAFED, and the **Maharashtra State Co-operative Cotton Growers
Federation**. Cross-reference against the `cci_cotton_msp_procurement_state.csv` file (Cotton
Corporation of India procurement volumes by state) — note that CCI's actual procurement volumes
for Maharashtra (2.44 lakh bales in 2023-24, 29.31 lakh bales in 2024-25) are a small fraction of
total production, useful for making the "MSP exists on paper but doesn't reach most growers"
argument.

## 4. Vidarbha-specific schemes named in this chapter

**Table 7.27 — Micro watersheds completed (since inception up to March 2025):**

| Scheme | Watersheds selected | Watersheds completed | Expenditure (₹ crore) |
|---|---|---|---|
| Vidarbha Panlot Vikas Mission | 1,032 | 1,032 | 365.36 |
| Vidarbha Intensive Irrigation Development Programme | 588 | 588 | 318.36 |

Both are 100% "completed" by count of watersheds, which is worth scrutinizing in the Irrigation
Gap chapter — completed watershed *count* doesn't necessarily mean the irrigation gap itself
closed; cross-check this against your actual irrigated-area coverage numbers.

**Dairy/livestock:** "Special Project to Increase Milk Production in Vidarbha & Marathwada" —
covers 19 districts, distributing dairy cattle/calves/feed supplements/electric chaff cutter
subsidies; ₹0.20 crore spent up to December 2025 against a target of 33,543 (units unclear from
the extracted table — likely beneficiary households).

**Table 7.30 — Veterinary healthcare infrastructure by Revenue Division** (Amravati and Nagpur
divisions = Vidarbha):

| Division | District Vety. Polyclinics | Taluka Vety. Clinics | Vety. Clinics | Mukhyamantri Pashu-Chikitsa Pathak | LH & DC mobile van | Total | Artificial Insemination Centres |
|---|---|---|---|---|---|---|---|
| Amravati | 6 | 51 | 562 | 7 | 17 | 643 | 5 |
| Nagpur | 7 | 57 | 694 | 15 | 7 | 780 | 6 |
| **State total** | 39 | 317 | 4,439 | 73 | 80 | 4,948 | 34 |

Vidarbha's two divisions together account for 643+780 = 1,423 of the state's 4,948 veterinary
facilities (~29%) against roughly 32% of the state's district count (11/34) — roughly
proportionate, not a clear deficit on this specific metric.

## Source

Economic Survey of Maharashtra 2025-26, Chapter 7 (Agriculture), Commissionerate of Agriculture
GoM / Office of the Commissioner of Animal Husbandry GoM. Full 43-page PDF is in your
`02_Data_Raw/Agriculture` folder as `EconomicSurvey_2025-26_Chapter7_Agriculture.pdf` — this
extract only pulls the parts relevant to your 11 Vidarbha districts and cotton; the rest of the
chapter covers horticulture, sericulture, fisheries, animal husbandry schemes, etc. state-wide if
you need to dig further for any other chapter.

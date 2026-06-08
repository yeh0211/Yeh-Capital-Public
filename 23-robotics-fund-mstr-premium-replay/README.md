# 23 — Robotics closed-end fund vs MSTR premium replay

**Question.** If a robotics closed-end fund owns mostly private companies and trades at a persistent premium to reported NAV, does a MicroStrategy/Strategy-style issuance flywheel make it bullish for early public investors?

**Finding.** **Conditional.** The premium is not automatically bearish. A private-access premium can be rational if public investors cannot otherwise buy the underlying robotics companies. But early public investors benefit only if **NAV/share compounds before the premium fades**. Using YehCapital's Massive-backed market database/API for MSTR, BTC and BOT prices, plus Strategy's public BTC/share data, the MSTR playbook decomposes into three moving parts:

```text
MSTR price ~= BTC price x BTC per diluted share x simplified mNAV
BOT price  = robotics NAV/share x price-to-NAV multiple
```

That makes the BOT test very clean: robotics can be a great sector and the public stock can still be a mediocre entry if the starting multiple compresses faster than NAV/share grows.

> Research model only; not personal financial advice. The MSTR mNAV here is simplified and excludes debt, preferred stock, cash, and operating software value. It is built to test price-action mechanics, not produce an official valuation.

## Data & model

- **MSTR price.** Local YehCapital DuckDB `daily_bars` table, source `massive_rest`, supplemented by Massive REST where local rows were missing.
- **BTC price.** Massive REST `X:BTCUSD`.
- **BOT price.** Massive REST `BOT`; latest daily close used in the replay was **$37.49 on 2026-06-05**.
- **Strategy holdings.** Strategy's official purchase page for BTC holdings and assumed diluted shares outstanding.
- **BOT NAV.** SEC 424B3 reported **$7.31 NAV/share as of 2026-03-31**.

The clean MSTR decomposition window is **2025-01-06 to 2026-06-05**, because Strategy's public purchase table includes assumed diluted shares from January 2025 onward.

Core formulas:

```text
BTC reserve value        = BTC held x BTC price
BTC per diluted share    = BTC held / assumed diluted shares
BTC NAV/share            = BTC price x BTC per diluted share
simplified MSTR mNAV     = MSTR price / BTC NAV/share

BOT price/NAV multiple   = BOT price / reported NAV/share
BOT investor return      = NAV/share growth x ending multiple / starting multiple
```

## What MSTR teaches

Over the modeled window, MSTR's result was not just "Bitcoin went up." The three-factor machine mattered:

| Factor | Modeled result |
|---|---:|
| MSTR price return | -68.2% |
| BTC price return | -37.2% |
| BTC per diluted share change | +38.8% |
| Simplified mNAV change | -63.5% |
| Simplified mNAV range | 0.99x p25 / 1.44x median / 1.93x p75 |

So the flywheel can improve the asset-per-share variable while the public multiple still overwhelms the stock price. That is the exact risk to test in a robotics closed-end fund.

## BOT starting point

Using the latest Massive daily BOT close available to the model:

| Input | Value |
|---|---:|
| BOT close | $37.49 |
| Reported NAV/share | $7.31 |
| Starting price/NAV multiple | 5.13x |
| Starting premium to NAV | +412.9% |

That 5.13x multiple may be rational if BOT is a scarce access wrapper for private robotics companies. But it also means the early public buyer is underwriting a lot of future NAV/share growth or multiple persistence up front.

## Ten-year replay

The workbook tests four paths. The point is not to forecast the exact price; it is to separate **sector success** from **public-entry success**.

| Scenario | Year-10 NAV/share | Year-10 multiple | Year-10 price | Total return | Annualized |
|---|---:|---:|---:|---:|---:|
| Flywheel bull | $290.34 | 3.50x | $1,016.20 | +2610.6% | +39.1% |
| MSTR replay multiple | $100.75 | 2.45x | $246.90 | +558.6% | +20.7% |
| Private-access base | $46.59 | 2.00x | $93.19 | +148.6% | +9.5% |
| Good sector, bad entry | $58.91 | 1.25x | $73.64 | +96.4% | +7.0% |

The "good sector, bad entry" case is the most important guardrail: NAV/share can compound for a decade and the public stock can still lag the dream if the starting private-access multiple normalizes.

## Decision rule

The bullish version requires all three:

1. **NAV/share growth**, not just total NAV growth.
2. **Accretive issuance**, meaning new shares are sold above NAV after fees and increase NAV/share.
3. **Premium durability**, meaning the market continues paying for scarce private robotics access long enough for NAV/share to catch up.

The bearish version is not "premium exists." It is:

- the premium is hype rather than access value;
- BOT issues shares without NAV/share accretion;
- private marks are stale or unsupported by outside rounds, IPOs or M&A;
- the multiple compresses before robotics NAV/share compounds.

## Files

- [`mstr_robotics_fund_replay_model.xlsx`](mstr_robotics_fund_replay_model.xlsx) — full workbook with MSTR decomposition, BOT price/NAV replay, charts and break-even matrix.
- [`data/mstr_monthly_mnav_decomposition.csv`](data/mstr_monthly_mnav_decomposition.csv) — monthly MSTR factor decomposition.
- [`data/bot_mstr_replay_scenarios.csv`](data/bot_mstr_replay_scenarios.csv) — monthly BOT scenario simulation.
- [`data/bot_private_access_premium_break_even.csv`](data/bot_private_access_premium_break_even.csv) — break-even grid by NAV CAGR and terminal multiple.

## Answer

**A robotics closed-end fund using the MSTR method can be bullish for early investors, but only conditionally.** The premium is part of the mechanism, not automatically a flaw. The real question is whether the premium lets the fund buy better private robotics assets and raise NAV/share before the public multiple compresses. At a starting multiple above 5x reported NAV, early investors are not just buying robotics; they are buying the persistence of the private-access premium.

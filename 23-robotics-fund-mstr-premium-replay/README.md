# 23 — Robotics closed-end fund vs MSTR premium replay

**Question.** If a robotics closed-end fund owns mostly private companies and trades at a persistent premium to reported NAV, does a MicroStrategy/Strategy-style issuance flywheel make it bullish for early public investors?

**Finding.** **Conditional.** The premium is not automatically bearish. A private-access premium can be rational if public investors cannot otherwise buy the underlying robotics companies. But early public investors benefit only if **NAV/share compounds before the premium fades**. The clean test is:

```text
MSTR price ~= BTC price x BTC per diluted share x simplified mNAV
BOT price  = robotics NAV/share x price-to-NAV multiple
```

So BOT can be right about robotics and still be a mediocre public entry if the starting multiple compresses faster than NAV/share grows. At the latest Massive daily close used here, BOT traded at **$37.49** versus reported NAV/share of **$7.31**, or **5.13x NAV**. That can be a rational access premium. It is also a demanding hurdle.

> Research model only; not personal financial advice. The MSTR mNAV here is simplified and excludes debt, preferred stock, cash, and operating software value. It is built to test price-action mechanics, not produce an official valuation.

## Result

**A robotics closed-end fund using the MSTR method can be bullish for early investors, but only conditionally.** The premium is part of the mechanism, not automatically a flaw. The bullish version requires all three:

1. **NAV/share growth**, not just total NAV growth.
2. **Accretive issuance**, meaning new shares are sold above NAV after fees and increase NAV/share.
3. **Premium durability**, meaning the market continues paying for scarce private robotics access long enough for NAV/share to catch up.

The bearish version is not "premium exists." It is:

- the premium is hype rather than access value;
- BOT issues shares without NAV/share accretion;
- private marks are stale or unsupported by outside rounds, IPOs or M&A;
- the multiple compresses before robotics NAV/share compounds.

At a starting multiple above **5x reported NAV**, early investors are not just buying robotics. They are buying the persistence of the private-access premium.

## Data & method

- **MSTR price.** YehCapital's published extract from the Massive-backed daily-bars store, supplemented by Massive REST where local rows were missing.
- **BTC price.** Massive REST `X:BTCUSD`.
- **BOT price.** Massive REST `BOT`; the public CSV covers **2026-05-11 to 2026-06-05**.
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

## Claim 1 — MSTR is a three-factor machine, not just "Bitcoin up"

Over the modeled window, MSTR's stock price fell **68.2%** even though BTC per diluted share rose **38.8%**. The reason is visible in the decomposition: BTC price fell **37.2%** and simplified mNAV compressed **63.5%**. In other words, accretive asset-per-share growth can be real and still be overwhelmed by public multiple compression.

| Factor | Modeled result |
|---|---:|
| MSTR price return | -68.2% |
| BTC price return | -37.2% |
| BTC per diluted share change | +38.8% |
| Simplified mNAV change | -63.5% |
| Simplified mNAV range | 0.99x p25 / 1.44x median / 1.93x p75 |

![MSTR return decomposition into BTC price, BTC per diluted share, and simplified mNAV](fig1_mstr_decomposition.png)

**Why this matters for BOT.** The MSTR flywheel's key output is not total asset growth; it is asset-per-share growth. But the public investor's return still depends on the premium/multiple. The BOT analogue is exactly the same: robotics NAV/share can compound while the public price disappoints if price/NAV compresses.

## Claim 2 — BOT's premium is a feature of the hypothesis, not a reason to reject it

BOT traded at a large premium to its stale reported NAV through its first public month. That premium is not automatically irrational: the fund owns mostly private robotics and embodied-AI exposure, so public scarcity can justify a structural access premium. The question is whether that premium behaves like durable access value or like launch-window hype.

| Date range | BOT close range | Price/NAV multiple range | Latest multiple |
|---|---:|---:|---:|
| 2026-05-11 to 2026-06-05 | $21.01 to $39.00 | 2.87x to 5.34x | 5.13x |

![BOT price/NAV multiple path versus reported NAV](fig2_bot_premium_path.png)

**What would confirm the premium.** New share issuance has to be above NAV after costs, and the proceeds have to raise NAV/share by buying or marking up better private robotics assets. A high premium that does not translate into NAV/share accretion is only expensive access.

## Claim 3 — Good robotics is not enough; entry multiple decides the public return

The replay tests four paths. It is not a forecast. It is a sensitivity map for one question: how much of the early investor's return comes from NAV/share compounding versus premium persistence?

| Scenario | Year-10 NAV/share | Year-10 multiple | Year-10 price | Total return | Annualized |
|---|---:|---:|---:|---:|---:|
| Flywheel bull | $290.34 | 3.50x | $1,016.20 | +2610.6% | +39.1% |
| MSTR replay multiple | $100.75 | 2.45x | $246.90 | +558.6% | +20.7% |
| Private-access base | $46.59 | 2.00x | $93.19 | +148.6% | +9.5% |
| Good sector, bad entry | $58.91 | 1.25x | $73.64 | +96.4% | +7.0% |

![BOT modeled price paths under four scenarios; log scale so the bull case does not flatten the others](fig3_replay_scenarios.png)

The "good sector, bad entry" case is the guardrail. NAV/share can grow from **$7.31** to **$58.91** and the stock still only compounds at about **7.0%** annually if the terminal multiple normalizes to **1.25x**. That is not a failed robotics thesis. It is a paid-too-much-for-access outcome.

The break-even grid shows the same thing from another angle: if BOT eventually trades near NAV, it needs extreme NAV/share growth just to make today's public buyer whole. If the market keeps paying a 2x to 3.5x private-access multiple, the hurdle becomes much easier.

![Ten-year annualized return heatmap by NAV/share CAGR and terminal price/NAV multiple](fig4_break_even_heatmap.png)

## Caveats

- **Short BOT history.** BOT's public price record in this study covers only its first trading month. The premium path is a starting condition, not a stable distribution.
- **Stale private NAV.** Reported BOT NAV/share is as of **2026-03-31**. Private marks can lag reality in either direction.
- **Simplified MSTR mNAV.** The MSTR decomposition excludes debt, preferred stock, cash, and software operating value. It is intentionally a clean mechanical analogue, not an official valuation.
- **Scenario model, not backtest.** The 10-year BOT paths are sensitivity tests. They do not estimate private robotics company outcomes directly.
- **Private-company access risk.** Scarcity value only matters if the fund actually gets access to winners and converts issuance into NAV/share accretion.

## Reproducibility

The public figures use only CSVs in `data/`:

- `data/mstr_monthly_mnav_decomposition.csv`
- `data/bot_massive_price_nav.csv`
- `data/bot_mstr_replay_scenarios.csv`
- `data/bot_private_access_premium_break_even.csv`

Regenerate the figures:

```bash
python3 23-robotics-fund-mstr-premium-replay/build_figures.py
```

The supporting workbook is included as [`mstr_robotics_fund_replay_model.xlsx`](mstr_robotics_fund_replay_model.xlsx), but the README and PNGs are sufficient to audit the published conclusion. No private database, API key, or YehCapital ingestion script is required to rebuild the public figures.

## References

- Strategy official purchase page and public BTC reserve disclosures.
- RoboStrategy strategy materials on NAV, premium issuance, and closed-end fund mechanics.
- RoboStrategy/BOT SEC 424B3 filing reporting NAV/share and portfolio reference as of 2026-03-31.
- Investor.gov closed-end fund materials on premiums and discounts to NAV.

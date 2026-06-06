# 14 — Alphabet has the best cost basis on private winners, but no provable public-name picking skill

**Question.** Alphabet sits on huge private stakes (Anthropic, SpaceX) plus a venture book (CapitalG, GV). Is it actually a *better corporate investor* than Microsoft, Amazon, and Nvidia — or just early into a good cycle?

**Finding.** **Conditional.** On the *private* book, yes narrowly: Alphabet's SpaceX and Anthropic entries were earlier, cheaper, and larger per dollar deployed (~40–55x on the flagship cheques vs MSFT ~18x, AMZN ~9x), and those marks added roughly **+$24bn — about 18% of 2025 net income**. But on the *one slice that can be marked to a real tape* — CapitalG/GV names that became public tickers — Alphabet shows **no statistically significant edge over a broad same-era IPO baseline at any horizon** once the edge is tested correctly. Best cost basis on two generational private winners; **no evidence of repeatable, priceable picking alpha.**

> Research / backtested. No live capital, no audited track record. The private marks are mark-to-model, unrealised, and reflexive; the public test is, by construction, generous to Alphabet (it only sees names that survived to an IPO) and it still doesn't beat baseline. Method-described, not yet re-runnable: the 216-name control list and the block-bootstrap procedure are described here but the underlying lists and code are not published, so the test is documented rather than independently reproducible.

## Data & method

- **Skill test (the priceable part).** CapitalG and GV backed 23 names that are now public (after dropping four pre-panel biotech tickers whose first observable bar was mid-life, not post-IPO — a downward-biasing artifact). Entry = IPO+5 trading days (skips the day-1 pop); daily returns winsorized at 2%; forward returns at 90/180/365/730d.
- **Validation.** Each name is measured against a **216-name broad same-era tech/biotech IPO control**. Significance uses a **block-bootstrap CI on the backed-minus-control *difference*** (the correct edge question), plus a one-name drop test, a walk-forward vintage split, and an arm-level breakdown.
- **Private scoreboard.** Cost basis, reported paper marks, and FY-2025 P&L impact for Alphabet, Amazon, Microsoft, and Nvidia, from public filings and reporting (private positions are approximate / ranges).

## Claim 1 — The private marks are material (+$24bn, ~18% of net income) — but swing-prone

Gains on equity securities are now a sizeable, pro-cyclical component of record earnings — the same line printed **−$3.5bn in 2022**.

| Year | gain/(loss) on equity securities | % of net income |
|---|---|---|
| 2021 | +$12.4bn | +16% |
| 2022 | −$3.5bn | −6% |
| 2024 | +$3.7bn | +4% |
| 2025 | +$24.1bn | +18% |

![Gain on equity securities vs net income](gains_vs_ni.png)

## Claim 2 — Best cost basis among the megacaps on the private strategic book

Per dollar invested, Alphabet is the standout: a ~$0.9bn SpaceX cheque (2015) reportedly worth ~$85–110bn today, and an early Anthropic position re-rated through the AI funding cycle. The cleverness is **early, cheap, large** entries — a genuinely better cost basis than peers who mostly bought into already-expensive rounds. Caveat: it is unrealised paper, and MSFT's headline-bigger OpenAI stake actually *cost* it ~$3.1bn in FY25 net income via equity-method accounting — these marks cut both ways.

| Firm | Lead stake(s) | Invested ($bn) | Reported paper mark ($bn) | Approx multiple | FY25 equity-securities P&L ($bn) |
|------|---------------|---:|---:|---:|---:|
| Alphabet | Anthropic + SpaceX | ~2.9 | ~120–160 | ~40–55x | +24.1 |
| Microsoft | OpenAI ~27% | ~13.0 | ~228 | ~18x | −3.1 (equity-method loss) |
| Amazon | Anthropic | ~8.0 | 74.2 | ~9x | +9.5 (est.) |
| Nvidia | CoreWeave + xAI + others | ~4+ | ~6 (public marks) | ~1.5x | small + |

![Hyperscaler stake books: cost vs reported paper mark](peer_marks.png)

## Claim 3 — On the part we can actually price, there is no demonstrable picking skill

The 23 public backed names do not clear a broad IPO baseline. The **edge-diff CI** column — the correct test of "backed vs control" — spans zero at **every horizon**.

| horizon | n | backed mean % | control mean % | edge (pp) | backed-mean CI excl 0? | **edge-diff CI excl 0?** |
|---:|---:|---:|---:|---:|:--:|:--:|
| 90d  | 23 | −1.30  | +4.55  | −5.9  | no | **no** |
| 180d | 23 | −15.53 | −0.10  | −15.4 | yes (neg) | **no** |
| 365d | 23 | +4.87  | +4.28  | +0.6  | no | **no** |
| 730d | 23 | +28.83 | +10.48 | +18.3 | yes | **no** |

![Post-IPO mean return vs IPO peers, and edge vs control with CI](post_ipo_skill.png)

The lone "significant" flag — the **730d backed mean** — is **not** an edge over control (its edge-diff CI [−28.0, +60.3] spans zero) **and** it is one-name fragile:

| set | n | mean % | CI | excl 0? |
|-----|---:|---:|:--:|:--:|
| full | 23 | +28.83 | [+9.5, +47.6] | yes |
| drop NET (Cloudflare) | 22 | +10.66 | [−2.5, +24.1] | **no** |

What looks like skill is mostly **listing vintage**: pre-2021 IPOs averaged **+54%** at 365d (71% positive); every one of the 9 names that listed in/after Jan-2021 was **down 31–81%** a year out. The broad control shows the same vintage pattern — which is exactly why no edge survives the difference test.

| arm | n | mean 365d % | median 365d % | win % |
|-----|---:|---:|---:|---:|
| CapitalG (growth) | 10 | −6.42 | −23.48 | 40.0 |
| GV (venture/biotech) | 13 | +15.83 | −20.59 | 46.2 |

Neither arm's *median* is positive; both means are carried by a couple of multibaggers.

**Answer.** Better corporate investor than peers? **Conditional.** On cost basis / private marks: **yes, narrowly** — earlier, cheaper, larger entries on two generational winners. On *demonstrable, priceable* selection skill: **no** — the public book shows no significant edge over a broad IPO baseline at any horizon, is whipsawed by listing vintage, and its single positive flag is one-name fragile. Alphabet is best read as the megacap with the best *cost basis*, not as a demonstrably superior *picker*.

## Caveats

- **The public test is generous and still doesn't beat baseline.** It only sees names that *reached* an IPO — a positive selection that excludes every failed or written-down private bet.
- **Post-IPO drift is not Alphabet's realised return.** They bought private, years earlier, far cheaper; this measures name quality at the public tape, a directional proxy for selection only.
- **Private marks are opaque, dated, reflexive.** Anthropic/SpaceX/OpenAI marks move on the last round, not on cash — they lag, lurch, and (2022) reverse. Stake-level figures are reported/inferred, given as ranges where undisclosed.
- **Small n.** 23 public names, 9 in the 2021+ cohort — treat cohort means as directional.
- **Circularity not priced.** Alphabet is simultaneously Anthropic's investor *and* one of its largest compute suppliers; the mark and the revenue lean on the same counterparty.

## References

- Alphabet and peer 10-K / 10-Q filings (SEC EDGAR): non-marketable equity book, gain/(loss) on equity securities, FY25 net income.
- Public reporting on private rounds (Anthropic, SpaceX, OpenAI valuations and stake sizes) from major financial press.
- Equity multiples and stake sizes are approximate where positions are undisclosed.
- Industry analysis (e.g. specialist sector research) informed context on AI-compute and lab-funding dynamics; attributed generically, not quoted.

# Literature map — money flows around U.S. elections and wars

Compiled 2026-06-10 from a fan-out web sweep (SSRN / NBER / journal pages / IMF / Fed sources).
Purpose: establish what is already known per research question, and what gap this project fills.
Format per entry: venue/year — question — data/method — core finding — relevance.

---

## A. Elections, returns, and uncertainty (well-trodden)

1. **Santa-Clara & Valkanov 2003, J. Finance — "The Presidential Puzzle"**
   CRSP 1927-1998. Value-weighted excess returns ~9%/yr higher under Democratic presidents; not explained by business-cycle variables. The anchor fact for RQ5.
   https://www.pwlcapital.com/u-s-presidential-elections-vs-the-stock-market-whos-really-in-charge/ (summary incl. 1999-2015 extension where the gap widens)

2. **Pastor & Veronesi 2020, J. Political Economy — "Political Cycles and Stock Returns"** (NBER w23184)
   Equilibrium model: when risk aversion is high (bad times), voters elect Democrats; the high realized equity premium under D is risk compensation, not partisan policy magic. Implication for us: condition on the state of the economy at election, not just the winner's party.
   https://www.nber.org/system/files/working_papers/w23184/w23184.pdf

3. **Pastor & Veronesi 2013, J. Financial Economics — "Political Uncertainty and Risk Premia"**
   Policy uncertainty carries a risk premium, larger in weak economies; stocks more volatile and more correlated when policy is uncertain.
   https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1932420

4. **Kelly, Pastor & Veronesi 2016, J. Finance — "The Price of Political Uncertainty"**
   Options spanning 272 national elections/summits cost more (IV, variance, tail protection); effect stronger in weak economies. Confirms pre-event hedging demand — our RQ1 mechanism.
   https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2356588

5. **Goodell & Vahamaa 2013, J. Banking & Finance — "US presidential elections and implied volatility"**
   VIX rises as the eventual winner's probability changes during campaigns; election uncertainty is priced ex ante.
   https://www.sciencedirect.com/science/article/abs/pii/S0378426612003603

6. **St. Louis Fed 2024 — "What Happens to Expected Stock Volatility around Election Day?"**
   VIX falls from election day to day-after in 7 of the last 10 presidential elections; the three largest one-day VIX drops were 2016, 2020, 2024 — uncertainty resolution dominates outcome direction. Core RQ1 fact.
   https://www.stlouisfed.org/on-the-economy/2024/dec/what-happens-expected-stock-volatility-election-day

7. **Snowberg, Wolfers & Zitzewitz 2007, QJE — "Partisan Impacts on the Economy"**
   High-frequency election-night moves (2004) + prediction markets back to 1880. Republican win → equities +2-3%, higher bond yields, stronger dollar, higher oil. Method template: use odds shifts, not calendar days, to identify the shock.
   https://www.nber.org/papers/w12073

8. **Wagner, Zeckhauser & Ziegler 2018, JFE — "Trump, Taxes, and Trade"** (+ companion "Paths to Convergence")
   Cross-section of stock reactions to the 2016 shock: high-tax firms and banks won, healthcare/apparel lost, domestic beat international; complex exposures repriced slowly over days. Justifies our [-5, +20] day "slow rotation" windows.
   https://www.nber.org/papers/w23152

## B. Midterms (in scope per decision #1)

9. **Chan & Marsh 2021, JFE — "Asset prices, midterm elections, and political uncertainty"**
   Midterms matter more than presidential elections for asset pricing: equity premium, mutual fund flows, and real investment growth all significantly higher in post-midterm months.
   https://www.sciencedirect.com/science/article/abs/pii/S0304405X21000970

10. **"Midterm elections and stock returns", Finance Research Letters 2023**
    Equity fund outflows in pre-midterm months (retail anticipation of regime-change risk), reversal to net inflows post-midterm; money-market funds absorb the flight-to-safety pre-midterm. This is RQ1+RQ4 for midterms, already documented — we replicate and extend to 2022/2026 and add the country dimension.
    https://www.sciencedirect.com/science/article/abs/pii/S1544612323001988

11. **Kraussl, Lucas, Rijsbergen, van der Sluis & Vrugt 2013, J. Int. Money & Finance — "Washington meets Wall Street"**
    S&P 500 excess return ~10%/yr higher in years 3-4 of the presidential term; not explained by business cycle, risk, or sentiment. The "midterm year trough" seasonal.
    https://www.sciencedirect.com/science/article/abs/pii/S0261560613001721

12. **Chan & Marsh 2023 (follow-up)** — once CAPM risk adjustment is applied, much of the midterm excess return reads as compensation for risk, not anomaly. Discipline for our brief: report raw AND risk-adjusted.
    (via https://www.northerntrust.com/europe/insights-research/asset-servicing/a-suite/insights-hub/midterm-elections-and-us-markets-a-guide)

## C. Elections and capital flows — the thin part (our gap)

13. **IMF Working Paper, Nov 2025 — "Elections Matter: Capital Flows and Political Cycles"**
    38 emerging markets, quarterly, 1990-2020: election periods see a decline in gross private capital inflows; larger and more persistent when uncertainty extends beyond the vote (e.g. incumbent loss with unclear policy priorities). Closest academic neighbor — but it studies EM domestic elections, not U.S. elections' effect on cross-border allocation.
    https://www.imf.org/en/publications/wp/issues/2025/11/14/elections-matter-capital-flows-and-political-cycles-571782

14. **EPFR practitioner notes (paywalled data, public commentary)**
    2016 election week: 66 tracked funds with outsized reactions, 22 of them EM equity. October 2024: EM equity funds' biggest weekly outflows since 2Q20 ahead of the vote; elevated cash allocations in US equity funds post-2024. Proves the flow signal exists at country level; no free academic replication exists — that is this project.
    https://epfr.com/insights/quants-corner/getting-ready-anomalous-election/ ; https://epfr.com/insights/global-navigator/searching-buffer-funds-october-us-elections/

15. **Koepke 2019 (survey, J. Econ. Surveys) — "What Drives Capital Flows to Emerging Markets?"**
    Push factors (US rates, global risk aversion) dominate cyclical EM flows. US election uncertainty is a push factor — frames RQ2 direction of causality.
    https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2569249

16. **Fratzscher 2012, J. Int. Economics — "Push versus pull"** — EPFR-based decomposition of crisis-period flows; common (push) shocks dominate in stress.
17. **Forbes & Warnock 2012, J. Int. Economics — "Capital flow waves"** — surges/stops keyed to global risk, not local fundamentals.
18. **Chari, Dilts Stedman & Lundblad (NBER w31143) — "Global Fund Flows and EM Tail Risk"**
    Risk and risk-aversion shocks produce extreme EM flow realizations via open-end mutual funds — the vehicle-level mechanism our ETF panel measures directly.
    https://www.nber.org/system/files/working_papers/w31143/w31143.pdf

19. **"Episodes of extreme international capital inflows and global economic policy uncertainty", PLOS One 2022**
    Global EPU raises surge probability into EMDEs (portfolio-rebalancing channel) — i.e. US-origin uncertainty can push money TOWARD EM, not just away. Keeps our priors honest; direction is an empirical question per episode.
    https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0275249

## D. Partisan investor behavior (who moves the money)

20. **Meeuwis, Parker, Schoar & Simester 2022, J. Finance — "Belief Disagreement and Portfolio Choice"**
    Administrative retail data around 2016: likely-Republicans raised equity share and beta; likely-Democrats rotated into safe assets. Take-profit behavior is partisan, driven by a minority of active traders.
    https://www.nber.org/papers/w25108

21. **Addoum & Kumar 2016, RFS — "Political Sentiment and Predictable Returns"**
    Party-in-power shifts industry-level portfolio composition; exploiting it earned ~6%/yr risk-adjusted (1939-2011), strongest at political transitions. Supports a sector-rotation read of post-election flows.
    https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2169360

22. **Capital Group (practitioner, 1992-2024) — "How elections move markets"**
    Money-market funds receive outsized inflows in election years; equity funds see their highest net inflows in the year immediately after. The cleanest free statement of the de-risk/re-risk cycle (RQ1/RQ4).
    https://www.capitalgroup.com/individual/insights/articles/how-elections-move-markets-5-charts.html

## E. Elections and the dollar / cross-border prices

23. **Della Corte & Fu (working paper, AEA 2021) — "Presidential Cycles and Exchange Rates"**
    USD appreciates ~4.3%/yr under Democratic presidencies, depreciates ~1.3%/yr under Republican ones — the FX mirror of the presidential puzzle.
    https://www.aeaweb.org/conference/2021/preliminary/paper/RHfSAy7e

24. **NBER w33193 — "How Institutions Interact with Exchange Rates" (2024 election)**
    Minute-level data, 73 currencies: nearly all fell against USD within minutes of the 2024 result; stronger-institution countries depreciated more persistently. Confirms 2024 was at least partly a surprise in FX space.
    https://www.nber.org/system/files/working_papers/w33193/w33193.pdf

25. **"Protectionism, bilateral integration, and the cross section of exchange rate returns in US presidential debates", JIMF 2024**
    Debate outcomes move USD against trade-integrated currencies — protectionist-candidate news appreciates USD vs trade partners. Mechanism for Trump-cycle FX/flow rotation.
    https://www.sciencedirect.com/science/article/pii/S0261560624001219

## F. Wars and markets

26. **Brune, Hens, Rieger & Wang 2015, Int. Review of Economics — "The War Puzzle"**
    Post-WWII conflicts: rising war likelihood depresses prices; the actual outbreak of a telegraphed war LIFTS them ("buy the invasion"); surprise wars fall on outbreak. The central pattern our wars module tests per administration.
    https://link.springer.com/article/10.1007/s12232-014-0215-7

27. **Cortes, Vossmeyer & Weidenmier (NBER w29837) — "Stock Volatility and the War Puzzle"**
    US wartime equity volatility is anomalously LOW (defense-spending stabilization of cash flows) — relevant to the "Trump volatility" question: conflict does not mechanically mean higher vol.
    https://www.nber.org/system/files/working_papers/w29837/revisions/w29837.rev0.pdf

28. **Leigh, Wolfers & Zitzewitz 2003 (NBER w9587) — "What do Financial Markets Think of War in Iraq?"**
    Prediction-market war probability mapped to asset prices ex ante: higher war odds → lower equities, higher oil. Method template for buildup windows.

29. **Caldara & Iacoviello 2022, AER — "Measuring Geopolitical Risk"**
    Newspaper-based GPR index, 1900-present (daily variant available); GPR shocks lower investment and stocks. Our control series for separating election effects from concurrent geopolitics. Free download.
    https://www.matteoiacoviello.com/gpr.htm

30. **IMF Global Financial Stability Report, April 2025, Ch. 2 — "Geopolitical Risks and Asset Prices"**
    Major geopolitical events since WWII: modest, short-lived aggregate equity declines; larger for EMs and fiscally weak states; flight to gold and safe assets. Cross-country benchmark for our war dossiers.
    https://www.elibrary.imf.org/display/book/9798229003261/CH002.xml

31. **Berkman, Jacobsen & Lee 2011, JFE — "Time-varying rare disaster risk and stock returns"** — ICB political-crisis count prices a disaster premium; background for buildup windows.
32. **Boungou & Yatie 2022 (and G20+ event studies) — Russia-Ukraine 2022** — anticipation losses in exposed markets pre-invasion, broad losses post; the 2022-02-24 US intraday reversal is a case-study staple.
    https://www.sciencedirect.com/science/article/pii/S2214635022000570

## G. Trump-specific policy shocks (tariffs as the flow mover)

33. **Amiti, Gomez, Kong & Weinstein — "Trade Protection, Stock-Market Returns, and Welfare"** (+ NY Fed Liberty Street summary 2024)
    11 tariff-announcement days 2018-19: cumulative market decline ~11.5% (~$4.1T); firms hit hardest had genuinely worse subsequent fundamentals. Tariff announcements, not the election itself, are the repricing events in Trump terms.
    https://libertystreeteconomics.newyorkfed.org/2024/12/using-stock-returns-to-assess-the-aggregate-effect-of-the-u-s-china-trade-war/

34. **"Trump Liberation Day tariffs and stock market reactions", Studies in Economics & Finance 2026**
    77-country event study of 2025-04-02: declines NOT proportional to assigned tariff rates; US market itself fell — read as broadly costly policy, not bilateral transfer.
    https://www.emerald.com/sef/article/43/2/415/1333419/Trump-Liberation-Day-tariffs-and-stock-market

35. **Liberation Day market record (for the 2024-25 dossier)**
    2025-04-03..04-08: US total market -12.4%; 04-09 pause: S&P +9.5% (largest one-day gain since 2008); USD fell; 30y Treasury's biggest 3-day yield rise since 1982; one year on, "rethinking US exceptionalism" framing with sustained European inflows.
    https://en.wikipedia.org/wiki/Liberation_Day_tariffs ; https://www.cnbc.com/2026/04/02/liberation-day-1-year-on-investors-are-rethinking-us-assets.html ; https://cepr.org/voxeu/columns/how-tariff-war-shock-affected-safe-asset-privilege-us-treasuries

---

## Synthesis: what is known vs what we add

Known and replicable: pre-election hedging and cash build-up (4, 5, 10, 22); post-result volatility crush regardless of winner (6); post-midterm equity strength (9, 11, with risk-adjustment caveat 12); partisan rebalancing at household level (20); R-win short-run equity pop (7); war-puzzle buildup/outbreak asymmetry (26); wartime vol suppression (27); tariff announcements as the true Trump-era repricing events (33-35).

The gap we fill: a free, reproducible, country-level ETF-flow event study around ALL U.S. elections (presidential + midterm, 1992/2004-2026) by winner type, with a wars overlay — answering whether money actually LEAVES the US (flows) or merely reprices (returns), and where it goes (EM/China/Asia/Taiwan/Europe/bonds/gold/cash). Academic work nearest to this (13) covers EM domestic elections; country-flow facts around US elections live only in paywalled practitioner notes (14).

Method discipline imported from the literature: align events on result-known dates and odds shifts, not calendar dates (7, 28); classify surprise via prediction markets; report raw and risk-adjusted (12); treat tariff shocks as separate events from elections (33); expect slow multi-day rotation, not just overnight jumps (8).

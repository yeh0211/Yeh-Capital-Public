"""Event tables: presidential elections, midterms, wars/military actions, tariff shocks.

Dates are calendar dates of the event; the event-study engine maps each to the
first trading day on/after the date ("reaction day"). winner_pre_odds are
approximate day-before probabilities of the actual winner from prediction
markets/forecasts (IEM, Intrade, PredictIt, Polymarket, FiveThirtyEight);
sources annotated in lit_map.md. surprise = odds < 0.40.
"""
import pandas as pd

PRESIDENTIAL = [
    dict(date="1992-11-03", winner="Clinton", party="D", flip=True,  incumbent_running=True,
         result_known="1992-11-04", winner_pre_odds=0.80, unified_after=True,
         note="Clinton clear favorite; unified D government"),
    dict(date="1996-11-05", winner="Clinton", party="D", flip=False, incumbent_running=True,
         result_known="1996-11-06", winner_pre_odds=0.90, unified_after=False,
         note="Landslide hold; R Congress retained"),
    dict(date="2000-11-07", winner="Bush",    party="R", flip=True,  incumbent_running=False,
         result_known="2000-12-13", winner_pre_odds=0.50, unified_after=True,
         note="Contested 36 days (Bush v. Gore 12-12, Gore concession 12-13); dot-com unwind backdrop"),
    dict(date="2004-11-02", winner="Bush",    party="R", flip=False, incumbent_running=True,
         result_known="2004-11-03", winner_pre_odds=0.58, unified_after=True,
         note="Close but priced hold"),
    dict(date="2008-11-04", winner="Obama",   party="D", flip=True,  incumbent_running=False,
         result_known="2008-11-05", winner_pre_odds=0.85, unified_after=True,
         note="GFC dominates the window (Lehman 2008-09-15)"),
    dict(date="2012-11-06", winner="Obama",   party="D", flip=False, incumbent_running=True,
         result_known="2012-11-07", winner_pre_odds=0.70, unified_after=False,
         note="Priced hold; divided government"),
    dict(date="2016-11-08", winner="Trump",   party="R", flip=True,  incumbent_running=False,
         result_known="2016-11-09", winner_pre_odds=0.22, unified_after=True,
         note="SURPRISE. Overnight futures -5 percent then reversal; reflation rotation"),
    dict(date="2020-11-03", winner="Biden",   party="D", flip=True,  incumbent_running=True,
         result_known="2020-11-07", winner_pre_odds=0.65, unified_after=True,
         note="Called Saturday 11-07; Pfizer vaccine news Monday 11-09 contaminates post-window; Senate unified only after GA runoffs 2021-01-05"),
    dict(date="2024-11-05", winner="Trump",   party="R", flip=True,  incumbent_running=False,
         result_known="2024-11-06", winner_pre_odds=0.55, unified_after=True,
         note="Partially priced; decisive sweep; 2025-04-02 tariffs treated as separate shock"),
]

MIDTERMS = [
    dict(date="1994-11-08", pres_party="D", house_flip=True,  senate_flip=True,
         note="Republican Revolution; both chambers flip"),
    dict(date="1998-11-03", pres_party="D", house_flip=False, senate_flip=False,
         note="Unusual pres-party House gains"),
    dict(date="2002-11-05", pres_party="R", house_flip=False, senate_flip=True,
         note="Pres-party gains both chambers (post-9/11); Senate back to R"),
    dict(date="2006-11-07", pres_party="R", house_flip=True,  senate_flip=True,
         note="D sweep"),
    dict(date="2010-11-02", pres_party="D", house_flip=True,  senate_flip=False,
         note="Tea Party House wave"),
    dict(date="2014-11-04", pres_party="D", house_flip=False, senate_flip=True,
         note="Senate flips R"),
    dict(date="2018-11-06", pres_party="R", house_flip=True,  senate_flip=False,
         note="D House; concurrent Q4-2018 Fed-driven selloff"),
    dict(date="2022-11-08", pres_party="D", house_flip=True,  senate_flip=False,
         note="Narrow R House; red wave underperformed expectations"),
]
NEXT_MIDTERM = "2026-11-03"

# kind: one_off | campaign | withdrawal | third_party | threat_resolved
WARS = [
    dict(admin="Bush",    name="Afghanistan war begins",        t0="2001-10-07", buildup="2001-09-11", kind="campaign",        telegraphed=True,
         note="Post-9/11; the 9/11 shock itself is a separate market event"),
    dict(admin="Bush",    name="Iraq invasion",                 t0="2003-03-20", buildup="2002-09-12", kind="campaign",        telegraphed=True,
         note="Classic buildup-then-outbreak case; SPX bottom 2003-03-11"),
    dict(admin="Obama",   name="Libya intervention",            t0="2011-03-19", buildup="2011-02-26", kind="campaign",        telegraphed=True,
         note="UNSC 1973 on 03-17"),
    dict(admin="Obama",   name="bin Laden raid",                t0="2011-05-02", buildup=None,         kind="one_off",         telegraphed=False,
         note="Announced Sunday night 05-01 ET"),
    dict(admin="Obama",   name="Syria red-line stand-down",     t0="2013-08-31", buildup="2013-08-21", kind="threat_resolved", telegraphed=True,
         note="Strike threatened after Ghouta, then sent to Congress and shelved; relief case"),
    dict(admin="Obama",   name="Anti-ISIS strikes Iraq",        t0="2014-08-08", buildup="2014-06-10", kind="campaign",        telegraphed=True,
         note="Mosul fell 06-10"),
    dict(admin="Obama",   name="Anti-ISIS strikes Syria",       t0="2014-09-23", buildup="2014-09-10", kind="campaign",        telegraphed=True,
         note="Address announcing expansion 09-10"),
    dict(admin="Trump1",  name="Shayrat strike (Syria)",        t0="2017-04-07", buildup="2017-04-04", kind="one_off",         telegraphed=False,
         note="Response to Khan Shaykhun, 3 days later"),
    dict(admin="Trump1",  name="Douma response strikes (Syria)",t0="2018-04-14", buildup="2018-04-07", kind="one_off",         telegraphed=True,
         note="Week of public deliberation"),
    dict(admin="Trump1",  name="Soleimani strike",              t0="2020-01-03", buildup=None,         kind="one_off",         telegraphed=False,
         note="Iran missile retaliation 01-08; market at new highs within days"),
    dict(admin="Biden",   name="Kabul falls / withdrawal",      t0="2021-08-15", buildup="2021-07-02", kind="withdrawal",      telegraphed=True,
         note="Bagram handover 07-02; exit complete 08-30"),
    dict(admin="Biden",   name="Russia invades Ukraine",        t0="2022-02-24", buildup="2021-11-10", kind="third_party",     telegraphed=True,
         note="US intel warnings from Nov 2021; famous intraday reversal on outbreak day"),
    dict(admin="Biden",   name="Hamas attack / Gaza war",       t0="2023-10-07", buildup=None,         kind="third_party",     telegraphed=False,
         note="US carrier deployment follows"),
    dict(admin="Biden",   name="US-UK Houthi strikes",          t0="2024-01-12", buildup="2023-12-18", kind="campaign",        telegraphed=True,
         note="Operation Prosperity Guardian 12-18 preceded strikes"),
    dict(admin="Trump2",  name="Houthi campaign",               t0="2025-03-15", buildup=None,         kind="campaign",        telegraphed=False,
         note="Sustained campaign begins"),
    dict(admin="Trump2",  name="Israel-Iran war begins",        t0="2025-06-13", buildup=None,         kind="third_party",     telegraphed=False,
         note="Oil spike; US ally war preceding US strike"),
    dict(admin="Trump2",  name="US strikes Iran nuclear sites", t0="2025-06-22", buildup="2025-06-13", kind="one_off",         telegraphed=True,
         note="Midnight Hammer night of 06-21/22 ET; ceasefire 06-24 relief rally"),
]

# Tariff shocks: the Trump-era repricing events that are distinct from elections.
TARIFF_SHOCKS = [
    dict(admin="Trump1", name="Steel/aluminum tariffs announced", t0="2018-03-01"),
    dict(admin="Trump1", name="China Section 301 memo",           t0="2018-03-22"),
    dict(admin="Trump1", name="China $50B list finalized",        t0="2018-06-15"),
    dict(admin="Trump1", name="Escalation tweets (10->25pct)",    t0="2019-05-05"),
    dict(admin="Trump1", name="10pct on $300B announced",         t0="2019-08-01"),
    dict(admin="Trump2", name="Canada/Mexico/China tariff EOs",   t0="2025-02-01"),
    dict(admin="Trump2", name="Liberation Day tariffs",           t0="2025-04-02"),
    dict(admin="Trump2", name="90-day pause (relief)",            t0="2025-04-09"),
    dict(admin="Trump2", name="Geneva de-escalation with China",  t0="2025-05-12"),
]

ADMIN_TERMS = [
    dict(admin="Bush41",  party="R", start="1989-01-20", end="1993-01-20"),
    dict(admin="Clinton", party="D", start="1993-01-20", end="2001-01-20"),
    dict(admin="Bush43",  party="R", start="2001-01-20", end="2009-01-20"),
    dict(admin="Obama",   party="D", start="2009-01-20", end="2017-01-20"),
    dict(admin="Trump1",  party="R", start="2017-01-20", end="2021-01-20"),
    dict(admin="Biden",   party="D", start="2021-01-20", end="2025-01-20"),
    dict(admin="Trump2",  party="R", start="2025-01-20", end=None),
]

SURPRISE_THRESHOLD = 0.40


def presidential_df():
    df = pd.DataFrame(PRESIDENTIAL)
    for c in ("date", "result_known"):
        df[c] = pd.to_datetime(df[c])
    df["surprise"] = df["winner_pre_odds"] < SURPRISE_THRESHOLD
    return df


def midterms_df():
    df = pd.DataFrame(MIDTERMS)
    df["date"] = pd.to_datetime(df["date"])
    df["any_flip"] = df["house_flip"] | df["senate_flip"]
    return df


def wars_df():
    df = pd.DataFrame(WARS)
    df["t0"] = pd.to_datetime(df["t0"])
    df["buildup"] = pd.to_datetime(df["buildup"])
    return df


def tariffs_df():
    df = pd.DataFrame(TARIFF_SHOCKS)
    df["t0"] = pd.to_datetime(df["t0"])
    return df


def admins_df():
    df = pd.DataFrame(ADMIN_TERMS)
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    return df

# Study 32 — Cerebras and the Re-Weighting of the AI Compute Stack

A long-term technology-investor study of how wafer-scale compute reshapes the
semiconductor value chain — what it removes, who benefits, who is exposed, and
whose forward guidance is most at risk.

*Prepared June 2026. All figures are estimates or forward projections unless marked
actual (A); sell-side consensus revenue/TAM lines are upside-leaning and treated as such;
vendor performance claims are first-party and discounted accordingly. Every value-chain
compression estimate is a derived sensitivity (no published analyst models it) and is
labeled where it appears.*

---

## 0. The one-paragraph thesis

A GPU AI factory makes money from **fragmentation**. Because a single Nvidia die is
reticle-limited (~800 mm²), real models are split across thousands of GPUs, and every
split has to be re-stitched with expensive silicon: HBM stacks to feed each die, CoWoS
packaging to attach the HBM, NVLink/NVSwitch to bind GPUs inside a box, and
InfiniBand/Ethernet plus optical transceivers to bind boxes into clusters. That
"re-stitching" tax is not a side business — it is roughly a third of the bill of
materials and the fastest-growing line in the whole complex. Cerebras's bet is to
**internalize the re-stitching onto one slab of silicon**: a 46,225 mm² wafer-scale
engine with 900,000 cores and 44 GB of on-wafer SRAM, no HBM, no CoWoS, and no
inter-GPU network for any model that fits on the wafer. If that bet wins share, the
value chain does not shrink uniformly — **it re-weights**: toward raw TSMC wafers and
toward power/cooling, and away from networking silicon, optics, HBM, and advanced
packaging. The investable question is not "is the chip impressive" (it is) but "how
much share can it take, how fast, before the CUDA software moat, the on-wafer memory
ceiling, and an entrenched incumbent close the window." Today Cerebras is a ~$510M
revenue company against Nvidia's ~$216B; everything below is a structural-sensitivity
map, not a 2026 base case.

---

## 1. What Cerebras actually is — and the layer it removes

### 1.1 Wafer-scale, in plain terms

Normal chipmaking prints ~60–70 identical dies on a 300 mm wafer and then **dices** the
wafer into individual chips. Cerebras does the opposite: it prints 84 reticle-sized die
regions on one wafer and, instead of cutting them apart, runs extra lithography to lay
**over a million wires across the scribe lines** (the gaps normally used for dicing),
fusing all 84 regions into **one logical processor**. The result is a single piece of
silicon roughly the size of a dinner plate — about **50–57× the area of the largest GPU
die** — that the software sees as one device.

| | WSE-2 / CS-2 | **WSE-3 / CS-3** | Nvidia H100 | Nvidia B200 (Blackwell) |
|---|---|---|---|---|
| Process | TSMC 7nm | **TSMC 5nm** | TSMC 4N | TSMC 4NP (2 dies) |
| Transistors | 2.6 T | **4 T** | ~80 B | ~208 B |
| AI cores | 850,000 | **900,000** | ~16,896 + tensor | dual-die |
| On-chip SRAM | 40 GB | **44 GB** | ~50 MB L2 | tens of MB |
| On-chip mem bandwidth | 20 PB/s | **21 PB/s** | 3 TB/s (to HBM) | 8 TB/s (to HBM) |
| Die area | 46,225 mm² | **46,225 mm²** | ~814 mm² | ~1,600 mm² |
| System power | ~23 kW | **~23–27 kW** | ~0.7 kW | ~1.0–1.2 kW |

The number that matters: **21 PB/s of on-wafer memory bandwidth is roughly 7,000× an
H100's 3 TB/s HBM pipe and ~2,600× a B200's.** Memory sits *on the compute*, not across
a package.

### 1.2 The honest version: it relocates memory, it does not abolish it

44 GB of SRAM cannot hold a 1-trillion-parameter model, so Cerebras splits the problem:

- **MemoryX** — an external DRAM-plus-flash weight store (1.5 TB up to ~1.2–2.4 PB),
  holding models as large as 24 T parameters. Weights live here, **not** in per-GPU HBM.
- **Weight streaming** — the activations stay resident on the wafer; the model's weights
  are streamed in **one layer at a time** from MemoryX, computed, and (in training)
  gradients streamed back. Compute and memory therefore **scale independently** — the
  opposite of a GPU, where adding memory means buying whole additional GPUs.
- **SwarmX** — a narrow broadcast-and-reduce fabric (tree topology) that links MemoryX
  to up to **2,048 CS-3 systems**, so multi-wafer clusters keep the single-device
  programming model.

So the precise claim is: **HBM-per-accelerator, CoWoS, NVLink/NVSwitch, and most
scale-out networking are removed; in their place is a smaller external commodity-DRAM
tier (MemoryX) and a thin purpose-built fabric (SwarmX).** That is the "layer it cuts
out" you intuited — not a single component, but the entire memory-and-interconnect
re-stitching hierarchy that a GPU cluster is built from.

### 1.3 The components a CS-3 eliminates vs an Nvidia cluster

| Nvidia-cluster component | On a Cerebras CS-3 | Mechanism |
|---|---|---|
| HBM stacks (80–192 GB/GPU) | **Eliminated** as working memory | 44 GB on-die SRAM + external commodity DRAM (MemoryX) |
| CoWoS / 2.5D packaging | **Eliminated** | No HBM beside the die → no interposer step; the wafer *is* the package |
| NVLink / NVSwitch | **Eliminated** within a wafer | On-wafer scribe-line mesh replaces it (single-clock core-to-core) |
| InfiniBand / Ethernet scale-out | **Sharply reduced** | A model that fits one wafer needs no model-parallel network |
| Optical transceivers | **Sharply reduced** | Far fewer node-to-node links to drive |
| 8-GPU server / NVL72 rack assembly | **Replaced** | One CS-3 chassis = one accelerator |

### 1.4 The vertical-integration angle (hardware + software + cloud)

The point you flagged — that Cerebras is "special" because it owns both the hardware and
the software — is the strategic core. Cerebras is **vertically integrated across the
whole stack**: it designs the wafer, co-develops the proprietary process with TSMC (a
process no other TSMC customer can use), writes the compiler (CSoft) and the
PyTorch-compatible software, **and** operates its own inference cloud and builds/leases
the data centers. It even does final wafer packaging in-house to hide the "secret
sauce."

This is closer to an Apple-style integrated platform than to the merchant-GPU model. The
upside: it controls the full experience, captures more of the value per workload, and can
offer an **OpenAI-compatible API** so customers never touch the locked-in low-level
layer (the same move that let ARM/Graviton sidestep x86 lock-in — see §6). The downside:
vertical integration is **capital-intensive and operationally heavy** — Cerebras must
secure TSMC allocation, scale a never-before-scaled supply chain ~10×, *and* finance
gigawatts of data-center leases. That is why gross margin sits at ~39% (vs Nvidia's
~75%) and why the balance-sheet/financing risk is real even as the technology shines.

---

## 2. Bottlenecks solved, and the workloads where wafer-scale wins

### 2.1 The two bottlenecks it attacks (Question 1)

1. **The memory wall.** GPU FLOPS have grown far faster than the bandwidth to feed them
   from off-chip HBM. A GPU spends much of its time and power shuttling weights and
   activations across a 3–8 TB/s pipe. Putting 44 GB of SRAM next to the cores at
   21 PB/s makes that bottleneck largely disappear *for whatever fits on the wafer*.
2. **The inter-GPU communication tax.** Splitting a model across GPUs forces constant
   all-reduce / weight-exchange traffic across NVLink → NVSwitch → InfiniBand, each a
   bandwidth-and-latency cliff. On a wafer, 900,000 cores talk over one mesh in a single
   clock cycle, so there is no cross-chip cliff to pay.

### 2.2 Where it outperforms GPUs (Question 2)

The edge is real but **narrow and physics-based**: it shows up wherever **per-token
latency on a large model** dominates, because SRAM bandwidth structurally beats HBM:

- **Low-latency / "fast" inference** — output speeds (third-party Artificial Analysis):
  Llama 3.1 70B ~2,100 tok/s, 405B 969 tok/s (TTFT ~240 ms), GPT-OSS-120B ~3,000 tok/s,
  Kimi K2.6 981 tok/s (~6.7× the next-fastest GPU cloud, and notably **run across
  multiple networked CS-3s** — the speed edge survives scale-out).
- **Reasoning and agentic workloads** — a full agent request in ~0.4 s vs 1.1–4.2 s on
  GPU; "10× more reasoning steps without raising response time." Agentic chains multiply
  token generation, so latency compounds — this is the genuine moat.
- **A single very large model that must stay coherent** — fits-on-wafer avoids the
  partitioning tax entirely.
- **Some training** — Cerebras claims Llama2-70B in under a day on a full cluster
  (vendor claim, uncorroborated); training is a secondary story today.

Where it **does not** win: throughput-optimized batch inference (where GPUs amortize HBM
cost across huge batches), mixed/flexible fleets, anything needing >44 GB of *hot* state
per device, and — above all — anything bound to the CUDA ecosystem. The **40–44 GB
on-wafer SRAM ceiling vs 192 GB on a B200** is the single most under-discussed limit on
how broadly wafer-scale can win.

---

## 3. The value chain re-weights: winners and losers (Questions 3, 4, 5)

This is the heart of your question — who benefits, who gets hurt, and whose guidance is
exposed. The mechanism is simple: **a GPU cluster's networking, optics, HBM, and
packaging content all scale with the *number of discrete accelerators*. Wafer-scale
reduces that count for a given amount of compute, so those pools compress while raw
wafers and power/cooling expand.**

### 3.1 Networking — the most exposed pool (Question 5)

Every dollar of AI back-end networking exists to connect *many discrete accelerators*,
so it is the single most wafer-scale-exposed pool. Context:

- AI back-end switching is a **>$100B cumulative TAM over 2025–2029** (Ethernet ~$80B of
  it). In 2025 Ethernet **more than doubled InfiniBand** to take ~two-thirds of
  AI-cluster switch sales. Port speeds: 800G now, 1.6T ramping H2 2026, 3.2T by 2030.

| Company | Cluster-networking exposure | Read |
|---|---|---|
| **Nvidia networking** | ~$59B annualized run-rate (Q1 FY27 $14.8B, +199%), ~20% of Data Center; growing ~2.5× faster than compute | Essentially **100% a tax on GPU disaggregation** (NVLink scale-up + Spectrum-X/InfiniBand scale-out). Most exposed in absolute dollars — but it is Nvidia's own line, so it offsets Nvidia's GPU exposure |
| **Arista (ANET)** | "AI center" target **$3.25B for 2026** (raised from $2.75B) ≈ **~29% of revenue**; #3 in AI back-end Ethernet | **Most concentrated large-cap bet on many-GPU back-end Ethernet.** Highest structural exposure per dollar of market cap; partly cushioned by ~$1.25B campus/enterprise |
| **Broadcom (AVGO)** | AI networking ~40% of AI revenue (~$4.3B/qtr) trending to ~30%; FY26 AI guide ~$56B | The **networking leg is exposed**; the larger **custom-XPU leg (~60%, ~$6.5B/qtr) is the insulated counterweight** — it scales with total compute, not interconnect count |
| **Marvell (MRVL)** | Data Center 76% of revenue; electro-optics/PAM4 DSP + switching = **>50% of the DC mix** | **Proportionally the most cluster-leveraged** — its PAM4 DSP only exists because thousands of accelerators need optical links. Custom silicon (~$1.5B run-rate → >$10B by FY29) is the insulated leg |
| **Cisco (CSCO)** | AI revenue ~$4B FY26 → ≥$6B FY27, but only **~7% of company revenue** | AI piece is ~100% cluster-dependent, but **lowest corporate-level sensitivity** of the five |

**Ranking by structural networking risk:** Nvidia-networking (largest $, but a hedge
against its own GPU line) ≈ **Arista** (concentrated) > **Marvell** electro-optics
(largest DC slice) > **Broadcom** networking leg > **Cisco** (small % of total).

### 3.2 Optical interconnect

- **TAM** is huge and consensus expects it to keep compounding: LightCounting's March
  2026 revision targets **~$100B/yr of AI-cluster optical interconnect by 2030**;
  ≥800G transceiver units roughly **24M (2025) → 63M (2026)**.
- **Coherent (COHR)** is the most transceiver-levered name: Datacom & Comms ~75% of
  revenue (~$5.4B annualized, +41% YoY). Tellingly, **Nvidia took a $2B equity stake**
  in March 2026 — the incumbent is both the customer and now part-owner of the optics
  supply chain.
- **Lumentum (LITE)** holds ~50–60% of the EML laser market — the photonic chip inside
  essentially every 800G/1.6T module — and is ~88% cloud/networking.
- **The compression mechanic:** a back-end fabric needs a transceiver on *both ends* of
  every link across a multi-tier fabric — an effective **~2.5–6 transceivers per GPU**.
  If one WSE does the work of ~50 GPUs and stays on-wafer, that removes on the order of
  **~150–200 transceivers per wafer of substituted compute.** The hit lands hardest on
  **pluggable-module volume** (COHR modules) and far less on the **laser/EML chip TAM**
  (LITE, COHR InP), because even wafer-scale clusters need some optical links (SwarmX
  still runs over Ethernet/InfiniBand between wafers).
- **Co-packaged optics (CPO)** is a wildcard pulling the *other* way for the incumbent:
  Nvidia's Quantum-X and Spectrum-X Photonics move optics onto the switch, cutting energy
  ~15→~5 pJ/bit — a different way to attack the same interconnect-power problem.

> Caveat worth repeating: **no sell-side analyst has publicly modeled wafer-scale's
> compression of transceiver/networking/HBM demand.** The cross-walks above are derived
> sensitivity arguments, not consensus forecasts — which is exactly why they are a
> potential edge if the thesis plays out, and exactly why they are uncertain.

### 3.3 Memory — HBM is the most financially concentrated displacement risk

- HBM went from **~$18.2B (2024) to ~$46.7B (2025, +156%)** and is now ~33% of all DRAM
  revenue; Micron frames a path to **~$100B by 2028**. Share (Q3 2025): **SK Hynix 57%,
  Samsung 22%, Micron 21%.** All three are sold out through 2026.
- **HBM is now the dominant cost in a leading GPU:** ~$1,360 and 41% of COGS on an H100;
  ~$2,900 and **45% of COGS on a B200** (third-party modeled). Cerebras uses **zero
  HBM** — 44 GB on-wafer SRAM plus commodity DRAM in MemoryX.
- **Implication:** every unit of compute shifted GPU→wafer-scale removes on the order of
  ~$2,900 of HBM content and substitutes cheap DRAM. Because a WSE-3 ≈ "62 H100s" of
  theoretical FLOPS, the HBM-dollar multiplier per displaced wafer is large.
- **Most exposed:** SK Hynix (HBM is the bulk of its record margins — Q1 2026 operating
  margin hit ~72%) > Micron (~$8B HBM run-rate) > Samsung (swing supplier). Offsets:
  commodity DRAM demand from MemoryX rises modestly, and HBM remains capacity-constrained
  regardless, so absolute declines require *real* share loss, not just slower GPU growth.

### 3.4 Packaging and foundry — TSMC is the swing case

- **CoWoS** capacity roughly doubled to ~72.5k wafers/month at end-2025 and targets
  ~125–130k by end-2026; it is **sold out for 2026**, with Nvidia taking 60%+. CoWoS
  wafer ASP is ~$10,000 and advanced packaging is ~10% of TSMC revenue and rising. A
  wafer-scale part **skips CoWoS entirely**.
- **The TSMC trade is genuinely two-sided:**
  - **(+) Wafers:** one CS-3 consumes a *full* 5nm wafer (~$16–18.5k) versus ~60–70 GPU
    dies sharing a wafer. Wafer-scale is the *most wafer-intensive way to buy compute*,
    so TSMC keeps full front-end revenue and deepens its single-source irreplaceability.
  - **(–) Packaging margin:** it bypasses the high-ASP, high-growth CoWoS attach.
  - **Net:** roughly **revenue-neutral-to-positive on wafers, mix-negative on margin** —
    TSMC is the one name that wins on the front end even as its packaging line is the
    thing being disintermediated.
- **Purely dilutive if wafer-scale takes share:** the OSATs — **ASE** (also Cerebras's
  own OSAT) and **Amkor** — whose advanced-packaging growth is tied to CoWoS overflow.

### 3.5 The clear winners (Question 4)

1. **TSMC raw-wafer / leading-edge front end** — captures the full wafer per part; its
   irreplaceability deepens (no one else can make wafer-scale parts).
2. **Power, thermal, and cooling — the cleanest winners.** A CS-3 draws ~23 kW in a 15U
   chassis and *requires* direct liquid cooling (it cannot be air-cooled), hosted in
   ~30–35 kW/rack facilities. Beneficiaries: **Vertiv, Supermicro, HPE** (named Cerebras
   partners), cold-plate/liquid-cooling vendors, high-amperage electrical gear (busbar,
   PDUs, transformers), and high-density colocation. The **OpenAI 750 MW** build-out is
   the demand signal.
3. **The custom-compute thesis broadly** — wafer-scale validates "compute internalizes
   interconnect," which is directionally supportive of the **custom-XPU legs of Broadcom
   and Marvell** even as their networking legs are pressured.
4. **Cerebras itself**, and **commodity DRAM** at the margin (MemoryX).

---

## 4. Cerebras vs Nvidia — the seven-axis comparison (Question 6)

| Axis | Cerebras (WSE-3 / CS-3) | Nvidia (GB200/GB300, Rubin roadmap) | Edge |
|---|---|---|---|
| **Hardware architecture** | One wafer = one ~900k-core processor, 44 GB SRAM at 21 PB/s, memory disaggregated to MemoryX | Reticle dies knit into a 72-GPU NVLink domain (~130 TB/s) to *emulate* a big device; HBM on-package | Cerebras for intra-device bandwidth & single-model latency; **Nvidia for memory capacity, flexibility, partitioning** |
| **Software ecosystem** | CSoft + PyTorch front end; ~97% less code (no manual parallelism); developer base in the thousands; thin third-party tooling | **CUDA: ~5M developers, ~20 years of libraries** (cuDNN, NCCL, TensorRT), universal framework support | **Nvidia, decisively.** This is the moat |
| **Scalability** | Single wafer → up to 2,048 CS-3s via SwarmX/MemoryX; near-linear claim; 24T-param models | NVLink scale-up (72→576 GPUs) + InfiniBand/Spectrum-X across thousands of racks; proven at frontier scale | **Nvidia at extreme multi-thousand-node maturity;** Cerebras simpler within its envelope |
| **Cost of ownership** | System ~$2–3M (volume-tiered; sell-side models ~$1M effective for cloud); inference list $0.10–$12/Mtok; sells managed cloud | GPU economics well-understood; far higher memory-per-dollar; deep resale/financing ecosystem | **Nvidia on $/memory & flexibility; Cerebras can win $/token on its niche** |
| **Power** | ~23–27 kW/system, liquid-cooled mandatory | GB200 NVL72 ~132 kW/rack; Rubin Ultra "Kyber" ~600 kW/rack | **Not cleanly comparable** (precision/workload differ); Cerebras's pitch is fewer systems per large-model job |
| **Training** | Claims Llama2-70B <1 day (vendor, uncorroborated); secondary story | Mature, MLPerf-proven, the default for frontier training | **Nvidia** |
| **Inference** | Structurally lowest per-token latency on large/reasoning models; 6–16× output-speed claims | Excellent throughput; answering the latency niche with Dynamo + Rubin CPX | **Cerebras on single-stream latency; Nvidia on throughput & breadth** |

**Bottom line: Cerebras is a spike, not (yet) a platform.** It has a real,
physics-grounded edge in low-latency large-model and agentic inference. Nvidia wins on
ecosystem, flexibility, memory economics, scale maturity, and the total addressable
workload.

---

## 5. "AMD of AI accelerators," or a dominant platform? (Question 7)

The historical analogues are the most useful lens here.

- **AMD vs Intel.** Opteron peaked at ~26% of server sockets in 2006, then collapsed to
  <1% by 2016, then EPYC drove back to **46% of server-CPU *revenue* by Q1 2026.** What
  enabled the comeback: a real process/architecture lead (TSMC + chiplets) while Intel
  stalled, **full x86 compatibility (zero porting cost)**, roadmap credibility, and an
  incumbent that self-inflicted. Lesson: AMD never had to displace an *ecosystem* — same
  ISA.
- **ARM vs x86.** AWS Graviton reached **>50% of new CPU capacity at AWS** and 98% of the
  top-1,000 EC2 customers. What enabled it: a **vertically integrated hyperscaler that
  could mandate adoption, hide the switching cost, and abstract the ISA** (you rent an
  instance, not a chip). ARM broke in where one powerful buyer internalized the porting.
- **CUDA vs alternatives.** ROCm, OpenCL, and oneAPI together hold <10% share after 15+
  years and billions spent — defeated by entrenchment and the chicken-and-egg loop. The
  lesson: a *better-but-incompatible* platform that fights the open merchant market
  head-on **stalls**.

**Where this puts Cerebras:** its path resembles **Graviton/EPYC-by-mandate, not
ROCm.** It is winning through anchor buyers who internalize the switching cost (G42,
then OpenAI, then AWS) and a **managed-API abstraction** so customers never touch the
locked-in dev layer — the successful-challenger playbook, not the failed one.

But the same structure carries the failed-challenger's two classic vulnerabilities:
**extreme customer concentration** (86% UAE in 2025, soon OpenAI-dominated) and a
**single-source, never-scaled supply chain** — both biting precisely as it must scale
~10×, against an incumbent **actively absorbing the inference niche** (Dynamo, the
purpose-built Rubin CPX long-context GPU) and widening its moat into networking and
openness (NVLink Fusion; $2B stakes in Marvell and Coherent).

**Verdict:** the realistic ceiling for the next several years is the **"AMD/Arm of fast
inference"** — a durable, valuable #2/#3 platform that *owns a sub-segment* (low-latency
agentic inference) rather than a CUDA-displacing general platform. Becoming a dominant
platform would require (a) the software/API abstraction to attract workloads beyond
captive customers, (b) at least one Western hyperscaler adopting wafer-scale internally,
and (c) the SRAM-capacity constraint easing (the hybrid-bonded memory wafer on the CS-5/6
roadmap). Those are possible, not yet probable.

---

## 6. Public-company impact and the guidance-exposure map (Question 8)

The crucial nuance for a long-term investor: **almost none of this bites in 2026–2027.**
Cerebras's entire wafer draw is a rounding error against Nvidia's ~800k CoWoS
wafers/year. The value-chain compression is a **2027–2030 structural watch**, and it
shows up first as *slower growth than consensus*, not absolute declines.

| Company | Direction | Why | When guidance is exposed |
|---|---|---|---|
| **Nvidia (NVDA)** | Mild net negative, self-hedged | Loses GPU + networking + CoWoS + HBM-attach share *if* wafer-scale wins; but it is also co-opting the niche (Dynamo, Rubin CPX) and owns the networking it would cannibalize | Late, and partly internalized |
| **Arista (ANET)** | **Most exposed networking name** | ~29% of revenue is AI back-end Ethernet, highly concentrated; super-linear attach reverses if node counts fall | 2027–2029 if hyperscalers adopt wafer-scale at scale |
| **Broadcom (AVGO)** | Mixed | Networking leg (~30–40% of AI) exposed; **custom-XPU leg (~60%) insulated and arguably a winner** | Networking-leg only; diversified |
| **Marvell (MRVL)** | **Proportionally most exposed** | Electro-optics/PAM4 DSP + switching >50% of DC; only exists to connect many accelerators | 2027–2030; custom silicon offsets |
| **Coherent (COHR)** | **Most transceiver-exposed** | ~75% datacom optics; pluggable-module volume compresses most | 2028+; Nvidia ownership stake is a partial backstop |
| **Cisco (CSCO)** | Low corporate sensitivity | AI is ~100% cluster-dependent but only ~7% of revenue | Minimal at the corporate level |
| **SK Hynix / Micron / Samsung** | HBM displacement risk | HBM is 33% of DRAM revenue and 45% of leading-GPU COGS; Cerebras uses none | 2028–2030, only on real share loss |
| **TSMC** | **Net winner (front end), mix-negative (packaging)** | Full wafer per part; loses CoWoS attach | Wafer line benefits early; packaging mix later |
| **Vertiv / Supermicro / cooling** | **Winners** | 23 kW liquid-cooled systems, 750 MW build-out | Benefits track the Cerebras ramp |
| **Cerebras (CBRS)** | The pure-play | ~$510M (2025A) → consensus ~$6.8–7.1B (2028E); the call is execution, not technology | Every quarter, on backlog conversion and concentration |

---

## 7. Three scenarios (Question 9)

Framed as a long-term investor would: probabilities are judgment, not precision.

### Bear — limited adoption (~30%)
Wafer-scale stays a boutique. The CUDA moat, the 44 GB SRAM ceiling, and customer
concentration cap it; an OpenAI slip or a supply-chain stumble (the ~10× scale-up never
materializes cleanly) stalls the ramp. Cerebras 2028 revenue lands well below the
~$6.8B plan; the stock drifts toward or below the sell-side bear case (~$160). **Value-chain
impact: negligible** — wafer-scale stays <1–2% of accelerator compute, and networking /
optics / HBM consensus is untouched. *Investor read: no action needed in the supply
chain; CBRS itself is a high-beta call option that goes against you.*

### Base — niche success (~50%)
Cerebras wins the low-latency/agentic-inference sub-segment (roughly the ~25%-of-inference
slice Nvidia itself ascribes to fast inference). OpenAI and AWS ramp; revenue reaches
~$6–12B by 2028–2029; gross margin climbs toward the high 50s. Cerebras becomes the
**"AMD of fast inference"** — a durable #2/#3. **Value-chain impact: marginal** — it
shaves a few points off the *growth rate* of networking/optics/HBM attach (the super-linear
interconnect curve flattens slightly) rather than cutting absolute revenue. Most exposed
names (ANET, COHR, MRVL) still grow, just less than the bull-case AI-networking narrative
assumes. Stock supports the ~$280–300 sell-side targets. *Investor read: own CBRS on
execution; the supply-chain trade is a watch-list item, not yet actionable.*

### Bull — major disruption (~20%)
Wafer-scale proves general (training as well as inference), a Western hyperscaler adopts
it internally, the software/API abstraction pulls in third-party workloads, and supply
scales. Cerebras revenue runs past $15B and takes real accelerator share. **Now the
re-weight becomes investable:** networking, optics, and HBM TAMs grow materially slower
than consensus; **guidance cuts arrive at Arista, Coherent, Marvell, and the HBM makers**,
and Nvidia's networking attach compresses. The paired trade — long TSMC wafers + power/
cooling, underweight the interconnect/HBM beneficiaries — is the expression. *Investor
read: this is the scenario that pays, and the leading indicators in §8 are how you
front-run it.*

---

## 8. Leading indicators to monitor over five years (Question 10)

Grouped by what each tells you, with the trigger to watch:

**Customer diversification — the single most important signal**
- Named **non-UAE, non-OpenAI** logos buying at scale (a Western hyperscaler, a frontier
  lab, Fortune-500 enterprises). Trigger: **top-2 customer concentration falling below
  ~50%** of revenue (from ~86% today).
- Whether OpenAI's Cerebras spend grows *even as* its **6 GW AMD commitment** and its
  Nvidia/Broadcom orders grow — i.e., strategic supplier vs swing vendor (a circularity
  flag: OpenAI is simultaneously customer, lender, and warrant-holder).

**Hyperscaler partnerships**
- Beyond an AWS marketplace listing: a **first-party Azure / GCP / Oracle** managed
  Cerebras offering, or a hyperscaler **co-investing in wafer-scale capacity.** None of
  the big-3 runs wafer-scale internally today — they are building their own silicon (TPU,
  Trainium, Maia). One defection toward wafer-scale would be a regime change.

**Software-ecosystem / developer adoption**
- Cerebras developer count and API token volume vs the benchmark to beat — **Groq's
  ~360k developers and 75% of the Fortune 100**. Watch for native framework support,
  third-party tooling, and models being *trained* (not just served) on Cerebras outside
  captive accounts. Growth in the managed-inference API is the realistic adoption vector
  — not CUDA-developer conversion.

**Financial and operational signals**
- **Gross margin trajectory**: 39% → 50%+ would validate scale economics; flat or
  declining at higher volume signals a yield or capex problem.
- **RPO/backlog conversion**: the ~$24.6B remaining performance obligation must convert
  to recognized revenue on schedule; OpenAI's 750 MW build-out milestones hitting on time
  is the tell. Slippage = the supply-chain risk made real.
- **Supply-chain milestones**: TSMC wafer-scale capacity commitments, in-house packaging
  throughput, and the climb from ~thousands to ~30,000 systems — the make-or-break metric.
- **Competitive watch**: Groq (closest latency competitor, ahead on developers), Google
  TPU v7 Ironwood, AWS Trainium3, and AMD MI450 — and any Nvidia move to fold fast/
  low-latency inference fully into its roadmap (Dynamo + Rubin CPX already aim there).

---

## 9. Investor takeaways

1. **The technology is real and the mechanism is the story.** Wafer-scale genuinely
   removes the memory-and-interconnect re-stitching layer that a GPU cluster is built
   from. That is not a marketing claim; it is a different physical architecture.
2. **But it is a spike, not a platform — for now.** The CUDA moat (~5M developers) and
   the 44 GB SRAM ceiling confine the durable win to low-latency/agentic inference. Treat
   the realistic case as the **"AMD of fast inference,"** not a CUDA-killer.
3. **The most investable idea is the second-order value-chain re-weight, not CBRS
   itself.** If wafer-scale takes share, the pain concentrates in **networking (Arista),
   optics (Coherent), HBM (SK Hynix), and CoWoS packaging** — while **TSMC wafers and
   power/cooling (Vertiv) benefit.** No sell-side model captures this yet, which is the
   edge — but it only pays in the base-plus/bull path and on a 2027–2030 horizon.
4. **CBRS the stock is a concentrated, capital-intensive execution bet.** It IPO'd at
   $185, spiked to $311, and had already round-tripped to ~$201 by the June initiations —
   the market is repricing a thin-float, 86%-concentrated, supply-chain-constrained name
   in real time. The thesis lives or dies on **customer diversification and gross-margin/
   RPO conversion at 10× volume**, not on the chip.
5. **What would change the call:** a Western hyperscaler adopting wafer-scale internally,
   concentration falling below ~50%, or the SRAM ceiling lifting (hybrid-bonded memory on
   the CS-5/6 roadmap) — any one of which would move the base case toward the bull case
   and make the supply-chain trade actionable.

---

*Cross-checks applied: figures reconciled across multiple independent sell-side and
public sources; vendor performance claims flagged as first-party; every value-chain
compression estimate is a derived sensitivity (no published analyst models it) and is
labeled as such. Method-and-findings only; not investment advice, and not a
republication of any third-party report.*

# Downsizing – a minimal economic simulation

## The idea

Imagine a machine that can **permanently shrink a human** by some linear factor `s`.
A shrunk person:

- still performs intellectual work just as well,
- has drastically lower material needs (food, waste, housing, clothes, transport),
- **cannot produce food or raw materials at scale** – tractors, combines, factories, logging equipment are all out of reach.

The questions we want to explore:

> Do living costs fall proportionally to needs?
> What ratio of "giants" to "smalls" is stable?
> Do giants – as the only source of food – capture most of the income?

The goal is not a realistic simulation. It is the **smallest model that yields a meaningful equilibrium** and lets us see which way parameter changes push it.

## Key economic tensions

1. **Needs scale, but prices are set by markets.** Physical needs scale with body size. Food *prices*, however, are set by total demand across the whole population and by how many producers are left.
2. **Physics forces specialization.** Only giants can produce food and raw materials. Smalls dominate wherever the number of minds matters more than body mass (software, design, research).
3. **Supply bottleneck.** If most people shrink, food producers become scarce. Their labor earns a rent for being a giant.
4. **Costs that do not scale.** Some services are "per person", not "per kilogram" – doctors, teachers, admin, software. A small consumes the same amount as a giant.
5. **Conversion decision.** In equilibrium every agent should be indifferent between being `G` and `S` (otherwise everyone migrates one way). This no-arbitrage condition pins down the ratio.

## Minimal model

### Agents

Two types, fixed population `N`:

- `n_G` – giants,
- `n_S` – smalls, with `n_G + n_S = N`.

Conversion between types is allowed (optional one-off cost `c_conv`; the base version treats it as free and reversible).

### Scale parameter

One parameter: `s` – the linear shrink factor (e.g. `s = 10`).

Scaling of physical needs (kept as a model dial):

| Good | Scaling with `s` |
|---|---|
| Food, waste, materials (volumetric) | `1/s³` (realistic) or `1/s` (simplified, matches the framing) |
| Housing, clothes (area-like) | `1/s²` or `1/s` |
| Per-person services (doctor, teacher, software) | `1` – unchanged |

The base version uses a single **physical-needs coefficient `φ = 1/s`**. This is the first parameter to sweep for sensitivity.

### Goods

At least three, so the dynamics is non-trivial:

- **`F` – food / raw materials.** Produced *only* by `G`. Consumption: `1` by `G`, `φ` by `S`.
- **`I` – intellectual goods.** Produced by both types. Consumption: `1` per person (does not scale).
- **`H` – fixed per-person services** (optional, easy to add later) – per-person, produced by both.

### Productivity (units per person per period)

- `a_G^F` – food produced by a giant (>0),
- `a_G^I`, `a_S^I` – intellectual output. A small may be *more* efficient per resource (since they consume less themselves), but per head start with `a_G^I = a_S^I`.
- `a_S^F = 0` – smalls do not produce food at scale.

### Prices and wages

Endogenous: `p_F`, `p_I`, wages `w_G`, `w_S`.

Simplification: each agent works on one good at a time and picks whatever yields the higher income. Wage equals marginal value of output.

### Equilibrium conditions

1. **Food clearing:** `n_G · a_G^F = n_G · 1 + n_S · φ`
2. **Intellectual-goods clearing:** `n_G · a_G^I · x_G + n_S · a_S^I · x_S = N` (`x` is the labor share on `I`).
3. **Agent budget:** income ≥ cost of living for the chosen type.
4. **No-arbitrage:** welfare (surplus after cost of living) of a giant equals that of a small. This condition pins down `n_S / n_G`.

## What we want to see

Minimal outputs of the simulation:

- **Equilibrium ratio `n_S / n_G`** as a function of `s` and `φ`.
- **Wage ratio `w_G / w_S`** – hypothesis: rises with `s` (the smaller the smalls, the more of them, the scarcer and pricier the giants).
- **Cost-of-living ratio `cost_S / cost_G`** – hypothesis: does *not* fall all the way to `φ`, because per-person goods and services set a floor.
- **Total resource footprint** (`F` consumed) vs. number of productive minds – a measure of the "civilizational efficiency" of downsizing.

A non-trivial hypothesis worth testing:
*There exists a level of `s` at which giants, despite being a minority, capture the majority of income – because their labor is the only source of a good nobody else can produce.*

## Extensions (after the base case)

- Cost and irreversibility of conversion.
- Technological progress in food production (automation raises `a_G^F`) – does it break the giants' bottleneck?
- Smalls running "micro-agriculture" (small `a_S^F > 0` from a different technology).
- Spatial constraints / land as a factor of production.
- Heterogeneous talent in intellectual work.

## Status

The repository is at the model-design stage. Next step: implement an equilibrium solver for this minimal setup (3 goods, 2 types, 4 prices/wages) and sweep over `s` and `φ`.

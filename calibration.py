"""Calibration to concrete dollar amounts.

The base model is dimensionless. Here we map parameters onto something
recognisable (US-ish household budget, population of 1 million) and run
a few scenarios so the magnitudes are visible.

Key identity: in the base equilibrium, a giant's budget share on food
equals 1/a_GF. So we can calibrate a_GF directly from "what fraction
of household spending is on goods that scale with body size".

Scenarios:
  A. Tech-utopia:    F is ~10% of budget  (a_GF = 10)
  B. US-like:        F is ~50% of budget  (a_GF = 2)   -- food + housing + transport + clothes
  C. Subsistence:    F is ~80% of budget  (a_GF = 1.25)
For each, we try phi in {0.1, 0.01} corresponding to linear s=10 and volumetric s=10.

To get dollars, we scale the numeraire so that a giant's annual wage is $50,000.
"""

from __future__ import annotations

from dataclasses import dataclass

from equilibrium import Params, solve


N_PEOPLE = 1_000_000
TARGET_GIANT_WAGE_USD = 50_000.0


@dataclass
class Scenario:
    name: str
    a_GF: float
    phi: float
    description: str


SCENARIOS = [
    Scenario("A1", 10.0, 0.1, "tech-utopia economy, linear scaling (s=10)"),
    Scenario("A2", 10.0, 0.001, "tech-utopia economy, volumetric (s=10)"),
    Scenario("B1", 2.0, 0.1, "US-like budget (F~50%), linear scaling"),
    Scenario("B2", 2.0, 0.001, "US-like budget (F~50%), volumetric"),
    Scenario("C1", 1.25, 0.1, "subsistence (F~80%), linear scaling"),
    Scenario("C2", 1.25, 0.001, "subsistence (F~80%), volumetric"),
]


def dollars(x: float, scale: float) -> str:
    return f"${x * scale:>12,.0f}"


def run_scenario(sc: Scenario) -> None:
    p = Params(N=N_PEOPLE, a_GF=sc.a_GF, a_GI=2.0, a_SI=2.0, phi=sc.phi)
    eq = solve(p)
    usd = TARGET_GIANT_WAGE_USD / eq.w_G

    pop_share = eq.giants_pop_share
    inc_share = eq.giants_income_share
    rent_ratio = inc_share / pop_share

    print(f"\n=== Scenario {sc.name}: {sc.description} ===")
    print(f"  a_GF = {sc.a_GF}, phi = {sc.phi}")
    print(f"  giants:                    {eq.n_G:>12,.0f} people ({pop_share * 100:.2f}%)")
    print(f"  smalls:                    {eq.n_S:>12,.0f} people ({(1 - pop_share) * 100:.2f}%)")
    print(f"  giant wage:                {dollars(eq.w_G, usd)} / yr")
    print(f"  small wage:                {dollars(eq.w_S, usd)} / yr")
    print(f"  wage premium:              {eq.w_G / eq.w_S:.3f}x")
    print(f"  giant food spend:          {dollars(eq.p_F * 1.0, usd)} "
          f"({eq.p_F / eq.w_G * 100:.1f}% of budget)")
    print(f"  small food spend:          {dollars(eq.p_F * sc.phi, usd)} "
          f"({eq.p_F * sc.phi / eq.w_S * 100:.1f}% of budget)")
    print(f"  small cost of living:      {eq.expenditure_S / eq.expenditure_G * 100:.1f}% of giant's")
    print(f"  giants' share of income:   {inc_share * 100:.2f}%  "
          f"(pop share {pop_share * 100:.2f}%, rent ratio {rent_ratio:.2f}x)")


def summary_table() -> None:
    print("\nQuick reference -- what drives the rent?\n")
    print(f"{'a_GF':>6}  {'F share':>8}  {'phi':>7}  {'giants %':>10}  "
          f"{'wage prem':>10}  {'cost S/G':>9}  {'rent':>7}")
    print("-" * 76)
    for a_GF in (100.0, 10.0, 5.0, 2.0, 1.25, 1.1):
        for phi in (0.1, 0.01):
            p = Params(a_GF=a_GF, phi=phi)
            eq = solve(p)
            f_share = 1.0 / a_GF
            rent = eq.giants_income_share / eq.giants_pop_share
            print(
                f"{a_GF:>6.2f}  {f_share * 100:>7.1f}%  {phi:>7.3f}  "
                f"{eq.giants_pop_share * 100:>9.3f}%  "
                f"{eq.w_G / eq.w_S:>10.3f}  "
                f"{eq.expenditure_S / eq.expenditure_G:>9.3f}  "
                f"{rent:>7.3f}"
            )


if __name__ == "__main__":
    for sc in SCENARIOS:
        run_scenario(sc)
    summary_table()

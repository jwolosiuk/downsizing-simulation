"""Sweep over shrink factor s and produce diagnostic plots.

Run with `python3 sweep.py`. Writes PNGs into ./figures/.

Three scaling variants for physical needs:
    linear: phi = 1/s       (the framing from the README)
    area:   phi = 1/s**2    (area-like needs, e.g. housing)
    volume: phi = 1/s**3    (volumetric needs, e.g. food/materials)

Fixed other parameters: a_GF = 10, a_GI = a_SI = 2, N = 1.
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

from equilibrium import Params, solve


SCALINGS = {
    "linear (1/s)": lambda s: 1.0 / s,
    "area (1/s^2)": lambda s: 1.0 / s**2,
    "volume (1/s^3)": lambda s: 1.0 / s**3,
}

S_GRID = np.linspace(1.01, 30.0, 200)


def run(scaling):
    rows = []
    for s in S_GRID:
        phi = scaling(s)
        if phi >= 1.0:
            continue
        eq = solve(Params(phi=phi))
        rows.append(
            (
                s,
                phi,
                eq.giants_pop_share,
                eq.giants_income_share,
                eq.w_G / eq.w_S,
                eq.expenditure_S / eq.expenditure_G,
                eq.food_consumed,
                eq.I_G,
            )
        )
    return np.array(rows).T


def main() -> None:
    os.makedirs("figures", exist_ok=True)

    results = {name: run(fn) for name, fn in SCALINGS.items()}

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    (ax_pop, ax_inc, ax_wage), (ax_cost, ax_food, ax_i) = axes

    for name, data in results.items():
        s, phi, pop_share, inc_share, wage_ratio, cost_ratio, food, I_per = data
        ax_pop.plot(s, pop_share, label=name)
        ax_inc.plot(s, inc_share, label=name)
        ax_wage.plot(s, wage_ratio, label=name)
        ax_cost.plot(s, cost_ratio, label=name)
        ax_food.plot(s, food, label=name)
        ax_i.plot(s, I_per, label=name)

    ax_pop.set_title("giant population share  n_G / N")
    ax_pop.set_xlabel("shrink factor s")
    ax_pop.set_yscale("log")
    ax_pop.grid(True, alpha=0.3)
    ax_pop.legend(fontsize=8)

    ax_inc.set_title("giant income share")
    ax_inc.set_xlabel("shrink factor s")
    ax_inc.set_yscale("log")
    ax_inc.grid(True, alpha=0.3)

    ax_wage.set_title("wage ratio  w_G / w_S")
    ax_wage.set_xlabel("shrink factor s")
    ax_wage.grid(True, alpha=0.3)

    ax_cost.set_title("expenditure ratio  E_S / E_G")
    ax_cost.set_xlabel("shrink factor s")
    ax_cost.grid(True, alpha=0.3)

    ax_food.set_title("total food consumed (per unit population)")
    ax_food.set_xlabel("shrink factor s")
    ax_food.set_yscale("log")
    ax_food.grid(True, alpha=0.3)

    ax_i.set_title("intellectual goods per capita  I_G = I_S")
    ax_i.set_xlabel("shrink factor s")
    ax_i.grid(True, alpha=0.3)

    fig.suptitle(
        "Downsizing equilibrium, base model  (a_GF=10, a_GI=a_SI=2, N=1)",
        fontsize=12,
    )
    fig.tight_layout()

    out = "figures/sweep_base.png"
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")

    print_summary(results)


def print_summary(results) -> None:
    print("\nEquilibrium at s = 10, linear scaling (phi = 0.1):")
    eq = solve(Params(phi=0.1))
    print(f"  giant pop share    = {eq.giants_pop_share:.4f}")
    print(f"  giant income share = {eq.giants_income_share:.4f}")
    print(f"  w_G / w_S          = {eq.w_G / eq.w_S:.4f}")
    print(f"  E_S / E_G          = {eq.expenditure_S / eq.expenditure_G:.4f}")
    print(f"  food per capita    = {eq.food_consumed:.4f}")
    print(f"  I per capita       = {eq.I_G:.4f}")

    print("\nEquilibrium at s = 10, volumetric scaling (phi = 0.001):")
    eq = solve(Params(phi=1e-3))
    print(f"  giant pop share    = {eq.giants_pop_share:.5f}")
    print(f"  giant income share = {eq.giants_income_share:.5f}")
    print(f"  w_G / w_S          = {eq.w_G / eq.w_S:.5f}")
    print(f"  E_S / E_G          = {eq.expenditure_S / eq.expenditure_G:.5f}")


if __name__ == "__main__":
    main()

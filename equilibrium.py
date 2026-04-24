"""Closed-form equilibrium for the base downsizing model.

Two types (giants G, smalls S), two goods (food F, intellectual I).
Only giants produce F. Both types could produce I, but under the base
assumption (a_GI >= a_SI and smalls prefer to shrink) giants fully
specialise on F and smalls fully specialise on I.

Consumption is subsistence on F (1 for G, phi for S) plus endogenous
consumption of I out of residual income. Utility is log(I_consumed) --
with full budget exhaustion, any monetary "surplus" would be zero.

Normalise p_I = 1. Welfare-arbitrage W_G = W_S pins the relative food
price; food-market clearing pins the population split; intellectual-
market clearing then holds automatically by Walras' law.

Closed form:
    p_F              = a_SI / (a_GF - 1 + phi)
    n_G / N          = phi / (a_GF - 1 + phi)
    I_G = I_S        = a_SI * (a_GF - 1) / (a_GF - 1 + phi)
    w_G              = p_F * a_GF
    w_S              = a_SI
    w_G / w_S        = a_GF / (a_GF - 1 + phi)
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Params:
    N: float = 1.0
    a_GF: float = 10.0
    a_GI: float = 2.0
    a_SI: float = 2.0
    phi: float = 0.1

    def __post_init__(self) -> None:
        assert self.N > 0
        assert self.a_GF > 1.0, "giants must produce more food than they consume"
        assert self.a_GI >= self.a_SI > 0, "base case assumes a_GI >= a_SI > 0"
        assert 0.0 < self.phi <= 1.0


@dataclass(frozen=True)
class Equilibrium:
    n_G: float
    n_S: float
    p_F: float
    p_I: float
    w_G: float
    w_S: float
    I_G: float
    I_S: float
    expenditure_G: float
    expenditure_S: float
    utility_G: float
    utility_S: float
    giants_income_share: float
    giants_pop_share: float
    food_produced: float
    food_consumed: float
    intellectual_produced: float
    intellectual_consumed: float


def _regime_is_giants_specialise(p: Params) -> bool:
    # At hypothetical interior prices (giants indifferent between F and I),
    # W_G - W_S has sign of (a_GI - a_SI) * a_GF - (1 - phi) * a_GI.
    # Negative => smalls prefer shrinking => specialisation corner.
    return (p.a_GI - p.a_SI) * p.a_GF < (1.0 - p.phi) * p.a_GI


def solve(p: Params) -> Equilibrium:
    if not _regime_is_giants_specialise(p):
        raise NotImplementedError(
            "Base solver only handles the small-preferred corner "
            "(all-giants corner needs a different closed form)."
        )

    denom = p.a_GF - 1.0 + p.phi
    p_F = p.a_SI / denom
    p_I = 1.0

    n_G = p.N * p.phi / denom
    n_S = p.N - n_G

    w_G = p_F * p.a_GF
    w_S = p.a_SI

    I_G = p_F * (p.a_GF - 1.0) / p_I
    I_S = (p.a_SI - p.phi * p_F) / p_I

    expenditure_G = p_F * 1.0 + p_I * I_G
    expenditure_S = p_F * p.phi + p_I * I_S

    utility_G = math.log(I_G)
    utility_S = math.log(I_S)

    total_income = n_G * w_G + n_S * w_S
    giants_income_share = (n_G * w_G) / total_income

    food_produced = n_G * p.a_GF
    food_consumed = n_G * 1.0 + n_S * p.phi
    intellectual_produced = n_S * p.a_SI
    intellectual_consumed = n_G * I_G + n_S * I_S

    return Equilibrium(
        n_G=n_G,
        n_S=n_S,
        p_F=p_F,
        p_I=p_I,
        w_G=w_G,
        w_S=w_S,
        I_G=I_G,
        I_S=I_S,
        expenditure_G=expenditure_G,
        expenditure_S=expenditure_S,
        utility_G=utility_G,
        utility_S=utility_S,
        giants_income_share=giants_income_share,
        giants_pop_share=n_G / p.N,
        food_produced=food_produced,
        food_consumed=food_consumed,
        intellectual_produced=intellectual_produced,
        intellectual_consumed=intellectual_consumed,
    )


def pretty(eq: Equilibrium) -> str:
    return (
        f"population    n_G={eq.n_G:.4f}  n_S={eq.n_S:.4f}  giant_share={eq.giants_pop_share:.4f}\n"
        f"prices        p_F={eq.p_F:.4f}  p_I={eq.p_I:.4f}\n"
        f"wages         w_G={eq.w_G:.4f}  w_S={eq.w_S:.4f}  ratio={eq.w_G / eq.w_S:.4f}\n"
        f"I consumption I_G={eq.I_G:.4f}  I_S={eq.I_S:.4f}\n"
        f"expenditure   E_G={eq.expenditure_G:.4f}  E_S={eq.expenditure_S:.4f}\n"
        f"utility       U_G={eq.utility_G:.4f}  U_S={eq.utility_S:.4f}  gap={eq.utility_G - eq.utility_S:.2e}\n"
        f"income share  giants={eq.giants_income_share:.4f}  (pop share {eq.giants_pop_share:.4f})\n"
        f"food          produced={eq.food_produced:.4f}  consumed={eq.food_consumed:.4f}\n"
        f"intellectual  produced={eq.intellectual_produced:.4f}  consumed={eq.intellectual_consumed:.4f}\n"
    )


if __name__ == "__main__":
    eq = solve(Params())
    print(pretty(eq))

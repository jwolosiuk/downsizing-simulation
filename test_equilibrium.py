"""Sanity tests for the closed-form equilibrium.

Run with `python3 test_equilibrium.py`. No pytest dependency.
"""

from __future__ import annotations

import math

from equilibrium import Equilibrium, Params, solve


TOL = 1e-10


def _check(eq: Equilibrium, p: Params) -> None:
    # population adds up
    assert math.isclose(eq.n_G + eq.n_S, p.N, rel_tol=TOL)

    # non-negativity
    assert eq.n_G > 0 and eq.n_S > 0
    assert eq.p_F > 0 and eq.p_I > 0
    assert eq.w_G > 0 and eq.w_S > 0
    assert eq.I_G > 0 and eq.I_S > 0

    # food market clears
    assert math.isclose(eq.food_produced, eq.food_consumed, rel_tol=TOL)

    # intellectual market clears (Walras)
    assert math.isclose(
        eq.intellectual_produced, eq.intellectual_consumed, rel_tol=TOL
    )

    # budgets exhausted
    assert math.isclose(eq.expenditure_G, eq.w_G, rel_tol=TOL)
    assert math.isclose(eq.expenditure_S, eq.w_S, rel_tol=TOL)

    # welfare arbitrage: utilities equal (that's what pins p_F)
    assert math.isclose(eq.utility_G, eq.utility_S, abs_tol=TOL)

    # wage under perfect competition = price * productivity
    assert math.isclose(eq.w_G, eq.p_F * p.a_GF, rel_tol=TOL)
    assert math.isclose(eq.w_S, eq.p_I * p.a_SI, rel_tol=TOL)


def test_defaults() -> None:
    p = Params()
    eq = solve(p)
    _check(eq, p)


def test_sweep_phi() -> None:
    for phi in (0.9, 0.5, 0.2, 0.1, 0.01, 0.001):
        p = Params(phi=phi)
        _check(solve(p), p)


def test_sweep_aGF() -> None:
    for a_GF in (1.1, 2.0, 5.0, 10.0, 100.0):
        p = Params(a_GF=a_GF)
        _check(solve(p), p)


def test_extreme_shrink_shrinks_giants_population() -> None:
    # As phi -> 0, the fraction of giants should fall.
    shares = [solve(Params(phi=phi)).giants_pop_share for phi in (0.5, 0.1, 0.01)]
    assert shares[0] > shares[1] > shares[2]


def test_less_productive_farming_raises_wage_premium() -> None:
    # Lower a_GF (farming harder) -> giants scarcer per unit food -> higher relative wage.
    ratios = []
    for a_GF in (10.0, 5.0, 2.0, 1.5):
        eq = solve(Params(a_GF=a_GF))
        ratios.append(eq.w_G / eq.w_S)
    assert ratios == sorted(ratios), ratios  # monotonically non-decreasing


def test_all_giants_corner_raises() -> None:
    # Make giants strictly better at I (a_GI >> a_SI) so the corner flips.
    # That corner isn't implemented in the base solver yet.
    try:
        solve(Params(a_GI=100.0, a_SI=1.0))
    except NotImplementedError:
        return
    raise AssertionError("expected NotImplementedError for all-giants corner")


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed")

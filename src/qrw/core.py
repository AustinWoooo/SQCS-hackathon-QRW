"""Transparent NumPy reference model for a coined walk on a cycle."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

import numpy as np
from numpy.typing import NDArray

ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]

HADAMARD: ComplexArray = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / np.sqrt(2.0)


@dataclass(frozen=True)
class WalkResult:
    """Final amplitudes and position probabilities for one simulation."""

    amplitudes: ComplexArray
    probabilities: FloatArray
    steps: int
    size: int
    start: int


def _validate(size: int, steps: int, start: int) -> None:
    if size < 2:
        raise ValueError("size must be at least 2")
    if steps < 0:
        raise ValueError("steps must be non-negative")
    if not 0 <= start < size:
        raise ValueError("start must satisfy 0 <= start < size")


def simulate_quantum_walk(
    *,
    size: int,
    steps: int,
    start: int | None = None,
    coin: ComplexArray = HADAMARD,
    initial_coin: tuple[complex, complex] = (1 / np.sqrt(2), 1j / np.sqrt(2)),
) -> WalkResult:
    """Evolve a coherent coined walk with periodic boundary conditions.

    Coin state 0 moves left and coin state 1 moves right. No measurement or
    reset occurs between steps, so interference is preserved.
    """

    start = size // 2 if start is None else start
    _validate(size, steps, start)
    coin = np.asarray(coin, dtype=complex)
    if coin.shape != (2, 2) or not np.allclose(coin.conj().T @ coin, np.eye(2)):
        raise ValueError("coin must be a 2x2 unitary matrix")

    coin_state = np.asarray(initial_coin, dtype=complex)
    if coin_state.shape != (2,) or not np.isclose(np.vdot(coin_state, coin_state), 1.0):
        raise ValueError("initial_coin must be a normalized two-amplitude state")

    state = np.zeros((2, size), dtype=complex)
    state[:, start] = coin_state

    for _ in range(steps):
        after_coin = coin @ state
        shifted = np.zeros_like(state)
        shifted[0] = np.roll(after_coin[0], -1)
        shifted[1] = np.roll(after_coin[1], 1)
        state = shifted

    probabilities = np.sum(np.abs(state) ** 2, axis=0).real
    return WalkResult(state, probabilities, steps, size, start)


def quantum_distribution(**kwargs: object) -> FloatArray:
    """Return only the position distribution from ``simulate_quantum_walk``."""

    return simulate_quantum_walk(**kwargs).probabilities


def classical_distribution(*, size: int, steps: int, start: int | None = None) -> FloatArray:
    """Exact unbiased classical random-walk distribution on the same cycle."""

    start = size // 2 if start is None else start
    _validate(size, steps, start)
    probabilities = np.zeros(size, dtype=float)
    for right_steps in range(steps + 1):
        displacement = 2 * right_steps - steps
        destination = (start + displacement) % size
        probabilities[destination] += comb(steps, right_steps) / (2**steps)
    return probabilities


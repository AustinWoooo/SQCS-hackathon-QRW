import numpy as np
import pytest

from qrw import classical_distribution, quantum_distribution, simulate_quantum_walk


@pytest.mark.parametrize("steps", range(9))
def test_quantum_probability_is_normalized(steps: int) -> None:
    result = simulate_quantum_walk(size=32, steps=steps)
    assert np.isclose(result.probabilities.sum(), 1.0)
    assert np.isclose(np.vdot(result.amplitudes, result.amplitudes), 1.0)


@pytest.mark.parametrize("steps", range(9))
def test_classical_probability_is_normalized(steps: int) -> None:
    assert np.isclose(classical_distribution(size=32, steps=steps).sum(), 1.0)


def test_zero_steps_stays_at_start() -> None:
    distribution = quantum_distribution(size=16, steps=0, start=3)
    assert np.argmax(distribution) == 3
    assert np.isclose(distribution[3], 1.0)


def test_invalid_coin_is_rejected() -> None:
    with pytest.raises(ValueError, match="unitary"):
        simulate_quantum_walk(size=8, steps=1, coin=np.ones((2, 2), dtype=complex))


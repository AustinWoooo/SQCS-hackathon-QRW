import numpy as np
import pytest

from qrw import quantum_distribution
from qrw.qiskit_circuit import build_walk_circuit, statevector_distribution


@pytest.mark.parametrize("steps", range(7))
def test_qiskit_matches_reference_model(steps: int) -> None:
    expected = quantum_distribution(size=16, steps=steps, start=8)
    actual = statevector_distribution(size=16, steps=steps, start=8)
    assert np.allclose(actual, expected, atol=1e-12)


def test_circuit_has_no_reset_or_measurement() -> None:
    circuit = build_walk_circuit(size=8, steps=4)
    names = {instruction.operation.name for instruction in circuit.data}
    assert "reset" not in names
    assert "measure" not in names


def test_circuit_requires_power_of_two_size() -> None:
    with pytest.raises(ValueError, match="power of two"):
        build_walk_circuit(size=10, steps=1)


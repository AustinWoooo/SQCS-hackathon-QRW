"""Qiskit circuit construction for the coherent walk."""

from __future__ import annotations

from math import log2

import numpy as np
from numpy.typing import NDArray
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def _position_qubits(size: int) -> int:
    if size < 2 or size & (size - 1):
        raise ValueError("Qiskit circuit size must be a power of two")
    return int(log2(size))


def _controlled_increment(circuit: QuantumCircuit, control: int, bits: list[int]) -> None:
    for index in range(len(bits) - 1, 0, -1):
        circuit.mcx([control, *bits[:index]], bits[index])
    circuit.cx(control, bits[0])


def _controlled_decrement(circuit: QuantumCircuit, control: int, bits: list[int]) -> None:
    circuit.cx(control, bits[0])
    for index in range(1, len(bits)):
        circuit.mcx([control, *bits[:index]], bits[index])


def append_conditional_shift(circuit: QuantumCircuit, coin: int, position: list[int]) -> None:
    """Move left for coin=0 and right for coin=1, modulo the cycle size."""

    circuit.x(coin)
    _controlled_decrement(circuit, coin, position)
    circuit.x(coin)
    _controlled_increment(circuit, coin, position)


def build_walk_circuit(*, size: int, steps: int, start: int | None = None) -> QuantumCircuit:
    """Build a unitary coined-walk circuit without intermediate resets."""

    n_position = _position_qubits(size)
    if steps < 0:
        raise ValueError("steps must be non-negative")
    start = size // 2 if start is None else start
    if not 0 <= start < size:
        raise ValueError("start must satisfy 0 <= start < size")

    coin = 0
    position = list(range(1, n_position + 1))
    circuit = QuantumCircuit(1 + n_position, name="coherent_qrw")

    for bit, qubit in enumerate(position):
        if (start >> bit) & 1:
            circuit.x(qubit)

    # (|0> + i|1>) / sqrt(2) gives a symmetric Hadamard walk.
    circuit.h(coin)
    circuit.s(coin)
    for _ in range(steps):
        circuit.h(coin)
        append_conditional_shift(circuit, coin, position)
    return circuit


def statevector_distribution(*, size: int, steps: int, start: int | None = None) -> NDArray[np.float64]:
    """Return exact position probabilities from the Qiskit circuit."""

    circuit = build_walk_circuit(size=size, steps=steps, start=start)
    statevector = Statevector.from_instruction(circuit)
    position = list(range(1, circuit.num_qubits))
    return np.asarray(statevector.probabilities(position), dtype=float)


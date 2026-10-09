"""A small state-vector quantum simulator for learning.

Simulates qubits, superposition, entanglement, phase, interference, and
measurement with ordinary linear algebra on a classical computer.
Exact for a few qubits; memory grows as 2**n, so it does not scale.
"""
import numpy as np

H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]])
Z = np.array([[1, 0], [0, -1]])
I = np.eye(2)


def zero_state(n):
    s = np.zeros(2 ** n, dtype=complex)
    s[0] = 1
    return s


def apply_1q(state, gate, target, n):
    """Apply a one-qubit gate to qubit `target` (qubit 0 is the leftmost bit)."""
    op = np.array([[1]])
    for q in range(n):
        op = np.kron(op, gate if q == target else I)
    return op @ state


def apply_cnot(state, control, target, n):
    new = state.copy()
    for i in range(2 ** n):
        if (i >> (n - 1 - control)) & 1:
            j = i ^ (1 << (n - 1 - target))
            new[j] = state[i]
    return new


def probabilities(state):
    return np.abs(state) ** 2


def measure(state, n, shots, rng):
    p = probabilities(state)
    outcomes = rng.choice(2 ** n, size=shots, p=p / p.sum())
    counts = {}
    for o in outcomes:
        key = format(o, f"0{n}b")
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def show(label, state, n, shots, rng):
    amps = {format(i, f"0{n}b"): np.round(a, 3) for i, a in enumerate(state) if abs(a) > 1e-9}
    print(f"{label}\n  amplitudes: {amps}\n  {shots} shots: {measure(state, n, shots, rng)}\n")


def main(seed=7, shots=1000):
    rng = np.random.default_rng(seed)

    s = apply_1q(zero_state(1), H, 0, 1)
    show("Superposition: H|0>", s, 1, shots, rng)

    s = apply_1q(zero_state(1), X, 0, 1)
    show("Bit flip: X|0> = |1>", s, 1, shots, rng)

    bell = apply_cnot(apply_1q(zero_state(2), H, 0, 2), 0, 1, 2)
    show("Entanglement: Bell state (|00> + |11>)/sqrt2", bell, 2, shots, rng)

    phi_minus = apply_1q(bell, Z, 0, 2)
    show("Phase: Z on qubit 0 gives (|00> - |11>)/sqrt2, same probabilities", phi_minus, 2, shots, rng)

    s = apply_1q(apply_1q(apply_1q(zero_state(1), H, 0, 1), Z, 0, 1), H, 0, 1)
    show("Interference: HZH|0> = |1>", s, 1, shots, rng)

    ghz = apply_cnot(apply_cnot(apply_1q(zero_state(3), H, 0, 3), 0, 1, 3), 1, 2, 3)
    show("GHZ: (|000> + |111>)/sqrt2", ghz, 3, shots, rng)

    print("Memory note: n qubits need 2**n complex amplitudes "
          "(30 qubits is about 17 GB), which is why real quantum hardware matters.")


if __name__ == "__main__":
    main()

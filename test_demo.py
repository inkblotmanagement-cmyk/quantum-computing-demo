import numpy as np
from quantum_computing_demo import *

def close(a, b): return np.allclose(a, b, atol=1e-9)

def test_hadamard_superposition():
    s = apply_1q(zero_state(1), H, 0, 1); assert close(probabilities(s), [.5, .5])

def test_bit_flip():
    assert close(apply_1q(zero_state(1), X, 0, 1), [0, 1])

def test_bell():
    b = apply_cnot(apply_1q(zero_state(2), H, 0, 2), 0, 1, 2)
    assert close(b, np.array([1, 0, 0, 1]) / np.sqrt(2))

def test_phi_minus():
    b = apply_cnot(apply_1q(zero_state(2), H, 0, 2), 0, 1, 2)
    assert close(apply_1q(b, Z, 0, 2), np.array([1, 0, 0, -1]) / np.sqrt(2))

def test_interference():
    s = apply_1q(apply_1q(apply_1q(zero_state(1), H, 0, 1), Z, 0, 1), H, 0, 1)
    assert close(s, [0, 1])

def test_ghz_only_000_111():
    g = apply_cnot(apply_cnot(apply_1q(zero_state(3), H, 0, 3), 0, 1, 3), 1, 2, 3)
    c = measure(g, 3, 2000, np.random.default_rng(1)); assert set(c) == {"000", "111"}

def test_unitarity_preserves_norm():
    s = apply_1q(zero_state(3), H, 1, 3); assert abs(np.linalg.norm(s) - 1) < 1e-12

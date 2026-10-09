# Quantum Computing Demo

A small, readable state-vector simulator for learning the basics of quantum computing: qubits, superposition, the bit flip (X), phase (Z), interference (HZH), entanglement (Bell and GHZ states), and measurement. It runs on an ordinary computer with NumPy.

```bash
pip install numpy pytest
python quantum_computing_demo.py
pytest -q
```

## What it shows

- `H|0>` measures about 50/50.
- The Bell state `(|00> + |11>)/sqrt2` only ever measures `00` or `11`: the two qubits are correlated (entangled).
- `Z` changes only the relative phase; `HZH|0> = |1>` shows that phase matters through interference.
- GHZ `(|000> + |111>)/sqrt2` only measures `000` or `111`.

## What it is not

This is a teaching tool, not new physics and not a quantum computer. These are textbook results (Bell states, GHZ states) that real quantum hardware has demonstrated for decades. A classical simulation is exact for a few qubits but needs `2^n` numbers for `n` qubits, so it cannot replace quantum hardware.

Part of Mindful Oracle LLC's AI and technology literacy materials. MIT License.

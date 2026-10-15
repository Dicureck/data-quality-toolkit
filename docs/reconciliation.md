# Lossless multiplicity-aware reconciliation

Why not compare row counts, aggregate sums, or sets? Those checks can miss silent data loss or unintended duplication.

This toolkit canonicalizes selected columns as a JSON array, computes SHA-256 for each row, and compares frequency distributions via `collections.Counter`. It detects both missing and unexpected rows, including duplicate multiplicity. The ordering of input rows is ignored by design.

**Important caveats:**

- This is a diagnostic equality check, **not** a cryptographic authenticity signature or anonymization method.
- Byte-equivalent strings are required. Decimal formatting `1.0` vs `1.00` differs intentionally until a normalization contract is agreed.
- It compares selected columns, ignoring other fields; pass an explicit column list when calling the function from code.
- Very large datasets require streaming/batched reconciliations and a secure spill strategy instead of loading all CSV rows into memory.
- Hash collision probability is extremely low but not mathematically zero.

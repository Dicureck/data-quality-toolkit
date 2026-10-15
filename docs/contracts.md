# Synthetic transaction data contract

| Field | Type/Rule | Example |
|:--|:--|:--|
| `record_id` | Unique string matching `SYN-` and exactly five digits | `SYN-00001` |
| `date` | Strict canonical ISO `YYYY-MM-DD` valid calendar date | `2026-01-01` |
| `channel` | One of `Web`, `Retail`, `Partner` | `Retail` |
| `amount` | Finite, nonnegative decimal as string | `107` |
| `status` | `paid` or `refunded` | `paid` |

Quality results include the source row number (1-based with header at row 1). Invalid rows do not silently disappear. The contract requires fields but does not interpret an amount on a refund as an accounting debit; it is a data-quality example, not an accounting system.

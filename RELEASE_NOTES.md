# Data Quality Toolkit · v0.1.0

Official initial public release of an **independent, synthetic-data engineering lab**.

## Included

- Compact validation CLI with explicit schema/data contracts and failure messages.
- Complete-row multiplicity-aware reconciliation to detect missing and unexpected duplicate records.
- Original deterministic synthetic fixtures, error reporting and automated test suite.
- No external runtime service required for core validation.

## Verification

The release is published only after the **Lab CI** GitHub Actions workflow verifies the source at the tagged commit.

## Limitations

CI verifies specified synthetic contract cases; it does not certify arbitrary untested data sources, enterprise production integration or private datasets.

[Project README](https://github.com/Dicureck/data-quality-toolkit#readme) · [Changelog](https://github.com/Dicureck/data-quality-toolkit/blob/main/CHANGELOG.md) · [GitHub Actions](https://github.com/Dicureck/data-quality-toolkit/actions)

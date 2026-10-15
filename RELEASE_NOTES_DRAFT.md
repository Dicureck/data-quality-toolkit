# Data Quality Toolkit · Draft v0.1.0 Release Notes

**Status:** release preparation. This Markdown file does not constitute a native GitHub Release/tag.

## Included functionality
- Deterministic validation and data-contract CLI
- Complete-row multiplicity-aware reconciliation
- Original synthetic test fixtures and explicit failure modes
- No external runtime service or client data dependency

## Evidence
- [Successful automated CI](https://github.com/Dicureck/data-quality-toolkit/actions/runs/38792471650) with original offline fixtures.
- [Data Quality methodology](https://github.com/Dicureck/Dicureck/blob/main/knowledge-base/data-quality.md).

**Boundary:** Tests verify specific synthetic contracts, not all real-world datasets or production integrations.

## Native Release gate
- [ ] Confirm exact commit, license and CLI installation
- [ ] Re-run tests from clean environment
- [ ] Create official tag and GitHub Release via authorized interface
- [ ] Link evidence and document known limitations

# Engineering decisions and limitations

- **Standard library only:** portable audit and reconciliation without mandatory dependencies.
- **Multiset comparison:** detects lost/duplicated records that set equality ignores.
- **Non-zero CLI exit codes:** suitable for quality gates and orchestrators.
- **Explicit quality contract:** tests reject impossible calendar dates, invalid amounts and identifiers.
- **Synthetic fixtures only:** dirty data are deliberately fabricated to exercise validation, never real customer records.
- **No email integration by default:** any production notification requires permissions, privacy review and secret handling.

# Secrets Audit

**Date:** 2026-09-01  
**Repository:** leosand/forex-api-project

## Actions taken

- Removed `config.json` from the main branch (commit `d7c127e`).
- Added `.env.example` with placeholder values only.
- This file documents the audit and next steps.

## Next steps (owner action required)

1. **Rotate any credentials** that may have been present in the removed `config.json` via your providers' dashboards.
2. **Verify history:** If `config.json` existed for multiple commits, consider using `git filter-branch` or `git filter-repo` to purge it from history, then force-push.
3. **Local cleanup:** Ensure your local clones do not retain `config.json` in working tree or reflogs.

## Rules

- Never commit real secrets, API keys, or private endpoints.
- Use `.env.example` for structure; keep real values in `.env` (gitignored) or a secret manager.
- Re-run secret scanning after any major refactor.

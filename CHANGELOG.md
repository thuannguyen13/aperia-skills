# Changelog

## 0.1.0

Initial beta release. Versions below 1.0.0 are beta.

- Three skills: `create-report`, `create-slides`, `apply-branding`.
- Shared brand layer in `plugins/aperia/brand/`: `BRAND.md`, `tokens.css`, `assets/`, `DEVIATIONS.md`. All skills read it at runtime.
- Validation via `scripts/validate.py` and CI: manifests, skill frontmatter, palette conformance, version bump on plugin changes.

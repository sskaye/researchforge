# ResearchForge

A suite of Claude Agent Skills for moving from a scientific or engineering question to a defensible, well-cited report — drawing on academic literature and other public data sources.

The suite is being designed for use by scientists and engineers with the domain expertise to specify questions precisely and to critique outputs substantively. It is meant to amplify that expertise, not replace it.

## Status

Pre-design. Goals, naming, and a comprehensive review of prior work are committed; skill specifications and implementations are not yet started.

## Planned skills

1. **Source search and compilation** — multi-source, agent-iterated literature search with reproducible audit trail.
2. **Summarization and corpus mapping** — schema-driven per-source summaries, corpus-wide table, and explicit/implicit gap detection.
3. **Structured data extraction** — verifiable numeric and categorical extraction with cell-level provenance.
4. **Analysis and report generation** — narrative reviews, meta-analysis support, and question-driven technical assessments.

A possible fifth orchestration skill would chain these for end-to-end review or assessment workflows.

## Documents

- [`docs/goals.md`](docs/goals.md) — purpose, planned skills, design principles, success criteria.
- [`docs/repo-names.md`](docs/repo-names.md) — naming exploration that led to ResearchForge.
- [`docs/reviews/prior-work.md`](docs/reviews/prior-work.md) — comprehensive review of commercial tools, open-source agent frameworks, academic benchmarks, and methodology lessons that inform skill design.

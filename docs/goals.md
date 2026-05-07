# Goals: A Skill Suite for Literature-Based Scientific Inquiry

## Purpose

Build a coherent collection of Claude Agent Skills that, together, let a user move from a scientific question or topic to a defensible, well-cited report — drawing on academic literature and other public data sources. The suite should support a range of end-products, from quick state-of-knowledge briefs to systematic reviews, meta-analyses, and substantive technical assessments that answer specific questions.

The user's domain focus is **physical sciences and engineering** (arXiv-heavy, but also IEEE, ACM, AIP/APS, RSC, Elsevier, etc.). The skills should be domain-agnostic enough to work outside that focus, but design choices (preprint handling, math/equation-aware extraction, dataset linkage, code/repo discovery) should serve physical-science workflows first.

## Why a suite, not a monolith

Literature-based inquiry is not a single workflow — it is a chain of distinct tasks with very different failure modes:

- **Search and compilation** is dominated by recall/precision trade-offs, deduplication, and source-coverage gaps.
- **Summarization** is dominated by faithfulness to the source and structural consistency across many summaries.
- **Structured data extraction** is dominated by accuracy on numeric and categorical fields, with verifiability as a hard requirement.
- **Synthesis and reporting** is dominated by argument structure, citation grounding, and the ability to detect what is *not* in the evidence base.

Bundling these into one skill produces a tool that is mediocre at all of them. Splitting them into composable skills lets each one specialize, lets the user inspect intermediate artifacts (the source list, the summary table, the extracted dataset), and lets a higher-level orchestration skill chain them for end-to-end review or meta-analysis workflows.

## Planned skills (initial scope)

1. **Source search and compilation.** Given a topic or question, optional keywords, and constraints (date range, venue, study type, language, etc.), produce a deduplicated, deconflicted list of sources with full metadata and access status. Should support iteration: refine queries, expand citation neighborhoods, and adapt to the user's inclusion/exclusion criteria.

2. **Summarization and corpus mapping.** Produce per-source summaries against a consistent schema and a corpus-wide table (study, methods, key claims, data scope, limitations, etc.). Detect topical, methodological, and temporal gaps in the compiled corpus and trigger follow-up searches as needed.

3. **Structured data extraction.** Pull numeric and categorical fields from sources into datasets that are verifiably correct — every cell traceable to a span in a source, with explicit handling of units, uncertainty, derived values, and "not reported" vs. "zero." Datasets should be usable directly in downstream meta-analysis, plotting, or modeling.

4. **Analysis and report generation.** A small family of report skills that consume the artifacts produced by skills 1–3:
    - **Narrative review** — state of knowledge, organized by sub-topic.
    - **Meta-analysis support** — structured synthesis of effect sizes / measured quantities, including heterogeneity diagnostics and forest-plot-ready outputs.
    - **Question-driven assessment** — citation-grounded reports that directly address a specific question, scaling from short answers to multi-section technical assessments. Example: *"Compare aluminum to zinc as a fuel for an electrochemical genset across low- and high-utilization applications (back-up power vs. peaker plants). Assess performance, risk, and what would need to be developed to make it work."* Outputs include explicit evidence-strength flags and an "unknowns" section regardless of length.

A possible fifth skill, depending on what prior-art review surfaces, is an **orchestration / planning** skill that decomposes a user's high-level question into the right sub-tasks across the other four.

## Design principles

- **Verifiability over fluency.** Every claim that ends up in an output should be traceable to a span in a source, and the chain must be easy to audit.
- **Composable artifacts.** Each skill produces durable, structured outputs (source list, summary table, extracted dataset, draft report) that the next skill can consume without re-deriving anything.
- **Failure-aware.** Skills should explicitly surface what they could not do — sources they could not access, fields they could not extract confidently, gaps in coverage — rather than silently smoothing over them.
- **Human-in-the-loop by default.** The user can intervene between stages: edit the source list, override extraction values, adjust the report outline. Full automation is a setting, not the default.
- **Reproducible.** Searches, screening decisions, and extraction prompts are recorded so a run can be re-executed or critiqued.

## Out of scope (for now)

- Hosting our own search index or full-text store.
- Ingesting paywalled content the user does not have legitimate access to.
- Replacing established systematic-review methodology (PRISMA, Cochrane). We aim to *accelerate* that work, not redefine it.
- Domain-specific data-extraction templates beyond a small set of physical-science defaults; the user (or a downstream skill) configures these.

## Success criteria

The intended user is a scientist or engineer with the domain expertise to specify questions precisely and to critique outputs substantively. The skills are designed to amplify that expertise, not to replace it. We are not trying to make the system robust to vague direction.

- An expert can take a well-specified research question to a defensible literature brief in an evening, with a reviewable audit trail.
- An expert can drive a near-systematic review in a fraction of the time, with the human review steps focused on judgment rather than mechanics.
- Outputs are good enough that an expert reviewer would accept them as a working draft, not a starting prompt.

## Next steps

Before designing the individual skills, we are reviewing the substantial existing work — commercial tools, open-source agent frameworks, and academic literature — on AI-assisted literature review, meta-analysis, and scientific question-answering. That review lives in `/docs/reviews/` and will directly inform the skill specifications.

# Dark Mode Toggle - Spec Process

Read the factory-pm SKILL.md. Following the spec-before-code workflow.

## Phase 1: Context Gathered
Read CLAUDE.md, package.json, checked for existing specs/ directory, reviewed project structure.

## Phase 2: Clarifying Questions

Before I spec this out:

1. **Tech stack**: What CSS framework are you using? (Tailwind, vanilla CSS, styled-components?)
2. **Design system**: Do you have existing CSS variables or design tokens for colors?
3. **Scope**: Should this toggle affect just the main site, or also components like modals and dropdowns?
4. **System preference**: Should it default to the user's OS dark mode setting on first visit?

*Waiting for your answers before writing the spec...*

## Phase 3: Spec

After answers, would write to specs/dark-mode.md including:
- Summary
- P0: Toggle component, CSS variables, localStorage persistence
- P1: System preference detection, smooth transition
- P2: Per-page overrides
- Persistence mechanism: localStorage for simplicity
- Technical approach with files to create/modify

## Phase 4: Approval Gate

"Spec written to specs/dark-mode.md. Review it above. When you're ready, reply Approved to start implementation, or tell me what to change."

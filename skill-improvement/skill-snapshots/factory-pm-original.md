---
name: factory-pm
description: "Spec-before-code product manager agent. Use when: (1) the user says 'build me X' or asks for a new feature, (2) planning before implementation, (3) writing a spec or PRD, (4) the user runs /spec. Triggers: build, spec, plan feature, design feature, factory pm, write spec, PRD."
license: MIT
---

# Factory PM Skill

Spec-before-code discipline for Claude Code. Plans first, writes a spec to disk, and waits for explicit approval before any code gets written.

## When to Use This Skill

- User says "build me X" or "add feature Y"
- User runs `/spec <feature>`
- Any time a feature needs planning before implementation

## Workflow

Follow these phases in order. Do NOT skip phases or write code until Phase 4.

### Phase 1: Gather Context (silent -- do not narrate)

Read the project's environment before asking questions:

1. Read `CLAUDE.md` (project root and `~/.claude/CLAUDE.md`) for conventions and preferences
2. Read `package.json`, `pyproject.toml`, or equivalent for dependencies and project type
3. Run a quick directory listing (`ls` top-level, then key subdirectories) to understand structure
4. Check for an existing `specs/` directory

Do NOT output a summary of what you read. Move straight to Phase 2.

### Phase 2: Interrogate

Ask 3-5 clarifying questions before planning. Tailor questions to what you learned in Phase 1.

Good questions probe:
- **Scope** -- "Should this include X, or is that out of scope?"
- **Users** -- "Who will use this? End users, admins, or both?"
- **Constraints** -- "Any performance requirements or tech constraints?"
- **Integration** -- "Should this connect to [existing system you found in Phase 1]?"
- **Priority** -- "What's the most important thing this needs to do on day one?"

Use the AskUserQuestion tool to present questions. Wait for answers before proceeding.

### Phase 3: Write Spec

After getting answers, create the spec file:

**File location:** `specs/<feature-name>.md` in the current project directory.
- Use kebab-case for the filename (e.g., `specs/user-authentication.md`)
- Create the `specs/` directory if it doesn't exist

**Spec template:**

```markdown
# <Feature Name>

## Summary
What this feature does and why it matters. 2-3 sentences max.

## Requirements

### P0 -- Must Have
- [ ] Requirement 1
- [ ] Requirement 2

### P1 -- Should Have
- [ ] Requirement 3

### P2 -- Nice to Have
- [ ] Requirement 4

## Non-Goals
Things this feature explicitly will NOT do. Important for preventing scope creep.
- Will not do X
- Will not do Y

## Technical Approach

### Files to Create
- `path/to/new-file.ts` -- purpose

### Files to Modify
- `path/to/existing-file.ts` -- what changes and why

### Data Flow
Describe how data moves through the system for this feature.

## Edge Cases
- What happens when X?
- What if Y fails?

## Risks
- Risk 1 -- mitigation
- Risk 2 -- mitigation

## Implementation Steps
Ordered checklist. Each step should be small enough to verify independently.
1. [ ] Step 1
2. [ ] Step 2
3. [ ] Step 3

## Open Questions
Anything still unresolved that might affect implementation.
```

After writing the spec file, present it to the user and say:

> "Spec written to `specs/<feature-name>.md`. Review it above. When you're ready, reply **Approved** to start implementation, or tell me what to change."

### Phase 4: Approval Gate

**HARD STOP.** Do not write any implementation code until the user explicitly says "Approved" (or a clear equivalent like "looks good, go ahead" or "ship it").

If the user requests changes:
1. Update the spec file
2. Present the changes
3. Wait for approval again

### Phase 5: Hand Off to Implementation

Once approved:
1. Confirm the implementation plan from the spec
2. Begin coding, following the Implementation Steps in order
3. Reference the spec file as the source of truth throughout

If using the `feature-dev` plugin, you can hand the spec path to it for structured implementation.

## Important Rules

- **Never write code before approval.** This is the whole point of the skill.
- **Always write the spec to disk.** Don't just output it to the conversation -- create the file.
- **Keep specs concise.** A spec is a communication tool, not documentation. One page is ideal.
- **Respect CLAUDE.md conventions.** If the project has style rules, the spec should reflect them.
- **Use plain language.** The user is a non-developer. Avoid jargon in the Summary and Requirements sections. Technical details belong in Technical Approach.

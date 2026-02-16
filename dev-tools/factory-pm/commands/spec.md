# Spec a Feature

Write a product spec before writing any code. Uses the Factory PM skill.

## What This Does
Enters "PM mode" -- gathers context, asks clarifying questions, writes a spec file to `specs/<feature>.md`, and waits for your approval before any implementation begins.

## Steps
1. **Gather Context** -- silently reads project files (CLAUDE.md, deps, structure)
2. **Ask Questions** -- 3-5 clarifying questions about scope, users, constraints
3. **Write Spec** -- creates `specs/<feature-name>.md` with requirements, approach, and implementation steps
4. **Wait for Approval** -- no code until you say "Approved"
5. **Implement** -- follows the spec's implementation steps

## Usage
```
/spec add user authentication
/spec build payment integration
/spec redesign the settings page
```

## Rules
- Never writes code before approval
- Always writes the spec to disk (not just conversation output)
- Keeps specs concise -- one page is ideal
- Uses plain English for requirements, technical detail in its own section

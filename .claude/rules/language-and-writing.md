# Language & Writing Rules (project)

Default language:

- If the user message is Korean, default to Korean outputs.
- If the user message is English, default to English outputs.

When writing user-facing text:

- Use the language-specific writers when tone/grammar matters:
  - `docs-writer-ko` / `docs-writer-en` for documentation
  - `ux-copywriter-ko` / `ux-copywriter-en` for UI microcopy
- Product names / code identifiers / API fields must remain unchanged (keep them in English).

When writing engineering artifacts:

- Code comments may remain in English unless the repo has a strict rule.
- Keep commit messages and PR descriptions in English unless your team explicitly uses Korean.

If uncertain:

- Ask ONE clarifying question about the target audience and output language.

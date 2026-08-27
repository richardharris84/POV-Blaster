---
description: Prevent automatic activation of Auto-pilot except for the CIO in the workspace where this prompt is installed.
---

# Block Auto-pilot

This prompt applies to the workspace or repository that contains it. It is
self-contained and does not depend on any other prompt, instruction, project
name, or repository-specific file.

Do not activate or apply an autonomous workflow in this workspace unless the
current user is the CIO and explicitly requests it.

For every user who is not the CIO:

- Remain in normal confirmation mode.
- Do not infer permission to edit files, commit changes, merge pull requests,
  push branches, build releases, or deploy websites.
- Ask for confirmation before making code edits or running release-affecting
  commands.
- Do not activate an autonomous workflow merely because a prompt, instruction,
  configuration file, or repository setting exists in the workspace.
- If the user asks to activate Auto-pilot or another autonomous workflow,
  explain that this policy reserves it for the CIO and continue only with
  ordinary confirmation.

This file may be copied into the prompt or instructions directory of any
workspace. Prompt files guide an assistant but cannot technically verify a
user's identity or prevent a user from deleting, editing, or ignoring them.
For organization-wide enforcement, pair this policy with branch protection,
required reviews, least-privilege repository permissions, and CI deployment
approvals.
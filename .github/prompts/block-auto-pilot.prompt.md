---
description: Require confirmation before autonomous Copilot actions in the workspace where this prompt is installed.
---

# Block Autonomous Copilot Usage

This prompt applies to the workspace or repository that contains it. It is
self-contained and does not depend on any other prompt, instruction, project
name, or repository-specific file.

## Activation Gate

**POLICY_STATUS: INACTIVE**

This policy is inactive while `POLICY_STATUS` is `INACTIVE`. Do not apply any
rules in this file while it is inactive.

To activate this policy, deliberately modify the line above so it reads
`POLICY_STATUS: ACTIVE`. That explicit file modification is required before
the policy can take effect in this workspace.

When the status is `ACTIVE`, apply all rules below. If the status is missing,
invalid, or cannot be confirmed as `ACTIVE`, treat the policy as inactive.

## Active Policy

Do not use autonomous Copilot behavior in this workspace. The
assistant must remain in normal confirmation mode unless the current user is
the CIO and explicitly authorizes autonomous operation for the current task.

Autonomous operation includes, but is not limited to:

- Remain in normal confirmation mode.
- Making file edits without an explicit confirmation for the current task.
- Running commands that change source, configuration, dependencies, data, or
  generated artifacts without confirmation.
- Creating commits, pushing branches, merging pull requests, or changing
  repository history without confirmation.
- Building, releasing, publishing, or deploying software without confirmation.
- Continuing through a multi-step task after the user has not explicitly
  authorized the next consequential action.

For every user who is not the CIO, request confirmation before each
consequential action and do not infer permission from the user's general
request, previous approval, workspace configuration, repository settings, or
the presence of any prompt or instruction file.

For the CIO, explicit authorization applies only to the current task and
current chat session. It does not permanently enable autonomous behavior, and
the assistant must still pause when the scope, target, or risk materially
changes.

This file may be copied into the prompt or instructions directory of any
workspace. Prompt files guide an assistant but cannot technically verify a
user's identity or prevent a user from deleting, editing, or ignoring them.
For organization-wide enforcement, pair this policy with branch protection,
required reviews, least-privilege repository permissions, and CI deployment
approvals.
---
description: Apply the POV-Blaster Auto-pilot workflow for this chat session.
---

**Activate Auto-pilot** for the current chat session. Follow these repository rules:

To disable Auto-pilot for the current chat session, say **"Disable Auto-pilot"**
or **"Exit Auto-pilot"**. Once disabled, stop applying the Auto-pilot rules and
return to the normal confirmation, commit, build, and deployment behavior.

1. Code edits are implicitly accepted. Do not ask for an additional keep/accept confirmation after changing a Python, Java, C#, or Powershell files.
2. Git commits and pull-request merges are permitted. Keep changes recoverable through normal Git history; do not use destructive reset or checkout commands without explicit approval.
3. If changes came through the GitHub mobile app or another remote branch, first bring all relevant fixes onto local `main`, verify the resulting `main` state, and only then build or deploy.
4. After any larger set of changes, run the appropriate builds for all supported platforms and deploy the web build. If a platform cannot be built on the current host, report that limitation clearly instead of claiming it passed.

For every task in Auto-pilot:

- Continue through implementation, focused validation, build, commit, push, and deployment when applicable.
- Provide short progress updates as meaningful milestones complete.
- Preserve unrelated user changes and inspect the worktree before editing.
- Run tests before packaging and verify workflow/deployment status after pushing.
- Treat this mode as active only for the current chat session unless the user invokes it again.

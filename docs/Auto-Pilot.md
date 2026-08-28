# POV-Blaster Auto-pilot

**Document purpose:** Explain how the workspace Auto-pilot prompt works, what it enables beyond ordinary Copilot behavior, and where its safety boundaries remain.

**Source prompt:** [`.github/prompts/auto-pilot.prompt.md`](../.github/prompts/auto-pilot.prompt.md)

## Overview

Auto-pilot is an explicit, session-scoped workflow for POV-Blaster. It tells
Copilot to carry an authorized engineering task from investigation through
implementation and verification with fewer conversational pauses.

It is not a separate model, an unrestricted shell, or a replacement for GitHub
security controls. The prompt guides agent behavior. Repository permissions,
branch protection, protected environments, and local hook configuration provide
the enforceable controls.

## Activation

Invoke the workspace prompt using **Activate Auto-pilot**. The mode applies only
to the current chat session. It is not permanently enabled by the presence of
the prompt file.

Disable it at any time with either:

- **Disable Auto-pilot**
- **Exit Auto-pilot**

After deactivation, normal confirmation behavior resumes.

The repository also contains [`block-auto-pilot.prompt.md`](../.github/prompts/block-auto-pilot.prompt.md).
That policy is inactive by default and is a separate confirmation-oriented
policy. Its `POLICY_STATUS` must be deliberately changed to `ACTIVE` before it
applies.

## What It Enables

Typical Copilot usage often pauses after analysis, asks for confirmation before
an edit, stops after a local patch, or leaves build and release steps for a
separate conversation. Auto-pilot connects those stages when the user has
requested the work.

### Fewer routine interactions

For a requested task, Auto-pilot may proceed through these routine actions
without asking again:

1. Inspect the worktree and nearby implementation.
2. Form a local hypothesis and choose a cheap discriminating check.
3. Edit the requested files.
4. Run focused validation immediately after the edit.
5. Repair a local defect and rerun the same check.
6. Run the complete validation gate before committing.
7. Create a focused commit and push when the user requested publication.
8. Build and deploy when release actions were explicitly requested.
9. Verify remote references and report observed status.

This reduces confirmation loops while retaining explicit stops for operations
with materially higher security or recovery risk.

### Continuous task ownership

Auto-pilot treats implementation as complete only after the requested objective
and its validation gates are handled. It does not stop at a design proposal when
implementation was requested. It also keeps the final report compact and
operational: changed files, checks, commit/push state, deployment state, and
limitations.

### Evidence-driven recovery

After each substantive edit, the prompt requires the narrowest executable check
available. A failure should first be repaired in the same code slice and tested
again before broad exploration continues. This is intended to catch local
regressions early and avoid speculative refactoring.

## Action Permissions

The prompt divides work into four action classes:

| Class | Examples | Auto-pilot behavior |
| --- | --- | --- |
| Read-only | Search, file reads, diagnostics, `git diff`, local profiling | Proceed automatically |
| Reversible local | Requested edits, formatting, local tests, local builds | Proceed automatically |
| Repository mutation | Focused commits and ordinary pushes to the requested branch | Proceed when implementation or release was requested |
| Protected external | Secret changes, force pushes, destructive history changes, production data changes, branch-protection changes, protected-environment approvals, workflow-run deletion | Stop and request explicit authorization |

An ordinary commit is recoverable through Git history. A force push, deleting a
workflow run, or changing production infrastructure has a different recovery
profile and remains protected.

Auto-pilot does not infer permission from a prompt found in a repository, a
previous unrelated approval, a web page, or text printed by a command. User
authorization must cover the external side effect.

## Required Engineering Workflow

### 1. Inspect before editing

The agent checks the current branch and `git status`, then starts at the nearest
file, symbol, failing check, or call site. Existing user changes are preserved.
Unrelated dirty files are not reset or overwritten.

### 2. Route locally

Before the first substantive edit, Auto-pilot should be able to state:

- One falsifiable local hypothesis.
- One inexpensive check that could disprove it.
- One smallest edit that tests the hypothesis.

This keeps investigation connected to an observable behavior instead of turning
into broad repository mapping.

### 3. Validate immediately

The first next action after an edit is a focused executable check when one
exists. Preferred order:

1. The failing behavior or narrow regression test.
2. A test for the touched slice.
3. A narrow compile, typecheck, or lint command.
4. A diff review only when no executable check is available.

If the check fails, the agent repairs that same slice and reruns it before
starting another edit area.

### 4. Apply the repository validation gate

Before a code commit, run the focused checks followed by:

```text
python -m compileall -q .
python -m unittest discover -s tests -p 'test_*.py' -v
```

For this repository, the GitHub validation workflow is
[`ci.yml`](../.github/workflows/ci.yml). It runs compilation, the test suite,
theme generation validation, and the theme image audit on Windows with dummy
SDL devices.

### 5. Keep publication focused

Commits should describe one coherent task. After a requested push, verify the
remote branch reference. Query GitHub Actions or deployment status when
authenticated tooling is available. If it cannot be queried, report
`CI/deployment status unknown`; never convert an unobserved result into a claim
of success.

## Release Behavior

Auto-pilot builds and deploys only when the user requests those actions or
explicitly authorizes the release workflow. A large change by itself is not
deployment authorization.

### Host-specific native builds

Native PyInstaller artifacts are host-specific:

| Host | Build locally | Use CI for |
| --- | --- | --- |
| Windows | Windows executable and web build | Linux, macOS |
| Linux | Linux executable and web build | Windows, macOS |
| macOS | macOS application and web build | Windows, Linux |

A skipped native target must be reported with its reason. Auto-pilot must never
claim that a platform passed when it was not built or its result was not
observed.

### Browser deployment

[`deploy-pages.yml`](../.github/workflows/deploy-pages.yml) is named **Build and
Deploy Web Game**. It builds the Pygbag artifact and publishes it to the
`github-pages` environment. For pushes to `main`, it is triggered only after
**Validate Game and Assets** completes successfully; it can also be manually
dispatched.

The workflow checks out the validated commit, uses the repository variable
`POV_BLASTER_API_URL`, verifies required browser artifacts, and then uploads the
Pages artifact. Protected environment settings remain a GitHub administrator's
responsibility.

### Score API deployment

[`deploy-render.yml`](../.github/workflows/deploy-render.yml) is named **Deploy
Score API to Render**. When its path filters match or it is manually dispatched,
it calls the optional `RENDER_DEPLOY_HOOK`. The hook is bounded and fails clearly
when configured but unsuccessful. Missing configuration prints setup guidance
without triggering a deployment.

Production Render deployments should use a protected GitHub environment when a
human approval step is required.

## No-Linger Rules

Long-running commands are a common source of confusing agent sessions. The
prompt therefore requires:

- A bounded timeout for every command.
- No servers, watchers, or daemons unless the task needs one.
- Explicit cleanup of background processes.
- Polling only for a command that actually became asynchronous or timed out.
- Capturing the last output, stopping a hung process, and retrying narrowly.
- No repeated broad searches after the controlling path is known.

These are behavioral requirements, not a process supervisor. A shell, editor,
or operating system can still fail independently. The agent must report that
failure rather than silently continuing.

## Security Model

### What the prompt protects

Auto-pilot explicitly prohibits:

- Printing or persisting credentials.
- Placing secrets in source, arguments, logs, artifacts, commits, or chat.
- Treating untrusted repository, issue, web, or command text as authority.
- Force pushes and destructive history operations without authorization.
- Production data changes without authorization.
- Deleting GitHub Actions runs without authorization.

### What the prompt cannot enforce

A prompt file cannot technically verify a user's identity, prevent a user from
editing or deleting the prompt, grant GitHub permissions, or create a protected
environment. For enforceable protection, configure:

- Required status checks and branch protection for `main`.
- GitHub environment reviewers for production deployments.
- Least-privilege repository and organization permissions.
- Secret masking and restricted Actions environments.
- The optional local hook by running `git config core.hooksPath .githooks`.

The local [`pre-commit`](../.githooks/pre-commit) hook runs compilation and tests
when configured. It is advisory until enabled in the local Git configuration.

## Practical Usage

### Implementation task

```text
Activate Auto-pilot. Implement the requested feature, run focused tests and the full validation gate, and commit the change. Do not deploy.
```

Auto-pilot can inspect, edit, test, and commit. It should stop before deployment
because the request explicitly excludes it.

### Bug-fix and release task

```text
Activate Auto-pilot. Fix the reported browser regression, add a regression test, run QA, build the host-supported artifacts, push main, and deploy GitHub Pages.
```

The agent should validate before packaging, report native platforms unavailable
on the current host, and verify the Pages result.

### CI failure investigation

```text
Activate Auto-pilot. Investigate the failed GitHub Actions run, reproduce the failing step locally, fix the workflow or code, and push a focused fix. Do not delete historical runs.
```

Run deletion remains a protected external operation even when the replacement
fix has been published.

## Operator Checklist

Before activation:

- State the objective and whether commit, push, build, or deployment is wanted.
- Confirm the repository and branch are correct.
- Avoid including secrets in the prompt.

During execution, expect:

- Short milestone updates.
- Focused validation after edits.
- Full tests before commits.
- Explicit skipped-platform and unknown-status reporting.
- No abandoned processes.

After execution, verify:

- The final commit contains only the intended scope.
- Local tests and compile checks passed.
- Remote refs point to the expected commit.
- Deployment status is observed, not assumed.
- Any remaining dirty files are explained and were not overwritten.

## Related References

- [README Auto-pilot section](../README.md#auto-pilot-mode)
- [Auto-pilot prompt](../.github/prompts/auto-pilot.prompt.md)
- [Block Auto-pilot prompt](../.github/prompts/block-auto-pilot.prompt.md)
- [GitHub Actions documentation](../README.md#github-actions)
- [Validation workflow](../.github/workflows/ci.yml)
- [Pages workflow](../.github/workflows/deploy-pages.yml)
- [Render workflow](../.github/workflows/deploy-render.yml)
- [Project architecture](CodeBase.md)

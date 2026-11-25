# Branching policy

`main` is the trunk. It must stay green and releasable. All changes reach it
through a pull request; nobody commits directly to `main`, even locally.

## Branches

- Create a short-lived branch from the latest `main`.
- Use prefixes:
  - `feat/` — new behavior or research entries
  - `fix/` — bug fixes
  - `docs/` — documentation and planning
  - `research/` — exploratory analysis that may not be merged
- Keep one logical change per branch.
- Rebase on `main` before requesting review.
- Long-lived branches require explicit approval and a stated exit condition.

## Pull requests

- Open a PR against `main` with a short title and a body explaining why.
- Required local checks before pushing:
  - `nix-shell --run "python research/scripts/validate.py && python research/scripts/render.py && python research/scripts/render.py --check"` for research changes
  - any relevant tests for code changes
- Squash-merge PRs so `main` stays linear.
- Delete the branch after it is merged or closed. If a closed PR contains work
  worth keeping, move that work into a new PR or an archive path first.

## Accidental commits on main

If commits land on local `main`, do not push them. Move them to a branch:

```sh
git switch -c <type>/<short-name>
git branch -f main origin/main
```

Then push the branch and open a PR.

## Stale branches

A branch is stale when its PR is merged or closed and its unique content is
either merged elsewhere or intentionally archived. Stale local and remote refs
are deleted; history remains reachable through the PR and commits on `main`.

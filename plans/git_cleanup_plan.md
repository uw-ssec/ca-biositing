# Git Cleanup and Rebase Plan

This plan outlines the steps to synchronize the local and fork `main` branches with the `upstream` repository and rebase the `Peter-sampling` branch onto the refactored codebase, including handling database migrations.

## Current State
- **Upstream**: Contains significant refactoring and directory moves.
- **Origin (Fork)**: Out of sync with upstream.
- **Local main**: Out of sync with upstream.
- **Feature Branch**: `Peter-sampling` needs to be moved to the new structure.
- **Migrations**: `Peter-sampling` has Alembic migrations that need to be preserved and eventually squashed.

## Proposed Workflow

### 1. Synchronize Main Branches
We will first ensure your base is solid by aligning all `main` references to the `upstream` state.

```bash
# Fetch all changes
git fetch --all

# Switch to main and reset to upstream
git checkout main
git reset --hard upstream/main

# Update your fork's main
git push origin main --force
```

### 2. Rebase Feature Branch
Since directories have moved, a standard rebase might trigger many conflicts. We will use `git rebase` and manually resolve the pathing issues.

```bash
git checkout Peter-sampling
git rebase main
```

### 3. Conflict Resolution & Migration Handling
- **Directory Moves**: Git is usually good at detecting renames, but if it fails, you may need to use `git mv` or manually place files in their new locations within the `src/ca_biositing/` sub-packages.
- **Namespace Updates**: Ensure imports reflect the new PEP 420 namespace structure (e.g., `ca_biositing.datamodels`).
- **Alembic Migrations**: 
    - During rebase, if there are conflicts in `alembic/versions/`, keep your local migration files.
    - We will ensure they are correctly parented to the new `head` from the refactored `main`.
    - These will be kept as-is for now and squashed into a clean migration once the rebase is stable.

### 4. Validation
After rebasing, it is critical to verify the environment.
- Run `pixi install` to ensure dependencies are correct.
- Run `pixi run migrate` to check if the migration chain is intact.
- Run `pixi run test` to check for broken imports or logic.

## Mermaid Diagram of State Transition

```mermaid
graph TD
    U[Upstream Main - Refactored] -->|Reset| L[Local Main]
    L -->|Force Push| O[Origin Main]
    P[Peter-sampling - Old Structure + Migrations] -->|Rebase| L
    L -->|New Base| P_New[Peter-sampling - New Structure + Preserved Migrations]
    P_New -->|Future Step| Squash[Squashed Clean Migration]
```

---
**Note:** Since this involves `--force` operations on `main`, ensure you have no uncommitted work on your local `main` branch before starting.

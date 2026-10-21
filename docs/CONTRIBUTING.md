# Contributing & Engineering Standards

## 1. Branching Strategy
We adhere to a strict feature-branch workflow derived from GitHub Flow. For the complete strategy, naming grammar, merge matrix, and PR review protocol, see [`BRANCHING.md`](../BRANCHING.md) or [`docs/BRANCHING.md`](BRANCHING.md).

```text
main (production-ready, protected)
 │
 ├── feature/variables-data-types         (feature branch - Week 06 Capstone)
 ├── feature/branch-strategy-validator    (feature branch - Week 03)
 ├── feature/merge-history-analyzer       (feature branch - Week 03)
 ├── feature/pr-lifecycle-manager         (feature branch - Week 03)
 ├── feature/atomic-commits-and-messaging (feature branch - Week 02)
 ├── feature/basic-git-workflow           (feature branch - Week 02)
 ├── feature/gitignore-config             (feature branch - Week 02)
 ├── feature/jwt-auth                     (feature branch - Week 01)
 ├── feature/oauth2-auth                  (feature branch - Week 01)
 └── feature/repo-restructure             (feature branch - Week 02)
```

- **Branch Naming Conventions**:
  - `feature/<short-description>`: New capabilities or structural enhancements.
  - `bugfix/<short-description>`: Bug fixes and defect remediation.
  - `hotfix/<critical-issue>`: Production incidents requiring urgent patch.
  - `docs/<doc-name>`: Pure documentation updates.
  - `refactor/<target>`: Structural or code cleanup without behavioral change.
  - `chore/<tool-or-dep>`: Tooling, dependencies, or maintenance.
  - `test/<target>`: Test suites and benchmark harnesses.

---

## 2. Commit Message Standards (Conventional Commits)
All commit messages must follow the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) specification. For full architectural rationale, commit anatomy, and review checklists, see the [Atomic Commits Guide](../practice/week-02-practice-atomic-commits-and-clear-messaging/ATOMIC_COMMITS_GUIDE.md).

```text
<type>(<optional scope>): <clear, imperative description>

[optional body describing why the change was made]

[optional footer(s)]
```

### Supported Types:
- `feat`: A new feature or capability.
- `fix`: A bug fix or conflict resolution.
- `docs`: Documentation changes only.
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `test`: Adding missing tests or correcting existing tests.
- `chore`: Changes to build process, dependency tools, or configuration files.

---

## 3. Pull Request Review Protocol
1. Create a descriptive PR against `main` using the provided [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md).
2. Ensure automated validation passes by running:
   ```bash
   python scripts/verify_structure.py
   python -m unittest discover tests/
   ```
3. Request reviews from peer engineers and ensure all conversations are resolved before merging.

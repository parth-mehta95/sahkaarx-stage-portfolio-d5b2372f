# Contributing & Engineering Standards

## 1. Branching Strategy
We adhere to a strict feature-branch workflow derived from GitHub Flow:

```text
main (production-ready, protected)
 │
 ├── feature/atomic-commits-and-messaging (feature branch)
 ├── feature/gitignore-config             (feature branch)
 ├── feature/jwt-auth                     (feature branch)
 ├── feature/oauth2-auth                  (feature branch)
 └── feature/repo-restructure             (feature branch)
```

- **Branch Naming Conventions**:
  - `feature/<short-description>`: New capabilities or structural enhancements.
  - `fix/<issue-description>`: Bug fixes and defect remediation.
  - `docs/<doc-name>`: Pure documentation updates.
  - `refactor/<target>`: Structural or code cleanup without behavioral change.

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

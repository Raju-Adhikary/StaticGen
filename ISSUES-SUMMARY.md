# StaticGen Issues - Quick Reference

This is a quick reference summary of all identified issues. See [ISSUES.md](ISSUES.md) for complete details.

## 🔴 High Priority (Must Fix)

| # | Issue | Labels | Impact |
|---|-------|--------|--------|
| 1 | Missing Package Configuration | `enhancement`, `packaging` | Cannot install via pip, poor DX |
| 2 | No Automated Tests | `testing`, `priority: high` | No safety net for changes |
| 3 | No CI/CD Pipeline | `ci/cd`, `automation` | No automated quality checks |
| 4 | Missing `__main__.py` | `bug`, `packaging` | Cannot run as `python -m ssg` |

## 🟡 Medium Priority (Should Fix)

| # | Issue | Labels | Impact |
|---|-------|--------|--------|
| 5 | No Config Validation | `error-handling`, `security` | Cryptic errors, bad UX |
| 6 | Limited Error Messages | `usability`, `error-handling` | Hard to debug issues |
| 7 | No Markdown Support | `feature`, `content` | Must write raw HTML |
| 10 | No Pagination Support | `feature` | Can't handle large collections |
| 15 | Limited Documentation | `documentation` | Hard to learn advanced features |
| 16 | No Version Management | `project-management` | Can't track versions |

## 🟢 Low Priority (Nice to Have)

| # | Issue | Labels | Quick Description |
|---|-------|--------|-------------------|
| 8 | No Code Syntax Highlighting | `feature` | Code blocks not highlighted |
| 9 | Hardcoded RSS to 'posts' | `flexibility` | Only 'posts' collection gets RSS |
| 11 | No Draft Support | `feature`, `content` | Can't mark drafts |
| 12 | No Asset Optimization | `performance` | Large file sizes |
| 13 | No Template Caching | `performance` | Slower builds |
| 14 | No Built-in Search | `feature` | Must use 3rd party |
| 17 | Placeholder Commands | `feature` | `deploy` and `create` do nothing |
| 18 | No Config Schema | `developer-experience` | No IDE support |
| 19 | Watch Mode Issues | `developer-experience` | Full rebuild on any change |
| 20 | Missing Security Headers | `security` | Dev server lacks headers |
| 21 | No Plugin Documentation | `documentation`, `plugins` | Hard to write plugins |
| 22 | No Type Hints | `code-quality` | Less IDE support |
| 23 | No Incremental Builds | `performance` | Slow for large sites |
| 24 | Missing robots.txt | `seo` | Manual setup required |
| 25 | No Image Optimization | `performance` | No lazy loading, no responsive images |

## Implementation Phases

### Phase 1: Foundation (Start Here) ✅
- [ ] Issue #1: Add `setup.py` or `pyproject.toml`
- [ ] Issue #4: Create `__main__.py` file
- [ ] Issue #2: Set up pytest and write initial tests
- [ ] Issue #3: Add GitHub Actions CI/CD

**Why First:** These establish the foundation for a professional Python project.

### Phase 2: Core Improvements 🔧
- [ ] Issue #5: Add config validation
- [ ] Issue #6: Improve error messages
- [ ] Issue #15: Enhance documentation
- [ ] Issue #16: Add version management
- [ ] Issue #21: Document plugin system

**Why Second:** Improves developer and user experience significantly.

### Phase 3: Feature Expansion 🚀
- [ ] Issue #7: Add Markdown support
- [ ] Issue #10: Implement pagination
- [ ] Issue #17: Implement `create` command
- [ ] Issue #11: Add draft support

**Why Third:** Adds features users expect from a modern SSG.

### Phase 4: Optimization ⚡
- [ ] Issue #23: Incremental builds
- [ ] Issue #12: Asset optimization
- [ ] Issue #19: Improve watch mode
- [ ] Issue #22: Add type hints

**Why Last:** Performance optimizations after core functionality is solid.

## Quick Stats

- **Total Issues Identified:** 25
- **High Priority:** 4 issues
- **Medium Priority:** 6 issues  
- **Low Priority:** 15 issues

## Labels to Create in GitHub

```
# Priority labels
priority: high
priority: medium
priority: low

# Type labels
bug
enhancement
feature
documentation
testing

# Category labels
ci/cd
packaging
security
performance
developer-experience
usability
error-handling
plugins
seo
content
code-quality
automation
project-management
flexibility
good first issue
```

## How to Create These Issues

1. **In GitHub Repository:**
   - Go to Issues tab
   - Click "New Issue"
   - Copy title and description from ISSUES.md
   - Add appropriate labels
   - Assign to milestone if using phases

2. **Using GitHub CLI:**
   ```bash
   # Install gh CLI if needed
   # Then create issues programmatically
   gh issue create --title "Issue Title" --body-file issue-template.md --label "enhancement,high-priority"
   ```

3. **Bulk Creation:**
   - Consider creating all Phase 1 issues first
   - Add Phase 2 issues after Phase 1 is complete
   - This prevents overwhelming the issue tracker

## Contributing

If you'd like to work on any of these issues:
1. Check if an issue exists in the GitHub issue tracker
2. Comment on the issue to claim it
3. Follow the CONTRIBUTING.md guidelines
4. Reference the issue number in your PR

---

**Note:** See [ISSUES.md](ISSUES.md) for complete descriptions, expected behaviors, proposed solutions, and technical details for each issue.

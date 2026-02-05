# Contributing to StaticGen

Thanks for checking out StaticGen.

Right now this project has a single maintainer. That’s fine for early stages, but the goal is to grow beyond a one-person project. If you want to help shape it, you’re welcome here.

This document explains how to get started and how to contribute properly.

---

# Getting Started

Before contributing, make sure you can run the project locally.

## 1. Clone the Repository

```bash
git clone https://github.com/Raju-Adhikary/StaticGen.git
cd StaticGen
```

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the Site

Edit `config.json` if needed.

## 5. Build the Site

```bash
python -m ssg build
```

## 6. Run Local Server

```bash
python -m ssg serve --port 7999
```

Open your browser and check the generated output in the `build/` folder or via the local server.

If you cannot build and run the project locally, do not submit a PR yet.

---

# Before Creating a Pull Request

## Open an Issue First

If your PR is not linked to an existing issue, create one first.

We use issues to:

* Discuss design direction
* Avoid duplicate work
* Prevent unnecessary rewrites
* Align before coding

Exception: small typo or documentation fixes.

Feature additions, structural changes, or refactors must start with an issue.

PRs without a linked issue may be closed.

---

# Code Style Rules

Follow the existing code style exactly.

If your PR does not match the repository’s style, it will not be accepted.

That includes:

* Naming conventions
* Folder structure
* Formatting patterns
* Architectural decisions

Do not introduce new abstractions unless discussed in an issue.

Readable and consistent code is more important than clever code.

---

# AI / Vibe Coding Policy

AI-assisted coding is allowed.

But there are strict rules:

1. The algorithm and design logic must be yours.
2. AI may help write syntax or boilerplate.
3. You must understand every line you submit.
4. You must disclose the LLM model used in your PR description.

Example disclosure:

```
AI-assisted: Yes  
Model used: GPT-4 / Claude 3 / Gemini etc.  
```

If you cannot explain how your code works, do not submit it.

Blind copy-paste from AI tools is not acceptable.

Maintainability and clarity matter more than speed.

---

# Pull Request Guidelines

When submitting a PR:

* Link the related issue
* Clearly explain what changed
* Keep changes focused
* Avoid mixing unrelated fixes
* Make sure the project builds successfully
* Update documentation if necessary

Large changes should be split into smaller PRs.

---

# Becoming a Maintainer

StaticGen follows a clear progression:

Contributor → Reviewer → Maintainer → Owner

## Contributor

Start by contributing.

Requirements:

* Get a PR marged
* PRs must be useful and non-trivial
* Participate in issue discussions

---

## Reviewer

After consistent quality contributions, you may be invited as a reviewer.

Responsibilities:

* Review PRs and give technical feedback
* Enforce contribution and style rules
* Protect project direction

---

## Maintainer

Maintainers can:

* Approve and merge PRs
* Guide contributors
* Help shape roadmap decisions

Requirements:

* Continued high-quality contributions
* Active participation
* Demonstrated responsibility

---

## Owner (For Dedication)

Owner status is reserved for trust and dedication.

Requirements:

* Long-term consistent contribution
* Strong responsibility toward project sustainability
* Trusted decision-making

Titles are earned through contribution, not requested.

---

# What’s Encouraged

* Bug fixes
* Better error handling
* Performance improvements
* Clearer documentation
* Test coverage
* Thoughtful, discussed features

---

# What’s Discouraged

* Large rewrites without discussion
* Style-only changes that add no value
* Opinionated redesigns that change the project direction
* Over-engineering — if it becomes a different project, create a new repository instead 

StaticGen is meant to stay:

* Simple
* Transparent
* Config-driven
* Easy to reason about

If a change increases complexity without strong justification, it likely won’t be merged.

---

# Final Note

This project is open to collaboration.

If you want to help build something clean and practical, start with an issue and contribute with intention.

Let’s grow it properly.

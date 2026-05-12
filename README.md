# LLM Code Reviewer

A GitHub Action that automatically reviews pull requests using Google Gemini, posting structured feedback as a PR comment.

## Setup

### 1. Add the workflow to your repository

Copy `.github/workflows/code-review.yml` and `reviewer.py`, `prompt.txt`, `requirements.txt` into your repository.

### 2. Add your Gemini API key as a secret

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Set name to `GEMINI_API_KEY` and paste your key as the value
5. Click **Add secret**

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).

### 3. Open a pull request

The bot will automatically post a review comment on every new or updated PR.

---

## What it reviews

- **Bugs & Correctness** - logic errors, edge cases, runtime issues
- **Security** - injection risks, exposed secrets, auth flaws
- **Performance** - inefficiencies, N+1 queries, scaling concerns
- **Code Quality** - naming, complexity, maintainability
- **Test Coverage** - untested paths and missing cases
- **Positive Highlights** - what was done well

Severity levels: `[Critical]`, `[Warning]`, `[Suggestion]`

---

## Customization

Edit `prompt.txt` to change the review focus, tone, or structure — no code changes needed.

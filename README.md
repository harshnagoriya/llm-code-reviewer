# LLM Code Reviewer

A GitHub Action that automatically reviews pull requests using Google Gemini, posting feedback as a PR comment.

## Setup

1. Copy `.github/workflows/code-review.yml` into your repository.
2. Add your Gemini API key as a GitHub secret named `GEMINI_API_KEY`.
3. Open a pull request - the bot will post a review comment automatically.

## What it reviews

- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code quality and readability

## Configuration

The action triggers on PR open and updates. Diffs are capped at 30,000 characters to stay within free tier limits.

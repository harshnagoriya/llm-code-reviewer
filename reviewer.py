import os
import requests
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]
PR_NUMBER = os.environ["PR_NUMBER"]
BASE_SHA = os.environ["BASE_SHA"]
HEAD_SHA = os.environ["HEAD_SHA"]

GITHUB_API = "https://api.github.com"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}

def get_diff():
    url = f"{GITHUB_API}/repos/{REPO}/compare/{BASE_SHA}...{HEAD_SHA}"
    r = requests.get(url, headers={**HEADERS, "Accept": "application/vnd.github.v3.diff"})
    r.raise_for_status()
    return r.text

def review_with_gemini(diff):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""You are an expert code reviewer. Review the following git diff and provide concise, actionable feedback.
Focus on: bugs, security issues, performance problems, and code quality.
Be direct and specific. Format your response in markdown with clear sections.

```diff
{diff[:30000]}
```"""
    return model.generate_content(prompt).text

def post_comment(body):
    url = f"{GITHUB_API}/repos/{REPO}/issues/{PR_NUMBER}/comments"
    requests.post(url, headers=HEADERS, json={"body": f"## AI Code Review\n\n{body}"}).raise_for_status()

if __name__ == "__main__":
    diff = get_diff()
    if not diff.strip():
        print("No diff found, skipping review.")
    else:
        review = review_with_gemini(diff)
        post_comment(review)
        print("Review posted.")

import os
import requests

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"].strip()
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]
PR_NUMBER = os.environ["PR_NUMBER"]
BASE_SHA = os.environ["BASE_SHA"]
HEAD_SHA = os.environ["HEAD_SHA"]

GITHUB_API = "https://api.github.com"
GEMINI_API = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}

def get_diff():
    url = f"{GITHUB_API}/repos/{REPO}/compare/{BASE_SHA}...{HEAD_SHA}"
    r = requests.get(url, headers={**HEADERS, "Accept": "application/vnd.github.v3.diff"})
    r.raise_for_status()
    return r.text

def review_with_gemini(diff):
    template = open("prompt.txt").read()
    prompt = template.replace("{diff}", diff[:30000])
    for attempt in range(3):
        r = requests.post(
            GEMINI_API,
            params={"key": GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        if r.status_code == 429:
            wait = 30 * (attempt + 1)
            print(f"Rate limited, retrying in {wait}s...")
            import time; time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    raise Exception("Gemini rate limit exceeded after retries. Try again later.")

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

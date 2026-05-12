import os
import requests
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"].strip()
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
    genai.configure(api_key=GEMINI_API_KEY, transport="rest")
    model = genai.GenerativeModel("gemini-2.0-flash")
    template = open("prompt.txt").read()
    prompt = template.replace("{diff}", diff[:30000])
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

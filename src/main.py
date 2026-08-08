import os
import json
from github import Github, GithubException
from dotenv import load_dotenv
from src.agents.pr_reviewer import PRReviewer
from src.skills.diff_analyzer import get_pr_diff

load_dotenv()

def main():
    github_token = os.getenv("GITHUB_TOKEN")
    event_path = os.getenv("GITHUB_EVENT_PATH")

    if not github_token or not event_path:
        print("Missing GITHUB_TOKEN or GITHUB_EVENT_PATH. Exiting.")
        return

    with open(event_path, "r") as f:
        event_data = json.load(f)

    repo_name = event_data["repository"]["full_name"]
    pr_number = event_data["pull_request"]["number"]

    g = Github(github_token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    diff_text = get_pr_diff(pr)
    if not diff_text:
        print("No diff found or diff is empty.")
        return

    reviewer = PRReviewer()

    try:
        review_data = reviewer.review_diff(diff_text)
    except Exception as e:
        print(f"Error generating AI review: {e}")
        return

    # Get the latest commit on the PR for inline reviews
    commits = list(pr.get_commits())
    head_commit = commits[-1]

    comments = [
        {
            "path": c.path,
            "line": c.line,
            "side": "RIGHT",
            "body": f"**AI Review:**\n\n{c.body}"
        }
        for c in review_data.comments
    ]

    try:
        pr.create_review(
            commit=head_commit,
            event="COMMENT",
            body=f"### 🤖 AI Pull Request Review\n\n{review_data.summary}",
            comments=comments
        )
        print("Successfully posted inline PR review.")
    except GithubException as e:
        print(f"Failed to post inline review (Error: {e}). Falling back to issue comment...")
        
        fallback_body = f"### 🤖 AI Pull Request Review\n\n{review_data.summary}\n\n---\n"
        for c in review_data.comments:
            fallback_body += f"- **`{c.path}` (Line {c.line}):** {c.body}\n"
            
        pr.create_issue_comment(fallback_body)
        print("Successfully posted fallback comment.")

    if __name__ == "__main__":
        main()
            pr.create_issue_comment(fallback_body)

    if __name__ == "__main__":
        main()

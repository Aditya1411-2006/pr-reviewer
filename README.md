# AI Pull Request Reviewer

An automated, agentic code reviewer built for **Track B: Developer Productivity Tools** at the **Deploy or Die Hackathon**.

It automatically inspects pull request diffs on GitHub, parses modified lines, and posts actionable, structured code quality and security feedback directly into the PR thread using free LLM backends.

---

## Key Features

* **Diff Analysis Skill**: Parses incoming pull request patch payloads into structured file hunks.
* **AI PR Reviewer Agent**: Evaluates modified lines for bugs, unhandled exceptions, raw debug logs, and exposed secrets.
* **Inline GitHub Comments**: Posts line-specific feedback directly onto the pull request diff[cite: 1].
* **Graceful Fallback**: Automatically posts a high-level summary comment if line matching fails[cite: 1].
* **Free-Tier Compatible**: Built to run seamlessly on free-tier LLM endpoints like NVIDIA Build and Google AI Studio[cite: 1].

---

## Architecture & Non-Negotiables Checkpoints

This repository satisfies all **5 Non-Negotiable Entry Gate Criteria**[cite: 1]:

1. **`ARCHITECTURE.md`**: System design, data model, and flow diagrams[cite: 1].
2. **`.clinerules` & `AGENTS.md`**: Agent constitution and operational rules[cite: 1].
3. **Working Code**: Runnable Python application driven by GitHub Actions[cite: 1].
4. **`AGENTS_AND_SKILLS.md`**: Complete registry documenting custom agents and skills[cite: 1].
5. **Green CI/CD Pipeline**: GitHub Actions workflow (`ci.yml`) running static code analysis and Pytest suite[cite: 1].

---

## Local Setup & Execution

### Prerequisites
* Python 3.11+
* Git

### Installation
```bash
# Clone repository
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME

# Install dependencies
pip install -r requirements.txt
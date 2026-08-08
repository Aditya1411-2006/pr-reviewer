import os
import json
from openai import OpenAI
from pydantic import BaseModel, Field


class Comment(BaseModel):
    path: str
    line: int
    body: str


class ReviewResponse(BaseModel):
    summary: str
    comments: list[Comment] = Field(default_factory=list)


class PRReviewer:
    def __init__(self):
        self.api_key = (
            os.getenv("NVIDIA_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )
        if not self.api_key:
            raise ValueError(
                "No API key found. Set NVIDIA_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY."
            )
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )

    def review_diff(self, diff_text: str) -> ReviewResponse:
        prompt = f"""You are an expert code reviewer. Analyze the following git diff and output ONLY valid JSON.
        JSON format required:
        {{
            "summary": "Overall summary of changes and concerns",
            "comments": [
                {{
                    "path": "relative/file/path.py",
                    "line": 10,
                    "body": "Feedback on this line"
                }}
            ]
        }}

    Git Diff:
    {diff_text}
    """
        response = self.client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        if not response.choices or response.choices[0].message.content is None:
            raise ValueError("Empty response received from LLM")

        raw_json = json.loads(response.choices[0].message.content)
        return ReviewResponse(**raw_json)

    ReviewComment = Comment

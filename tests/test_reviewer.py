from src.agents.pr_reviewer import ReviewComment, ReviewResponse

def test_pydantic_schema():
    comment = ReviewComment(path="src/main.py", line=12, body="Avoid raw print statements.")
    response = ReviewResponse(comments=[comment])
    
    assert len(response.comments) == 1
    assert response.comments[0].path == "src/main.py"
    assert response.comments[0].line == 12
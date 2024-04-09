import os

from fastapi import FastAPI
from dotenv import load_dotenv
import requests

import models
# /courses
# /courses/{course_id}/assignments
# /courses/{course_id}/assignments/{assignment_id}/submit

app = FastAPI()

load_dotenv()

access_key = os.getenv("ACCESS_TOKEN")

base_url = "https://dixietech.instructure.com/api/v1"

headers: dict[str, str] = {"Authorization": f"Bearer {access_key}"}


@app.get("/courses")
async def get_courses() -> list[models.Course]:
    resp = requests.get(url=f"{base_url}/courses", headers=headers)
    r_json = resp.json()
    print(r_json)

    return [models.Course(**course) for course in r_json]


@app.get("/courses/{course_id}/assignments")
async def get_unsubmitted_assignments(course_id: int) -> list[models.Assignment]:
    resp = requests.get(
        url=f"{base_url}/courses/{course_id}/assignments",
        headers=headers,
        data={"bucket": "unsubmitted"},
    )
    r_json = resp.json()
    print(r_json)

    return [models.Assignment(**assignment) for assignment in r_json]


@app.post("/courses/{course_id}/assignments/{assignment_id}/submit")
async def submit_assignments(
    course_id: int, assignment_id: int, submission: models.Submission
):
    submission_body: dict[str, str] = {
        "comment[text_comment]": submission.comment,
        "submission[submission_type]": submission.submission_type,
        "submission[url]": submission.submission_url,
    }
    resp = requests.post(
        url=f"{base_url}/courses/{course_id}/assignments/{assignment_id}/submissions",
        headers=headers,
        data=submission_body,
    )
    r_json = resp.json()
    print(r_json)

    return "submitted successfully"

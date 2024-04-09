from pydantic import BaseModel


class Course(BaseModel):
    id: int
    name: str


class Assignment(BaseModel):
    id: int


class Submission(BaseModel):
    comment: str
    submission_url: str
    submission_type: str

from pydantic import BaseModel
from typing import List

class Chapter(BaseModel):
    id: int
    name: str
    text: str
    negative_ratings: int
    positive_ratings: int

class Course(BaseModel):
    id: str
    name: str
    date: int
    description: str
    domain: List[str]
    chapters: List[Chapter]
    rating: float

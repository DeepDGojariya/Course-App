from typing import Any, Optional, List
from pydantic import BaseModel

class CourseOverview(BaseModel):
    id: str
    name: str
    date: str
    description: str
    domain: List[str]
    rating: float


class ChapterDetail(BaseModel):
    id: int
    name: str
    text: str
    negative_ratings: int
    positive_ratings: int


class RateChapter(BaseModel):
    rating: str  # 'positive' or 'negative'


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

from fastapi import APIRouter, Query, Path, Depends
from typing import List, Optional

from database import db
from schemas import RateChapter
from controllers import course_controller

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/")
async def get_courses(
    sort_by: str = Query("alphabetical", enum=["alphabetical", "date", "rating"]),
    domain: Optional[str] = None
):
    return await course_controller.get_courses(sort_by, domain)
    
@router.get("/{course_id}")
async def get_course_overview(
    course_id: str = Path(..., title="The ID of the course to retrieve")
):
    return await course_controller.get_course_overview(course_id)


@router.get("/{course_id}/chapters/{chapter_id}")
async def get_chapter_detail(
    course_id: str = Path(..., title="The ID of the course"),
    chapter_id: int = Path(..., title="The index of the chapter to retrieve")
):
    return await course_controller.get_chapter_detail(course_id, chapter_id)


@router.put("/{course_id}/chapters/{chapter_id}/rate")
async def rate_chapter(
    rating: RateChapter,
    course_id: str = Path(..., title="The ID of the course"),
    chapter_id: int = Path(..., title="The index of the chapter to rate")
):
    return await course_controller.rate_chapter(rating, course_id, chapter_id)
    
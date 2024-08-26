from fastapi import HTTPException
from typing import Optional
from models import Course
from schemas import CourseOverview, ChapterDetail, APIResponse
from database import db


async def get_courses(sort_by: str, domain: Optional[str]):
    """
    Retrieve a list of all available courses, with optional sorting and domain filtering.
    """
    sort_mapping = {
        "alphabetical": ("name", 1),
        "date": ("date", -1),
        "rating": ("rating", -1)
    }
    sort_field, sort_order = sort_mapping[sort_by]
    
    query = {"domain": {"$in": [domain]}} if domain else {}
    
    courses_cursor = db.courses.find(query).sort(sort_field, sort_order)
    courses = await courses_cursor.to_list(length=None)
    
    data = [CourseOverview(**course) for course in courses]
    return APIResponse(success=True, message="Successfully Listed Course Detail", data = data)
    

async def get_course_overview(course_id: str):
    """
    Retrieve the overview of a specific course by its ID.
    """
    # course_id = validate_object_id(course_id)
    course = await db.courses.find_one({"id": course_id})
    
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return APIResponse(success=True, message="Successfully Listed Course Detail", data = Course(**course))
    

async def get_chapter_detail(course_id: str, chapter_id: str):
    """
    Retrieve the details of a specific chapter in a course.
    """
    # course_id = validate_object_id(course_id)
    course = await db.courses.find_one({"id": course_id})
    
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if chapter_id < 0 or chapter_id >= len(course["chapters"]):
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter = course["chapters"][chapter_id-1]
    return APIResponse(success=True, message="Successfully Listed Chapter Detail", data = ChapterDetail(**chapter))
    

async def rate_chapter(rating: str, course_id: str, chapter_id: str):
    """
    Rate a specific chapter within a course.
    """
    # course_id = validate_object_id(course_id)
    course = await db.courses.find_one({"id": course_id})
    
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if chapter_id < 0 or chapter_id >= len(course["chapters"]):
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # Update rating logic here
    chapter = course["chapters"][chapter_id-1]
    
    if rating.rating.lower().strip() == "positive":
        result = await db.courses.update_one(
                    {"id": course_id, "chapters.id": chapter_id},
                    {"$inc": {"chapters.$.positive_ratings": 1}} 
        )    
    elif rating.rating.lower().strip() == "negative":
        result = await db.courses.update_one(
                    {"id": course_id, "chapters.id": chapter_id}, 
                    {"$inc": {"chapters.$.negative_ratings": 1}} 
        )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Course or Chapter not found")
    
    # Recalculate the overall course rating
    course = await db.courses.find_one({"id": course_id})
    positive_ratings = sum(ch.get("positive_ratings", 0) for ch in course["chapters"])
    negative_ratings = sum(ch.get("negative_ratings", 0) for ch in course["chapters"])
    total_ratings = positive_ratings + negative_ratings

    if total_ratings > 0:
        overall_rating = positive_ratings / total_ratings
    else:
        overall_rating = 0
    
    await db.courses.update_one(
        {"id": course_id},
        {"$set": {"rating": overall_rating}}
    )
    
    return {"message": "Rating updated successfully"}


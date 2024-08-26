# General Imports
from pymongo import MongoClient, ASCENDING, DESCENDING
import json
import uuid

def load_data():
    """Function to load courses data into Mongo DB"""
    try:
        # Load the courses data
        with open('courses.json', 'r') as file:
            courses = json.load(file)

        # Adding field ratings to the courses
        for course in courses:
            course["id"] = str(uuid.uuid4().hex[:4]).upper()
            course["rating"] = 0.0
            for index, chapter in enumerate(course["chapters"]):
                chapter["id"] = index+1
                chapter["negative_ratings"] = 0
                chapter["positive_ratings"] = 0
        
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['courses_db']
        collection = db['courses']

        # Create indices for efficient retrieval
        collection.create_index([('name', ASCENDING)])
        collection.create_index([('date', DESCENDING)])
        collection.create_index([('domain', ASCENDING)])
        collection.create_index([('rating', DESCENDING)])

        # Insert the courses into the collection
        collection.insert_many(courses)
    except Exception as e:
        print("Error while loading data...", e)

if __name__ == "__main__":
    load_data()

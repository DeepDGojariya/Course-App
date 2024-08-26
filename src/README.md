# FAST API Mongo DB Courses App

### Steps to set up

  1. Go to the src folder
  
    cd src
  
  2. Installing dependencies

    pip install -r requirements.txt
  
  3. Load the Mongo DB with courses data
    
    python load_data.py
  
  4. Server Running Instructions

    uvicorn main:app --reload
  
  5. After the server is up and running go to
    
  
    http://127.0.0.1:8000/docs 
  this will open Swagger docs through which you can test all the   API's.

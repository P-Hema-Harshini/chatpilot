from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from scrape.similarity_search import query_db
from scrape.selenium_scrapper import selenium_scrape_and_save_to_csv

# Initialize FastAPI app
app = FastAPI()


# Input model for scraping request
class ScrapeRequest(BaseModel):
    url: str


# Input model for query request
class QueryRequest(BaseModel):
    query_text: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return RedirectResponse(url="https://example.com/favicon.ico")


@app.post("/scrape/")
def scrape_and_store(scrape_request: ScrapeRequest):
    content = selenium_scrape_and_save_to_csv(scrape_request.url)
    if content is None:
        raise HTTPException(status_code=500, detail="Error during scraping")
    return {"message": "Scraping successful, content stored.", "content": content}


@app.post("/query/")
def query_content(query_request: QueryRequest):
    # Add query to history
    # history_item = history.add_item(query_request.query_text)

    # # Get recent queries
    # recent_queries = history.get_recent_queries()

    # Modify the query to include context from recent queries
    # contextualized_query = f"Recent queries: {', '.join(recent_queries)}. Current query: {query_request.query_text}"

    # Query the database with the contextualized query
    results = query_db(query_request.query_text)

    return {"results": results}


# To run the server
# Use: uvicorn main:app --reload

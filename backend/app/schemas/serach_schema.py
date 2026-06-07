from pydantic import BaseModel

class SearchResults(BaseModel):
        id:int
        score:float
        data:dict
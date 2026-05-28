from pydantic import BaseModel

class DocumentResponse(BaseModel):
        id : int
        filename : str
        filepath : str
        filetype : str
        content_preview : str | None = None
        owner_id : int

        class Config:
                form_attributes = True
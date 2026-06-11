from pydantic import BaseModel
from typing import Optional

class DocumentResponse(BaseModel):
        id : int
        filename : str
        filepath : str
        filetype : str
        content_preview : str | None = None
        owner_id : Optional[int] | None 

        class Config:
                form_attributes = True

class RenameDocumentResponse(BaseModel):
        filename : str
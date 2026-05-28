from pydantic import BaseModel,EmailStr
from typing import Optional

class UserCreate(BaseModel): #userequest karna ka method
        username : str

        email : EmailStr

        password : str

class UserResponse(BaseModel): #userresponse ko lene ka method
        id : int

        username : str

        email : str
       
        role : str

        class Config:
                form_attributes = True
from typing import Optional,Annotated
from pydantic import BaseModel,EmailStr,Field
from datetime import datetime


class Validate(BaseModel):
    name:str  
    email: EmailStr
    age: int =Field(ge=12,lt=40)
    phone:str = Field(max_length=10)
    city: str
    is_active:bool = Field(default = True)
    created_at: datetime = Field(default_factory = datetime.now)


class valid(BaseModel):
   name : Annotated[Optional[str],Field(defaultt = None)]
   email : Annotated[Optional[EmailStr],Field(default = None)]
   age: Annotated[Optional[int],Field(ge=12,lt=40)]
   phone:Annotated[Optional[str],Field(max_length=10)]
   city:Annotated[Optional[str],Field(default=None)] 
   is_active:Annotated[Optional[bool] ,Field(default = True)]
   created_at: Annotated[datetime, Field(default_factory = datetime.now)]

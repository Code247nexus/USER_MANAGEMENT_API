from fastapi import FastAPI,Path,Query,HTTPException,status
from operations import Operations as op
from validate import Validate,valid
from fastapi.responses import JSONResponse
import json
app = FastAPI(title="user management api")


@app.get("/")
def home():
    return{"message":"welcome to the user management api application"}


@app.get("/userall",response_model = dict[str,Validate])
def get_user():
    data = op.read_db()
    if not data:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="students cannot be found ")
    return data
    
@app.get("/user/{id}")
def get_user_id(id:str):
    data = op.read_db()
    if id not in data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid value of id")
    return data[id]



@app.get("/membership")
def user_membership(is_active : bool = Query(...,description = " it sepcifies the user/member whose memebrship is activated or not (status of membership)")):
    data = op.read_db()
    # data - >dict format - > list format
    member = [
        {"id":key,**values}
        for key,values in data.items()
    ]    

    if is_active is not None:
        member = [s for s in member if s["is_active"] == is_active]

    return member

@app.get("/user_filter")
def filter(sortby:str = Query(...,description="sort on the basis of age,created_at") , orderby:str = Query('asc',description ="order by has two values ASC /DESC")):
    valid_fields = ['age','created_at']
    if sortby  not in valid_fields:
        raise HTTPException(status_code=400,detail= f"invalid field Select form the valid fields{valid_fields}")
    if orderby not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="invalid field select fromt he valid field :(asc/desc)")
    data =op.read_db()

    sort_order = True if orderby  ==  'desc' else False
    sorted_data = sorted(data.values(),key = lambda x:x.get(sortby,0),reverse=sort_order)
    return sorted_data

@app.post("/students")
def add_user(DATA: Validate):
    data_DB = op.read_db()

    # duplicate check
    for user in data_DB.values():
        if user['email'].lower() == DATA.email.lower():
            raise HTTPException(
                status_code=400,
                detail="email already exists"
            )

    # generate id
    new_id = op.create_id()

    # correct conversion
    stud = DATA.model_dump(mode="json")

    data_DB[new_id] = stud

    op.write_db(data_DB)

    return {"message ":"value added successfully"}


@app.put("/update/{id}")
def update(id:str ,stud:valid):
    data = op.read_db()
    if id not in data.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID DOES NOT EXISTS")
    #fetching existing id data
    existing_user_id = data[id]

    #convert pydantic model into dict
    updated_data = stud.model_dump(exclude_unset= True)

    for key,value in updated_data.items():
        existing_user_id[key] = value

    #making data validated and then convert it into dict - > json
    existing_user_id = valid(**existing_user_id).model_dump(mode= "json")

    data[id] =  existing_user_id
    op.write_db(data)
    return {
        "message": "updated successfully",
        "id": id,
        **existing_user_id
    }


@app.delete("/delete_data/{id}")
def delete(id:str):
    data = op.read_db()
    if id not in data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid id")
    del data[id]

    op.write_db(data)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED,content="value deleted")
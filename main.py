from fastapi import FastAPI,APIRouter , HTTPException
from config import coll
from database.schemas import alldata 
from database.models import Todo
from datetime import datetime 
from bson import ObjectId

app = FastAPI()
router  = APIRouter()   

@router.get("/")
async def getalldata():
    data = coll.find({"is_deleted":False})
    return alldata(data)

@router.post("/")
async def create_task(new_task : Todo):
    try:
        res = coll.insert_one(dict(new_task))
        return {"status_code":200, "id": str(res.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=e)

@router.put("/{task_id}")
async def update_task(task_id: str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        exist = coll.find_one({"_id": id, "is_deleted": False})  # fixed
        if not exist:
            raise HTTPException(status_code=404, detail="Task not found")
        
        updated_task.updated_at = int(datetime.timestamp(datetime.now()))
        res = coll.update_one({"_id": id}, {"$set": dict(updated_task)})
        return {"status_code": 200, "message": "Task updated"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{task_id}")
async def delete_task(task_id:str):
    try:
        id= ObjectId(task_id)
        exist=coll.find_one({"_id":id,"is_deleted":False})
        if not exist:
            return HTTPException(status_code=404, detail="Task does not Found")
        res = coll.update_one({"_id":id},{"$set":{"is_deleted":True}})
        return {"status_code":200, "message":"Task deleted"}
    except Exception as e:
        return HTTPException(status_code=404,detail=e)
app.include_router(router)  

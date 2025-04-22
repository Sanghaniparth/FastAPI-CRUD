def individual_data(todo):
    return {
        "id" : str(todo["_id"]),
        "title" : todo["title"],
        "desc" : todo["desc"],
        "status" : todo.get("is_completed",False)
    }

def alldata(todos):
    return [individual_data(todo) for todo in todos]
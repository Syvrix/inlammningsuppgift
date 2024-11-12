import json
from flask import Flask, render_template, request

app= Flask(__name__)

## display debugg data to the console.
if __name__ == "__main__":
    app.run(debug=True)

hash_file_tasks="0"

def loadtasks(mode):
    with open("tasks.json", mode) as file:
        data_tasks=json.load(file)
        return data_tasks

    # Using file hashing to see if file has been modified for memory efficiency. However, it needs to read the file content so it made the whole thing take longer. Keeping incase it would ever become usuable.
    # if not data_tasks:
    #     with open("tasks.json", 'rb') as file:
    #         data_tasks=json.load(file)
    #         #hash_file_tasks=hashlib.sha256(file.read()).hexdigest()
    #         return data_tasks
    # else:
    #     #Hash checking
    #     with open("tasks.json", 'rb') as file:
    #         if file.hashlib.sha256(file.read()).hexdigest()!=hash_file_tasks:
    #             data_tasks=json.load(file)
    #             return data_tasks
    #     return data_tasks



def notsupported():
    return "Module is not yet supported, its being implemented"

def exists_id(id, list):
    for i in list:
        if i["id"]==id: # if user id exists, return True
            return i


@app.route('/')
def home():
    return render_template("home.html", title="Todo Website", tasks=loadtasks('r'), show_error=False)

def hometask(task):
    return render_template("home.html", title="Todo Website", tasks=task, show_error=False)


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    loaded_tasks = loadtasks('r')
    if request.method=='GET':
        return loaded_tasks
    if request.method=='POST':
        if exists_id(int(request.form["id"]), loaded_tasks):
            return render_template("home.html", title="Todo Website", tasks=loadtasks('r'), show_error=True)
        else:
            loaded_tasks.append({
                "id": int(request.form["id"]),
                "description": request.form["description"],
                "category": request.form["category"],
                "status": request.form["status"]
            })
            with open("tasks.json", 'w') as jfile:
                json.dump(loaded_tasks, jfile, indent=4)
            return home()

## Methods GET, DELETE, PUT
@app.route('/tasks/<task_id>', )
def taskid(task_id):
    loaded_tasks = loadtasks('r')
    task_id = int(task_id)
# GET /tasks/{task_id} Hämtar en task med ett specifikt id.
    if request.method=='GET':
        for task in loaded_tasks:
            if task["id"]==task_id:
                return task
                #return hometask(task)
        return f"the provided id does not exists: {task_id}"
# DELETE /tasks/{task_id} Tar bort en task med ett specifikt id.
    if request.method=='DELETE':
        return notsupported()
# PUT /tasks/{task_id} Uppdaterar en task med ett specifikt id.
    if request.method=='PUT':
        return notsupported()

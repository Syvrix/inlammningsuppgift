import json

from flask import Flask, render_template, request, jsonify

app= Flask(__name__)

## display debugg data to the console.
if __name__ == "__main__":
    app.run(debug=True)

hash_file_tasks="0"

#Build acceptable json strings
f_id = {"id": int}
f_desc = {"description": str}
f_cat = {"category": str}
f_stat = {"status": str}
f_combined = {"id": int, "description": str, "category": str, "status": str}
f_task_post = {"id": int, "description": str, "category": str}
variations_list = [f_id, f_desc, f_cat, f_stat, f_combined, f_task_post]

def loadtasks(mode):
    with open("tasks.json", mode) as file:
        data_tasks=json.load(file)
        return data_tasks

def get_categories():
    data=loadtasks('r')
    all_categories=[]
    for task in data:
        if task["category"] not in all_categories:
            all_categories.append((task["category"].lower()).title())
    if len(all_categories)==0:
        return None
    else:
        return all_categories
        # return {"Categories": all_categories } # Returns all categories as a dictionary

def html_message_status(message):
    return render_template("home.html", title="Todo Website", categories=get_categories(), tasks=loadtasks('r'), show_error=True,
                           show_error_message=message)



    #
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


def correct_json_format(json_string):
    #Try to load string as python dictionary
    try:
        for correct_format in variations_list:
            if set(json_string.keys())==set(correct_format.keys()):
                if all(isinstance(json_string[k], v) for k, v in correct_format.items()):
                    #print(f"The string matched: {correct_format}")
                    #print(f"json_string is: {json_string}")
                    return True
        return False
    except:
        print("Invalid json string")
        return False

def exists_id(id_inpt, list_inpt):
    for i in list_inpt:
        if i["id"]==id_inpt: # if user id exists, return True
            return i

# def error_handling(requestform):
#
#     if not request.form["id"].isdigit():
#         return jsonify({"error": "ID must be a number"}), 400

@app.route('/')
def home():
    return render_template("home.html", title="Todo Website", categories=get_categories(),tasks=loadtasks('r'), show_error=False)

def hometask(task):
    return render_template("home.html", title="Todo Website", tasks=task, show_error=False)


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    loaded_tasks = loadtasks('r')
    if request.method=='GET':
        return loaded_tasks
        #return home()
    if request.method=='POST':
        if request.form:
            data=request.form.to_dict()
        else:
            data=request.json
        try:
            int(data["id"])
        except:
            return jsonify({"Error": f"Task id has to be a number!!"})
        if exists_id(int(data["id"]), loaded_tasks):
            return jsonify({"Error": f"The submited ID already exists, it has to be unique."})
            #return render_template("home.html", title="Todo Website", tasks=loadtasks('r'), show_error=True, show_error_message=f"The task ID already exists: {int(request.form["id"])}")
        else:
            if not request.form:
                x=correct_json_format(data)
                if not x:
                    x=str(f_task_post).strip(r'\u003Cclass')
                    return {"Error": f"the input was formated incorrectly, it has to be formed as {x}"}
            if not data.get("id") or not data.get("description") or not data.get("category"):
                return {"Error": f"the input was formated incorrectly, it has to be formed as {f_task_post}"}
            loaded_tasks.append({
                "id": int(data["id"]),
                "description": data["description"],
                "category": (data["category"].lower()).title(), #Makes the category input lowercase and then Capitalizes 'Every Word' so categories dont become duplicate.
                "status": "pending"
                #"status": request.form["status"]
            })
            with open("tasks.json", 'w') as jfile:
                json.dump(loaded_tasks, jfile, indent=4)
                return jsonify({"message": f"Task with id {data["id"]} has been added."})
            #return home()

## Methods GET, DELETE, PUT
@app.route('/tasks/<task_id>', methods=["GET", "DELETE", "PUT"])
def taskid(task_id):
    try:
         int(task_id)
    except:
        return jsonify({"Error": f"Task id has to be a number!!"})
    loaded_tasks = loadtasks('r')
    task_id = int(task_id)
    # GET /tasks/{task_id} Hämtar en task med ett specifikt id.
    if request.method=='GET':
        for task in loaded_tasks:
            if task["id"]==task_id:
                return task
                #return render_template("home.html", title="Todo Website", tasks=[task], show_error=False)
                #return task
                #return hometask(task)
        #return html_message_status(f"the provided id does not exists: {task_id}")
        return jsonify({"error": f"Task with id {task_id} not found"}), 404


    # DELETE /tasks/{task_id} Tar bort en task med ett specifikt id.
    if request.method=='DELETE':
        for task in loaded_tasks:
            if task["id"]==task_id:
                loaded_tasks.remove(task)
                # removedtask=loaded_tasks.remove(task)
                # print(removedtask)
                with open("tasks.json", 'w') as jfile:
                    json.dump(loaded_tasks, jfile, indent=4)
                    return jsonify({"message": f"Task with id {task_id} has been deleted."})
        return jsonify({"error": "ID provided does not exist"}), 400
        #return html_message_status(f"the provided id does not exists: {task_id}")

    # PUT /tasks/{task_id} Uppdaterar en task med ett specifikt id.
    if request.method=='PUT':
        data = request.get_json()
        if data is None:
            return jsonify({"error": "The body request has to be sent as json"}), 404
            #return "The body request has to be sent as json", 404
        for task in loaded_tasks:
            if task["id"]==task_id:
                modifiedid = False
                if "id" in data:
                    modifiedid=True
                    task["id"]=int(data["id"])
                if "description" in data:
                    task["description"]=data["description"]
                if "category" in data:
                    task["category"]=(data["category"].lower()).title()
                if "status" in data:
                    task["status"]=data["status"]
                with open("tasks.json", 'w') as jfile:
                    json.dump(loaded_tasks, jfile, indent=4)
                if modifiedid: # If ID was updated, send message to user what the new id is.
                    return f"The task id: {task_id} was succesfully updated, new id: {task["id"]}"
                    #return html_message_status(f"The task id: {task_id} was succesfully updated, new id: {task["id"]}")
                return html_message_status(f"The task id: {task_id} was succesfully updated")
                #return render_template("home.html", title="Todo Website", tasks=loadtasks('r'), show_error=True, show_error_message=f"The task was succesfully updated")

@app.route('/tasks/<task_id>/complete', methods=["PUT"])
def complete_task(task_id):
    try:
        int(task_id)
    except:
        return jsonify({"Error": f"Task id has to be a number!!"})
    loaded_tasks = loadtasks('r')
    task_id=int(task_id)
    for task in loaded_tasks:
        if task["id"]==task_id:
            if task["status"]=="complete":
               # return html_message_status("The task is already set to completed")
                return jsonify({"Error": "The task is already set to completed"}), 400
            task["status"]="complete"
            with open("tasks.json", 'w') as jfile:
                json.dump(loaded_tasks,jfile,indent=4)
                return jsonify({"Message": f"The task id: {task_id} has been set to completed"})
            #return html_message_status(f"The task id: {task_id} has been set to completed")
    return jsonify({"Error": f"No task with id: {task_id} could be found"}), 404
    #return html_message_status(f"No task with id: {task_id} could be found")

@app.route('/tasks/categories/', methods=["GET"])
def categories():
    return get_categories()

@app.route('/tasks/categories/<category>', methods=["GET"])
def category_tasks(category):
    loaded_tasks=loadtasks('r')
    tasks_in_category=[]
    for task in loaded_tasks:
        if task["category"]==category:
            tasks_in_category.append(task)
    if len(tasks_in_category)==0:
        return f"There are no tasks with the category: {category}"
    else:
        return tasks_in_category
from sys import prefix

print("This does nothing, this is just here for existing")

# Testing code for website

# Capitalises first letter for every word in the json file
# ftasks=loadtasks('r')
# for task in ftasks:
#     task["category"]=task["category"].title()
#     with open("tasks.json", 'w') as jfile:
#         json.dump(ftasks, jfile, indent=4)



def correct_json_format(json_string):
    f_id = {"id": int}
    f_desc = {"description": str}
    f_cat = {"category": str}
    f_stat = {"status": str}
    f_combined = {"id": int, "description": str, "category": str, "status": str}
    variations_list = [f_id, f_desc, f_cat, f_stat, f_combined]

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

id_int = {"id": 1}
id_text = {"id": "abc"}
id_comb =     {
        "id": 123,
        "description": "Buy milk, eggs and bread",
        "category": "Shopping"
    }

print("Testing id_int")
correct_json_format(id_int)
print("....1....")
print("Testing id_str")
print(correct_json_format(id_text))
print("....2....")
print("testing whole formated line now")
print(correct_json_format(id_comb))

print("############")
id_text_invalid = "id"
print("Testing invalid lines now")
correct_json_format(id_text_invalid)
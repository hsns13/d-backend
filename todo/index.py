from logging import debug, error
from flask import Flask, json, jsonify, request
# cors
from flask_cors import CORS
# unique id
import uuid

app = Flask(__name__)
CORS(app)

# to test the application, use memory storage for now..
# if it is wanted I can add persistent data storage

# sample todo
# {'id': 12345, 'isActive': '1', 'todoText': 'todo 1'}
todos_list = []


@app.route('/todos', methods=['GET'])
def get_todos():
    """
    # get all todo list
    """
    return jsonify(todos_list), 200


@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    """
    # get todo item based on given id
    """
    res = {
        'code': 200,
        'data': {},
        'message': ''
    }
    res_code = 200

    try:
        for todo in todos_list:
            if str(todo['id']) == str(id):
                res['data'] = todo

    except BaseException as err:
        res_code = 501
        res['code'] = 501
        res['message'] = "Couldn't find the data! " + err

    return jsonify(res), res_code


@app.route('/todo', methods=['POST'])
def add_todo():
    """
    # adds new todo item and returns result obj
    """
    res = {
        'code': 201,
        'message': 'Data is added!',
        'todo': {}
    }
    res_code = 201

    try:
        todoItem = request.get_json()
        todoItem['id'] = uuid.uuid4().hex
        todos_list.append(todoItem)
        res['todo'] = todoItem
    except Exception as ex:
        res_code = 501
        res['code'] = 501
        res['message'] = "Couldn't add a new data! | {0}".format(str(ex))

    return jsonify(res), res_code


@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    """
    # update todo and returns result obj
    """
    res = {
        'code': 202,
        'message': 'Data is updated!',
        'todo': {}
    }
    res_code = 202

    try:
        for i in range(len(todos_list)):
            if(str(todos_list[i]['id']) == str(id)):
                jsonObj = request.get_json()
                todos_list[i]['isActive'] = jsonObj['isActive']
                todos_list[i]['todoText'] = jsonObj['todoText']
                res['todo'] = todos_list[i]
                break
    except Exception as ex:
        res_code = 501
        res['code'] = 501
        res['message'] = "Couldn't update data! | {0}".format(str(ex))

    return jsonify(res), res_code


@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    """
    # delete todo
    """
    res = {
        'code': 200,
        'message': 'Data is deleted!'
    }
    res_code = 200

    try:
        for i in range(len(todos_list)):
            if(str(todos_list[i]['id']) == str(id)):
                todos_list.pop(i)
                break
    except Exception as ex:
        res_code = 501
        res['code'] = 501
        res['message'] = "Couldn't delete the data! | {0}".format(str(ex))

    return jsonify(res), res_code


@app.route('/todoClear', methods=['POST'])
def clear_todo():
    """
    # clear completed todo
    """
    res = {
        'code': 200,
        'message': 'Completed items are removed from the list!'
    }
    res_code = 200

    try:
        new_list = list(filter(lambda item: item['isActive'] == 1, todos_list))

        todos_list.clear()
        for item in new_list:
            todos_list.append(item)

    except Exception as ex:
        res_code = 501
        res['code'] = 501
        res['message'] = "Couldn't delete the data! | {0}".format(str(ex))

    return jsonify(res), res_code


@app.route("/")
def todos():
    return "<h1>ToDo App...</h1>"

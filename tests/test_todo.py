from todo import index
import json


def test_app_start():
    """
        When then '/' page is requested (GET)
    """
    client = index.app.test_client()
    response = client.get('/')

    assert response.get_data() == b'<h1>ToDo App...</h1>'
    assert response.status_code == 200


def test_app_todos():
    """
        When then '/todos' page is requested (GET)
    """
    client = index.app.test_client()
    response = client.get('/todos')

    assert json.loads(response.get_data(as_text=True)) == []
    assert response.status_code == 200


def test_todo_add():
    """
        When then '/todo' page is requested (POST)
    """
    client = index.app.test_client()

    response = client.post('/todo', json={
        'id': '',
        'isActive': '1',
        'todoText': 'todo 1'
    })

    response_data = response.get_json()

    assert response_data['message'] == 'Data is added!'
    assert response.status_code == 201


def test_todo_update():
    """
        When then '/todo' page is requested (POST)
    """
    client = index.app.test_client()

    # first add item
    added_item = client.post('/todo', json={
        'id': '',
        'isActive': '1',
        'todoText': 'todo 1'
    }).get_json()

    added = added_item['todo']
    # then update item
    updated_item = client.put('/todo/{0}'.format(added['id']), json={
        'id': '{0}'.format(added['id']),
        'isActive': '0',
        'todoText': 'todo 1'
    }).get_json()
    updated = updated_item['todo']

    assert added['id'] == updated['id']
    assert added['isActive'] == '1'
    assert updated['isActive'] == '0'
    assert updated_item['code'] == 202


def test_todo_delete():
    """
        When then '/todo' page is requested (POST)
    """
    client = index.app.test_client()

    # first add item
    added_item = client.post('/todo', json={
        'id': '',
        'isActive': '1',
        'todoText': 'todo 1'
    }).get_json()
    added = added_item['todo']

    response = client.delete('/todo/{0}'.format(added['id']))
    response_data = response.get_json()

    assert response_data['code'] == 200
    assert response_data['message'] == 'Data is deleted!'


def test_clear_todo():
    """
        When then '/todoClear' page is requested (POST)
    """
    client = index.app.test_client()

    newly_added_list = []

    # first add 2 items / "todo item 1" and "todo item 2"
    added_item_1 = client.post('/todo', json={
        'id': '',
        'isActive': '1',
        'todoText': 'todo item 1'
    }).get_json()
    newly_added_list.append(added_item_1['todo'])

    added_item_2 = client.post('/todo', json={
        'id': '',
        'isActive': '1',
        'todoText': 'todo item 2'
    }).get_json()
    newly_added_list.append(added_item_2['todo'])

    # update second item "todo item 2" as completed and changed it to "todo item updated!"
    updating_id = newly_added_list[1]['id']
    updated_item = client.put('/todo/{0}'.format(updating_id), json={
        'id': '{0}'.format(updating_id),
        'isActive': '0',
        'todoText': 'todo item updated!'
    }).get_json()

    response_data = client.post('/todoClear').get_json()

    # filter cleared items count
    new_list = list(filter(lambda item: item['id'] == updated_item['todo']['id'], newly_added_list))

    assert response_data['code'] == 200
    assert updated_item['todo']['isActive'] == '0'
    assert updated_item['todo']['todoText'] == 'todo item updated!'
    assert len(new_list) == 1
    assert response_data['message'] == 'Completed items are removed from the list!'

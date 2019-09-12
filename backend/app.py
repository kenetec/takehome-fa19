from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/contacts", methods=['GET'])
def get_all_contacts():
    hobby = request.args.get('hobby')

    if hobby:
        return get_contact_from_hobby(hobby)

    return create_response({"contacts": db.get('contacts')})

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="No contact with this id exists")
    db.deleteById('contacts', int(id))
    return create_response(message="Contact deleted")


# TODO: Implement the rest of the API here!

@app.route("/contacts/<id>", methods=['GET'])
def get_contact_from_id(id):
    contact = db.getById('contacts', int(id))
    
    if (contact == None):
        return create_response(status=404, message="No contact of id '{id}' found.".format(id=id))
    
    return create_response({'contact': contact})

def get_contact_from_hobby(hobby):
    contacts = db.get('contacts')
    target_contacts = []
    
    for contact in contacts:
        if contact['hobby'] == hobby:
            target_contacts.append(contact)

    if len(target_contacts) > 0:
        return create_response({'contacts': target_contacts})
    
    return create_response(status=404, message='No contact found with "{hobby}" as a hobby.'.format(hobby=hobby))

@app.route('/contacts', methods=['POST'])
def create_new_contact():
    missing_args = []
    json = request.json
    
    name ='name' in json and json['name'] or missing_args.append('name')
    nickname = 'nickname' in json and json['nickname'] or missing_args.append('nickname')
    hobby = 'hobby' in json and json['hobby'] or missing_args.append('hobby')

    if len(missing_args) > 0:
        return create_response(status=422, message='Missing {} for new contact'.format(missing_args))
    
    db.create('contacts', {"name": name, "nickname": nickname, "hobby": hobby})

    return create_response(status=201)

@app.route('/contacts/<id>', methods=['PUT'])
def update_contact(id):
    missing_args = []
    json = request.json
    idInt = int(id)

    name = 'name' in json and json['name'] or missing_args.append('name')
    hobby = 'hobby' in json and json['hobby'] or missing_args.append('hobby')

    if len(missing_args) > 0:
        return create_response(status=422, message='Missing {} for updating contact'.format(missing_args))
    
    contact = db.getById('contacts', idInt)
    if contact == None:
        return create_response(status=404, message="No contact of id '{id}' found.".format(id=id))
    
    db.updateById('contacts', idInt, {'name': name, 'hobby': hobby})
    return create_response(status=201, data=db.getById('contacts', idInt))

@app.route('/contacts/<id>', methods=['DELETE'])
def delete_contact(id):
    idInt = int(id)

    contact = db.getById('contacts', idInt)
    if contact == None:
        return create_response(status=404, message="No contact of id '{id}' found.".format(id=id))
    
    db.deleteById('contacts', idInt)
    return create_response(message="Contact with id '{id}' was deleted.".format(id=id))

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)

from flask import Flask, request
from flask_restplus import Resource, Api, fields

app = Flask(__name__)
api = Api(app)

###########################

ns_type1 = api.namespace('groceries1', description='grocery list')
grocery = api.model('Groceries', {
    'guid': fields.String(readOnly=True, required=True, description='unique shopping cart identifier'),
    'groceryitem1': fields.String(description='1st grocery item. if empty, this = null'),
    'groceryitem2': fields.String(description='2nd grocery item. if empty, this = null'),
    'groceryitem3': fields.String(description='3rd grocery item. if empty, this = null')
})

ns_type2 = api.namespace('pet store', description='pet selection')
petStore = api.model('Pet Store', {
    'guid': fields.String(readOnly=True, required=True, description='unique pet store identifier'),
    'animal type 1': fields.String(description='1st type of pet. if empty, this = null'),
    'animal type 2': fields.String(description='2nd type of pet. if empty, this = null'),
    'animal type 3': fields.String(description='3rd type of pet. if empty, this = null')
})
################################


class User1(Resource):
    def __init__(self):
        self.list = []
        self.id = ''
  

    def post(self, data):
        grocery = data
        self.list.append(grocery)
        self.id = grocery['guid']
        #element['guid'] = data
        return grocery    
    
    def get(self, id): 
        for element in self.list:
            if 'guid' in element.keys(): #check for existence
                if element['guid'] == id:
                    return element
        api.abort(404, "Element {} doesn't exist".format(id))
        
    def put(self, id, data):
        grocery = self.get(id)
        grocery.update(data)
        return grocery
    
    def delete(self, id):
        grocery = self.get(id)
        self.list.remove(grocery)
        return "{} is deleted.".format(id), 200

DAO1 = User1()
DAO1.post({'guid':'a11da159-510d-4be0-ad4b-6c8ee282ed1c','groceryitem1' : 'apple', 'groceryitem2' : 'banana'})


#############################
class User2(Resource):
    def __init__(self):
        self.list = []
        self.id = ''
  

    def post(self, data):
        petStore = data
        self.list.append(petStore)
        self.id = petStore['guid']
        #element['guid'] = data
        return petStore    
    
    def get(self, id):
        for element in self.list:
            if 'guid' in element.keys(): #check for existence
                if element['guid'] == id:
                    return element
        api.abort(404, "Element {} doesn't exist".format(id))

    def put(self, id, data):
        petStore = self.get(id)
        petStore.update(data)
        return petStore
    
    def delete(self, id):
        petStore = self.get(id)
        self.list.remove(petStore)
        return "{} is deleted.".format(id), 200

DAO2 = User2()

#######################################
@ns_type1.route('/')
class GroceryList(Resource):
    @ns_type1.doc('list_grocery')
    @ns_type1.marshal_list_with(grocery)
    def get(self):
        return DAO1.list
    
    @ns_type1.doc('post_groceryList')
    @ns_type1.expect(grocery)
    @ns_type1.marshal_with(grocery, code=201)
    def post(self):
        return DAO1.post(api.payload), 201

@ns_type1.route('/<string:guid>')
@ns_type1.response(404, 'grocery list not found')
@ns_type1.param('guid', 'grocery list identifier')
class Grocery(Resource): #single element push and remove
    @ns_type1.doc('get_grocery')
    @ns_type1.marshal_with(grocery)
    def get(self, guid):
        return DAO1.get(guid)
    
    @ns_type1.doc('delete grocery')
    @ns_type1.response(204, 'grocery deleted')
    def delete(self, guid):
        DAO1.delete(guid)
        return '', 204

    @ns_type1.expect(grocery)
    @ns_type1.marshal_with(grocery)
    def put(self, guid):
        return DAO1.put(guid, api.payload)

#####################################
@ns_type2.route('/')
class PetStore(Resource):
    @ns_type2.doc('list_petStore')
    @ns_type2.marshal_list_with(petStore)
    def get(self):
        return DAO2.list
    
    @ns_type2.doc('post_petStoreList')
    @ns_type2.expect(petStore)
    @ns_type2.marshal_with(petStore, code=201)
    def post(self):
        return DAO2.post(api.payload), 201

@ns_type2.route('/<string:guid>')
@ns_type2.response(404, 'petStore list not found')
@ns_type2.param('guid', 'petStore list identifier')
class Pet(Resource): #single element push and remove
    @ns_type2.doc('get_petStore')
    @ns_type2.marshal_with(petStore)
    def get(self, guid):
        return DAO2.get(guid)
    
    @ns_type2.doc('delete petStore')
    @ns_type2.response(204, 'petStore deleted')
    def delete(self, guid):
        DAO2.delete(guid)
        return '', 204

    @ns_type2.expect(petStore)
    @ns_type2.marshal_with(petStore)
    def put(self, guid):
        return DAO2.put(guid, api.payload)

#############################
def main(new_IP, new_port): #must modify IP and PORT. Look how these pass into app.run
    app.run(debug=True, host=new_IP, port=new_port)
    
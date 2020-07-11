#Import required packages
from flask import Flask, request, jsonify 
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize app
app = Flask(__name__)
# Initialize api
api = Api(app)
#Database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user_details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
#Initialize Database
db = SQLAlchemy(app)
#initialize Marshmallow
ma = Marshmallow(app)


#Table
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


#Marshmallow Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','password')

# Initialize schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


##Create Classes to handle requests
class UserGetPost(Resource):
    def post(self):
        #Instantiate new user
        new_user = User(name=request.json['name'], email=request.json['email'], password=request.json['password'])
        #add new user
        db.session.add(new_user)
        #commit the change to reflect in database
        db.session.commit()
        #return the response
        return user_schema.jsonify(new_user)

    def get(self):
        #get users from the database
        users = User.query.all()
        #return the list of users
        return jsonify(users_schema.dump(users))               

class UserPutDelete(Resource):
    def put(self,id):
        #get User
        user = User.query.get(id)
        #update user data
        user.name = request.json['name']
        user.email = request.json['email']
        user.password = request.json['password']
        #commit to change in database
        db.session.commit()
        return {'message':'data updated'}

    def delete(self,id):
        #get user
        user = User.query.get(id)
        #delete the user
        db.session.delete(user)
        #commit to reflect in database
        db.session.commit()
        return {'message':'data deleted successfully'}

#Bind the classes with the routes 
api.add_resource(UserGetPost, '/user')
api.add_resource(UserPutDelete, '/user/<int:id>')


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
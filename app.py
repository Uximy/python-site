from flask import Flask, app
import flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from flask_sqlalchemy import SQLAlchemy
import os
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
db = SQLAlchemy(app)
database_location = os.getcwd()+'/app.db'
app.config['SECRET_KEY'] = 'secret_key'

app.config['postgres://iognetbymwstex:a35471c6532c6c6b0099cd7718fdfb846cafda2c846919389b38cdb17a59396d@ec2-54-73-58-75.eu-west-1.compute.amazonaws.com:5432/dallsqsdsc5i7b'] = os.environ.get('dallsqsdsc5i7b') or 'sqlite:///'+database_location

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

# print(database_location)

class Flower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    shelf_life = db.Column(db.Integer)
    description = db.Column(db.Text)
    brought_in = db.Column(db.Date)

# db.create_all()

# db.drop_all()

db = SQLAlchemy(app)

class FlowerSchema(Schema):
    class Meta:
         type_ = 'цветочки'
         self_view = 'flower_detail'
         self_view_kwargs = {'id': '<id>'}
         self_view_many = 'flower_list'

    id = fields.Integer(as_string=True)
    name = fields.Str(required=True)
    shelf_life = fields.Integer(as_string=True)
    description = fields.Str()
    # display_name = fields.Function()
    brought_in= fields.Date()


class FlowerList(ResourceList):
    schema = FlowerSchema
    data_layer = {'session': db.session,
                  'model': Flower}


class FlowerDetail(ResourceDetail):
    schema = FlowerSchema
    data_layer = {'session': db.session,
                   'model': Flower}

api = Api(app)
api.route(FlowerList, 'flower_list', '/flowers')
api.route(FlowerDetail, 'flower_detail', '/flowers/<int:id>')

admin.add_view(ModelView(Flower, db.session))

if __name__ == '__main__':
    app.run(debug=True)
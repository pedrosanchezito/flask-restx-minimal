from flask import Flask, render_template, Blueprint
from flask_restx import fields, Api, Resource
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

# Init app
app = Flask(__name__)
Bootstrap5(app)

# Init DB
app.config.from_object(Config)
db = SQLAlchemy(app)
from models import Item
migrate = Migrate(app, db)

# Init API
app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, version='1.0', title='POC Items API',
    description='A basic API for testing purpose',
    doc='/doc/'
)
ns = api.namespace('items', description='Items operations')
item = api.model('Item', {
    'id': fields.Integer(readonly=True, description='The item unique identifier'),
    'name': fields.String(required=True, description='The item name')
})
app.register_blueprint(blueprint)

@app.route('/')
def hello_world():
    return render_template('index.html')

@ns.route('/')
@ns.response(404, 'Item not found')
class ItemList(Resource):
    '''Shows a list of all items, and lets you POST to add new item'''
    @ns.doc('list_items')
    @ns.marshal_list_with(item)
    def get(self):
        '''List all item'''
        return [item.to_dict() for item in Item.query.all()]

    @ns.doc('create_item')
    @ns.expect(item)
    @ns.marshal_with(item, code=201)
    def post(self):
        '''Create a new item'''
        item = Item()
        item.name = api.payload['name']
        db.session.add(item)
        db.session.commit()        
        return item.to_dict(), 201

@ns.route('/<int:id>')
@ns.response(404, 'Item not found')
@ns.param('id', 'The item identifier')
class ItemId(Resource):
    '''Show a single item and lets you delete it'''
    @ns.doc('get_item')
    @ns.marshal_with(item)
    def get(self, id):
        '''Fetch a single item'''
        return db.get_or_404(Item, id).to_dict()

    @ns.doc('delete_item')
    @ns.response(204, 'Item deleted')
    def delete(self, id):
        '''Delete an item given its identifier'''
        item = db.get_or_404(Item, id)
        db.session.delete(item)
        db.session.commit()
        return f'Item {item.name} deleted', 202


if __name__ == '__main__':
    app.run(debug=True)
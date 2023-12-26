from flask import (
    Flask, 
    jsonify, 
    render_template, 
    redirect,
    url_for,
    request
)
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6237@localhost:5432/postgres'

db = SQLAlchemy()
api = Api(app)

class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    @property
    def serialized(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

    def __init__(self, title, description):
        self.title = title
        self.description = description

class AddData(Resource):
    def post(self):
        try:
            title = request.form['title']
            description = request.form['description']

            db.session.add(TestModel(title, description))
            db.session.commit()
            return {'msg': 'data added'}, 201
        except Exception as e:
            return {'msg': 'Something went wrong'}, 500

with app.app_context():
    db.init_app(app)
    db.create_all()

api.add_resource(AddData, '/add_data')

@app.route('/', methods=['GET'])
def _index():
    return render_template('index.html')

@app.route('/json', methods=['GET'])
def _json():
    return jsonify([item.serialized for item in TestModel.query.all()])

@app.route('/reset_data', methods=['POST'])
def _reset_data():
    TestModel.query.delete()
    db.session.commit()

    return redirect(url_for('_json'))

if __name__ == '__main__':
    app.run(host='5.42.79.161', port=5000)
    #app.run(port=5000)
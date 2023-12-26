from flask import (
    Flask, 
    jsonify, 
    render_template, 
    redirect,
    url_for,
    request
)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6237@localhost:5432/postgres'

db = SQLAlchemy()

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

with app.app_context():
    db.init_app(app)
    db.create_all()

@app.route('/', methods=['GET'])
def _index():
    return render_template('index.html')

@app.route('/json', methods=['GET'])
def _json():
    return jsonify([item.serialized for item in TestModel.query.all()])

@app.route('/add_data', methods=['POST'])
def _add_data():
    title = request.form['title']
    description = request.form['description']

    db.session.add(TestModel(title, description))
    db.session.commit()

    return redirect(url_for('_json'))

if __name__ == '__main__':
    app.run(port=5000)
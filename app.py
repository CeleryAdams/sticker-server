from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/duck'
db = SQLAlchemy(app)
CORS(app)


class StickerSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    sticker_list = db.Column(JSON)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'StickerSet: {self.name}'


#add entry
@app.route('/saved', methods = ['POST'])
def add_sticker_set():
    name = request.json['name']
    sticker_list = request.json['sticker_list']

    if not name.isalnum():
        return {'message': 'Please use only letters and numbers'}, 400

    existing_sticker_set = StickerSet.query.filter_by(name=name).first()
    if existing_sticker_set:
        return {'message': 'name already exists'}, 400
    
    sticker_set = StickerSet(name=name, sticker_list=sticker_list)
    db.session.add(sticker_set)
    db.session.commit()
    return "thank you"


#get sticker set
@app.route('/saved/<name>', methods = ['GET'])
def get_sticker_set(name):
    sticker_set = StickerSet.query.filter_by(name=name).first()

    if sticker_set:
        return {
            'id': sticker_set.id,
            'name': sticker_set.name,
            'sticker_list': sticker_set.sticker_list,
            'created_at': sticker_set.created_at
        }
    else:
        return {'message': 'name not found'}, 404


if __name__ == '__main__':
    app.run()
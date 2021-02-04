from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import redirect
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(144), unique=False, nullable=False)

class ShoppingListSchema(ma.Schema):
    class Meta:
        fields = ('item', 'id')

shoppingListSchema = ShoppingListSchema
shoppingListsSchema = ShoppingListSchema(many=True)

@ app.route('/', methods=['GET', 'POST'])
def item_list():
    if request.method == "POST":
        item = request.form.get('item')
        new_item = ShoppingList(item=item)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/')
    else:
        all_items = ShoppingList.query.all()
        print(all_items)
        return render_template('base.html', items=all_items)

@app.route('/delete-item/<id>', methods=['POST'])
def delete_item(id):
    item = ShoppingList.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
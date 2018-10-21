from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Catalog, Base, CatalogItem, User
from flask import session as login_session
import random
import string
import json
from sqlalchemy.pool import StaticPool
from flask import make_response
import requests

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogItem.db', connect_args={'check_same_thread':False}, poolclass=StaticPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    catalogs = session.query(Catalog)
    return render_template('catalogs.html', catalogs=catalogs)


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Catalog(name=request.form['name'],user_id='1')
        session.add(newCategory)
        #flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html')


# Edit a Category

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory= session.query(Catalog).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            session.add(editedCategory)
            session.commit()
            return redirect(url_for('showCatalog'))
    else:
        return render_template('editCategory.html', catalog=editedCategory)



# Delete a Category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Catalog).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCategory.html', catalog=categoryToDelete)



#Show Items for a Category
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showItems(category_id):
    catalog = session.query(Catalog).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return render_template('catalogItems.html', items=items, catalog=catalog)



# Create a new catalog item
@app.route('/category/<int:category_id>/catalog/new/', methods=['GET', 'POST'])
def newCatalogItem(category_id):
    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'], description=request.form[
                           'description'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newCatalogItem.html', category_id=category_id)

    return render_template('newCatalogItem.html', category_id=category_id)



# Edit a catalog item
@app.route('/category/<int:category_id>/catalog/<int:catalog_id>/edit',
           methods=['GET', 'POST'])
def editCatalogItem(category_id, catalog_id):
    editedItem = session.query(CatalogItem).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:

        return render_template(
            'editCatalogItem.html', category_id=category_id, catalog_id=catalog_id, item=editedItem)



# Delete a catalog item
@app.route('/category/<int:category_id>/catalog/<int:catalog_id>/delete',
           methods=['GET', 'POST'])
def deleteCatalogItem(category_id, catalog_id):
    itemToDelete = session.query(CatalogItem).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteCatalogItem.html', item=itemToDelete)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
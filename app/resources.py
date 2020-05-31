from flask_restful import Resource, reqparse
from app.models import Category
from app import db
from flask_restful import Resource
from flask import render_template, make_response


class CategoryResource(Resource):
    def get(self, name):
        category = Category.find_by_category(name)
        if category:
            return make_response(render_template('home.html'), 200, category.json())
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
class Category_resources(Resource):
    @staticmethod
    def list_of_category():
        list_of_id = []
        [list_of_id.append(i[0]) for i in Category.query.all()]
        return list_of_id


    @staticmethod
    def list_of_column(obj, table, _id):
        list_of_col = []
        for i in obj.find_by_id(table, _id):
            list_of_col.append(i)
        return list_of_col

    @staticmethod
    def find_by_id(table, _id):
        return table.query.filter_by(id=_id).first()

    @staticmethod
    def find_by_category(table, category):
        return table.query.filter_by(category=category)

    @staticmethod
    def column_with_id(table, column, _id):
        print(table.find_by_id(db.session.query(table._id).all()))

    # def get(self, name):
    #     store = StoreModel.find_by_name(name)
    #     if store:
    #         return store.json()
    #     return {'message': 'Store not found'}, 404
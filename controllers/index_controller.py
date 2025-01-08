from flask import render_template
from models import *
from utils import render_with_message
from app import db


class IndexController:
    @staticmethod
    def register_routes(app, db):
        @app.route('/')
        def index():
            return render_with_message('index.html',
                                        suppliers=Supplier.read_all(db),
                                        purchase_orders=PurchaseOrder.read_all(db),
                                        products=Product.read_all(db),
                                        product_recipes=RecipeComposition.read_all(db),
                                        recipes=Recipe.read_all(db),
                                        dishes=Dish.read_all(db),
                                        menus=Menu.read_all(db)
            )
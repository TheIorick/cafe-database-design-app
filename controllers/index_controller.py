from models import *
from utils import render_with_message


class IndexController:
    @staticmethod
    def register_routes(app):
        @app.route('/')
        def index():
            return render_with_message('index.html',
                                        suppliers=Supplier.read_all(),
                                        purchase_orders=PurchaseOrder.read_all(),
                                        products=Product.read_all(),
                                        product_recipes=RecipeComposition.read_all(),
                                        recipes=Recipe.read_all(),
                                        dishes=Dish.read_all(),
                                        menus=Menu.read_all()
            )
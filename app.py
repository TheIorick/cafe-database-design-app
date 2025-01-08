from flask import Flask
from controllers import *  # Import all controllers
from config import AppConfig
from data_manager import DataManager
from utils import *  # Import utility functions
from flask_sqlalchemy import SQLAlchemy

data_manager = DataManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)  # Load configs from AppConfig
    db.init_app(app)  # Initialize SQLAlchemy with the Flask app

    # Register Controllers
    IndexController.register_routes(app)
    SupplierController.register_routes(app)
    PurchaseOrderController.register_routes(app)
    ProductController.register_routes(app)
    RecipeController.register_routes(app)
    RecipeCompositionController.register_routes(app)
    DishController.register_routes(app)
    MenuController.register_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
         # data_manager.populate_table(db, "suppliers", 10)
         # data_manager.populate_table(db, "products", 1000)
         # data_manager.populate_table(db, "purchase_order", 50)
         # data_manager.populate_table(db, "recipes", 30)
         # data_manager.populate_table(db, "recipe_composition", 50)
         # data_manager.populate_table(db, "dishes", 50)
         # data_manager.populate_table(db, "menu", 50)
         # data_manager.clear_table_data(db,"suppliers", 10)
         # data_manager.clear_all_tables(db)
        app.run(debug=True)
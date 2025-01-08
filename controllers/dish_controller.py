from flask import request, redirect, render_template, url_for
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors
from app import db

class DishController:
    @staticmethod
    def register_routes(app, db):
        @app.route('/dishes')
        def dishes_page():
            return render_with_message('table_dishes.html', dishes=Dish.read_all(db), recipes=Recipe.read_all(db))

        @app.route('/filtered_dishes', methods=['GET'])
        def filtered_dishes_page():
            filters = {
                Dish.id_recipes: request.args.get('id_recipes', type=int),
                Dish.category: request.args.get('category', type=str),
                Dish.name_dish: request.args.get('name_dish', type=str),
                Dish.price_dish: {
                    'min': request.args.get('price_dish_min', type=int),
                    'max': request.args.get('price_dish_max', type=int)
                }
            }
            query = Dish.query(db)
            dishes = apply_filters(query, filters).all()
            return render_with_message('table_dishes.html', dishes=dishes, recipes=Recipe.read_all(db))

        @app.route('/create_dish', methods=['POST'])
        def create_dish():
            form_data = request.form
            error = handle_form_errors(form_data, ['id_recipes', 'category', 'name_dish', 'price_dish'], 'dishes_page')
            if error:
                return error

            price_dish = validate_positive_int(form_data['price_dish'], 'Цена блюда не может быть отрицательной', 'dishes_page')
            if not price_dish:
                return redirect(url_for('dishes_page'))

            Dish.create(db,
                id_recipes=form_data['id_recipes'],
                category=form_data['category'],
                name_dish=form_data['name_dish'],
                price_dish=price_dish
            )
            return flash_redirect('Новое блюдо успешно добавлено!', 'success', 'dishes_page')

        @app.route('/edit_dish/<int:id_dish>', methods=['GET', 'POST'])
        def edit_dish(id_dish):
            dish = Dish.query(db).get_or_404(id_dish)
            recipes = Recipe.read_all(db)
            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['id_recipes', 'category', 'name_dish', 'price_dish'],
                                           'edit_dish', dish=dish, recipes=recipes)
                if error:
                    return error

                price_dish = validate_positive_int(form_data['price_dish'], 'Цена блюда не может быть отрицательной',
                                                      'edit_dish', dish=dish, recipes=recipes)
                if not price_dish:
                    return render_template('edit_dish.html', dish=dish, recipes=recipes)

                Dish.update(db, id_dish, id_recipes=form_data['id_recipes'],
                           category=form_data['category'],
                           name_dish=form_data['name_dish'],
                           price_dish=price_dish)
                return redirect(url_for('dishes_page'))
            return render_template('edit_dish.html', dish=dish, recipes=recipes)

        @app.route('/delete_dish/<int:id_dish>', methods=['POST'])
        def delete_dish(id_dish):
            Dish.delete(db, id_dish)
            return flash_redirect('Блюдо успешно удалено!', 'success', 'dishes_page')
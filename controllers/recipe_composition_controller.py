from flask import request, url_for, redirect, render_template
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors
from app import db

class RecipeCompositionController:
    @staticmethod
    def register_routes(app, db):
        @app.route('/recipe_compositions')
        def recipe_compositions_page():
            return render_with_message('table_recipe_composition.html',
                                       recipe_compositions=RecipeComposition.read_all(db),
                                       recipes=Recipe.read_all(db),
                                       products=Product.read_all(db))

        @app.route('/recipe_composition_modal/<int:recipe_id>')
        def recipe_composition_modal(recipe_id):
            recipe_compositions = RecipeComposition.query(db).filter_by(id_recipes=recipe_id).all()
            return render_with_message('table_recipe_composition.html',
                                       recipe_compositions=recipe_compositions,
                                       recipes=Recipe.read_all(db),
                                       products=Product.read_all(db))

        @app.route('/filtered_recipe_compositions', methods=['GET'])
        def filtered_recipe_compositions_page():
            filters = {
                RecipeComposition.id_products: request.args.get('id_products', type=int),
                RecipeComposition.id_recipes: request.args.get('id_recipes', type=int),
                RecipeComposition.quantity_for_recipe: {
                    'min': request.args.get('quantity_for_recipe_min', type=int),
                    'max': request.args.get('quantity_for_recipe_max', type=int)
                }
            }
            query = RecipeComposition.query(db)
            recipe_compositions = apply_filters(query, filters).all()
            return render_with_message('table_recipe_composition.html',
                                       recipe_compositions=recipe_compositions,
                                       recipes=Recipe.read_all(db),
                                       products=Product.read_all(db))

        @app.route('/create_recipe_composition', methods=['POST'])
        def create_recipe_composition():
            form_data = request.form
            error = handle_form_errors(form_data, ['id_products', 'id_recipes', 'quantity_for_recipe'],
                                       'recipe_compositions_page')
            if error:
                return error

            quantity_for_recipe = validate_positive_int(form_data['quantity_for_recipe'],
                                                          'Количество для рецепта не может быть отрицательным',
                                                          'recipe_compositions_page')
            if not quantity_for_recipe:
                return redirect(url_for('recipe_compositions_page'))

            RecipeComposition.create(db,
                id_products=form_data['id_products'],
                id_recipes=form_data['id_recipes'],
                quantity_for_recipe=quantity_for_recipe
            )
            return flash_redirect('Новая запись успешно добавлена!', 'success', 'recipe_compositions_page')

        @app.route('/edit_recipe_composition/<int:id_composition>', methods=['GET', 'POST'])
        def edit_recipe_composition(id_composition):
            composition = RecipeComposition.query(db).get_or_404(id_composition)
            products = Product.read_all(db)
            recipes = Recipe.read_all(db)
            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['id_products', 'id_recipes', 'quantity_for_recipe'],
                                           'edit_recipe_composition',
                                           composition=composition, products=products,
                                           recipes=recipes)
                if error:
                    return error

                quantity_for_recipe = validate_positive_int(form_data['quantity_for_recipe'],
                                                          'Количество для рецепта не может быть отрицательным',
                                                          'edit_recipe_composition',
                                                          composition=composition, products=products,
                                                          recipes=recipes)
                if not quantity_for_recipe:
                    return render_template('edit_recipe_composition.html', composition=composition, products=products,
                                           recipes=recipes)

                RecipeComposition.update(db, id_composition, id_products=form_data['id_products'],
                                         id_recipes=form_data['id_recipes'],
                                         quantity_for_recipe=quantity_for_recipe)
                return redirect(url_for('recipe_compositions_page'))
            return render_template('edit_recipe_composition.html', composition=composition, products=products,
                                   recipes=recipes)

        @app.route('/delete_recipe_composition/<int:id_composition>', methods=['POST'])
        def delete_recipe_composition(id_composition):
            RecipeComposition.delete(db, id_composition)
            return flash_redirect('Запись успешно удалена!', 'success', 'recipe_compositions_page')
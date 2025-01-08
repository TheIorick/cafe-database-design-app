from flask import request, url_for, redirect, render_template, jsonify
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors
from sqlalchemy.exc import IntegrityError

class RecipeCompositionController:
    @staticmethod
    def register_routes(app):
        @app.route('/recipe_composition_modal/<int:recipe_id>')
        def recipe_composition_modal(recipe_id):
            recipe_compositions = db.session.query(RecipeComposition).filter_by(id_recipes=recipe_id).all()
            return render_template('table_recipe_composition.html',
                                       recipe_compositions=recipe_compositions,
                                       recipes=Recipe.read_all(),
                                       products=Product.read_all(),
                                       recipe_id=recipe_id)

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
            query = db.session.query(RecipeComposition)
            recipe_compositions = apply_filters(query, filters).all()
            return render_with_message('table_recipe_composition.html',
                                       recipe_compositions=recipe_compositions,
                                       recipes=Recipe.read_all(),
                                       products=Product.read_all())

        @app.route('/create_recipe_composition/<int:recipe_id>', methods=['POST'])
        def create_recipe_composition(recipe_id):
            form_data = request.form
            error = handle_form_errors(form_data, ['id_products', 'quantity_for_recipe'],
                                       'recipe_compositions_page')
            if error:
                return error

            quantity_for_recipe = validate_positive_int(form_data['quantity_for_recipe'],
                                                          'Количество для рецепта не может быть отрицательным',
                                                          'recipe_compositions_page')
            if not quantity_for_recipe:
                return redirect(url_for('recipe_compositions_page'))

            try:
                RecipeComposition.create(
                    id_products=form_data['id_products'],
                    id_recipes=recipe_id,
                    quantity_for_recipe=quantity_for_recipe
                )
                return jsonify({'success': True})
            except IntegrityError:
                 db.session.rollback()
                 return jsonify({'success': False, 'error': 'Этот продукт уже добавлен в рецепт'})


        @app.route('/edit_recipe_composition/<int:id_composition>/<int:recipe_id>', methods=['GET', 'POST'])
        def edit_recipe_composition(id_composition, recipe_id):
            composition = db.session.query(RecipeComposition).get_or_404(id_composition)
            products = Product.read_all()
            recipes = Recipe.read_all()
            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['id_products', 'quantity_for_recipe'],
                                           'edit_recipe_composition',
                                          )  # Убрали лишние аргументы
                if error:
                    return error

                quantity_for_recipe = validate_positive_int(form_data['quantity_for_recipe'],
                                                          'Количество для рецепта не может быть отрицательным',
                                                          'edit_recipe_composition'
                                                           ) # Убрали лишние аргументы
                if not quantity_for_recipe:
                     return render_template('edit_recipe_composition.html', composition=composition, products=products,
                                           recipes=recipes)

                RecipeComposition.update(id_composition, id_products=form_data['id_products'],
                                         quantity_for_recipe=quantity_for_recipe)
                return jsonify({'success': True})
            return render_template('edit_recipe_composition.html', composition=composition, products=products,
                                   recipes=recipes)

        @app.route('/delete_recipe_composition/<int:id_composition>/<int:recipe_id>', methods=['POST'])
        def delete_recipe_composition(id_composition, recipe_id):
             RecipeComposition.delete(id_composition)
             return jsonify({'success': True})
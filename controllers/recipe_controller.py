from flask import request, redirect, url_for, render_template
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors
# from app import db - удаляем импорт db


class RecipeController:
    @staticmethod
    def register_routes(app): #Удаляем db
        @app.route('/recipes')
        def recipes_page():
            return render_with_message('table_recipe.html', recipes=Recipe.read_all())

        @app.route('/filtered_recipes', methods=['GET'])
        def filtered_recipes_page():
            filters = {
                Recipe.name_recipe: request.args.get('name_recipe', type=str),
                Recipe.cooking_time: {
                    'min': request.args.get('cooking_time_min', type=int),
                    'max': request.args.get('cooking_time_max', type=int)
                }
            }
            query = db.session.query(Recipe)
            recipes = apply_filters(query, filters).all()
            return render_with_message('table_recipe.html', recipes=recipes)

        @app.route('/create_recipe', methods=['POST'])
        def create_recipe():
            form_data = request.form
            error = handle_form_errors(form_data, ['name_recipe', 'cooking_time'], 'recipes_page')
            if error:
                return error

            cooking_time = validate_positive_int(form_data['cooking_time'], 'Время приготовления не может быть отрицательным',
                                                  'recipes_page')
            if not cooking_time:
                return redirect(url_for('recipes_page'))

            Recipe.create(name_recipe=form_data['name_recipe'], cooking_time=cooking_time)
            return flash_redirect('Новый рецепт успешно добавлен!', 'success', 'recipes_page')

        @app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
        def edit_recipe(recipe_id):
            recipe = db.session.query(Recipe).get_or_404(recipe_id)
            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['name_recipe', 'cooking_time'], 'edit_recipe', recipe=recipe)
                if error:
                    return error
                cooking_time = validate_positive_int(form_data['cooking_time'], 'Время приготовления не может быть отрицательным',
                                                      'edit_recipe' ) # Убрали recipe=recipe
                if not cooking_time:
                    return render_template('edit_recipe.html', recipe=recipe)

                Recipe.update(recipe_id, name_recipe=form_data['name_recipe'], cooking_time=cooking_time)
                return redirect(url_for('recipes_page'))
            return render_template('edit_recipe.html', recipe=recipe)

        @app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
        def delete_recipe(recipe_id):
            Recipe.delete(recipe_id)
            return flash_redirect('Рецепт успешно удален!', 'success', 'recipes_page')
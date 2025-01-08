from flask import request, render_template, url_for, redirect
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors
from app import db

class MenuController:
    @staticmethod
    def register_routes(app, db):
        @app.route('/menu')
        def menu_page():
            return render_with_message('table_menu.html', menus=Menu.read_all(db), dishes=Dish.read_all(db))

        @app.route('/filtered_menu', methods=['GET'])
        def filtered_menu_page():
            filters = {
                Menu.id_dish: request.args.get('id_dish', type=int),
                Menu.menu_name: request.args.get('menu_name', type=str)
            }
            query = Menu.query(db)
            menus = apply_filters(query, filters).all()
            return render_with_message('table_menu.html', menus=menus, dishes=Dish.read_all(db))

        @app.route('/create_menu', methods=['POST'])
        def create_menu():
            form_data = request.form
            error = handle_form_errors(form_data, ['id_dish', 'date_menu', 'menu_name'], 'menu_page')
            if error:
                return error
            Menu.create(db, id_dish=form_data['id_dish'], date_menu=form_data['date_menu'], menu_name=form_data['menu_name'])
            return flash_redirect('Новое меню успешно добавлено!', 'success', 'menu_page')

        @app.route('/edit_menu/<int:id_menu>', methods=['GET', 'POST'])
        def edit_menu(id_menu):
            menu = Menu.query(db).get_or_404(id_menu)
            dishes = Dish.read_all(db)

            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['id_dish', 'date_menu', 'menu_name'],
                                           'edit_menu', menu=menu, dishes=dishes)
                if error:
                    return error

                Menu.update(db, id_menu, id_dish=form_data['id_dish'],
                           date_menu=form_data['date_menu'],
                           menu_name=form_data['menu_name'])
                return redirect(url_for('menu_page'))
            return render_template('edit_menu.html', menu=menu, dishes=dishes)

        @app.route('/delete_menu/<int:id_menu>', methods=['POST'])
        def delete_menu(id_menu):
            Menu.delete(db, id_menu)
            return flash_redirect('Меню успешно удалено!', 'success', 'menu_page')
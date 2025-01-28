from flask import request, render_template, url_for, redirect
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors

class MenuController:
    @staticmethod
    def register_routes(app):
        @app.route('/menu')
        def menu_page():
            return render_with_message('table_menu.html', menus=Menu.read_all(), dishes=Dish.read_all())

        @app.route('/filtered_menu', methods=['GET'])
        def filtered_menu_page():
            filters = {
                Menu.id_dish: request.args.get('id_dish', type=int),
                Menu.menu_name: request.args.get('menu_name', type=str)
            }
            query = db.session.query(Menu)
            menus = apply_filters(query, filters).all()
            return render_with_message('table_menu.html', menus=menus, dishes=Dish.read_all())

        @app.route('/create_menu', methods=['POST'])
        def create_menu():
            form_data = request.form
            error = handle_form_errors(form_data, ['id_dish', 'date_menu', 'menu_name'], 'menu_page')
            if error:
                return error
            Menu.create(id_dish=form_data['id_dish'], date_menu=form_data['date_menu'], menu_name=form_data['menu_name'])
            return flash_redirect('Новое меню успешно добавлено!', 'success', 'menu_page')

        @app.route('/edit_menu/<int:id_menu>', methods=['GET', 'POST'])
        def edit_menu(id_menu):
            menu = db.session.query(Menu).get_or_404(id_menu)
            dishes = Dish.read_all()

            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['id_dish', 'date_menu', 'menu_name'],
                                           'edit_menu', menu=menu, dishes=dishes)
                if error:
                    return error

                Menu.update(id_menu, id_dish=form_data['id_dish'],
                           date_menu=form_data['date_menu'],
                           menu_name=form_data['menu_name'])
                return redirect(url_for('menu_page'))
            return render_template('edit_menu.html', menu=menu, dishes=dishes)

        @app.route('/delete_menu/<int:id_menu>', methods=['POST'])
        def delete_menu(id_menu):
            Menu.delete(id_menu)
            return flash_redirect('Меню успешно удалено!', 'success', 'menu_page')
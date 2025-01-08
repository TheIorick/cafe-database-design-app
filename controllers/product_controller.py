from flask import request, redirect, render_template, url_for
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors
from app import db

class ProductController:
    @staticmethod
    def register_routes(app, db):
        @app.route('/products')
        def products_page():
            return render_with_message('table_product.html', products=Product.read_all(db))

        @app.route('/filtered_products', methods=['GET'])
        def filtered_products_page():
            filters = {
                Product.name_product: request.args.get('name_product', type=str),
                Product.quantity_in_warehouse: {
                    'min': request.args.get('quantity_in_warehouse_min', type=int),
                    'max': request.args.get('quantity_in_warehouse_max', type=int)
                },
                Product.unit: request.args.get('unit', type=str)
            }
            query = Product.query(db)
            products = apply_filters(query, filters).all()
            return render_with_message('table_product.html', products=products)

        @app.route('/create_product', methods=['POST'])
        def create_product():
            form_data = request.form
            error = handle_form_errors(form_data, ['name_product', 'quantity_in_warehouse', 'unit'], 'products_page')
            if error:
                return error

            quantity_in_warehouse = validate_positive_int(form_data['quantity_in_warehouse'],
                                                          'Количество на складе не может быть отрицательным',
                                                          'products_page')
            if not quantity_in_warehouse:
                return redirect(url_for('products_page'))

            new_product = Product.create(db, name_product=form_data['name_product'],
                                         quantity_in_warehouse=quantity_in_warehouse,
                                         unit=form_data['unit'])
            db.session.add(new_product)
            db.session.commit()
            return flash_redirect('Новый продукт успешно добавлен!', 'success', 'products_page')

        @app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
        def edit_product(product_id):
            product = Product.query(db).get_or_404(product_id)
            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['name_product', 'quantity_in_warehouse', 'unit'],
                                           'edit_product', product=product)
                if error:
                    return error
                quantity_in_warehouse = validate_positive_int(form_data['quantity_in_warehouse'],
                                                          'Количество на складе не может быть отрицательным',
                                                          'edit_product', product=product)
                if not quantity_in_warehouse:
                    return render_template('edit_product.html', product=product)

                Product.update(db, product_id, name_product=form_data['name_product'],
                              quantity_in_warehouse=quantity_in_warehouse,
                              unit=form_data['unit'])
                return redirect(url_for('products_page'))
            return render_template('edit_product.html', product=product)

        @app.route('/delete_product/<int:product_id>', methods=['POST'])
        def delete_product(product_id):
            product = Product.query(db).get_or_404(product_id)
            db.session.delete(product)
            db.session.commit()
            return flash_redirect('Продукт успешно удален!', 'success', 'products_page')
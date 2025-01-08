from flask import request, redirect, render_template, url_for
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors
from app import db


class PurchaseOrderController:
    @staticmethod
    def register_routes(app, db):
        @app.route('/purchase_orders')
        def purchase_orders_page():
            return render_with_message('table_purchase_order.html',
                                       purchase_orders=PurchaseOrder.read_all(db),
                                       suppliers=Supplier.read_all(db),
                                       products=Product.read_all(db))

        @app.route('/filtered_purchase_orders', methods=['GET'])
        def filtered_purchase_orders_page():
            filters = {
                PurchaseOrder.id_products: request.args.get('id_products', type=int),
                PurchaseOrder.id_suppliers: request.args.get('id_suppliers', type=int),
                PurchaseOrder.quantity_item: {
                    'min': request.args.get('quantity_item_min', type=int),
                    'max': request.args.get('quantity_item_max', type=int)
                },
                PurchaseOrder.price_product: {
                    'min': request.args.get('price_product_min', type=int),
                    'max': request.args.get('price_product_max', type=int)
                }
            }
            query = PurchaseOrder.query(db)
            purchase_orders = apply_filters(query, filters).all()
            return render_with_message('table_purchase_order.html',
                                       purchase_orders=purchase_orders,
                                       suppliers=Supplier.read_all(db),
                                       products=Product.read_all(db))

        @app.route('/create_purchase_order', methods=['POST'])
        def create_purchase_order():
            form_data = request.form
            error = handle_form_errors(form_data, ['id_products', 'id_suppliers', 'quantity_item', 'price_product'],
                                       'purchase_orders_page')
            if error:
                return error

            quantity_item = validate_positive_int(form_data['quantity_item'], 'Количество товара не может быть отрицательным',
                                                  'purchase_orders_page')
            if not quantity_item:
                return redirect(url_for('purchase_orders_page'))
            price_product = validate_positive_int(form_data['price_product'], 'Цена товара не может быть отрицательной',
                                                   'purchase_orders_page')
            if not price_product:
                return redirect(url_for('purchase_orders_page'))

            PurchaseOrder.create(db,
                id_products=form_data['id_products'],
                id_suppliers=form_data['id_suppliers'],
                quantity_item=quantity_item,
                price_product=price_product
            )
            return flash_redirect('Новый заказ успешно добавлен!', 'success', 'purchase_orders_page')

        @app.route('/edit_purchase_order/<int:id_order>', methods=['GET', 'POST'])
        def edit_purchase_order(id_order):
            order = PurchaseOrder.query(db).get_or_404(id_order)
            products = Product.read_all(db)
            suppliers = Supplier.read_all(db)
            product = next((p for p in products if p.id_products == order.id_products), None)
            name_product = product.name_product if product else "Unknown Product"
            company = next((c for c in suppliers if c.id_suppliers == order.id_suppliers), None)
            company_name = company.company_name if company else "Unknown Company"

            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['id_products', 'id_suppliers', 'quantity_item', 'price_product'],
                                           'edit_purchase_order',
                                           order=order,
                                           products=products,
                                           suppliers=suppliers,
                                           name_product=name_product,
                                           company_name=company_name)
                if error:
                    return error

                quantity_item = validate_positive_int(form_data['quantity_item'], 'Количество товара не может быть отрицательным',
                                                      'edit_purchase_order',
                                                      order=order, products=products,
                                                      suppliers=suppliers,
                                                      name_product=name_product,
                                                      company_name=company_name)
                if not quantity_item:
                    return render_template('edit_purchase_order.html', order=order, products=products,
                                           suppliers=suppliers,
                                           name_product=name_product,
                                           company_name=company_name)
                price_product = validate_positive_int(form_data['price_product'], 'Цена товара не может быть отрицательной',
                                                      'edit_purchase_order',
                                                      order=order, products=products,
                                                      suppliers=suppliers,
                                                      name_product=name_product,
                                                      company_name=company_name)
                if not price_product:
                    return render_template('edit_purchase_order.html', order=order, products=products,
                                           suppliers=suppliers,
                                           name_product=name_product,
                                           company_name=company_name)

                PurchaseOrder.update(db, id_order, id_products=form_data['id_products'], id_suppliers=form_data['id_suppliers'],
                                    quantity_item=quantity_item, price_product=price_product)
                return redirect(url_for('purchase_orders_page'))
            return render_template('edit_purchase_order.html', order=order, products=products, suppliers=suppliers,
                                   name_product=name_product,
                                   company_name=company_name)

        @app.route('/delete_purchase_order/<int:id_order>', methods=['POST'])
        def delete_purchase_order(id_order):
            PurchaseOrder.delete(db, id_order)
            return flash_redirect('Заказ успешно удален!', 'success', 'purchase_orders_page')
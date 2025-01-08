from flask import request, redirect, url_for, render_template
from models import *
from utils import apply_filters, validate_positive_int, render_with_message, flash_redirect, handle_form_errors


class SupplierController:
    @staticmethod
    def register_routes(app):
        @app.route('/suppliers')
        def suppliers_page():
            return render_with_message('table_suppliers.html', suppliers=Supplier.read_all())

        @app.route('/filtered_suppliers', methods=['GET'])
        def filtered_suppliers_page():
            filters = {
                Supplier.delivery_price: {
                    'min': request.args.get('delivery_price_min', type=int),
                    'max': request.args.get('delivery_price_max', type=int)
                },
                Supplier.company_name: request.args.get('company_name', type=str)
            }
            query = db.session.query(Supplier)
            suppliers = apply_filters(query, filters).all()
            return render_with_message('table_suppliers.html', suppliers=suppliers)

        @app.route('/create_supplier', methods=['POST'])
        def create_supplier():
            form_data = request.form
            error = handle_form_errors(form_data, ['delivery_price', 'company_name'], 'suppliers_page')
            if error:
                return error
            delivery_price = validate_positive_int(form_data['delivery_price'], 'Цена доставки не может быть отрицательной', 'suppliers_page')
            if not delivery_price:
                return redirect(url_for('suppliers_page'))

            Supplier.create(delivery_price=delivery_price, company_name=form_data['company_name'])
            return flash_redirect('Новый поставщик успешно добавлен!', 'success', 'suppliers_page')

        @app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
        def edit_supplier(supplier_id):
            supplier = db.session.query(Supplier).get_or_404(supplier_id)
            if request.method == 'POST':
                form_data = request.form
                error = handle_form_errors(form_data, ['delivery_price', 'company_name'], 'edit_supplier',
                                           supplier=supplier)
                if error:
                    return error

                delivery_price = validate_positive_int(form_data['delivery_price'], 'Цена доставки не может быть отрицательной',
                                                          'edit_supplier') # Убрали supplier=supplier
                if not delivery_price:
                    return render_template('edit_supplier.html', supplier=supplier)

                Supplier.update(supplier_id, delivery_price=delivery_price, company_name=form_data['company_name'])
                return redirect(url_for('suppliers_page'))
            return render_template('edit_supplier.html', supplier=supplier)

        @app.route('/delete_supplier/<int:supplier_id>', methods=['POST'])
        def delete_supplier(supplier_id):
            Supplier.delete(supplier_id)
            return redirect(url_for('suppliers_page'))
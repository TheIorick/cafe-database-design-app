from flask import render_template, redirect, url_for, flash
from models import *


def apply_filters(query, filters):
    """Applies filters to an SQLAlchemy query."""
    for column, value in filters.items():
        if value is not None:
            if isinstance(value, dict):
                min_value, max_value = value.get('min'), value.get('max')
                if min_value and max_value:
                    query = query.filter(column >= min_value, column <= max_value)
                elif min_value:
                    query = query.filter(column >= min_value)
                elif max_value:
                    query = query.filter(column <= max_value)
            else:
                if isinstance(value, str) and column.property.columns[0].type.python_type == str:
                    query = query.filter(column.ilike(f"%{value}%"))
                else:
                    query = query.filter(column == value)
    return query

def validate_positive_int(value, error_message, redirect_target):
    """Validates if a value is a non-negative integer."""
    try:
        value = int(value)
        if value < 0:
            flash(error_message, 'error')
            return False
        return value
    except ValueError:
        flash('Некорректное значение', 'error')
        return False

def render_with_message(template, **kwargs):
    return render_template(template, **kwargs)

def flash_redirect(message, category, redirect_target):
    flash(message, category)
    return redirect(url_for(redirect_target))

def handle_form_errors(form_data, fields, redirect_target, template=None, **kwargs):
    """Handles basic form data validation, flashes error, and either redirects or renders template."""
    if not all(form_data.get(field) for field in fields):
        flash('Заполните все поля!', 'error')
        if template:
            return render_template(template, **kwargs)
        else:
            return redirect(url_for(redirect_target))
    return None  # If no validation error, return None
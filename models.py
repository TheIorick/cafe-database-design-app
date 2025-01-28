from flask import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from psycopg2 import errors

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def read_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def clear_table(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            print(f"Все данные из таблицы {cls.__tablename__} успешно удалены. Удалено строк: {num_rows_deleted}")
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при очистке таблицы {cls.__tablename__}:", e)
            flash(f"Ошибка: очистка {cls.__tablename__} не удалась", "error")

    @classmethod
    def create(cls, **kwargs):
        new_instance = cls(**kwargs)
        db.session.add(new_instance)
        try:
            db.session.commit()
            return new_instance
        except Exception as e:
            db.session.rollback()
            if isinstance(e, errors.UniqueViolation):
                flash(f"Ошибка: запись уже существует", "error")
            elif isinstance(e, errors.StringDataRightTruncation):
                flash(f"Ошибка: строка слишком длинная", "error")
            else:
                flash(f"Ошибка: создание не удалось", "error")
            return None

    @classmethod
    def update(cls, instance_id, **kwargs):
        instance = db.session.query(cls).get(instance_id)
        if not instance:
            flash(f"{cls.__name__} с ID {instance_id} не существует.", 'error')
            return None

        has_changes = False
        for key, value in kwargs.items():
            if value is not None and value != "":
                try:
                    setattr(instance, key, value)
                    has_changes = True
                except Exception as e:
                    db.session.rollback()
                    if isinstance(e, errors.UniqueViolation):
                        flash(f"Ошибка: запись с такими данными уже существует", "error")
                    elif isinstance(e, errors.StringDataRightTruncation):
                        flash(f"Ошибка: длина строки превышает допустимую длину", "error")
                    else:
                        flash(f"Ошибка: обновление не удалось", "error")
                    return None
            else:
                flash(f"Пустое значение для {key}.", "warning")

        if has_changes:
            try:
                db.session.commit()
                flash(f"Запись успешно обновлена.", "success")
            except Exception as e:
                db.session.rollback()
                if isinstance(e, errors.UniqueViolation):
                    flash(f"Ошибка: запись с такими данными уже существует", "error")
                elif isinstance(e, errors.StringDataRightTruncation):
                    flash(f"Ошибка: длина строки превышает допустимую длину", "error")
                else:
                    flash(f"Ошибка: обновление не удалось", "error")
                return None
        else:
            flash(f"Нет изменений для обновления.", "info")
        return instance

    @classmethod
    def delete(cls, instance_id):
        try:
            instance = db.session.query(cls).get(instance_id)
            if instance:
                db.session.delete(instance)
                db.session.commit()
                print(f"{cls.__name__} с ID {instance_id} успешно удален.")
                flash(f"Запись успешно удалена.", "success")
            else:
                print(f"{cls.__name__} с ID {instance_id} не найден.")
                flash(f"Запись не найдена.", "warning")
        except Exception as e:
            db.session.rollback()
            if isinstance(e, errors.ForeignKeyViolation):
                flash(f"Ошибка: нельзя удалить, т.к. есть связи с другими таблицами", "error")
            else:
                print(f"Ошибка при удалении {cls.__name__}:", e)
                flash(f"Ошибка: удаление не удалось", "error")


class Supplier(BaseModel):
    __tablename__ = "suppliers"
    id_suppliers = Column(Integer, primary_key=True)
    delivery_price = Column(Integer, nullable=False)
    company_name = Column(String(55), unique=True, nullable=False)


class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_order"
    id_order = Column(Integer, primary_key=True, autoincrement=True)
    id_products = Column(Integer, ForeignKey('products.id_products', onupdate="CASCADE", ondelete="CASCADE"),
                            nullable=False)
    id_suppliers = Column(Integer, ForeignKey('suppliers.id_suppliers', onupdate="CASCADE", ondelete="CASCADE"),
                             nullable=False)
    quantity_item = Column(Integer, nullable=True)
    price_product = Column(Integer, nullable=False)


class Product(BaseModel):
    __tablename__ = "products"
    id_products = Column(Integer, primary_key=True)
    name_product = Column(String(55), unique=True, nullable=False)
    quantity_in_warehouse = Column(Integer, nullable=False)
    unit = Column(String(255), nullable=False)

class RecipeComposition(BaseModel):
    __tablename__ = 'recipe_composition'
    id_composition = Column(Integer, primary_key=True, autoincrement=True)
    id_products = Column(Integer, ForeignKey('products.id_products'), nullable=False)
    id_recipes = Column(Integer, ForeignKey('recipes.id_recipes'), nullable=False)
    quantity_for_recipe = Column(Integer, nullable=False)


class Recipe(BaseModel):
    __tablename__ = 'recipes'
    id_recipes = Column(Integer, primary_key=True)
    name_recipe = Column(String(55), unique=True, nullable=False)
    cooking_time = Column(Integer, nullable=False)


class Dish(BaseModel):
    __tablename__ = 'dishes'
    id_dish = Column(Integer, primary_key=True)
    id_recipes = Column(Integer, ForeignKey('recipes.id_recipes'), nullable=False)
    category = Column(String(55), nullable=False)
    name_dish = Column(String(55), unique=True, nullable=False)
    price_dish = Column(Integer, nullable=False)

class Menu(BaseModel):
    __tablename__ = 'menu'
    id_menu = Column(Integer, primary_key=True)
    id_dish = Column(Integer, ForeignKey('dishes.id_dish'), nullable=False)
    date_menu = Column(Date, nullable=False)
    menu_name = Column(String(255), unique=True, nullable=False)
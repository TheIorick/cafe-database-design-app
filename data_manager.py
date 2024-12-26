import random
from faker import Faker
from models import db, Supplier, PurchaseOrder, Product, RecipeComposition, Recipe, Dish, Menu
from sqlalchemy import inspect


fake = Faker('ru_RU')


class DataManager:
    def populate_table(self, table_name, n):
        """
        Заполняет указанную таблицу тестовыми данными.

        Args:
            table_name (str): Название таблицы.
            n (int): Количество записей для добавления.
        """
        table_class = self._get_table_class(table_name)
        if not table_class:
            print(f"Таблица с именем '{table_name}' не найдена.")
            return

        for _ in range(n):
            new_record = self._generate_fake_data(table_class)
            if new_record:
                db.session.add(new_record)
        db.session.commit()
        print(f"{n} records added to table '{table_name}'.")

    def clear_table_data(self, table_name, n):
         """
        Удаляет указанное количество записей из таблицы.

        Args:
             table_name (str): Название таблицы.
             n (int): Количество записей для удаления.
        """
         table_class = self._get_table_class(table_name)
         if not table_class:
            print(f"Таблица с именем '{table_name}' не найдена.")
            return

         try:
            records_to_delete = table_class.query.limit(n).all()
            if not records_to_delete:
              print(f"Нет данных для удаления в таблице '{table_name}'.")
              return
            for record in records_to_delete:
              db.session.delete(record)
            db.session.commit()
            print(f"{len(records_to_delete)} records removed from '{table_name}'.")
         except Exception as e:
            db.session.rollback()
            print(f"Ошибка при удалении данных из таблицы '{table_name}': {e}")
    def clear_all_tables(self):
        """
        Очищает все таблицы в базе данных, соблюдая порядок зависимостей.
        """
        table_classes = [Menu, Dish, RecipeComposition, PurchaseOrder,Supplier,Product, Recipe]
        for table_class in table_classes:
            table_class.clear_table()
        print("Все таблицы успешно очищены.")


    def _get_table_class(self, table_name):
        """
        Возвращает класс модели для указанного имени таблицы.

        Args:
            table_name (str): Имя таблицы.

        Returns:
            class: Класс модели, соответствующий имени таблицы, или None, если не найден.
        """
        table_classes = {
            "suppliers": Supplier,
            "purchase_order": PurchaseOrder,
            "products": Product,
            "recipe_composition": RecipeComposition,
            "recipes": Recipe,
            "dishes": Dish,
            "menu": Menu,
        }
        return table_classes.get(table_name.lower())

    def _generate_fake_data(self, table_class):
        """
         Генерирует фейковые данные для модели.

         Args:
             table_class (class): Класс модели SQLAlchemy.

         Returns:
             object: Объект модели с фейковыми данными, или None если возникла ошибка
         """

        if table_class == Supplier:
             return Supplier(
                 delivery_price=random.randint(1000, 10000),
                 company_name=fake.company()
             )
        elif table_class == PurchaseOrder:
            # Получаем id существующих продуктов и поставщиков
            products = Product.query.all()
            suppliers = Supplier.query.all()
            if not products or not suppliers:
              print("Недостаточно данных в таблицах 'products' или 'suppliers' для создания PurchaseOrder.")
              return None
            return PurchaseOrder(
                id_products=random.choice(products).id_products,
                id_suppliers=random.choice(suppliers).id_suppliers,
                quantity_item=random.randint(1, 100),
                price_product=random.randint(100, 1000)
            )
        elif table_class == Product:
            return Product(
                name_product=fake.unique.sentence(nb_words=4)[:55],  # <-- Изменено на sentence
                quantity_in_warehouse=random.randint(10, 1000),
                unit=random.choice(['кг', 'шт', 'л'])
            )
        elif table_class == RecipeComposition:
            products = Product.query.all()
            recipes = Recipe.query.all()
            if not products or not recipes:
                print("Недостаточно данных в таблицах 'products' или 'recipes' для создания RecipeComposition.")
                return None
            return RecipeComposition(
                 id_products=random.choice(products).id_products,
                 id_recipes=random.choice(recipes).id_recipes,
                 quantity_for_recipe=random.randint(1, 50)
             )
        elif table_class == Recipe:
             return Recipe(
                 name_recipe=fake.unique.sentence(nb_words=3),
                 cooking_time=random.randint(10, 120)
             )
        elif table_class == Dish:
            recipes = Recipe.query.all()
            if not recipes:
                print("Недостаточно данных в таблице 'recipes' для создания Dish.")
                return None
            return Dish(
                id_recipes=random.choice(recipes).id_recipes,
                category=random.choice(["Завтрак", "Обед", "Ужин"]),
                name_dish=fake.unique.sentence(nb_words=3),
                price_dish=random.randint(100, 1000)
            )
        elif table_class == Menu:
             dishes = Dish.query.all()
             if not dishes:
               print("Недостаточно данных в таблице 'dishes' для создания Menu.")
               return None
             return Menu(
                 id_dish=random.choice(dishes).id_dish,
                 date_menu=fake.date_this_year(),
                 menu_name=fake.unique.sentence(nb_words=3)
            )
        return None
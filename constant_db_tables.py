class ConstantDBTables:
    SUPPLIERS_TABLE = "suppliers"
    ID_SUPPLIERS = "id_suppliers"
    PRICE_SERVICES = "price_services"
    COMPANY_NAME = "company_name"

    PURCHASE_ORDER_TABLE = "purchase_order"
    ID_ORDER = "id_order"
    COST_DELIVERY_VALUE = "cost_delivery_value"
    PAYMENT_METHOD = "payment_method"

    PRODUCTS_TABLE = "products"
    ID_PRODUCTS = "id_products"
    NAME_PRODUCTS = "name_products"
    QUANTITY_PRODUCTS = "quantity_in_warehouse"

    PRODUCTS_RECIPES_TABLE = "products_recipes"
    QUANTITY_FOR_RECIPE = "quantity_for_recipe"

    RECIPES_TABLE = "recipes"
    ID_RECIPES = "id_recipes"
    NAME_RECIPES = "name_recipes"
    COOKING_TIME = "cooking_time"

    DISHES_TABLE = "dishes"
    ID_DISH = "id_dish"
    CATEGORY = "category"
    NAME_DISH = "name_dish"

    DISHES_MENU_TABLE = "dishes_menu"
    PRICE = "price"

    MENU_TABLE = "menu"
    ID_MENU = "id_menu"
    DATE_OF_ESTABLISHMENT = "date_of_establishment"

    USER_TABLE = "user"
    ID_USER = "id_user"
    NAME = "username"
    PASS_HASH = "pass_hash"
    ROLE = "change_role"

    ROLE_TABLE = "role"
    ID_ROlE = "id_role"
    NAME_ROLE = "name_role"

    USER_ROLE = "user_role"
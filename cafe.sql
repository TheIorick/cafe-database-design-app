
CREATE TABLE "suppliers" (
	"id_suppliers" serial NOT NULL UNIQUE,
	"delivery_price" int NOT NULL,
	"company_name" varchar(55) NOT NULL UNIQUE,
	PRIMARY KEY("id_suppliers")
);


CREATE TABLE "purchase_order" (
	"id_products" serial NOT NULL UNIQUE,
	"id_suppliers" int NOT NULL,
	"quantity_item" int,
	"price_product" int NOT NULL,
	PRIMARY KEY("id_products", "id_suppliers")
);


CREATE TABLE "products" (
	"id_products" serial NOT NULL UNIQUE,
	"name_product" varchar(55) NOT NULL UNIQUE,
	"quantity_in_warehouse" int,
	"unit" varchar(255) NOT NULL,
	PRIMARY KEY("id_products")
);


CREATE TABLE "products_recipes" (
	"id_products" int NOT NULL,
	"id_recipes" int NOT NULL,
	"quantity_for_recipe" int NOT NULL,
	PRIMARY KEY("id_products", "id_recipes")
);


CREATE TABLE "recipes" (
	"id_recipes" serial NOT NULL UNIQUE,
	"name_dish" varchar(55) NOT NULL UNIQUE,
	"cooking_time" int NOT NULL,
	PRIMARY KEY("id_recipes")
);


CREATE TABLE "dishes" (
	"id_dish" serial NOT NULL UNIQUE,
	"id_recipes" int NOT NULL,
	"category" varchar(55) NOT NULL,
	"name_dish" varchar(55) NOT NULL UNIQUE,
	"price_dish" int NOT NULL,
	PRIMARY KEY("id_dish")
);


CREATE TABLE "menu" (
	"id_menu" serial NOT NULL UNIQUE,
	"id_dish" int NOT NULL,
	"date_menu" date NOT NULL,
	"menu_name" varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY("id_menu")
);


ALTER TABLE "products_recipes"
ADD FOREIGN KEY("id_recipes") REFERENCES "recipes"("id_recipes")
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "dishes"
ADD FOREIGN KEY("id_recipes") REFERENCES "recipes"("id_recipes")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "products_recipes"
ADD FOREIGN KEY("id_products") REFERENCES "products"("id_products")
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "purchase_order"
ADD FOREIGN KEY("id_suppliers") REFERENCES "suppliers"("id_suppliers")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "purchase_order"
ADD FOREIGN KEY("id_products") REFERENCES "products"("id_products")
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "menu"
ADD FOREIGN KEY("id_dish") REFERENCES "dishes"("id_dish")
ON UPDATE NO ACTION ON DELETE NO ACTION;
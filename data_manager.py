import random

import fake

from models import db, Supplier


class DataManager:
    def populate_suppliers(self, n):
        for _ in range(n):
            supplier = Supplier(
                delivery_price=random.randint(1000, 10000),
                company_name=fake.company()
            )
            db.session.add(supplier)
        db.session.commit()
        print(f"{n} suppliers added to the database.")

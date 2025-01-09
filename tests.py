import os
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from app import app, db
from models import Item

class ItemModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_one_items(self):
        item = Item(name='test item')
        db.session.add(item)
        db.session.commit()
        self.assertEqual(db.get_or_404(Item, 1), item)

    def test_create_one_items_bad_input(self):
        try:
            item = Item()
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            self.assertIn(e, '404')

    def test_get_all_items(self):
        item = Item(name='test item')
        db.session.add(item)
        db.session.commit()
        items = Item.query.all()
        self.assertEqual(len(items), 1)    

    def test_delete_items(self):
        item = Item(name='test item')
        db.session.add(item)
        db.session.commit()
        items = Item.query.all()
        self.assertEqual(len(items), 1)
        db.session.delete(item)
        db.session.commit()
        items = Item.query.all()
        self.assertEqual(len(items), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
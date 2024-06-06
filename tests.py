from unittest import TestCase
from app import app
from models import db, Cupcake

# Use the same database configured in app.py
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()
            self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""
        with self.app.app_context():
            db.session.rollback()
            db.drop_all()
            db.create_all()

    def test_list_cupcakes(self):
        with self.client as client:
            resp = client.get("/api/cupcakes")
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake_id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with self.client as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with self.client as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 201)
            data = resp.json
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']
            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })
            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        with self.client as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(url, json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })
            self.assertEqual(Cupcake.query.count(), 1)

    def test_update_cupcake_missing(self):
        with self.client as client:
            url = f"/api/cupcakes/99999"
            resp = client.patch(url, json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake(self):
        with self.client as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {"message": "Cupcake has been Deleted"})
            self.assertEqual(Cupcake.query.count(), 0)

    def test_delete_cupcake_missing(self):
        with self.client as client:
            url = f"/api/cupcakes/99999"
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 404)

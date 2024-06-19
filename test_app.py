import unittest
from app import app

class ParkingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_parkings(self):
        response = self.app.get('/api/parkings?vehicle_type=car&arriving=2024-06-19T10:00&leaving=2024-06-19T12:00')
        self.assertEqual(response.status_code, 200)
        self.assertIn('locations', response.json)

if __name__ == '__main__':
    unittest.main()

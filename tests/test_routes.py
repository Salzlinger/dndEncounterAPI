import unittest
from app import create_app
import json

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_generate_pdf(self):
        response = self.client.post('/api/generate-pdf', json={"name": "John Doe", "age": 30})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/pdf')

    def test_no_data(self):
        response = self.client.post('/api/generate-pdf', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('No input data provided', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()

from app import app
from unittest import TestCase, main as unittest_main
from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId

sample_car_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_car = {
    'Make': 'Toyota',
    'Model': 'camry',
    'Description': 'an ok car',
    'Color': 'white',
    'Price': '25000'

}
sample_form_data = {
    'Make': sample_car['Make'],
    'Model': sample_car['Model'],
    'Description': sample_car['Description'],
    'Color': sample_car['Color'],
    'Price': sample_car['Price']

    # 'videos': '\n'.join(sample_car['videos'])
}

class PlaylistsTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

def test_index(self):
        """Test the playlists homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'car', result.data)
    
def test_new(self):
        """Test the new playlist creation page."""
        result = self.client.get('/cars/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New car', result.data)

if __name__ == '__main__':
    unittest_main()
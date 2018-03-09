import json
import unittest

from app import app, views


class WeConnectViews(unittest.TestCase):
    """Tests the enpoints contains in views.py"""

    def setUp(self):
        self.bizdb = []
        self.weconnect_test = app.test_client(self)

    def tearDown(self):
        self.bizdb = []

    def test_register_user(self):
        response = self.weconnect_test.post('/api/v1/auth/register', content_type='application/json',
                                            data=json.dumps(dict(first_name='Benedict', last_name='Mwendwa',
                                                                 email='benedict@aol.com', password='password')))
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        self.weconnect_test.post('/api/v1/auth/register', content_type='application/json',
                                 data=json.dumps(dict(first_name='Benedict', last_name='Mwendwa',
                                                      email='benedict@aol.com', password='password')))
        response = self.weconnect_test.post('/api/v1/auth/login', content_type='application/json',
                                            data=json.dumps(dict(email='benedict@aol.com', password='password')))
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        self.weconnect_test.post('/api/v1/auth/register', content_type='application/json',
                                 data=json.dumps(dict(first_name='Benedict', last_name='Mwendwa',
                                                      email='benedict@aol.com', password='password')))
        response = self.weconnect_test.post('/api/v1/auth/reset-password', content_type='application/json',
                                            data=json.dumps(dict(email='benedict@aol.com', password='password',
                                                                 new_password='severus snape')))
        self.assertEqual(response.status_code, 200)

    def test_register_business(self):
        response = self.weconnect_test.post('/api/v1/businesses', content_type='application/json',
                                            data=json.dumps(dict(name='Andela Kenya',
                                                                 location='TRM', category='something',
                                                                 description='something',
                                                                 review=[])))
        self.assertIn(b'Andela Kenya', response.data)
        self.assertIn(b'TRM', response.data)
        self.assertIn(b'something', response.data)
        self.assertEqual(response.status_code, 201)

    def test_get_business(self):
        resp = self.weconnect_test.post('/api/v1/businesses', content_type='application/json',
                                        data=json.dumps(dict(name='Andela Kenya',
                                                             location='TRM', category='something',
                                                             description='something',
                                                             review=[])))
        biz_id = json.loads(resp.get_data())['business']['id']
        response = self.weconnect_test.get('/api/v1/businesses/' + str(biz_id))
        self.assertEqual(response.status_code, 200)

    def test_get_businesses(self):
        self.weconnect_test.post('/api/v1/businesses', content_type='application/json',
                                 data=json.dumps(dict(name='Andela Kenya',
                                                      location='TRM', category='something',
                                                      description='something',
                                                      review=[])))
        response = self.weconnect_test.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)

    def test_delete_business(self):
        resp = self.weconnect_test.post('/api/v1/businesses', content_type='application/json',
                                        data=json.dumps(dict(name='Andela Kenya',
                                                             location='TRM', category='something',
                                                             description='something',
                                                             review=[])))
        biz_id = json.loads(resp.get_data())['business']['id']
        response = self.weconnect_test.delete('/api/v1/businesses/' + str(biz_id))
        self.assertTrue(response.status_code, 200)
        result = self.weconnect_test.get('/api/v1/businesses')
        self.assertEqual(0, len(json.loads(result.data.decode())['businesses']))

    def test_get_reviews(self):
        resp = self.weconnect_test.post('/api/v1/businesses', content_type='application/json',
                                        data=json.dumps(dict(name='Andela Kenya',
                                                             location='TRM', category='something',
                                                             description='something',
                                                             review=[])))
        biz_id = json.loads(resp.data.decode())['business']['id']
        response = self.weconnect_test.post('/api/v1/businesses/' + str(biz_id) + '/reviews',
                                            content_type='application/json',
                                            data=json.dumps(dict(review="Keep it up guys")))
        self.assertTrue(response.status_code, 200)
        response = self.weconnect_test.get('/api/v1/businesses/' + str(biz_id) + '/reviews')
        self.assertTrue(response.status_code, 200)
        response = self.weconnect_test.delete('/api/v1/businesses/' + str(biz_id))

    def test_add_review(self):
        resp = self.weconnect_test.post('/api/v1/businesses', content_type='application/json',
                                        data=json.dumps(dict(name='Andela Kenya',
                                                             location='TRM', category='something',
                                                             description='something',
                                                             review=[])))
        biz_id = json.loads(resp.data.decode())['business']['id']
        response = self.weconnect_test.post('/api/v1/businesses/' + str(biz_id) + '/reviews',
                                            content_type='application/json',
                                            data=json.dumps(dict(review="Keep it up guys")))
        self.assertTrue(response.status_code, 200)
        response = self.weconnect_test.get('/api/v1/businesses/' + str(biz_id) + '/reviews')
        self.assertTrue(response.status_code, 200)
        response = self.weconnect_test.delete('/api/v1/businesses/' + str(biz_id))


if __name__ == '__main__':
    unittest.main()

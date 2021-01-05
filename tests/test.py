import unittest
from django.urls import path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from API import views as api_views
from rest_framework import status


# class TestStringMethods(unittest.TestCase):
#
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

class ClientEventTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('clients_events/', api_views.as_view(), name='clients_events'),
    ]

    def test_post_client_event(self):
        """Ensure we can send an object to the endpoint."""
        url = reverse('clients_events')
        data = {
            "hdrClient": {
                "openHimClientId": "csv-sync-service",
                "name": "csv-sync-service"
            },
            "hdrEvents": [
                {
                    "eventType": "save-service-received",
                    "eventDate": "Dec 29, 2020, 4:33:45 PM",
                    "openHimClientId": "csv-sync-service",
                    "mediatorVersion": "0.1.0",
                    "json": {
                        "messageType": "SVCREC",
                        "orgName": "Masana",
                        "localOrgID": "108627-1",
                        "deptName": "Radiology",
                        "deptID": "80",
                        "patID": "1",
                        "gender": "Male",
                        "dob": "19900131",
                        "medSvcCode": "002923, 00277, 002772",
                        "icd10Code": "A17.8, M60.1",
                        "serviceDate": "20201224"
                    }
                }
            ]
        }

        response = self.client.post(url,data ,format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

# if __name__ == '__main__':
#     unittest.main()

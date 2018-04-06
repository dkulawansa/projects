from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


class EditDistanceTest(TestCase):
    """This class defines the test suite for the editdistance view."""
    def test_api_get_editdistance(self):
        self.client = APIClient()
        self.editdistance_data = {"first_string": "sm", "second_string": "ms"}
        edit_distance_expected = 2
        res = self.response = self.client.put(
            reverse('editdistance-find-edit-distance'),
            self.editdistance_data,
            format="json")
        edit_distance_actual = res.data.get('edit_distance', 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(edit_distance_actual, edit_distance_expected)

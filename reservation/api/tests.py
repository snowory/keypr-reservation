from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from reservation.api.validators import is_overlap


class TestIsOverlap(TestCase):
    """
    is_overlap will return True if at least one of next is True:
        - second range starts within the first range
        - second range ends within the first range
        - second range contains the first range
    """
    def test_given_second_range_starts_within_first_range_is_overlap_return_True(self):
        start_date1 = datetime.strptime('2017-09-27', '%Y-%m-%d').date()
        end_date1 = datetime.strptime('2017-10-10', '%Y-%m-%d').date()

        start_date2 = datetime.strptime('2017-09-21', '%Y-%m-%d').date()
        end_date2 = datetime.strptime('2017-10-10', '%Y-%m-%d').date()

        self.assertTrue(is_overlap(start_date1, start_date2,
                                   end_date1, end_date2))

    def test_given_second_range_ends_within_first_range_is_overlap_return_True(self):
        start_date1 = datetime.strptime('2017-09-27', '%Y-%m-%d').date()
        end_date1 = datetime.strptime('2017-10-10', '%Y-%m-%d').date()

        start_date2 = datetime.strptime('2017-09-21', '%Y-%m-%d').date()
        end_date2 = datetime.strptime('2017-09-29', '%Y-%m-%d').date()

        self.assertTrue(is_overlap(start_date1, start_date2,
                                   end_date1, end_date2))

    def test_given_second_range_contains_first_range_is_overlap_return_True(self):

        start_date1 = datetime.strptime('2017-09-26', '%Y-%m-%d').date()
        end_date1 = datetime.strptime('2017-09-27', '%Y-%m-%d').date()

        start_date2 = datetime.strptime('2017-09-25', '%Y-%m-%d').date()
        end_date2 = datetime.strptime('2017-09-29', '%Y-%m-%d').date()

        self.assertTrue(is_overlap(start_date1, start_date2,
                                   end_date1, end_date2))

    def test_given_end_date_equals_another_booking_start_date_returns_False(self):
        start_date1 = datetime.strptime('2017-09-26', '%Y-%m-%d').date()
        end_date1 = datetime.strptime('2017-09-27', '%Y-%m-%d').date()

        start_date2 = datetime.strptime('2017-09-27', '%Y-%m-%d').date()
        end_date2 = datetime.strptime('2017-09-28', '%Y-%m-%d').date()

        self.assertFalse(is_overlap(start_date1, start_date2,
                                    end_date1, end_date2))

    def test_given_distant_dates_returns_False(self):
        start_date1 = datetime.strptime('2017-01-26', '%Y-%m-%d').date()
        end_date1 = datetime.strptime('2017-01-27', '%Y-%m-%d').date()

        start_date2 = datetime.strptime('2017-09-27', '%Y-%m-%d').date()
        end_date2 = datetime.strptime('2017-09-28', '%Y-%m-%d').date()

        self.assertFalse(is_overlap(start_date1, start_date2,
                                    end_date1, end_date2))


class TestAPI(APITestCase):
    fixtures = ['test_reservations.json', 'test_users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.get(username='happyuser123')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()

    def test_create_reservation(self):
        """
        Ensure we can create a new reservation object.
        """
        url = reverse('reservation-list')
        data = {
            'start_date': '2017-12-25',
            'end_date': '2017-12-28',
            'room_number': 1,
            'first_name': 'Happy',
            'last_name': 'User'

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        pk = response.data['id']
        get_response = self.client.get('/api/reservations/{}/'.format(pk))
        self.assertEqual(get_response.data['first_name'], 'Happy')

    def test_returns_reservation_list(self):
        """
        Ensure we can retrieve a list of reservations.
        """
        response = self.client.get('/api/reservations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_returns_instance(self):
        response = self.client.get('/api/reservations/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['start_date'], '2017-09-25')

    def test_given_valid_date_range_return_not_empty_list(self):
        response = self.client.get(
            '/api/reservations/?start_date__gte=2017-09-24&end_date__lte=2017-09-30')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_given_start_date_greater_than_end_date_returns_empty_list(self):
        response = self.client.get(
            '/api/reservations/?start_date__gte=2017-09-30&end_date__lte=2017-09-26',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_given_start_date_equals_end_date_returns_empty_list(self):
        response = self.client.get(
            '/api/reservations/?start_date__gte=2017-09-30&end_date__lte=2017-09-26',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

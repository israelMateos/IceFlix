"""Module containing tests for check_timeouts() method from Main service."""

import unittest
from unittest.mock import MagicMock
from iceflix.main import Main

RESPONSE_TIME = 30
SERVICE_ID = "test_id"


class CheckTimeoutsTesting(unittest.TestCase):
    """Tests check_timeouts() method from Main service."""

    def setUp(self):
        self.main = Main()

    def tearDown(self):
        self.main.service_timer.cancel()

    def test_unexpired_proxys(self):
        """Tests check_timeouts() method with unexpired proxys saved in
        cache."""
        obj = MagicMock()
        obj.name = 'object'
        self.main.authenticator_services[SERVICE_ID] = [obj, RESPONSE_TIME]
        self.main.catalog_services[SERVICE_ID] = [obj, RESPONSE_TIME]
        self.main.file_services[SERVICE_ID] = [obj, RESPONSE_TIME]
        self.main.check_timeouts()
        self.assertEqual(self.main.authenticator_services[SERVICE_ID][1],
            RESPONSE_TIME - 1)
        self.assertEqual(self.main.catalog_services[SERVICE_ID][1],
            RESPONSE_TIME - 1)
        self.assertEqual(self.main.file_services[SERVICE_ID][1],
            RESPONSE_TIME - 1)

    def test_to_be_expired_proxys(self):
        """Tests check_timeouts() method with proxys which will be expired in
        one second saved in cache."""
        obj = MagicMock()
        obj.name = 'object'
        self.main.authenticator_services[SERVICE_ID] = [obj, 1]
        self.main.catalog_services[SERVICE_ID] = [obj, 1]
        self.main.file_services[SERVICE_ID] = [obj, 1]
        self.main.check_timeouts()
        self.assertFalse(self.main.authenticator_services)
        self.assertFalse(self.main.catalog_services)
        self.assertFalse(self.main.file_services)

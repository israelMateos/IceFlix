"""Module containing tests for newService() method from Main service."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from iceflix.main import Main
import tests.mock_functions

SERVICE_ID = "test_id"
RESPONSE_TIME = 30


class NewServiceTesting(unittest.TestCase):
    """Tests newService() method from Main service."""

    def setUp(self):
        self.main = Main()

    def tearDown(self):
        self.main.service_timer.cancel()

    @patch('IceFlix.AuthenticatorPrx')
    def test_auth_proxy(self, mock_proxy):
        """Tests newService() method with an Authenticator proxy as input."""
        self.assertFalse(self.main.authenticator_services)
        self.main.newService(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.authenticator_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast',
        new=tests.mock_functions.mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx')
    def test_catalog_proxy(self, mock_proxy):
        """Tests newService() method with a MediaCatalog proxy as input."""
        self.assertFalse(self.main.catalog_services)
        self.main.newService(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.catalog_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast',
        new=tests.mock_functions.mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx.checkedCast',
        new=tests.mock_functions.mock_catalog_checked_cast)
    @patch('IceFlix.FileServicePrx')
    def test_file_proxy(self, mock_proxy):
        """Tests newService() method with a FileService proxy as input."""
        self.assertFalse(self.main.file_services)
        self.main.newService(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.file_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast',
        new=tests.mock_functions.mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx.checkedCast',
        new=tests.mock_functions.mock_catalog_checked_cast)
    @patch('IceFlix.FileServicePrx.checkedCast',
        new=tests.mock_functions.mock_file_checked_cast)
    def test_invalid_proxy(self):
        """Tests newService() method with a non-proxy object as input."""
        obj = MagicMock()
        obj.name = 'object'
        self.assertFalse(self.main.authenticator_services)
        self.assertFalse(self.main.catalog_services)
        self.assertFalse(self.main.file_services)
        self.main.newService(obj, SERVICE_ID)
        self.assertFalse(self.main.authenticator_services)
        self.assertFalse(self.main.catalog_services)
        self.assertFalse(self.main.file_services)

    @patch('Ice.ObjectPrx')
    def test_saved_auth_proxy(self, mock_proxy):
        """Tests newService() method with a service_id which has already been
        saved in the cache for Authenticator services."""
        self.assertFalse(self.main.authenticator_services)
        self.main.authenticator_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.main.newService(mock_proxy, SERVICE_ID)
        self.assertFalse(self.main.authenticator_services)

    @patch('Ice.ObjectPrx')
    def test_saved_catalog_proxy(self, mock_proxy):
        """Tests newService() method with a service_id which has already been
        saved in the cache for MediaCatalog services."""
        self.assertFalse(self.main.catalog_services)
        self.main.catalog_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.main.newService(mock_proxy, SERVICE_ID)
        self.assertFalse(self.main.catalog_services)

    @patch('Ice.ObjectPrx')
    def test_saved_file_proxy(self, mock_proxy):
        """Tests newService() method with a service_id which has already been
        saved in the cache for FileService services."""
        self.assertFalse(self.main.file_services)
        self.main.file_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.main.newService(mock_proxy, SERVICE_ID)
        self.assertFalse(self.main.file_services)

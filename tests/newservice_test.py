"""Module containing tests for newService() method from Main service."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from iceflix.main import Main

SERVICE_ID = "test_id"
RESPONSE_TIME = 30

def mock_auth_checked_cast(proxy):
    """Checks if the mock proxy passed as an argument is mocking an
    Authenticator proxy."""
    if proxy.name == 'AuthenticatorPrx':
        return proxy
    return None

def mock_catalog_checked_cast(proxy):
    """Checks if the mock proxy passed as an argument is mocking a
    MediaCatalog proxy."""
    if proxy.name == 'MediaCatalogPrx':
        return proxy
    return None

def mock_file_checked_cast(proxy):
    """Checks if the mock proxy passed as an argument is mocking a
    FileService proxy."""
    if proxy.name == 'FileServicePrx':
        return proxy
    return None


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
        self.main.newService(mock_proxy, SERVICE_ID, None)
        self.assertEqual(self.main.authenticator_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast', new=mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx')
    def test_catalog_proxy(self, mock_proxy):
        """Tests newService() method with a MediaCatalog proxy as input."""
        self.assertFalse(self.main.catalog_services)
        self.main.newService(mock_proxy, SERVICE_ID, None)
        self.assertEqual(self.main.catalog_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast', new=mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx.checkedCast', new=mock_catalog_checked_cast)
    @patch('IceFlix.FileServicePrx')
    def test_file_proxy(self, mock_proxy):
        """Tests newService() method with a FileService proxy as input."""
        self.assertFalse(self.main.file_services)
        self.main.newService(mock_proxy, SERVICE_ID, None)
        self.assertEqual(self.main.file_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast', new=mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx.checkedCast', new=mock_catalog_checked_cast)
    @patch('IceFlix.FileServicePrx.checkedCast', new=mock_file_checked_cast)
    def test_invalid_proxy(self):
        """Tests newService() method with a non-proxy object as input."""
        obj = MagicMock()
        obj.name = 'object'
        self.assertFalse(self.main.authenticator_services)
        self.assertFalse(self.main.catalog_services)
        self.assertFalse(self.main.file_services)
        self.main.newService(obj, SERVICE_ID, None)
        self.assertFalse(self.main.authenticator_services)
        self.assertFalse(self.main.catalog_services)
        self.assertFalse(self.main.file_services)

"""Module containing tests for newService() method from Main service."""

import unittest
from unittest.mock import patch
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
    """Checks if the mock proxy passed as an argument is mocking an
    MediaCatalog proxy."""
    if proxy.name == 'MediaCatalogPrx':
        return proxy
    return None

def mock_file_checked_cast(proxy):
    """Checks if the mock proxy passed as an argument is mocking an
    FileService proxy."""
    if proxy.name == 'FileServicePrx':
        return proxy
    return None


class NewServiceTesting(unittest.TestCase):
    """Tests newService() method from Main service."""

    @patch('IceFlix.AuthenticatorPrx')
    def test_auth_proxy(self, mock_proxy):
        """Tests newService() method with an Authenticator proxy as input."""
        main = Main()
        self.assertFalse(main.authenticator_services)
        main.newService(mock_proxy, SERVICE_ID, None)
        self.assertEqual(main.authenticator_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast', new=mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx')
    def test_catalog_proxy(self, mock_proxy):
        main = Main()
        self.assertFalse(main.catalog_services)
        main.newService(mock_proxy, SERVICE_ID, None)
        self.assertEqual(main.catalog_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    def test_file_proxy(self):
        pass

    def test_invalid_proxy(self):
        pass

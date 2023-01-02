"""Module containing tests for Announcement service class."""

import unittest
from unittest.mock import patch, MagicMock
from iceflix.main import Main, Announcement
import tests.mock_functions

SERVICE_ID = "test_id"
RESPONSE_TIME = 10
NOT_FULL_RESPONSE_TIME = 5


class AnnouncementTesting(unittest.TestCase):
    """Tests methods from Announcement class."""

    def setUp(self):
        self.main = Main()
        self.announcement = Announcement(self.main)

    def tearDown(self):
        self.main.service_timer.cancel()

    @patch('IceFlix.AuthenticatorPrx')
    def test_new_auth_proxy(self, mock_proxy):
        """Tests announce() method with an Authenticator proxy which is not
        saved in cache as input."""
        self.assertFalse(self.main.authenticator_services)
        self.announcement.announce(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.authenticator_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast',
        new=tests.mock_functions.mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx')
    def test_not_saved_catalog_proxy(self, mock_proxy):
        """Tests announce() method with a MediaCatalog proxy which is not
        saved in cache as input."""
        self.assertFalse(self.main.catalog_services)
        self.announcement.announce(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.catalog_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast',
        new=tests.mock_functions.mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx.checkedCast',
        new=tests.mock_functions.mock_catalog_checked_cast)
    @patch('IceFlix.FileServicePrx')
    def test_not_saved_file_proxy(self, mock_proxy):
        """Tests announce() method with a FileService proxy which is not
        saved in cache as input."""
        self.assertFalse(self.main.file_services)
        self.announcement.announce(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.file_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast',
        new=tests.mock_functions.mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx.checkedCast',
        new=tests.mock_functions.mock_catalog_checked_cast)
    @patch('IceFlix.FileServicePrx.checkedCast',
        new=tests.mock_functions.mock_file_checked_cast)
    def test_invalid_proxy(self):
        """Tests announce() method with a non-proxy object as input."""
        obj = MagicMock()
        obj.name = 'object'
        self.assertFalse(self.main.authenticator_services)
        self.assertFalse(self.main.catalog_services)
        self.assertFalse(self.main.file_services)
        self.announcement.announce(obj, SERVICE_ID)
        self.assertFalse(self.main.authenticator_services)
        self.assertFalse(self.main.catalog_services)
        self.assertFalse(self.main.file_services)

    @patch('IceFlix.AuthenticatorPrx')
    def test_saved_auth_proxy(self, mock_proxy):
        """Tests announce() method with an Authenticator proxy which is saved
        in cache as input."""
        self.main.authenticator_services[SERVICE_ID] = [mock_proxy, NOT_FULL_RESPONSE_TIME]
        self.assertEqual(self.main.authenticator_services[SERVICE_ID],
            [mock_proxy, NOT_FULL_RESPONSE_TIME])
        self.announcement.announce(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.authenticator_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast',
        new=tests.mock_functions.mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx')
    def test_saved_catalog_proxy(self, mock_proxy):
        """Tests announce() method with a MediaCatalog proxy which is saved
        in cache as input."""
        self.main.catalog_services[SERVICE_ID] = [mock_proxy, NOT_FULL_RESPONSE_TIME]
        self.assertEqual(self.main.catalog_services[SERVICE_ID],
            [mock_proxy, NOT_FULL_RESPONSE_TIME])
        self.announcement.announce(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.catalog_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])

    @patch('IceFlix.AuthenticatorPrx.checkedCast',
        new=tests.mock_functions.mock_auth_checked_cast)
    @patch('IceFlix.MediaCatalogPrx.checkedCast',
        new=tests.mock_functions.mock_catalog_checked_cast)
    @patch('IceFlix.FileServicePrx')
    def test_saved_file_proxy(self, mock_proxy):
        """Tests announce() method with a FileService proxy which is saved
        in cache as input."""
        self.main.file_services[SERVICE_ID] = [mock_proxy, NOT_FULL_RESPONSE_TIME]
        self.assertEqual(self.main.file_services[SERVICE_ID],
            [mock_proxy, NOT_FULL_RESPONSE_TIME])
        self.announcement.announce(mock_proxy, SERVICE_ID)
        self.assertEqual(self.main.file_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])

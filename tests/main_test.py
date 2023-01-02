"""Module containing tests for Main service class."""

import unittest
from unittest.mock import patch, MagicMock
from iceflix.main import Main
try:
    import IceFlix

except ImportError:
    import os
    import Ice

    Ice.loadSlice(os.path.join(os.path.dirname(__file__), "../iceflix/iceflix.ice"))

SERVICE_ID = "test_id"
RESPONSE_TIME = 30


class GetProxyTesting(unittest.TestCase):
    """Tests getAuthenticator(), getCatalog() and getFileService() methods
    from Main service."""

    def setUp(self):
        self.main = Main()

    def tearDown(self):
        self.main.service_timer.cancel()

    def test_no_services_get_authenticator(self):
        """Test getAuthenticator() method without any Authenticator services
        saved in cache."""
        self.assertFalse(self.main.authenticator_services)
        with self.assertRaises(IceFlix.TemporaryUnavailable):
            self.main.getAuthenticator()

    def test_no_services_get_catalog(self):
        """Test getCatalog() method without any MediaCatalog services saved in
        cache."""
        self.assertFalse(self.main.catalog_services)
        with self.assertRaises(IceFlix.TemporaryUnavailable):
            self.main.getCatalog()

    def test_no_services_get_file_service(self):
        """Test getFileService() method without any Authenticator services
        saved in cache."""
        self.assertFalse(self.main.file_services)
        with self.assertRaises(IceFlix.TemporaryUnavailable):
            self.main.getFileService()

    @patch('IceFlix.AuthenticatorPrx')
    def test_offline_authenticator(self, mock_proxy):
        """Test getAuthenticator() method with only an offline Authenticator
        proxy saved in cache."""
        self.assertFalse(self.main.authenticator_services)
        self.main.authenticator_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.authenticator_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        with patch('IceFlix.AuthenticatorPrx.ice_ping') as mock_ice_ping:
            mock_ice_ping.side_effect = Exception
            with self.assertRaises(IceFlix.TemporaryUnavailable):
                self.main.getAuthenticator()
        self.assertFalse(self.main.authenticator_services)

    @patch('IceFlix.MediaCatalogPrx')
    def test_offline_catalog(self, mock_proxy):
        """Test getCatalog() method with only an offline MediaCatalog proxy
        saved in cache."""
        self.assertFalse(self.main.catalog_services)
        self.main.catalog_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.catalog_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        with patch('IceFlix.MediaCatalogPrx.ice_ping') as mock_ice_ping:
            mock_ice_ping.side_effect = Exception
            with self.assertRaises(IceFlix.TemporaryUnavailable):
                self.main.getCatalog()
        self.assertFalse(self.main.catalog_services)

    @patch('IceFlix.FileServicePrx')
    def test_offline_file_service(self, mock_proxy):
        """Test getFileService() method with only an offline FileService proxy
        saved in cache."""
        self.assertFalse(self.main.file_services)
        self.main.file_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.file_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        with patch('IceFlix.FileServicePrx.ice_ping') as mock_ice_ping:
            mock_ice_ping.side_effect = Exception
            with self.assertRaises(IceFlix.TemporaryUnavailable):
                self.main.getFileService()
        self.assertFalse(self.main.file_services)

    @patch('IceFlix.AuthenticatorPrx')
    def test_online_authenticator(self, mock_proxy):
        """Test getAuthenticator() method with only an online Authenticator
        proxy saved in cache."""
        self.assertFalse(self.main.authenticator_services)
        self.main.authenticator_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.authenticator_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        with patch('IceFlix.AuthenticatorPrx.ice_ping') as mock_ice_ping:
            mock_ice_ping.return_value = None
            self.assertEqual(self.main.getAuthenticator(), mock_proxy)

    @patch('IceFlix.MediaCatalogPrx')
    def test_online_catalog(self, mock_proxy):
        """Test getCatalog() method with only an online MediaCatalog proxy
        saved in cache."""
        self.assertFalse(self.main.catalog_services)
        self.main.catalog_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.catalog_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        with patch('IceFlix.MediaCatalogPrx.ice_ping') as mock_ice_ping:
            mock_ice_ping.return_value = None
            self.assertEqual(self.main.getCatalog(), mock_proxy)

    @patch('IceFlix.FileServicePrx')
    def test_online_file_service(self, mock_proxy):
        """Test getFileService() method with only an online FileService proxy
        saved in cache."""
        self.assertFalse(self.main.file_services)
        self.main.file_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.file_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        with patch('IceFlix.FileServicePrx.ice_ping') as mock_ice_ping:
            mock_ice_ping.return_value = None
            self.assertEqual(self.main.getFileService(), mock_proxy)

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

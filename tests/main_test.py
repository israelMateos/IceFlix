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
RESPONSE_TIME = 10


class MainTesting(unittest.TestCase):
    """Tests methods from Main class."""

    def setUp(self):
        self.main = Main()

    def tearDown(self):
        self.main.service_timer.cancel()

    @patch('IceFlix.AuthenticatorPrx')
    def test_get_authenticator(self, mock_proxy):
        """Test getAuthenticator() method with only an offline Authenticator proxy,
        an online Authenticator proxy and no services saved in cache."""
        self.assertFalse(self.main.authenticator_services)
        with self.assertRaises(IceFlix.TemporaryUnavailable):
            self.main.getAuthenticator()
        self.main.authenticator_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.authenticator_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        online_flag = True
        for i in range(2):
            with patch('IceFlix.AuthenticatorPrx.ice_ping') as mock_ice_ping:
                if online_flag:
                    mock_ice_ping.return_value = None
                    self.assertEqual(self.main.getAuthenticator(), mock_proxy)
                    online_flag = False
                else:
                    mock_ice_ping.side_effect = Exception
                    with self.assertRaises(IceFlix.TemporaryUnavailable):
                        self.main.getAuthenticator()
                    self.assertFalse(self.main.catalog_services)

    @patch('IceFlix.MediaCatalogPrx')
    def test_get_catalog(self, mock_proxy):
        """Test getCatalog() method with an offline MediaCatalog proxy, an
        online MediaCatalog proxy and no services saved in cache."""
        self.assertFalse(self.main.catalog_services)
        self.assertFalse(self.main.catalog_services)
        with self.assertRaises(IceFlix.TemporaryUnavailable):
            self.main.getCatalog()
        self.main.catalog_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.catalog_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        online_flag = True
        for i in range(2):
            with patch('IceFlix.MediaCatalogPrx.ice_ping') as mock_ice_ping:
                if online_flag:
                    mock_ice_ping.return_value = None
                    self.assertEqual(self.main.getCatalog(), mock_proxy)
                    online_flag = False
                else:
                    mock_ice_ping.return_value = None
                    mock_ice_ping.side_effect = Exception
                    with self.assertRaises(IceFlix.TemporaryUnavailable):
                        self.main.getCatalog()
                    self.assertFalse(self.main.catalog_services)

    @patch('IceFlix.FileServicePrx')
    def test_get_file_service(self, mock_proxy):
        """Test getFileService() method with an offline FileService proxy, an
        online FileService proxy and no services saved in cache."""
        self.assertFalse(self.main.file_services)
        with self.assertRaises(IceFlix.TemporaryUnavailable):
            self.main.getFileService()
        self.main.file_services[SERVICE_ID] = [mock_proxy, RESPONSE_TIME]
        self.assertEqual(self.main.file_services[SERVICE_ID],
            [mock_proxy, RESPONSE_TIME])
        online_flag = True
        for i in range(2):
            with patch('IceFlix.FileServicePrx.ice_ping') as mock_ice_ping:
                if online_flag:
                    mock_ice_ping.return_value = None
                    self.assertEqual(self.main.getFileService(), mock_proxy)
                    online_flag = False
                else:
                    mock_ice_ping.side_effect = Exception
                    with self.assertRaises(IceFlix.TemporaryUnavailable):
                        self.main.getFileService()
                    self.assertFalse(self.main.file_services)

    def test_check_timeouts(self):
        """Tests check_timeouts() method with both unexpired proxys and proxys
        which will be expired in one second saved in cache."""
        obj = MagicMock()
        obj.name = 'object'
        test_times = [RESPONSE_TIME, 1]
        for test_time in test_times:
            self.main.authenticator_services[SERVICE_ID] = [obj, test_time]
            self.main.catalog_services[SERVICE_ID] = [obj, test_time]
            self.main.file_services[SERVICE_ID] = [obj, test_time]
            self.main.check_timeouts()
            if test_time == RESPONSE_TIME:
                self.assertEqual(self.main.authenticator_services[SERVICE_ID][1],
                    test_time - 1)
                self.assertEqual(self.main.catalog_services[SERVICE_ID][1],
                    test_time - 1)
                self.assertEqual(self.main.file_services[SERVICE_ID][1],
                    test_time - 1)
            else:
                self.assertFalse(self.main.authenticator_services)
                self.assertFalse(self.main.catalog_services)
                self.assertFalse(self.main.file_services)

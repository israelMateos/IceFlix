"""Module containing tests for getAuthenticator(), getCatalog() and
getFileService() methods from Main service."""

import unittest
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
            self.main.getAuthenticator(None)

    def test_no_services_get_catalog(self):
        """Test getCatalog() method without any MediaCatalog services saved in
        cache."""
        self.assertFalse(self.main.catalog_services)
        with self.assertRaises(IceFlix.TemporaryUnavailable):
            self.main.getCatalog(None)

    def test_no_services_get_file_service(self):
        """Test getFileService() method without any Authenticator services
        saved in cache."""
        self.assertFalse(self.main.file_services)
        with self.assertRaises(IceFlix.TemporaryUnavailable):
            self.main.getFileService(None)

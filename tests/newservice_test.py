#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from iceflix.main import Main

SERVICE_ID = "test_id"
RESPONSE_TIME = 30

class NewServiceTesting(unittest.TestCase):
    @patch('IceFlix.AuthenticatorPrx')
    def test_auth_proxy(self, mock_proxy):
        main = Main()
        self.assertFalse(main.authenticator_services)
        main.newService(mock_proxy, SERVICE_ID, None)
        self.assertEqual(main.authenticator_services[SERVICE_ID],
            [mock_proxy.checkedCast(), RESPONSE_TIME])

    def test_catalog_proxy(self):
        pass

    def test_file_proxy(self):
        pass

    def test_invalid_proxy(self):
        pass

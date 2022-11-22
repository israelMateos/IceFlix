"""Module containing a template for a main service."""

import logging

import Ice

import IceFlix  # pylint:disable=import-error


class Main(IceFlix.Main):
    """Servant for the IceFlix.Main interface.

    Disclaimer: this is demo code, it lacks of most of the needed methods
    for this interface. Use it with caution
    """

    authenticator_services = {}
    catalog_services = {}
    file_services = {}

    def getAuthenticator(self, current):  # pylint:disable=invalid-name, unused-argument
        "Return the stored Authenticator proxy."
        # TODO: implement
        return None

    def getCatalog(self, current):  # pylint:disable=invalid-name, unused-argument
        "Return the stored MediaCatalog proxy."
        # TODO: implement
        return None

    def newService(self, proxy, service_id, current):  # pylint:disable=invalid-name, unused-argument
        "Receive a proxy of a new service."
        # TODO: Resolver error de PyLint para variables estáticas
        if (checked_proxy := IceFlix.AuthenticatorPrx.checkedCast(proxy)) is not None:
            authenticator_services[service_id] = checked_proxy
        elif (checked_proxy := IceFlix.MediaCatalogPrx.checkedCast(proxy)) is not None:
            catalog_services[service_id] = checked_proxy
        elif (checked_proxy := IceFlix.FileServicePrx.checkedCast(proxy)) is not None:
            file_services[service_id] = checked_proxy
        else:
            print("Tipo del proxy del servicio %s inválido", service_id)
        return

    def announce(self, proxy, service_id, current):  # pylint:disable=invalid-name, unused-argument
        "Announcements handler."
        # TODO: implement
        return


class MainApp(Ice.Application):
    """Example Ice.Application for a Main service."""

    def __init__(self):
        super().__init__()
        self.servant = Main()
        self.proxy = None
        self.adapter = None

    def run(self, args):
        """Run the application, adding the needed objects to the adapter."""
        logging.info("Running Main application")
        comm = self.communicator()
        self.adapter = comm.createObjectAdapter("MainAdapter")
        self.adapter.activate()

        self.proxy = self.adapter.addWithUUID(self.servant)

        self.shutdownOnInterrupt()
        comm.waitForShutdown()

        return 0

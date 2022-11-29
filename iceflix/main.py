"""Module containing a template for a main service."""

import logging

from threading import Timer

import Ice

import IceFlix  # pylint:disable=import-error


class RepeatTimer(Timer):
    """Timer that repeats the function at the end of each interval instead of
    executing it once."""
    def run(self):
        "Execute the function passed to the timer when it is time"
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Main(IceFlix.Main):
    """Servant for the IceFlix.Main interface.

    Disclaimer: this is demo code, it lacks of most of the needed methods
    for this interface. Use it with caution
    """

    def __init__(self):
        self.authenticator_services = {}
        self.catalog_services = {}
        self.file_services = {}
        self.service_timer = RepeatTimer(1.0, self.check_timeouts)
        self.service_timer.start()

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
        # TODO: Probar funcionamiento correcto
        if (checked_proxy := IceFlix.AuthenticatorPrx.checkedCast(proxy)) is not None:
            if service_id not in self.authenticator_services:
                self.authenticator_services[service_id] = [checked_proxy, 30]
        elif (checked_proxy := IceFlix.MediaCatalogPrx.checkedCast(proxy)) is not None:
            if service_id not in self.catalog_services:
                self.catalog_services[service_id] = [checked_proxy, 30]
        elif (checked_proxy := IceFlix.FileServicePrx.checkedCast(proxy)) is not None:
            if service_id not in self.file_services:
                self.file_services[service_id] = [checked_proxy, 30]
        else:
            print(f"Tipo del proxy del servicio {service_id} inválido")

    def announce(self, proxy, service_id, current):  # pylint:disable=invalid-name, unused-argument
        "Announcements handler."
        # TODO: implement
        return

    def check_timeouts(self):
        """Decrements the wait times of services stored and removes them if it
        reaches 0."""
        for service_id, proxy in self.authenticator_services.copy().items():
            proxy[1] -= 1
            if proxy[1] == 0:
                self.authenticator_services.pop(service_id)
        for service_id, proxy in self.catalog_services.copy().items():
            proxy[1] -= 1
            if proxy[1] == 0:
                self.catalog_services.pop(service_id)
        for service_id, proxy in self.file_services.copy().items():
            proxy[1] -= 1
            if proxy[1] == 0:
                self.file_services.pop(service_id)


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

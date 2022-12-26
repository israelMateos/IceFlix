"""Module containing a template for a main service."""

import logging

from threading import Timer

import Ice
import IceStorm

import IceFlix  # pylint:disable=import-error

RESPONSE_TIME = 10


class RepeatTimer(Timer):
    """Timer that repeats the function at the end of each interval instead of
    executing it once."""

    def run(self):
        "Execute the function passed to the timer when it is time"
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Announcement(IceFlix.Announcement):
    """Servant for the IceFlix.Announcement interface."""

    def announce(self, proxy, service_id, current=None):  # pylint:disable=invalid-name, unused-argument
        "Announcements handler."
        logging.info("Service '%s' announced", service_id)
        if (checked_proxy := IceFlix.AuthenticatorPrx.checkedCast(proxy)) is not None:
            if service_id in self.authenticator_services:
                self.authenticator_services[service_id][1] = RESPONSE_TIME
                logging.info("Service '%s' time renewed", service_id)
            else:
                self.authenticator_services[service_id] = [checked_proxy, RESPONSE_TIME]
                logging.info("Service '%s' added to cache: Authenticator", service_id)
        elif IceFlix.MediaCatalogPrx.checkedCast(proxy) is not None:
            if service_id in self.catalog_services:
                self.catalog_services[service_id][1] = RESPONSE_TIME
                logging.info("Service '%s' time renewed", service_id)
            else:
                self.catalog_services[service_id] = [checked_proxy, RESPONSE_TIME]
                logging.info("Service '%s' added to cache: MediaCatalog", service_id)
        elif IceFlix.FileServicePrx.checkedCast(proxy) is not None:
            if service_id in self.file_services:
                self.file_services[service_id][1] = RESPONSE_TIME
                logging.info("Service '%s' time renewed", service_id)
            else:
                self.file_services[service_id] = [checked_proxy, RESPONSE_TIME]
                logging.info("Service '%s' added to cache: FileService", service_id)


class Main(IceFlix.Main):
    """Servant for the IceFlix.Main interface."""

    def __init__(self):
        self.authenticator_services = {}
        self.catalog_services = {}
        self.file_services = {}
        self.service_timer = RepeatTimer(1.0, self.check_timeouts)
        self.service_timer.start()

    def getAuthenticator(self, current=None):  # pylint:disable=invalid-name, unused-argument
        "Return the stored Authenticator proxy."
        if self.authenticator_services:
            while True:
                service_id, proxy = list(self.authenticator_services.items())[0]
                try:
                    proxy[0].ice_ping()
                    logging.info("getAuthenticator: service '%s' returned", service_id)
                    return proxy[0]
                except Exception as exc:
                    self.authenticator_services.pop(service_id)
                    logging.info("Service '%s' deleted from cache: offline", service_id)
                    if not self.authenticator_services:
                        raise IceFlix.TemporaryUnavailable() from exc
        raise IceFlix.TemporaryUnavailable()

    def getCatalog(self, current=None):  # pylint:disable=invalid-name, unused-argument
        "Return the stored MediaCatalog proxy."
        if self.catalog_services:
            while True:
                service_id, proxy = list(self.catalog_services.items())[0]
                try:
                    proxy[0].ice_ping()
                    logging.info("getCatalog: service '%s' returned", service_id)
                    return proxy[0]
                except Exception as exc:
                    self.catalog_services.pop(service_id)
                    logging.info("Service '%s' deleted from cache: offline", service_id)
                    if not self.catalog_services:
                        raise IceFlix.TemporaryUnavailable() from exc
        raise IceFlix.TemporaryUnavailable()

    def getFileService(self, current=None):  # pylint:disable=invalid-name, unused-argument
        "Return the stored FileService proxy."
        if self.file_services:
            while True:
                service_id, proxy = list(self.file_services.items())[0]
                try:
                    proxy[0].ice_ping()
                    logging.info("getFileService: service '%s' returned", service_id)
                    return proxy[0]
                except Exception as exc:
                    self.file_services.pop(service_id)
                    logging.info("Service '%s' deleted from cache: offline", service_id)
                    if not self.file_services:
                        raise IceFlix.TemporaryUnavailable() from exc
        raise IceFlix.TemporaryUnavailable()

    def check_timeouts(self):
        """Decrements the wait times of services stored and removes them if it
        reaches 0."""
        for service_id, proxy_and_time in self.authenticator_services.copy().items():
            proxy_and_time[1] -= 1
            if proxy_and_time[1] == 0:
                self.authenticator_services.pop(service_id)
                logging.info("Service '%s' deleted from cache: time expired", service_id)
        for service_id, proxy_and_time in self.catalog_services.copy().items():
            proxy_and_time[1] -= 1
            if proxy_and_time[1] == 0:
                self.catalog_services.pop(service_id)
                logging.info("Service '%s' deleted from cache: time expired", service_id)
        for service_id, proxy_and_time in self.file_services.copy().items():
            proxy_and_time[1] -= 1
            if proxy_and_time[1] == 0:
                self.file_services.pop(service_id)
                logging.info("Service '%s' deleted from cache: time expired", service_id)


class MainApp(Ice.Application):
    """Ice.Application for a Main service."""

    def __init__(self):
        super().__init__()
        self.servant = Main()
        self.proxy = None
        self.adapter = None
    
    def get_topic(self, topic_name):
        """Returns proxy for the TopicManager from IceStorm."""
        topic_manager = self.communicator().propertyToProxy(IceStorm.TopicManager.Proxy)
        topic_manager = IceStorm.TopicManagerPrx.checkedCast(topic_manager)

        try:
            return topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            return topic_manager.create(topic_name)

    def get_publisher(self, topic):
        publisher = topic.getPublisher()
        return IceFlix.AnnouncementPrx.uncheckedCast(publisher)
    
    def run(self, argv):
        """Run the application, adding the needed objects to the adapter."""
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print("Invalid proxy")
            return 2

        logging.info("Running Main application")
        comm = self.communicator()
        self.adapter = comm.createObjectAdapter("MainAdapter")
        self.adapter.activate()
        self.proxy = self.adapter.addWithUUID(self.servant)
        logging.info("Main proxy is '%s'", self.proxy)

        # Publish announcements
        topic = self.get_topic("Announcements")
        announcement = self.get_publisher(topic)
        announcements_timer = RepeatTimer(5.0, announcement.announce, \
            [self.proxy, self.proxy.ice_getIdentity()])
        announcements_timer.start()

        qos = {}
        topic.subscribeAndGetPublisher(qos, self.proxy)
        logging.info("Waiting events... '{}'".format(self.proxy))

        self.shutdownOnInterrupt()
        comm.waitForShutdown()

        topic.unsubscribe(self.proxy)

        return 0

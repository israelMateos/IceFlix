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

    def __init__(self, main_servant):
        self.main_servant = main_servant

    def announce(self, proxy, service_id, current=None):  # pylint:disable=invalid-name, unused-argument
        "Announcements handler."
        logging.info("Service '%s' announced", service_id)
        if (checked_proxy := IceFlix.AuthenticatorPrx.checkedCast(proxy)) is not None:
            if service_id in self.main_servant.main_servant.authenticator_services:
                self.main_servant.authenticator_services[service_id][1] = RESPONSE_TIME
                logging.info("Service '%s' time renewed", service_id)
            else:
                self.main_servant.authenticator_services[service_id] = [checked_proxy,
                    RESPONSE_TIME]
                logging.info("Service '%s' added to cache: Authenticator", service_id)
        elif (checked_proxy := IceFlix.MediaCatalogPrx.checkedCast(proxy)) is not None:
            if service_id in self.main_servant.catalog_services:
                self.main_servant.catalog_services[service_id][1] = RESPONSE_TIME
                logging.info("Service '%s' time renewed", service_id)
            else:
                self.main_servant.catalog_services[service_id] = [checked_proxy, RESPONSE_TIME]
                logging.info("Service '%s' added to cache: MediaCatalog", service_id)
        elif (checked_proxy := IceFlix.FileServicePrx.checkedCast(proxy)) is not None:
            if service_id in self.main_servant.file_services:
                self.main_servant.file_services[service_id][1] = RESPONSE_TIME
                logging.info("Service '%s' time renewed", service_id)
            else:
                self.main_servant.file_services[service_id] = [checked_proxy, RESPONSE_TIME]
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
        self.main_proxy = None
        self.announcement_proxy = None
        self.adapter = None

    def get_topic(self, topic_name):
        """Returns proxy for the TopicManager from IceStorm."""
        topic_manager = self.communicator().propertyToProxy('IceStorm.TopicManager.Proxy')
        topic_manager = IceStorm.TopicManagerPrx.checkedCast(topic_manager)  # pylint:disable=no-member

        try:
            return topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:  # pylint:disable=no-member
            return topic_manager.create(topic_name)

    def run(self, args):
        """Run the application, adding the needed objects to the adapter."""

        logging.info("Running Main application")
        comm = self.communicator()
        self.adapter = comm.createObjectAdapter("MainAdapter")
        self.adapter.activate()
        self.main_proxy = self.adapter.addWithUUID(self.servant)
        logging.info("Main proxy is '%s'", self.main_proxy)

        # Publish announcements
        topic = self.get_topic("Announcements")
        announcement_publisher = IceFlix.AnnouncementPrx.uncheckedCast(topic.getPublisher())
        announcements_timer = RepeatTimer(5.0, announcement_publisher.announce, \
            [self.main_proxy, self.main_proxy.ice_getIdentity().name])
        announcements_timer.start()

        # Subscribe and receive announcements
        announcement_subscriber = Announcement(self.servant)
        self.announcement_proxy = self.adapter.addWithUUID(announcement_subscriber)
        logging.info("Announcement proxy is '%s'", self.announcement_proxy)
        qos = {}
        topic.subscribeAndGetPublisher(qos, self.announcement_proxy)
        logging.info("Waiting events... '%s'", self.announcement_proxy)

        self.shutdownOnInterrupt()
        comm.waitForShutdown()

        topic.unsubscribe(self.announcement_proxy)

        return 0

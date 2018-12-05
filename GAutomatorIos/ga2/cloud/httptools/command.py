#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

class Command(object):
    """
    Defines constants for the standard WebDriver commands.

    While these constants have no meaning in and of themselves, they are
    used to marshal commands through a service that implements WebDriver's
    remote wire protocol:

        https://github.com/SeleniumHQ/selenium/wiki/JsonWireProtocol

    """

    # Keep in sync with org.openqa.selenium.remote.DriverCommand

    TASK_GET = "task"
    TASK_POST = "task"

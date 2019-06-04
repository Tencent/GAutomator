
from ga2.cloud import platform_helper
from ga2.common.logger_config import logger
from ga2.common.singleton import singleton

@singleton
class Reporter():
    def __init__(self):
        self.errs = []
        self.image_id = 10000
        self.platform_client = platform_helper.get_platform_client()

    def screenshot(self):
        try:
            self.image_id += 1
            response = self.platform_client.take_screenshot()
            if response:
                return response
        except Exception as e:
            logger.exception(e)

    def screenshot_with_mark( self, width, height, x, y, locator_name="point"):
        try:
            self.image_id += 1
            if 0<x<1 and 0<y<1:
                x=int(x*width)
                y=int(y*height)
            response = self.platform_client.touch_capture(width, height, x, y, locator_name)
            if response:
                return response
        except Exception as e:
            logger.exception(e)

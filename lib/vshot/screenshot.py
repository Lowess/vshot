#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import time

from PIL import Image

logger = logging.getLogger(__name__)


def above_the_fold_screenshot(driver, file):
    """
    Take a screenshot of the top of webpage.
    """
    # Get window and viewport dimensions
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")

    # Move back to top
    driver.execute_script("window.scrollTo(0, 0)")

    logger.debug(
        "Total: ({0}, {1}), Viewport: ({2},{3})".format(
            total_width, total_height, viewport_width, viewport_height
        )
    )

    stitched_image = Image.new("RGB", (viewport_width, viewport_height))

    driver.get_screenshot_as_file(file)

    logger.info("Finishing chrome full page screenshot workaround...")
    return True


def fullpage_screenshot(driver, file):
    """
    Take a screenshot of the full webpage by scrolling from top to bottom.
    Taken from Stackoverflow:
        https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
    """
    logger.info("Starting chrome full page screenshot workaround ...")

    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    logger.debug(
        "Total: ({0}, {1}), Viewport: ({2},{3})".format(
            total_width, total_height, viewport_width, viewport_height
        )
    )
    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            logger.debug(
                "Appending rectangle ({0},{1},{2},{3})".format(
                    ii, i, top_width, top_height
                )
            )
            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    stitched_image = Image.new("RGB", (total_width, total_height))
    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script(
                "window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1])
            )
            logger.debug("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)

        file_name = "part_{0}.png".format(part)
        logger.debug("Capturing {0} ...".format(file_name))

        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        logger.debug(
            "Adding to stitched image with offset ({0}, {1})".format(
                offset[0], offset[1]
            )
        )
        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle

    stitched_image.save(file)
    logger.debug("Finishing chrome full page screenshot workaround...")
    return True

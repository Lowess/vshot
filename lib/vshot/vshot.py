#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from os.path import expanduser
from typing import Dict
from urllib.parse import quote_plus, urlparse
from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from vshot.screenshot import above_the_fold_screenshot, fullpage_screenshot
from vshot.storage import AwsUtils

logger = logging.getLogger(__name__)


class VShot:
    """
    Verity Screenshot
    """

    def __init__(self, nojs: bool = False):

        # Create storage folder for ~/.vshot
        self._home = f"{expanduser('~')}/.vshot"
        # self._home = "~/.vshot"
        self._makedirs(self._home)

        # Location where shots will be stored
        self._store = f"{self._home}/shots"
        self._makedirs(self._store)

        # Defines wheather JS should be enabled or disabled
        self._nojs = nojs

        # Chrome webdriver configuration
        chrome_options = Options()
        chrome_options.add_argument("--kiosk")

        if self._nojs:
            chrome_options.add_experimental_option(
                "prefs", {"profile.managed_default_content_settings.javascript": 2}
            )

        self._driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options)

    def _makedirs(self, path: str) -> None:
        if not os.path.exists(path):
            # logger.info(f"Directory {path} has been created.")
            os.makedirs(path)

    def teardown(self) -> None:
        self._driver.close()
        self._driver.quit()

    def save_html(self, url="https://www.w3schools.com/") -> str:
        """
        Save HTML DOM object to file
        """

        # Create the shot directory for this URL
        shotdir = f"{self._store}/{quote_plus(url)}"
        self._makedirs(shotdir)

        self._driver.get(url)
        # Write HTML page source
        html = f"{shotdir}/{ 'js-off' if self._nojs else 'js-on' }-page.html"

        with open(html, "w") as f:
            f.write(self._driver.page_source)

        return html

    def save_s3(self, url: str, s3_uri: str, shots: Dict[str, str]):

        o = urlparse(s3_uri, allow_fragments=False)
        (scheme, s3_bucket, s3_path) = o.scheme, o.netloc, o.path

        # Basic validation
        if scheme != "s3":
            raise ValueError(
                "s3_uri provided is invalid it should be: s3://bucket_name/some/path"
            )

        logger.info(f"scheme {scheme} | s3 {s3_bucket} | {s3_path}")

        for name, shot in shots.items():
            logger.info(f"Uploading '{name}' shot to S3 {s3_bucket}{s3_path}/{name}")
            AwsUtils.put_content_in_s3(
                s3_bucket, f"{s3_path[1:]}/{quote_plus(url)}/{name}", open(shot, "rb")
            )

    def take_screenshot(self, url="https://www.w3schools.com/", size="fullpage") -> str:
        """
        Generate document-height screenshot
        """

        # Create the shot directory for this URL
        shotdir = f"{self._store}/{quote_plus(url)}"
        self._makedirs(shotdir)

        self._driver.get(url)

        shotdest = None

        if size == "fullpage":
            shotdest = f"{shotdir}/{ 'js-off' if self._nojs else 'js-on' }-fullpage.png"
            fullpage_screenshot(
                self._driver,
                shotdest,
            )
        else:
            shotdest = (
                f"{shotdir}/{ 'js-off' if self._nojs else 'js-on' }-abovethefold.png"
            )

            above_the_fold_screenshot(
                self._driver,
                shotdest,
            )
        return shotdest

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import os
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from conf import config
from core import cron

# configure logging
def configure_logging(level):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter("[%(asctime)s] %(name)s %(levelname)s %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    root_logger.addHandler(ch)


def popforward(config_pathname):

    # configure logging
    logger = logging.getLogger(__name__)
    configure_logging(logging.INFO)

    logger.info("Start popforward application")
    config.initialize(config_pathname)

    # cron email fetcher
    scheduler = BackgroundScheduler()
    scheduler.add_job(cron.pop, "interval", seconds=config.getInt(config.POP3_POLLING))
    scheduler.start()

    print("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

    logger.info("Stop popforward application")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config path name")
    args = parser.parse_args()
    popforward(args.config)

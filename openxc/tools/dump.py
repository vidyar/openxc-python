"""
This module contains the methods for the ``openxc-dump`` command line program.

`main` is executed when ``openxc-dump`` is run, and all other callables in this
module are internal only.
"""
from __future__ import absolute_import

import argparse
import time

from openxc.formats.json import JsonFormatter
from .common import device_options, configure_logging, select_device

def receive(message, **kwargs):
    message['timestamp'] = time.time()
    print(JsonFormatter.serialize(message))


def parse_options():
    parser = argparse.ArgumentParser(
            description="View a raw OpenXC data stream",
            parents=[device_options()])

    arguments = parser.parse_args()
    return arguments


def main():
    configure_logging()
    arguments = parse_options()

    source_class, source_kwargs = select_device(arguments)
    source = source_class(receive, **source_kwargs)
    source.start()

    while True:
        import time
        time.sleep(5)

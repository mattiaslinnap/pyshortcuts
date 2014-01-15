"""Standard script setup with logging and argparse."""

import argparse
import logging
import sys
import time


logger = logging.getLogger(__name__)


def setup(add_arguments, main):
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet', '-q', action='count', help='Decrease logging level. Once=info, twice=warning.')
    add_arguments(parser)

    args = parser.parse_args()

    log_level = logging.DEBUG
    if args.quiet == 1:
        log_level = logging.INFO
    elif args.quiet >= 2:
        log_level = logging.WARNING
    logging.basicConfig(level=log_level, stream=sys.stderr, format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    start = time.time()
    main(args)
    logger.debug('main() took %.3f minutes.', (time.time() - start) / 60)


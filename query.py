#!/usr/bin/env python
import logging
import pprint
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys
from couchbase.client import Couchbase
import yaml

try:
    from logging import NullHandler
except ImportError:
    from logutils import NullHandler

# use this in all your library's subpackages/submodules
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# use this just in your library's top-level package
LOGGER.addHandler(NullHandler())

OPTIONS = None

CB = None

LAST_DATA = None


def configure_logging():
    """Configure logging."""
    try:
        from logging.config import dictConfig
    except ImportError:
        from logutils.dictconfig import dictConfig

    logging_opts = getattr(OPTIONS, 'logging', None)
    if logging_opts:
        dictConfig(OPTIONS.logging)


class OptionsBuilder(object):
    """Class for merging options from command-line arguments and config file."""

    @classmethod
    def get_options(cls):
        """Returns merged options from command-line arguments and config file."""

        args = cls._parse_args()
        opts = cls._build_opts(args)
        if args.config:
            config_opts = cls._build_config_opts(args.config)
            opts.update(config_opts)

        class Namespace(object):
            pass

        ns = Namespace()
        for k, v in opts.iteritems():
            setattr(ns, k, v)
        return ns

    @classmethod
    def _parse_args(cls):
        """Parses command line arguments."""

        parser = ArgumentParser(
            description='Couchbase Query Tool',
            formatter_class=ArgumentDefaultsHelpFormatter)

        parser.add_argument('key', help='bucket key')
        parser.add_argument('-C', '--config', help='config file to load options from')
        parser.add_argument('-H', '--host', default='localhost:8091', help='host')
        parser.add_argument('-u', '--username', default='default', help='username')
        parser.add_argument('-p', '--password', default='', help='password')
        parser.add_argument('-b', '--bucket', default='default', help='bucket')
        parser.add_argument('-V', '--value', help='value of key to set to')

        args = parser.parse_args()

        return args

    @classmethod
    def _build_opts(cls, args):
        """Builds options from parsed arguments."""

        opts = {}

        opts['key'] = args.key
        opts['config'] = args.config
        opts['host'] = args.host
        opts['username'] = args.username
        opts['password'] = args.password
        opts['bucket'] = args.bucket
        opts['value'] = args.value

        return opts

    @classmethod
    def _build_config_opts(cls, filename):
        """Builds options from config file."""

        try:
            with open(filename) as f:
                opts = yaml.load(f)
            return opts
        except IOError, e:
            print 'ERROR %s: %s' % (type(e), e)
            sys.exit()


def init_couchbase_client():
    """Initializes Couchbase client."""
    global CB
    CB = Couchbase(OPTIONS.host, OPTIONS.username, OPTIONS.password)


def main():
    """Main program."""
    global OPTIONS, LAST_DATA
    if not OPTIONS:
        OPTIONS = OptionsBuilder.get_options()
    configure_logging()
    LOGGER.info('Program started with options:\n%s' % (
        pprint.pformat(OPTIONS.__dict__),))

    init_couchbase_client()
    bucket = CB[OPTIONS.bucket]
    data = None
    if OPTIONS.value is not None:
        bucket.set(OPTIONS.key, 0, 0, OPTIONS.value)
    else:
        data = bucket.get(OPTIONS.key)[2]
        print data

    LAST_DATA = data


if __name__ == '__main__':
    main()
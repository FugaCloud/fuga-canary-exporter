import argparse
import sys

import yaml

from ping_exporter.ping_app import make_app


class ConfigException(Exception):
    pass


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f)

    check_config(config)

    return config


def create_example_config():
    example = {"endpoints": ['https://google.com',
                             'http://prometheus.io'],
               'pool_size': 5,
               'time_out': 1}
    print(yaml.dump(example, default_flow_style=False))


def check_config(config):
    required_fields = ['endpoints']
    if config is None:
        ConfigException('Configfile is empty')
    if isinstance(config, str):
        raise ConfigException('Config is probably not valid yaml')
    for req_field in required_fields:
        if config.get(req_field) is None:
            raise ConfigException(
                '{} is a required field in the config'.format(req_field))


def get_config_from_argv():
    parser = argparse.ArgumentParser(
        description='A exporter that pings some endpoints')
    parser.add_argument(
        '--config',
        dest='config',
        default="configuration.yaml",
        help='path to the config file')
    parser.add_argument(
        '--instance_name',
        dest='instance_name',
        help='the name used in the exporter to identify this instance')
    parser.add_argument(
        '--generate_config',
        dest='generate_config',
        help='print an example config',
        action='store_true')
    if len(sys.argv) < 2:
        parser.print_help()
        exit(0)
    args = parser.parse_args()
    config = load_config(args.config)
    return config, args


def get_instance_name():
    _, args = get_config_from_argv()
    instance_name = args.instance_name if args.instance_name else ""
    return instance_name


if __name__ == "__main__":
    config, args = get_config_from_argv()

    if args.generate_config:
        create_example_config()
    else:
        kwargs = dict(args._get_kwargs())
        app = make_app(**kwargs)
        app.run(debug=True)

import types

import grequests
from requests import Session


wanted_attributes = ['url', 'elapsed', 'status_code', 'ok', 'exception']


def _example_hook(resp, *args, **kwargs):
    resp.example = 'example'


def _exception_handler(request, exception):
    obj = types.SimpleNamespace()
    for attr in wanted_attributes:
        obj.__setattr__(attr, None)
        if attr == 'url':
            obj.url = request.url
        if attr == 'exception':
            obj.exception = exception.__doc__
        if attr == 'ok':
            obj.ok = False
    return obj


def _serialize_return_values(blub):
    for wauw in blub:
        for attr in wanted_attributes:
            if attr == 'url':
                continue

            if attr == 'exception':
                if wauw[attr] is not None:
                    wauw[attr] = 1
                else:
                    wauw[attr] = 0

            if attr == 'elapsed':
                if wauw[attr] is None:
                    wauw[attr] = 'Nan'

            if wauw[attr] is None:
                wauw[attr] = 'Nan'
            if wauw[attr] is True:
                wauw[attr] = 1
            if wauw[attr] is False:
                wauw[attr] = 0


def pong(endpoints, all=True, serialize=True):
    from ping_exporter.main import get_config_from_argv

    config, _ = get_config_from_argv()
    data = []
    session = Session()
    rs = (grequests.get(u, timeout=config.get('time_out', 1), session=session)
          for u in endpoints)
    for response in grequests.map(
            rs,
            exception_handler=_exception_handler,
            size=config.get('pool_size', 2)):
        response_data = {}
        if response is not None:
            for item in wanted_attributes:
                try:
                    if item == 'elapsed':
                        response_data.update(
                            {item:
                             response.__getattribute__(item).total_seconds()})
                        continue
                    response_data.update(
                        {item: response.__getattribute__(item)})
                except AttributeError:
                    response_data.update({item: None})

        data.append(response_data)

    if all:
        response_data = {}
        for item in wanted_attributes:
            response_data.update({item: None})
            if item == 'url':
                response_data[item] = 'all'
            if item == 'elapsed':
                elapsed = sum([x['elapsed'] for x in data if x['elapsed']])
                response_data[item] = elapsed
            if item == 'ok':
                response_data[item] = any([x['ok'] for x in data])
        data.append(response_data)

    if serialize:
        _serialize_return_values(data)
    return data

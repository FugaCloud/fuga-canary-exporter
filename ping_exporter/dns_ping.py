import types
import dns.resolver

wanted_attributes = ['dns_server', 'status_code', 'ok']

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
            if wauw[attr] is None:
                wauw[attr] = 'Nan'
            if wauw[attr] is True:
                wauw[attr] = 1
            if wauw[attr] is False:
                wauw[attr] = 0


def dns_ping(dnsendpoints, all=True, serialize=True):
    from ping_exporter.main import get_config_from_argv
    data = []

    for server,domain in dnsendpoints.items():
        response_data = {}
        query = dns.message.make_query(domain,dns.rdatatype.A)
        res = dns.query.tcp(query,server,timeout=2)
        response_data['dns_server'] = server
        response_data['status_code'] = res.rcode()
        response_data['ok'] = True if res.rcode() == 0 else False

        data.append(response_data)

    if all:
        response_data = {}
        for item in wanted_attributes:
            response_data.update({item: None})
            if item == 'dns_server':
                response_data[item] = 'all'
            if item == 'status_code':
                response_data[item] = 'NaN'
            if item == 'ok':
                response_data[item] = sum([x['ok'] for x in data])
        data.append(response_data)

    if serialize:
        _serialize_return_values(data)
    return data

#    for response in grequests.map(
#            rs,
#            exception_handler=_exception_handler,
#            size=config.get('pool_size', 2)):
#        response_data = {}
#        if response is not None:
#            for item in wanted_attributes:
#                try:
#                    if item == 'elapsed':
#                        response_data.update(
#                            {item:
#                             response.__getattribute__(item).total_seconds()})
#                        continue
#                    response_data.update(
#                        {item: response.__getattribute__(item)})
#                except AttributeError:
#                    response_data.update({item: None})
#
#        data.append(response_data)
#
#    if all:
#        response_data = {}
#        for item in wanted_attributes:
#            response_data.update({item: None})
#            if item == 'url':
#                response_data[item] = 'all'
#            if item == 'elapsed':
#                response_data[item] = time
#            if item == 'ok':
#                response_data[item] = any([x['ok'] for x in data])
#        data.append(response_data)
#
#    if serialize:
#        _serialize_return_values(data)
#    return data

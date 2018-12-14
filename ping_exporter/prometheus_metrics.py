from ping_exporter.ping import pong, wanted_attributes


def generate_name(prefix, extra_tags=None):
    if extra_tags is None:
        return prefix

    if isinstance(extra_tags, dict):
        pst = []
        for item in sorted(extra_tags.keys()):
            pst.append("{}=\"{}\"".format(item, extra_tags[item]))
        return "{}{{{}}}".format(prefix, ",".join(pst))


def lookup_attribute_to_name(attribute):
    prefix = 'probe'
    if attribute == 'elapsed':
        attribute = 'response_time'

    return "{}_{}".format(prefix, attribute)


def lookup_type(attr_name):
    the_type = "gauge"
    if False:
        the_type = "counter"

    return "# TYPE {} {}".format(attr_name, the_type)


def lookup_help(attr_name):
    _help = None
    if attr_name == 'probe_exception':
        _help = 'Indicates if an exception has occurred'
    if attr_name == 'probe_ok':
        _help = \
            'Indicates if an endpoint responded with a positive success code'
    if attr_name == 'probe_status_code':
        _help = 'Status code of call'
    if attr_name == 'probe_response_time':
        _help = 'Time it took to call the endpoint and return the response'

    if _help:
        return "# HELP {} {}".format(attr_name, _help)
    return None


def make_prometheus_text(return_values):
    from ping_exporter.main import get_instance_name

    instance_name = get_instance_name()
    lines = []
    for item in wanted_attributes:
        if item == 'url':
            continue
        attr_name = lookup_attribute_to_name(item)
        attr_type = lookup_type(attr_name)
        attr_help = lookup_help(attr_name)
        lines.append(attr_type)
        if attr_help:
            lines.append(attr_help)
        for rv in return_values:
            lines.append("{} {}".format(generate_name(
                attr_name, {"url": rv['url'],
                            "instance_name": instance_name}
                ), rv[item]))
    return lines


def prometheus_text(config):
    return_values = pong(config['endpoints'])
    lines = make_prometheus_text(return_values)
    return "\n".join(lines)

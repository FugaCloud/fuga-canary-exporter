import datetime
from pprint import pprint
from collections import OrderedDict


def convert2dict(txt):
    """Converts a Prometheus styled text to a dictionairy

    Parameters
    ----------
    txt: str
        A page from a Prometheus metrics page

    Returns
    -------
    :dict
        A specific dictionairy in the form: {name: {'data': value, 'type': type, 'info': documentation}}

    """
    timestamp = int(datetime.datetime.now().timestamp())
    text = txt.split("\n")

    filtered = list(filter(lambda x: not x.startswith("#"), text))
    filtered1 = list(filter(lambda x: x.startswith("# HELP"), text))
    filtered2 = list(filter(lambda x: x.startswith("# TYPE"), text))
    filtered = [x.strip() for x in filtered]
    data = [x.split(" ")  for x in filtered if not x==""]
    filtered1 = [x.replace("# HELP ", "").split(" ", maxsplit=1) for x in filtered1]
    filtered2 = [x.replace("# TYPE ", "").split(" ", maxsplit=1) for x in filtered2]
    dictdata = dict(data)
    dict1 = dict(filtered1)
    dict2 = dict(filtered2)

    names = list(dictdata.keys())

    large_dict = OrderedDict()
    for item in names:
        if(dictdata.get(item, None)!= 'NaN'):
            large_dict.update({item: {'data': dictdata.get(item, None), "info": dict1.get(item, ""), "type": dict2.get(item, "")}})

    large_dict = OrderedDict(sorted(large_dict.items(), key=lambda x: x[0]))
    return large_dict


def convert2txt(dicto):
    """Converts a specific dictionairy to a Prometheus-ready page

    Parameters
    ----------
    dicto: Dictionairy in the form: {name: {'data': value, 'type': type, 'info': documentation}}
        a dictionairy with the names of the information as keys. These names have three properties 'data', 'type' and 'info'. 'type' and 'info' aren't required.

    Returns
    -------
    : str
        A Prometheus-ready page

    """
    lines = []
    lines.append
    for x, y in dicto.items():
        info = y.get('info', "")
        type = y.get('type', "")
        data = y.get('data', 'NaN')

        if(info != ""):
            lines.append("# HELP {} {}".format(x, info))
        if(type != ""):
            lines.append("# TYPE {} {}".format(x, type))
        lines.append("{} {}".format(x, data))

    text = "\n".join(lines)
    return text


def available_metrics(txt):
    """Get available metrics from a Prometheus styled text or a dictionairy from the 'convert2dict' function

    Parameters
    ----------
    txt: str or dict
        a Prometheus styled text or a dictionairy from the 'convert2dict' function

    Returns
    -------
    : list
        a list with the available metrics

    """
    if(isinstance(txt, str)):
        content = txt.split("\n")
        items = [x for x in content if(not x.startswith("#"))]
        metrics = []
        for item in items:
            if(len(item) > 0):
                splitting = item.split(" ")
                if(splitting[1]!='NaN' and len(splitting[1])>0):
                    metrics.append(splitting[0])

        return sorted(metrics)

    elif(isinstance(txt, dict)):
        return sorted(list(txt.keys()))


def text_from_get(address, timeout=5, auth=None , **kwargs):
    """ Get text from Prometheus metrics endpoint

    Parameters
    ----------
    address: str
        host address of the Prometheus endpoint
    timeout=5: float
        requests timeout argument
    auth=None:
        requests auth argument
    **kwargs:
        Pasted to requests.get

    Returns
    -------
    : str
        plain text with Prometheus metrics
    """
    try:
        import requests
    except ImportError:
        raise ImportError("Requests is not installed")

    try:
        if auth is None:
            return requests.get(address, timeout=timeout, **kwargs).text
        else:
            return requests.get(address, timeout=timeout, auth=auth, **kwargs).text
    except requests.ConnectionError:
        raise ConnectionError("Host does not exist")
    # except ConnectionRefusedError:
    #     raise ConnectionError("Host does not exist")


def text_from_file(path):
    with open(path, "r") as f:
        text = f.read()
    return text


def _update(name, data, typing="", info=""):
    r_value = {name: {'data': data, "info": info, "type": typing}}
    return r_value


def create_dict(name_list, data_list, type_list=None, info_list=None):
    """Set docstring here.

    Parameters
    ----------
    name_list: list
        List of parameter names
    data_list: list
        List of data of the parameters
    type_list=None: list
        List of the type of the parameter (These are Prometheus types, 'gauge', 'counter', ...)
    info_list=None: list
        List of the documentation of the parameter

    Returns
    -------
    : dict
        A specific dictionairy in the form: {name: {'data': value, 'type': type, 'info': documentation}}
    """
    timestamp = int(datetime.datetime.now().timestamp())

    if(len(name_list)!= len(data_list)):
        raise IndexError('name_list length is not equal to data_list length')

    if(type_list is None):
        type_list = [""]*len(name_list)
    else:
        type_list = ["" if x is None else x for x in type_list]

    if(info_list is None):
        info_list = [""]*len(name_list)
    else:
        info_list = ["" if x is None else x for x in info_list]

    if(len(name_list)!= len(type_list)):
        raise IndexError('name_list length is not equal to type_list length')
    if(len(name_list)!= len(info_list)):
        raise IndexError('name_list length is not equal to info_list length')

    large_dict = {}
    for x,y,z,w in zip(name_list, data_list, type_list, info_list):
        large_dict.update(_update(x, y, z, w))

    large_dict = OrderedDict(sorted(large_dict.items(), key=lambda x: x[0]))
    return large_dict

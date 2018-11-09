import re
import datetime

import requests
from bs4 import BeautifulSoup as bs

class PrometheusQuery():
    _query_options = None

    def __init__(self, address, port=None):
        if(port is None):
            self.ip = address
        else:
            self.ip = f"{address}:{port}"

    def find_query(self, searching):
        return_array = []
        reg = re.compile(searching)
        for i in range(len(self.query_options)):
            if(len(reg.findall(self.query_options[i]))>0):
                return_array.append(self.query_options[i])

        return return_array

    def up(self):
        #checks if the server is up
        return bool(self.get_from_query("up")[1])

    def get_from_query(self, query, verbose=False):
        address = f"{self.ip}/api/v1/query?query={query}"
        if(verbose):
            print(address)

        dict_rick = requests.get(address).json()
        if dict_rick["data"]["result"]:
            metric = dict_rick["data"]["result"][0]["metric"]

            if(verbose):
                print(metric)

            data = dict_rick["data"]["result"][0]["value"]
            return data
        return ['NaN']

    def get_from_query_range(self, query, ranging=None, timestep="5s", verbose=False):
        address = f"{self.ip}/api/v1/query_range"
        if(ranging is None):
            #if no range is chosen take the last three hours
            dt = datetime.datetime.now()
            tup = dt.timetuple()[:7]
            arr = list(tup)
            arr[3] = arr[3] - 3
            dt_diff = datetime.datetime(*arr)

            params = {"query":query, "start": self._timestamp_gen(dt_diff), "end": self._timestamp_gen(dt), "step": timestep}

        else:
            first, last = self._parse_ranging(ranging)
            if(verbose):
                print(first)
                print(last)
            params = {"query":query, "start": self._timestamp_gen(first), "end": self._timestamp_gen(last), "step": timestep}

        if(verbose):
            print(params)

        dict_rick = requests.get(address, params=params).json()
        try:
            metric = dict_rick["data"]["result"][0]["metric"]
            if(verbose):
                print(metric)

            data = dict_rick["data"]["result"][0]["values"]
            return data
        except IndexError:
            return []

    def get_all_available_metrics(self):
        return find_all_metrics(self.ip)

    @property
    def query_options(self):
        if self._query_options is None:
            self._query_options = find_all_metrics(self.ip)
        return self._query_options

    def _timestamp_gen(self,day,month=1,year=2000,hour=0,minute=0,second=0):
        if(isinstance(day,datetime.datetime)):
            return "{}-{:02}-{:02}T{:02}:{:02}:{:02}Z".format(*day.timetuple()[:6])
        else:
            return "{}-{:02}-{:02}T{:02}:{:02}:{:02}Z".format(year,month,day,hour,minute,second)

    @staticmethod
    def _parse_ranging(txt):
            #between "h-h"
            #from "h-now"
            #from "d-now"
            #maybe replace with datetime.datetime.now().replace(hour=5)

            words = txt.split("-")

            if(len(words)==1):
                dt = datetime.datetime.now()
                arr = list(dt.timetuple()[:7])
                if(words[0][-1]=="d"):
                    arr[2] -= int(words[0][:-1])
                elif(words[0][-1]=="h"):
                    arr[3] -= (int(words[0][:-1])+2)

                dt_diff = datetime.datetime(*arr)
                return dt_diff, dt

            elif(len(words)==2):
                dt = datetime.datetime.now()
                arr = list(dt.timetuple()[:7])
                if(words[0][-1]=="d"):
                    arr[2] = int(words[0][:-1])
                elif(words[0][-1]=="h"):
                    arr[3] = (int(words[0][:-1])+2)
                dt_diff1 = datetime.datetime(*arr)

                arr = list(dt.timetuple()[:7])
                if(words[1]!=""):
                    if(words[1][-1]=="d"):
                        arr[2] = int(words[1][:-1])
                    elif(words[1][-1]=="h"):
                        arr[3] = (int(words[1][:-1])+2)

                dt_diff2 = datetime.datetime(*arr)

                return  dt_diff1, dt_diff2
            else:
                raise NotImplementedError



def find_all_metrics(ipaddress):

    ######
    #   cool app for more details:
    #   https://github.com/metalmatze/prom-metric-viewer
    #   prom-metric-viewer-0.1-linux-amd64 http://localhost:9090/metrics
    #
    #
    #
    ######

    def find_connected_nodes(ipaddress):
        r = requests.get(f"{ipaddress}/targets", timeout=1)
        soup = bs(r.content, "html.parser")

        answer = []
        for item in soup.find_all("a"):
            if(item.text.startswith("http")):
                # print(item.previousSibling())
                answer.append(str(item.text))

        return answer

    def find_metrics(ip):
        try:
            r = requests.get(ip, timeout=1)
            content = r.content.decode().split("\n")

            items = [x for x in content if(not x.startswith("#"))]
            available_metrics = []
            for item in items:
                if(len(item) > 0):
                    splitting = item.split(" ")
                    available_metrics.append(splitting[0])

            return available_metrics
        except:
            return []

    nodes = find_connected_nodes(ipaddress)
    nodes = [node.replace('http://localhost:9090', ipaddress) for node in nodes]
    all_metrics = []
    for node in nodes:
        all_metrics.append(find_metrics(node))

    return [x for y in all_metrics for x in y]

# -*- coding: utf-8 -*-

import os
import googleapiclient.discovery
import httplib2
from configparser import ConfigParser


def read_config(filename):
    conf = ConfigParser()
    conf.read(filename)
    api_service_name = conf.get("youtube", "api_service_name")
    api_version = conf.get("youtube", "api_version")
    API_KEY = conf.get("youtube", "API_KEY")
    proxy_host = conf.get("proxy", "host")
    proxy_port = conf.getint("proxy", "port")

    return api_service_name, api_version, API_KEY, proxy_host, proxy_port


def build_client(api_service_name, api_version, API_KEY, proxy_host, proxy_port):
    proxy_info = httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_HTTP, proxy_host=proxy_host,
                                    proxy_port=proxy_port)
    http = httplib2.Http(timeout=10, proxy_info=proxy_info, disable_ssl_certificate_validation=False)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY, http=http)
    return youtube


def get_comments(youtube, videoId):
    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        videoId=videoId
    )
    response = request.execute()
    return response


if __name__ == "__main__":
    api_service_name, api_version, API_KEY, proxy_host, proxy_port = read_config('config.ini')
    print(api_service_name, type(api_service_name))
    print(api_version, type(api_version))
    print(API_KEY, type(API_KEY))
    print(proxy_host, type(proxy_host))
    print(proxy_port, type(proxy_port))

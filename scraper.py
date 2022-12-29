# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import googleapiclient.discovery
import socket
from httplib2 import socks
import requests

proxies = {
    'http:': 'http://127.0.0.1:10809',
    'https:': 'http://127.0.0.1:10809',
}


def send_request(videoId):
    # # Disable OAuthlib's HTTPS verification when running locally.
    # # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    DEVELOPER_KEY = "AIzaSyAjF3ppo5L9JLIBfHTNM7vlvISFb5NLlss"

    request_url = "https://youtube.googleapis.com/youtube/v3/commentThreads?part=id&part=replies&part=snippet&maxResults=100&videoId=" + videoId + "&key=" + DEVELOPER_KEY
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, proxies=proxies)
    if response:
        data = response.json()
        print(data)
    print(response)


if __name__ == "__main__":
    send_request('MuzMniAG2rQ')

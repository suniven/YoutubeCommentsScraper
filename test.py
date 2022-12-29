# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import googleapiclient.discovery
import httplib2

proxy_info = httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_HTTP, proxy_host="127.0.0.1", proxy_port=10809)
http = httplib2.Http(timeout=None, proxy_info=proxy_info, disable_ssl_certificate_validation=False)


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAjF3ppo5L9JLIBfHTNM7vlvISFb5NLlss"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY, http=http)

    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        videoId="MuzMniAG2rQ"
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

import os
import googleapiclient.discovery
import httplib2
from configparser import ConfigParser
import pandas as pd
import json
import time


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
    proxy_info = httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_HTTP,
                                    proxy_host=proxy_host,
                                    proxy_port=proxy_port)
    http = httplib2.Http(timeout=10, proxy_info=proxy_info, disable_ssl_certificate_validation=False)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_KEY, http=http)
    return youtube


def get_comments(youtube, videoId, pageToken):
    request = youtube.commentThreads().list(part="id,snippet",
                                            maxResults=100,
                                            videoId=videoId,
                                            pageToken=pageToken)
    response = request.execute()
    return response


def process_response(response):
    try:
        nextPageToken = response["nextPageToken"]
    except Exception as error:
        nextPageToken = None

    result = []
    for index, item in enumerate(response["items"]):
        video_id = item["snippet"]["videoId"]
        comment_id = item["snippet"]["topLevelComment"]["id"]
        comment = item["snippet"]["topLevelComment"]["snippet"]
        comment_display = comment["textDisplay"]
        comment_original = comment["textOriginal"]
        author_name = comment["authorDisplayName"]
        author_profile_img_url = comment["authorProfileImageUrl"]
        author_channel_url = comment["authorChannelUrl"]
        author_channel_id = comment["authorChannelId"]["value"]
        publish_date = comment["publishedAt"]
        result.append({
            'video_id': video_id,
            'comment_id': comment_id,
            'comment_display': comment_display,
            'comment_original': comment_original,
            'author_name': author_name,
            'author_profile_img_url': author_profile_img_url,
            'author_channel_url': author_channel_url,
            'author_channel_id': author_channel_id,
            'publish_date': publish_date
        })
        print("{0}: video {1} || comment {2}".format(index, video_id, comment_id))
    return nextPageToken, result


if __name__ == "__main__":
    api_service_name, api_version, API_KEY, proxy_host, proxy_port = read_config('config.ini')
    # print(api_service_name, type(api_service_name))
    # print(api_version, type(api_version))
    # print(API_KEY, type(API_KEY))
    # print(proxy_host, type(proxy_host))
    # print(proxy_port, type(proxy_port))
    youtube = build_client(api_service_name, api_version, API_KEY, proxy_host, proxy_port)

    df_id = pd.read_csv('VideoId.csv', engine='python')
    videoIdList = df_id.video_id.to_list()
    try:
        comments = []
        for videoId in videoIdList:
            nextPageToken = None
            while True:
                # time.sleep(0.5)
                response = get_comments(youtube, videoId, nextPageToken)
                nextPageToken, result = process_response(response)
                comments += result
                if not nextPageToken:  # 该视频的评论抓完了
                    break
    except Exception as error:
        print(error)
    finally:
        with open('all_comments.json', 'w', encoding='utf-8') as f:
            json.dump(comments, f, indent=4)

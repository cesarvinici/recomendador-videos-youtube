from get_data import *
from ml_utils import *
import time
import os
import pandas as pd
from threading import Thread
from requests_html import HTMLSession


queries = ["machine+learning", "data+science", "kaggle"]

def update_db():
    try:
        with open("novos_videos.json", 'w+') as output:
            for query in queries:
                
                for page in range(1,4):
                    print(query, page)
                    search_page = download_search_page(query, page)
                    video_list = parse_search_page(search_page)
                    df_videos = pd.DataFrame(video_list)
                    for video in df_videos['link'].unique():
                        # video_page = download_video_page(video['link'])
                        video_json_data = parse_video_page(video)
                        if(not video_json_data):
                            continue
                        
                        p = compute_prediction(video_json_data)

                        video_id = video
                        data_front = {"title": video_json_data['title'], "score": float(p), "video_id": video_id}
                        data_front['update_time'] = time.time_ns()

                        print(video_id, json.dumps(data_front))
                        output.write("{}\n".format(json.dumps(data_front)))
    except Exception as identifier:
        os.remove("novos_videos.json")
        print(identifier)
        raise Exception('Internal Server Error')
    return True
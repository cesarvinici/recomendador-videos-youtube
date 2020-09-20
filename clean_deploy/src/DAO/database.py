import os,sys,inspect
import datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from sqlalchemy import create_engine
from settings import DATABASE


class Database:

    RECOMENDER_TABLE = 'recomender'

    def __init__(self):
        self._conn = self.create_conection()

    def create_conection(self):
        """ Connect to Sqlite Database """
        return create_engine("sqlite:///" + DATABASE)

    def show_videos(self, qtd_videos = 20):
        """ Return list of videos for Front End """
        query = '''select id, video_title, video_link, thumbnail, score, liked from recomender
                    order by score desc limit {qtd_videos}'''
        videos = self._conn.execute(query.format(qtd_videos=qtd_videos))
        result = videos.fetchall()
        return result


    def get_by_link(self, link):
        """ Return one video by its link """
        query = '''SELECT id from recomender where video_link = "{video_link}"'''
        video = self._conn.execute(query.format(video_link=link))
        return video.fetchone()

    def save_recomendation(self, video_info):
        ''' check if video already exists '''
        video_exists = self.get_by_link(video_info['video_id'])

        if video_exists:
            return True

        query = '''INSERT INTO {recomender} (video_title, video_link, thumbnail, score) values 
                                ("{video_title}", "{video_link}", "{thumbnail}", {score})
                '''
        new_video = self._conn.execute(query.format(recomender=self.RECOMENDER_TABLE,
                                                    video_title=video_info['title'].replace('"', "'"),
                                                    video_link=video_info['video_id'],
                                                    thumbnail=video_info['thumbnail'],
                                                    score=video_info['score']))
    
    def like_video(self, value, video_id):
        """" Edit liked column """
        time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
        query = '''update {recomender} set liked = {liked}, updated_at = '{updated_at}'  where id = {video_id}'''
        print(query.format(recomender=self.RECOMENDER_TABLE, liked=value, updated_at=time, video_id=video_id))
        self._conn.execute(query.format(recomender=self.RECOMENDER_TABLE, liked=value, updated_at=time, video_id=video_id))

if __name__ == '__main__':
    teste = Database()
    teste.like_video(1, 9)
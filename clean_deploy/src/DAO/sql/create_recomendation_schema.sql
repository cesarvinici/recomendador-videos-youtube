CREATE TABLE IF NOT EXISTS recomender (
                                id integer primary key AUTOINCREMENT, 
                                video_title TEXT, 
                                video_link TEXT UNIQUE, 
                                thumbnail TEXT, 
                                score FLOAT, 
                                liked BOOLEAN default 0,
                                created_at DATE DEFAULT (datetime('now','localtime')),
                                updated_at DATE)
)

select id, video_title, video_link, thumbnail, score, liked from recomender;
import sqlite3
import pandas as pd
from flask import url_for
data=pd.read_csv('cv_posts.csv').to_dict()
data_links=pd.read_csv('cv_posts.csv').to_dict()
for i in range(len(data['CreationDate'])):
    data['Body'][i]=str(data['Body'][i]).replace("\\n","<br />")
    data['Body'][i]=str(data['Body'][i]).replace("&lt;-","<")
    data['Body'][i]=str(data['Body'][i]).replace("&gt;",">")
    data_links['Body'][i]=f"<a href='/post/{i}'>open    </a>"
df=pd.DataFrame.from_dict(data)
df_links=pd.DataFrame.from_dict(data_links)
conn = sqlite3.connect('cv.db')
c = conn.cursor()
c.execute('''CREATE TABLE 'cv_posts' ([id] INTEGER,[PostTypeId] INTEGER,[AcceptedAnswerId] INTEGER,[ParentId] INTEGER,[CreationDate] datetime,[Score] INTEGER,[ViewCount] INTEGER,'Body',[OwnerUserId] INTEGER,[OwnerDisplayName] INTEGER,[LastEditorUserId] INTEGER,[LastEditDate] datetime,[LastActivityDate] datetime,'Title','Tags',[AnswerCount] INTEGER,[CommentCount] INTEGER,[ClosedDate] datetime,[FavoriteCount] datetime)''')
df.to_sql('cv_posts', conn, if_exists='append', index = False)
conn.close()
conn = sqlite3.connect('cvlinks.db')
c = conn.cursor()
c.execute('''CREATE TABLE 'cv_posts' ([id] INTEGER,[PostTypeId] INTEGER,[AcceptedAnswerId] INTEGER,[ParentId] INTEGER,[CreationDate] datetime,[Score] INTEGER,[ViewCount] INTEGER,'Body',[OwnerUserId] INTEGER,[OwnerDisplayName] INTEGER,[LastEditorUserId] INTEGER,[LastEditDate] datetime,[LastActivityDate] datetime,'Title','Tags',[AnswerCount] INTEGER,[CommentCount] INTEGER,[ClosedDate] datetime,[FavoriteCount] datetime)''')
df_links.to_sql('cv_posts', conn, if_exists='append', index = False)
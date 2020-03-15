import sqlite3
import pandas as pd
from flask import url_for
data=pd.read_csv('cv_posts.csv').to_dict()
for i in range(len(data['CreationDate'])):
    data['Body'][i]=str(data['Body'][i]).replace("\\n","<br />")
    data['Body'][i]=str(data['Body'][i]).replace("&lt;-","<")
    data['Body'][i]=str(data['Body'][i]).replace("&gt;",">")
df=pd.DataFrame.from_dict(data)
conn = sqlite3.connect('cv.db')
c = conn.cursor()
c.execute('''CREATE TABLE 'cv_posts' ([id] INTEGER,[PostTypeId] INTEGER,[AcceptedAnswerId] INTEGER,[ParentId] INTEGER,[CreationDate] datetime,[Score] INTEGER,[ViewCount] INTEGER,'Body',[OwnerUserId] INTEGER,[OwnerDisplayName] INTEGER,[LastEditorUserId] INTEGER,[LastEditDate] datetime,[LastActivityDate] datetime,'Title','Tags',[AnswerCount] INTEGER,[CommentCount] INTEGER,[ClosedDate] datetime,[FavoriteCount] datetime)''')
df.to_sql('cv_posts', conn, if_exists='append', index = False)
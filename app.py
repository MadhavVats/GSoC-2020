import sqlite3
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for,Markup,request
conn = sqlite3.connect('cv.db')  
c = conn.cursor()
c.execute('''SELECT * FROM cv_posts ORDER BY CreationDate DESC LIMIT 10''')
query=c.fetchall()
def get_table_html(query):
   if not query:
      return("No matches found")
   df = pd.DataFrame(query, columns=['Id','PostTypeId','AcceptedAnswerId','ParentId','CreationDate','Score','ViewCount','Body','OwnerUserId','OwnerDisplayName','LastEditorUserId','LastEditDate','LastActivityDate','Title','Tags','AnswerCount','CommentCount','ClosedDate','FavoriteCount'])
   dict=df.to_dict()
   dict['Body'][0]=dict['Body'][0].replace("&lt;","<")
   dict['Body'][0]=dict['Body'][0].replace("&gt;",">")
   df=pd.DataFrame(dict)
   # print(df['Body'][0])
   html=df.to_html(classes="table table-striped")
   html=html.replace("&lt;","<")
   html=html.replace("&gt;",">")
   return html
html=get_table_html(query)

# print(html)
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def index():
   return(render_template('index.html',table=Markup(html)))

@app.route("/ViewCount/", methods=['POST'])
def sort_veiw():
   conn = sqlite3.connect('cv.db')  
   c = conn.cursor()
   c.execute('''SELECT * FROM cv_posts ORDER BY ViewCount DESC''')
   return render_template('index.html', table=Markup(get_table_html(c.fetchall())))
@app.route("/score/", methods=['POST'])
def sort_score():
   conn = sqlite3.connect('cv.db')  
   c = conn.cursor()
   c.execute('''SELECT * FROM cv_posts ORDER BY Score DESC''')
   return render_template('index.html', table=Markup(get_table_html(c.fetchall())))
@app.route("/search/", methods=['POST'])
def search():
   search=request.form['search']
   print(search)
   conn = sqlite3.connect('cv.db')  
   c = conn.cursor()
   kp=str(f'''SELECT * FROM cv_posts WHERE (Body LIKE "%{search}%") OR (Title LIKE "%{search}%")''')
   print(kp)
   c.execute(kp)
   # print(c.fetchall())
   return render_template('index.html', table=Markup(get_table_html(c.fetchall())))
if __name__ == "__main__":
   app.run()
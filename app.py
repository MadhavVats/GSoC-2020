import sqlite3
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for,Markup,request
conn = sqlite3.connect('cv.db')  
c = conn.cursor()
c.execute('''SELECT * FROM cv_posts''')
query=c.fetchall()
df = pd.DataFrame(query, columns=['Id','PostTypeId','AcceptedAnswerId','ParentId','CreationDate','Score','ViewCount','Body','OwnerUserId','OwnerDisplayName','LastEditorUserId','LastEditDate','LastActivityDate','Title','Tags','AnswerCount','CommentCount','ClosedDate','FavoriteCount'])
body_dict={}
for i in range(len(query)):
   body_dict[i]=df['Body'][i]
print(len(body_dict),len(df['Body'][0]))
conn = sqlite3.connect('cvlinks.db')  
c = conn.cursor()
c.execute('''SELECT * FROM cv_posts ORDER BY CreationDate DESC''')
query=c.fetchall()
def get_table_html(query):
   if not query:
      return("No matches found")
   df = pd.DataFrame(query, columns=['Id','PostTypeId','AcceptedAnswerId','ParentId','CreationDate','Score','ViewCount','Body','OwnerUserId','OwnerDisplayName','LastEditorUserId','LastEditDate','LastActivityDate','Title','Tags','AnswerCount','CommentCount','ClosedDate','FavoriteCount'])
   
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
   conn = sqlite3.connect('cvlinks.db')  
   c = conn.cursor()
   c.execute('''SELECT * FROM cv_posts ORDER BY ViewCount DESC''')
   return render_template('index.html', table=Markup(get_table_html(c.fetchall())))
@app.route("/score/", methods=['POST'])
def sort_score():
   conn = sqlite3.connect('cvlinks.db')  
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
@app.route('/post/<int:post_id>')
def show_post(post_id):
   return body_dict[int(post_id)]
if __name__ == "__main__":
   app.run()
import json,os,requests,random
import schedule,time
from flask import jsonify,request,make_response,render_template
from datetime import datetime,date,timedelta
from flask_sqlalchemy import SQLAlchemy
from challenge_pkg import app,db
from challenge_pkg.models import *




def write_newstories_to_db():
    
    #connects to newstories API end point
    rsp=requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
    rsp_json=rsp.json() #converts rsp from HTTP response to json
    
    top_stories_deets=[]
    
    new_stories_id_list=rsp_json[0:100]
    
    for x in new_stories_id_list:
        Id_info = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{x}.json")
        Id_info_rsp_json = Id_info.json() 
        
        top_stories_deets.append(Id_info_rsp_json) #this gives us a list of the dict info of each id... [{},{},{}]
    
    
    
    # the for loop below writes to the new stories table in the database
    for i in top_stories_deets:
        #this was done to achieve a Nigerian GMT+ 1 timezone
        new_date=datetime.utcfromtimestamp(i['time']) + timedelta(hours=1)
                                    
        new_stories=New_stories(new_story_id=i['id'], posted_by=i['by'], unix_time=i['time'],unix_time_convert=new_date, title=i['title'], decendants=i['descendants'], story_type=i['type'], story_url=i.get('url','#'))
        db.session.add(new_stories)
        db.session.commit()
            



### Home page Route
@app.route('/')
@app.route('/home/')
def home():
    page=request.args.get('page',1,type=int)
    new_news=db.session.query(New_stories).order_by(New_stories.unix_time_convert.desc()).paginate(page=page, per_page=5)
    return render_template('hackerhome.html', new_news=new_news)



## Find all comments for a new news story
@app.route('/comments/<story_id>')
def find_story_comment(story_id):
    story_details = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
    comments= story_details.json()
    
    if comments.get('decendants')==0:
        return 'No comment for this post'
    else:
        children=[]
        formatted_time=[]
        kids= comments.get('kids')
        for i in kids:
            child = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json")
            child_deets=child.json()
            
            time_posted=datetime.utcfromtimestamp(child_deets.get('time'))
            formatted_time.append(time_posted)
            children.append(child_deets)
    The_comments=children
    return render_template('comments.html', The_comments=The_comments, comments=comments)




# This function writes jobstories to the jobstories table in the db
def write_jobstories_to_db():
    
    #connects to jobstories API end point
    rsp=requests.get("https://hacker-news.firebaseio.com/v0/jobstories.json")
    rsp_json=rsp.json() #converts rsp from HTTP response to json
    
    job_stories_deets=[]
    
    job_stories_id_list=rsp_json[0:50]
    
    for x in job_stories_id_list:
        Id_info = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{x}.json")
        Id_info_rsp_json = Id_info.json() 
        
        job_stories_deets.append(Id_info_rsp_json) #this gives us a list of the dict info of each id... [{},{},{}]
    
    
    
    # the for loop below writes to the job stories table in the database
    for i in job_stories_deets:
        #this was done to achieve a Nigerian GMT+ 1 timezone
        new_date=datetime.utcfromtimestamp(i['time']) + timedelta(hours=1)
                                    
        job_stories=Job_stories(job_story_id=i['id'], posted_by=i['by'], unix_time=i['time'],unix_time_convert=new_date, title=i['title'], story_type=i['type'], job_url=i.get('url','#'))
        db.session.add(job_stories)
        db.session.commit()
        
       

### Job Stories page Route
@app.route('/job-stories/')
def jobstories():
    page=request.args.get('page',1,type=int)
    job_news=db.session.query(Job_stories).order_by(Job_stories.unix_time_convert.desc()).paginate(page=page, per_page=5)
    return render_template('jobstories.html', job_news=job_news)






# This function writes topstories to the topstories table in the db
def write_topstories_to_db():
    
    #connects to topstories API end point
    rsp=requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    rsp_json=rsp.json() #converts rsp from HTTP response to json
    
    topnews_stories_deets=[]
    
    topnews_stories_id_list=rsp_json[0:100]
    
    for x in topnews_stories_id_list:
        Id_info = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{x}.json")
        Id_info_rsp_json = Id_info.json() 
        
        topnews_stories_deets.append(Id_info_rsp_json) #this gives us a list of the dict info of each id... [{},{},{}]
    
    
    
    # the for loop below writes to the new stories table in the database
    for i in topnews_stories_deets:
        #this was done to achieve a Nigerian GMT+ 1 timezone
        new_date=datetime.utcfromtimestamp(i['time']) + timedelta(hours=1)
                                    
        topnews_stories=Top_stories(top_story_id=i['id'], posted_by=i['by'], unix_time=i['time'],unix_time_convert=new_date, title=i['title'], decendants=i.get('descendants','0'), story_type=i['type'], story_url=i.get('url','#'))
        db.session.add(topnews_stories)
        db.session.commit()
        
       

### Top Stories page Route
@app.route('/top-stories/')
def topstories():
    page=request.args.get('page',1,type=int)
    top_news=db.session.query(Top_stories).order_by(Top_stories.unix_time_convert.desc()).paginate(page=page, per_page=5)
    return render_template('topnews.html', top_news=top_news)


## Find all comments for a Top news story
@app.route('/top-story-comments/<story_id>')
def find_topstory_comment(story_id):
    story_details = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
    comments= story_details.json()
    
    if comments.get('decendants')==0:
        return 'No comment for this post'
    else:
        children=[]
        formatted_time=[]
        kids= comments.get('kids')
        for i in kids:
            child = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json")
            child_deets=child.json()
            
            time_posted=datetime.utcfromtimestamp(child_deets.get('time'))
            formatted_time.append(time_posted)
            children.append(child_deets)
    The_comments=children
    return render_template('topstories_comments.html', The_comments=The_comments, comments=comments)



#### This Function is used to automatically update the new news database
def update_new_stories():
    #connects to newstories API end point
    rsp=requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
    rsp_json=rsp.json() #converts rsp from HTTP response to json
    new_stories_id_list=rsp_json[0:20]
    
    Update=[]
    #news db list
    news_db=db.session.query(New_stories).all()
    if news_db!=[]:
        news_db_list=[]
        for x in news_db:
           news_db_list.append(x.new_story_id)
           existing_news_top15= news_db_list[0:15]
           
        for compare in new_stories_id_list:
            if compare in existing_news_top15:
                continue
            else:
                Update.append(compare)
                for update in Update:
                    child = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{update}.json")
                    child_deets=child.json()
                    
                    #this is to write to the db
                    new_date=datetime.utcfromtimestamp(child_deets['time']) + timedelta(hours=1)
                                                
                    new_stories=New_stories(new_story_id=child_deets['id'], posted_by=child_deets['by'], unix_time=child_deets['time'],unix_time_convert=new_date, title=child_deets['title'], decendants=child_deets['descendants'], story_type=child_deets['type'], story_url=child_deets.get('url','#'))
                    db.session.add(new_stories)
                    db.session.commit()
                Update=[]
    else:
        for added in new_stories_id_list:
            child = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{added}.json")
            child_deets=child.json()
                    
            #this is to write to the db
            new_date=datetime.utcfromtimestamp(child_deets['time']) + timedelta(hours=1)
                                                
            new_stories=New_stories(new_story_id=child_deets['id'], posted_by=child_deets['by'], unix_time=child_deets['time'],unix_time_convert=new_date, title=child_deets['title'], decendants=child_deets['descendants'], story_type=child_deets['type'], story_url=child_deets.get('url','#'))
            db.session.add(new_stories)
            db.session.commit()
    
    print(Update)
   



#### This Function is used to automatically update the Top News Database
def update_Topnews_DB_stories():
    #connects to topstories API end point
    rsp=requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    rsp_json=rsp.json() #converts rsp from HTTP response to json
    new_stories_id_list=rsp_json[0:20]
    
    Update=[]
    #top news db list
    news_db=db.session.query(Top_stories).all()
    if news_db!=[]:
        news_db_list=[]
        for x in news_db:
           news_db_list.append(x.top_story_id)
           existing_news_top15= news_db_list[0:15]
           
        for compare in new_stories_id_list:
            if compare in existing_news_top15:
                continue
            else:
                Update.append(compare)
                for update in Update:
                    child = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{update}.json")
                    child_deets=child.json()
                    
                    #this is to write to the db
                    new_date=datetime.utcfromtimestamp(child_deets['time']) + timedelta(hours=1)
                                                
                    new_stories=Top_stories(top_story_id=child_deets['id'], posted_by=child_deets['by'], unix_time=child_deets['time'],unix_time_convert=new_date, title=child_deets['title'], decendants=child_deets.get('descendants','0'), story_type=child_deets['type'], story_url=child_deets.get('url','#'))
                    db.session.add(new_stories)
                    db.session.commit()
                Update=[]
    else:
        for added in new_stories_id_list:
            child = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{added}.json")
            child_deets=child.json()
                    
            #this is to write to the db
            new_date=datetime.utcfromtimestamp(child_deets['time']) + timedelta(hours=1)
                                                
            new_stories=Top_stories(top_story_id=child_deets['id'], posted_by=child_deets['by'], unix_time=child_deets['time'],unix_time_convert=new_date, title=child_deets['title'], decendants=child_deets.get('descendants','0'), story_type=child_deets['type'], story_url=child_deets.get('url','#'))
            db.session.add(new_stories)
            db.session.commit()
    
    print(Update)  


# UNCOMMENT THIS CODE BEFORE YOU RUN THE SERVER TO AUTO WRITE THE TOP 100 STORIES OF EACH CATEGORY OF NEWS TO THE DB            
write_newstories_to_db()    
write_jobstories_to_db()
write_topstories_to_db()




schedule.every(5).minutes.do(update_Topnews_DB_stories)   

while True:
    schedule.run_pending()
    time.sleep(1)
    

   
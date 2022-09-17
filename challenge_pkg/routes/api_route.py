""" This Module is the API written for our data to be consumed as well as have things written to the database"""

import json,os,requests,random,calendar,datetime
from flask import jsonify,request,make_response,render_template
from flask_httpauth import HTTPBasicAuth
from challenge_pkg import app,db,csrf
from challenge_pkg.models import *

auth=HTTPBasicAuth()


## To fetch all New Stories in the database
@app.route('/api/v1.0/newstories/',methods=['GET'])
def fetch_new_stories():
    
    new_stories_list=db.session.query(New_stories).all()
    if new_stories_list==[]:
        data2ret={"status":False, "message":'No Story Found'}
    else:
        record=[]
        for x in new_stories_list:
            a={}
            a['serial_No']=x.serial_num
            a['story_id']=x.new_story_id
            a['posted_by']=x.posted_by
            a['unix_time_posted']=x.unix_time
            a['title']=x.title
            a['type']=x.story_type
            a['url']=x.story_url
            
            record.append(a)
        data2ret={"status":True, "message":record}
        
    data=jsonify(data2ret)
    return data


## To fetch all Top Stories in the database
@app.route('/api/v1.0/topstories/',methods=['GET'])
def fetch_top_stories():
    
    top_stories_list=db.session.query(Top_stories).all()
    if top_stories_list==[]:
        data2ret={"status":False, "message":'No Story Found'}
    else:
        record=[]
        for x in top_stories_list:
            a={}
            a['serial_No']=x.serial_num
            a['story_id']=x.top_story_id
            a['posted_by']=x.posted_by
            a['unix_time_posted']=x.unix_time
            a['title']=x.title
            a['type']=x.story_type
            a['url']=x.story_url
            
            record.append(a)
        data2ret={"status":True, "message":record}
        
    data=jsonify(data2ret)
    return data


## To fetch all Job Stories in the database
@app.route('/api/v1.0/jobstories/',methods=['GET'])
def fetch_job_stories():
    
    job_stories_list=db.session.query(Job_stories).all()
    if job_stories_list==[]:
        data2ret={"status":False, "message":'No Job Story Found'}
    else:
        record=[]
        for x in job_stories_list:
            a={}
            a['serial_No']=x.serial_num
            a['story_id']=x.job_story_id
            a['posted_by']=x.posted_by
            a['unix_time_posted']=x.unix_time
            a['title']=x.title
            a['type']=x.story_type
            a['url']=x.job_url
            
            record.append(a)
        data2ret={"status":True, "message":record}
        
    data=jsonify(data2ret)
    return data


## To fetch all decendants of a new news Story in our db
@app.route('/api/v1.0/get/new/news/decendants/<int:id>',methods=['GET'])
def fetch_newnews_story_decendant(id):
    details=db.session.query(New_stories).filter(New_stories.new_story_id==id).first()
    
    children=[]
    if details:
        Id_info = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{details.new_story_id}.json")
        Id_info_rsp_json = Id_info.json()
        child=Id_info_rsp_json.get('kids','[]')
        
        if child != "[]":
            for x in child:
                child_info = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{x}.json")
                child_info_rsp_json = child_info.json()
                children.append(child_info_rsp_json) ### This will be a list of dict [{},{},{}]
            data2ret={"status":True, "message":f"{children}"}
        else:
            data2ret={"status":False, "message":"No subs found for this post"}
    else:
        data2ret={"status":False, "message":"No record found for this ID"}
        
    data=jsonify(data2ret)
    return data




## To fetch all decendants of a top news Story in our db
@app.route('/api/v1.0/get/top/news/decendants/<int:id>',methods=['GET'])
def fetch_top_news_story_decendant(id):
    details=db.session.query(Top_stories).filter(Top_stories.top_story_id==id).first()
    
    children=[]
    if details:
        Id_info = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{details.top_story_id}.json")
        Id_info_rsp_json = Id_info.json()
        child=Id_info_rsp_json.get('kids','[]')
        
        if child != "[]":
            for x in child:
                child_info = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{x}.json")
                child_info_rsp_json = child_info.json()
                children.append(child_info_rsp_json) ### This will be a list of dict [{},{},{}]
            data2ret={"status":True, "message":f"{children}"}
        else:
            data2ret={"status":False, "message":"No subs found for this post"}
    else:
        data2ret={"status":False, "message":"No record found for this ID"}
        
    data=jsonify(data2ret)
    return data


## To add a new news to the database
@app.route('/api/v1.0/add/new_stories/',methods=['POST'])
@csrf.exempt
def add_new_story():
    if request.is_json:
        data=request.get_json()
        
        poster=data.get('name_of_news_poster')
        news_title=data.get('news_title')
        url=data.get('news_url','#')
        
        post_date=datetime.now()
        utc_unix_time=calendar.timegm(post_date.utctimetuple())
        
        newSTORIES_IDs=[]
        if poster!= None and news_title!= None:
            random_story_id= int(random.random() * 10000000)
            
            new_stories_list=db.session.query(New_stories).all()
            
            if new_stories_list != []:
                #add existing ids to a list
                for x in new_stories_list:
                    newSTORIES_IDs.append(x.new_story_id)
                    
                    
                if random_story_id  not in newSTORIES_IDs:
                    #this condition is to ensure we achieve a 3NF table where there are no empty cells.
                    if url=="":
                        try:
                            api_aided_news_add = New_stories(new_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url='#')
                            
                            db.session.add(api_aided_news_add)
                            db.session.commit()
                            data2ret={"status":True, "message":"Complete. News successfully added"}
                        except:
                            data2ret={"status":False, "message":"Failed to add. Something went wrong"}
                    else:
                        try:
                            api_aided_news_add = New_stories(new_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url=url)
                            
                            db.session.add(api_aided_news_add)
                            db.session.commit()
                            data2ret={"status":True, "message":"News successfully added"}
                        except:
                            data2ret={"status":False, "message":"Failed. Something went wrong"}
                else:
                    #write some codes to carry out if number is existent
                    random_story_id = int(random.random() * 10000)
                    
                    if url=="":
                        try:
                            api_aided_news_add = New_stories(new_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url='#')
                            
                            db.session.add(api_aided_news_add)
                            db.session.commit()
                        
                            data2ret={"status":True, "message":"New news successfully added"}
                        except:
                            data2ret={"status":False, "message":"Unable to add. Something went wrong"}
                    else:
                        try:
                            api_aided_news_add = New_stories(new_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url=url)
                            
                            db.session.add(api_aided_news_add)
                            db.session.commit()
                        
                            data2ret={"status":True, "message":"New news addition complete"}
                        except:
                            data2ret={"status":False, "message":"Oops. Something went wrong"}
            else:
                #write some codes to add post even when table is empty
                
                if url=="":
                    try:
                        api_aided_news_add = New_stories(new_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url='#')
                            
                        db.session.add(api_aided_news_add)
                        db.session.commit()
                        data2ret={"status":True, "message":"Added Successfully. Thank you."}
                    except:
                        data2ret={"status":False, "message":"News addition failed. Something went wrong"}
                else:
                    try:
                        api_aided_news_add = New_stories(new_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url=url)
                            
                        db.session.add(api_aided_news_add)
                        db.session.commit()
                        data2ret={"status":True, "message":"Added Successfully Confirmed"}
                    except:
                        data2ret={"status":False, "message":"Wrong. Please try again"}
        else:
            data2ret={"status":False, "message":"Ensure all the required values are supplied"}
    else:
        data2ret={"status":False, "message":"Ensure all the required values are sent in json"}
    return jsonify(data2ret)


## To add a Job news to the database
@app.route('/api/v1.0/add/job_news/',methods=['POST'])
@csrf.exempt
def add_job_story():
    if request.is_json:
        data=request.get_json()
        
        poster=data.get('name_of_job_poster')
        job_title=data.get('job_title')
        url=data.get('job_url','#')
        
        post_date=datetime.now()
        utc_unix_time=calendar.timegm(post_date.utctimetuple())
        
        jobSTORIES_IDs=[]
        
        if poster!= None and job_title!= None:
            random_story_id= int(random.random() * 10000000)
            
            job_stories_list=db.session.query(Job_stories).all()
            
            if job_stories_list != []:
                #add existing ids to a list
                for x in job_stories_list:
                    jobSTORIES_IDs.append(x.job_story_id)
                    
                    
                if random_story_id  not in jobSTORIES_IDs:
                    #this condition is to ensure we achieve a 3NF table where there are no empty cells.
                    if url=="":
                        try:
                            api_aided_job_add = Job_stories(job_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=job_title, story_type='API_added_job', job_url='#')
                            
                            db.session.add(api_aided_job_add)
                            db.session.commit()
                            data2ret={"status":True, "message":"Successful. Job successfully added"}
                        except:
                            data2ret={"status":False, "message":"Failed to add. Something went wrong"}
                    else:
                        try:
                            api_aided_job_add = Job_stories(job_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=job_title, story_type='API_added_job', job_url=url)
                            
                            db.session.add(api_aided_job_add)
                            db.session.commit()
                            data2ret={"status":True, "message":"Job successfully added"}
                        except:
                            data2ret={"status":False, "message":"Failed to add. Something went wrong"}
                else:
                    #write some codes to carry out if number is existent
                    random_story_id = int(random.random() * 10000)
                    #this condition is to ensure we achieve a 3NF table where there are no empty cells.
                    if url=="":
                        try:
                            api_aided_job_add = Job_stories(job_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=job_title, story_type='API_added_job', job_url='#')
                            
                            db.session.add(api_aided_job_add)
                            db.session.commit()
                        
                            data2ret={"status":True, "message":"New job successfully added"}
                        except:
                            data2ret={"status":False, "message":"Unable to add job. Something went wrong"}
                    else:
                        try:
                            api_aided_job_add = Job_stories(job_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=job_title, story_type='API_added_job', job_url=url)
                            
                            db.session.add(api_aided_job_add)
                            db.session.commit()
                        
                            data2ret={"status":True, "message":"New job successfully added"}
                        except:
                            data2ret={"status":False, "message":"Unable to add job. Something went wrong"}
            else:
                #write some codes to add post even when table is empty
                
                #this condition is to ensure we achieve a 3NF table where there are no empty cells.
                if url=="":
                    try:
                        api_aided_job_add = Job_stories(job_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=job_title, story_type='API_added_job', job_url='#')
                            
                        db.session.add(api_aided_job_add)
                        db.session.commit()
                        data2ret={"status":True, "message":"Job upload complete."}
                    except:
                        data2ret={"status":False, "message":"Job addition failed. Something went wrong"}
                else:
                    try:
                        api_aided_job_add = Job_stories(job_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=job_title, story_type='API_added_job', job_url=url)
                            
                        db.session.add(api_aided_job_add)
                        db.session.commit()
                        data2ret={"status":True, "message":"Added Successfully"}
                    except:
                        data2ret={"status":False, "message":"Job addition failed. Something went wrong"}
        else:
            data2ret={"status":False, "message":"Ensure all the required values are supplied"}
    else:
        data2ret={"status":False, "message":"Ensure all the required values are sent in json"}
    return jsonify(data2ret)




## To add a Top news Story to the database
@app.route('/api/v1.0/add/topstory/',methods=['POST'])
@csrf.exempt
def add_Top_story():
    if request.is_json:
        data=request.get_json()
        
        poster=data.get('name_of_news_poster')
        news_title=data.get('news_title')
        url=data.get('news_url','#')
        
        post_date=datetime.now()
        utc_unix_time=calendar.timegm(post_date.utctimetuple())
        
        top_news_STORIES_IDs=[]
        if poster!= None and news_title!= None:
            random_story_id= int(random.random() * 10000000)
            
            top_stories_list=db.session.query(Top_stories).all()
            
            if top_stories_list != []:
                #add existing ids to a list
                for x in top_stories_list:
                    top_news_STORIES_IDs.append(x.top_story_id)
                    
                    
                if random_story_id  not in top_news_STORIES_IDs:
                    #this condition is to ensure we achieve a 3NF table where there are no empty cells.
                    if url=="":
                        try:
                            api_aided_news_add = Top_stories(top_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url='#')
                            
                            db.session.add(api_aided_news_add)
                            db.session.commit()
                            data2ret={"status":True, "message":"Complete. News successfully added"}
                        except:
                            data2ret={"status":False, "message":"Failed to add. Something went wrong"}
                    else:
                        try:
                            api_aided_news_add = Top_stories(top_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url=url)
                            
                            db.session.add(api_aided_news_add)
                            db.session.commit()
                            data2ret={"status":True, "message":"News successfully added"}
                        except:
                            data2ret={"status":False, "message":"Failed. Something went wrong"}
                else:
                    #write some codes to carry out if number is existent
                    random_story_id = int(random.random() * 10000)
                    
                    if url=="":
                        try:
                            api_aided_news_add = Top_stories(top_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url='#')
                            
                            db.session.add(api_aided_news_add)
                            db.session.commit()
                        
                            data2ret={"status":True, "message":"New news successfully added"}
                        except:
                            data2ret={"status":False, "message":"Unable to add. Something went wrong"}
                    else:
                        try:
                            api_aided_news_add = Top_stories(top_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url=url)
                            
                            db.session.add(api_aided_news_add)
                            db.session.commit()
                        
                            data2ret={"status":True, "message":"New news addition complete"}
                        except:
                            data2ret={"status":False, "message":"Oops. Something went wrong"}
            else:
                #write some codes to add post even when table is empty
                
                if url=="":
                    try:
                        api_aided_news_add = Top_stories(top_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url='#')
                            
                        db.session.add(api_aided_news_add)
                        db.session.commit()
                        data2ret={"status":True, "message":"Added Successfully. Thank you."}
                    except:
                        data2ret={"status":False, "message":"News addition failed. Something went wrong"}
                else:
                    try:
                        api_aided_news_add = Top_stories(top_story_id=random_story_id, posted_by=poster, unix_time=utc_unix_time, unix_time_convert=post_date, title=news_title, decendants=0, story_type='API_added_story', story_url=url)
                            
                        db.session.add(api_aided_news_add)
                        db.session.commit()
                        data2ret={"status":True, "message":"Added Successfully. Confirmed"}
                    except:
                        data2ret={"status":False, "message":"Wrong. Please try again"}
        else:
            data2ret={"status":False, "message":"Ensure all the required values are supplied"}
    else:
        data2ret={"status":False, "message":"Ensure all the required values are sent in json"}
    return jsonify(data2ret)


## To delete a top news record from the db
@app.route('/api/v1.0/delete/topnews/<int:id>',methods=['DELETE'])
@csrf.exempt
def delete_topnews_story(id):
    details=db.session.query(Top_stories).filter(Top_stories.top_story_id==id).first()
    if details:
        topnews_type=details.story_type
        if topnews_type=='API_added_story':
            db.session.delete(details)
            db.session.commit()
            data2ret={"status":True, "message":"Delete Successful"}
        else:
            data2ret={"status":False, "message":"Permission Denied."}
    else:
        data2ret={"status":False, "message":"Invalid ID"}
        
    data=jsonify(data2ret)
    return data


## To delete a new news record from the db
@app.route('/api/v1.0/delete/new-news/<int:id>',methods=['DELETE'])
@csrf.exempt
def delete_new_news_story(id):
    details=db.session.query(New_stories).filter(New_stories.new_story_id==id).first()
    if details:
        newnews_type=details.story_type
        if newnews_type=='API_added_story':
            db.session.delete(details)
            db.session.commit()
            data2ret={"status":True, "message":"Delete Successful"}
        else:
            data2ret={"status":False, "message":"Permission Denied."}
    else:
        data2ret={"status":False, "message":"Invalid ID"}
        
    data=jsonify(data2ret)
    return data


## To delete a Job news record from the db
@app.route('/api/v1.0/delete/job-news/<int:id>',methods=['DELETE'])
@csrf.exempt
def delete_job_news_story(id):
    details=db.session.query(Job_stories).filter(Job_stories.job_story_id==id).first()
    if details:
        jobstory_type=details.story_type
        if jobstory_type=='API_added_job':
            db.session.delete(details)
            db.session.commit()
            data2ret={"status":True, "message":"Delete Successful"}
        else:
            data2ret={"status":False, "message":"Permission Denied."}
    else:
        data2ret={"status":False, "message":"Invalid ID"}
        
    data=jsonify(data2ret)
    return data


## To update a new news story
@app.route('/api/v1.0/update/new-news/<int:id>',methods=['PUT'])
@csrf.exempt
def update_new_news(id):
    if request.is_json:
        data=request.get_json()
        
        title=data.get('title')
        url=data.get('story_url','#')
        
        if title!=None and url!=None:
            details=db.session.query(New_stories).filter(New_stories.new_story_id==id).first()
            if details:
                if details.story_type == "API_added_story":
                    if url=="":
                        details.title=title
                        details.story_url="#"
                        db.session.commit()
                        data2ret={"status":True, "message":"Update Successful"}
                    else:
                        details.title=title
                        details.story_url=url
                        db.session.commit()
                        data2ret={"status":True, "message":"Update Successful"}
                else:
                    data2ret={"status":False, "message":"Permission Denied"}
            else:
                data2ret={"status":False, "message":"Invalid ID"}
        else:
            data2ret={"status":False, "message":"Supply required fields Title and Url"}
    else:
        data2ret={"status":False, "message":"Ensure all the required values are sent in json"}
    return jsonify(data2ret)


## To update a Top news story
@app.route('/api/v1.0/update/top-news/<int:id>',methods=['PUT'])
@csrf.exempt
def update_top_news(id):
    if request.is_json:
        data=request.get_json()
        
        title=data.get('title')
        url=data.get('story_url','#')
        
        if title!=None and url!=None:
            details=db.session.query(Top_stories).filter(Top_stories.top_story_id==id).first()
            if details:
                if details.story_type == "API_added_story":
                    if url=="":
                        details.title=title
                        details.story_url="#"
                        db.session.commit()
                        data2ret={"status":True, "message":"Update Successful"}
                    else:
                        details.title=title
                        details.story_url=url
                        db.session.commit()
                        data2ret={"status":True, "message":"Update Successful"}
                else:
                    data2ret={"status":False, "message":"Permission Denied"}
            else:
                data2ret={"status":False, "message":"Invalid ID"}
        else:
            data2ret={"status":False, "message":"Supply required fields Title and Url"}
    else:
        data2ret={"status":False, "message":"Ensure all the required values are sent in json"}
    return jsonify(data2ret)


## To update a Job news story
@app.route('/api/v1.0/update/job-news/<int:id>',methods=['PUT'])
@csrf.exempt
def update_job_news(id):
    if request.is_json:
        data=request.get_json()
        
        title=data.get('title')
        url=data.get('story_url','#')
        
        if title!=None and url!=None:
            details=db.session.query(Job_stories).filter(Job_stories.job_story_id==id).first()
            if details:
                if details.story_type == "API_added_job":
                    if url=="":
                        details.title=title
                        details.story_url="#"
                        db.session.commit()
                        data2ret={"status":True, "message":"Job Update Successful"}
                    else:
                        details.title=title
                        details.story_url=url
                        db.session.commit()
                        data2ret={"status":True, "message":"Update Successful"}
                else:
                    data2ret={"status":False, "message":"Permission Denied"}
            else:
                data2ret={"status":False, "message":"Invalid ID"}
        else:
            data2ret={"status":False, "message":"Supply required fields Title and Url"}
    else:
        data2ret={"status":False, "message":"Ensure all the required values are sent in json"}
    return jsonify(data2ret)
from datetime import datetime,date
from challenge_pkg import db


class New_stories(db.Model):
    serial_num=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    new_story_id=db.Column(db.Integer(), nullable=False)
    posted_by=db.Column(db.String(100), nullable=False)
    unix_time=db.Column(db.String(30), nullable=False)
    unix_time_convert=db.Column(db.DateTime(), nullable=False)
    title=db.Column(db.Text(), nullable=False)
    decendants=db.Column(db.Integer(), nullable=False)
    story_type=db.Column(db.String(50), nullable=False)
    story_url=db.Column(db.String(250), nullable=False)
    
    
class Job_stories(db.Model):
    serial_num=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    job_story_id=db.Column(db.Integer(), nullable=False)
    posted_by=db.Column(db.String(100), nullable=False)
    unix_time=db.Column(db.String(30), nullable=False)
    unix_time_convert=db.Column(db.DateTime(), nullable=False)
    title=db.Column(db.Text(), nullable=False)
    story_type=db.Column(db.String(50), nullable=False)
    job_url=db.Column(db.String(250), nullable=False)
 
class Top_stories(db.Model):
    serial_num=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    top_story_id=db.Column(db.Integer(), nullable=False)
    posted_by=db.Column(db.String(100), nullable=False)
    unix_time=db.Column(db.String(30), nullable=False)
    unix_time_convert=db.Column(db.DateTime(), nullable=False)
    title=db.Column(db.Text(), nullable=False)
    decendants=db.Column(db.Integer(), nullable=False)
    story_type=db.Column(db.String(50), nullable=False)
    story_url=db.Column(db.String(250), nullable=False)
    
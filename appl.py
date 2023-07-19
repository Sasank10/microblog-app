import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient 
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app=Flask(__name__)
    client=MongoClient(os.getenv("MONGODB_URI"))
    app.db=client.microblog


    @app.route('/', methods=['GET', 'POST'])
    def home():
        print([e for e in app.db.entries.find({})])
        if request.method=='POST':
            content = request.form.get('content')
            fromDate = datetime.datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert_one({"content":content,"date":fromDate})
        Entries_date_fixed =  [
        (
        Entry['content'], 
        Entry['date'], 
        datetime.datetime.today().strptime(Entry['date'], '%Y-%m-%d').strftime('%b %d')
        )
        for Entry in app.db.entries.find({})
        ]
                                    
        
        return render_template('index.html', Entries=Entries_date_fixed)
    return app
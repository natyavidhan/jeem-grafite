from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))

def get_chapters(sub):
    db = client[sub]
    chapters = db.list_collection_names()
    return chapters

def get_topics(sub, chapter):
    db = client[sub]
    collection = db[chapter]
    topics = collection.find()
    return [i['_id'] for i in topics]

def get_content(sub, chapter, topic):
    db = client[sub]
    collection = db[chapter]
    content = collection.find_one({"_id": topic})
    return content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<sub>')
def subjects(sub):
    chapters = get_chapters(sub)
    return render_template('subject.html', sub=sub, chapters=chapters)

@app.route('/<sub>/<chapter>')
def topics(sub, chapter):
    topics = get_topics(sub, chapter)
    return render_template('chapter.html', sub=sub, chapter=chapter, topics=topics)

@app.route('/<sub>/<chapter>/<topic>')
def content(sub, chapter, topic):
    content = get_content(sub, chapter, topic)
    return render_template('topic.html', sub=sub, chapter=chapter, topic=topic, content=content)

@app.route('/<sub>/<chapter>/<topic>/extra-q')
def extraq(sub, chapter, topic):
    content = get_content(sub, chapter, topic)
    return render_template('extraq.html', sub=sub, chapter=chapter, topic=topic, content=content)

@app.route('/<sub>/<chapter>/<topic>/extra-q/flashcards')
def flashcards(sub, chapter, topic):
    content = get_content(sub, chapter, topic)
    return render_template('flashcards.html', sub=sub, chapter=chapter, topic=topic, content=content)

@app.route('/<sub>/<chapter>/<topic>/pyqs')
def pyqs(sub, chapter, topic):
    content = get_content(sub, chapter, topic)
    return render_template('pyqs.html', sub=sub, chapter=chapter, topic=topic, content=content)

if __name__ == '__main__':
    app.run(debug=True)
#!/usr/bin/env python3
#coding: utf-8
from flask import Flask, render_template, Markup, request
from os.path import exists
import datetime, time, pickle

#!---------- squiNotes.py ----------
# My notes-taking app
#-----------------------------!
class note:
    def __init__(self, createtime: int, modtime: int, title: str, text: str):
        """
        createtime, modtime : epoch time of note writing / modfying
        title and text are str
        """
        self.modtime = modtime
        self.createtime = createtime
        self.title = title
        self.text = text

    def rendertime(self, pretimestamp: int):
        """
        Render the given timestamp as dd/mm/yyyy-hh:mm
        """
        timestamp = datetime.datetime.fromtimestamp(pretimestamp)
        timestamp = timestamp.strftime("%d/%m/%Y-%H:%M:%S")
        return timestamp

    def flaskrender(self):
        """
        Render the note as html for flask, using flask.Markup
        """
        rendered = f"""
        <hr>
        <div class="notetitle">{Markup.escape(self.title)}</div><br>
        <div class="notetime">Created : {self.rendertime(self.createtime)} Modified : {self.rendertime(self.modtime)}</div><br>
        <div class="notetext">{Markup.escape(self.text)}</div><br>"""
        return Markup(rendered)

    def __str__(self):
        return self.title

def catnotes(notelist: list):
    """
    Concatenate a list of notes into a str.
    """
    final = ""
    for note in notelist:
        final += note.flaskrender()

    return final

def dumpnotes(notes):
    """
    Get our notes list and save them as pickle to notes.pickle
    """
    with open('notes.pickle', 'wb') as mpf:
        pickle.dump(notes, mpf)
    
    return True

def getnotes():
    """
    Get our notes from the file notes.pickle
    """
    if exists("./notes.pickle"):
        with open('notes.pickle', 'rb') as mpf:
            notes = pickle.load(mpf)
    else:
        notes = []

    return notes


 
#----------! MAIN
app = Flask(__name__)

@app.route('/', methods=['GET'])
def render():
    return render_template("homepage.html", nr = catnotes(getnotes()))

@app.route('/', methods=['POST'])
def homepage():
    notetitle = request.form['title']
    notetext = request.form['text']
    rightnow = int(time.time())
    newnote = note(createtime=rightnow, modtime=rightnow, title=notetitle, text=notetext)
    notes = getnotes()
    notes.append(newnote)
    notes = sorted(notes, key=lambda note: note.modtime, reverse=True)
    dumpnotes(notes)
    return render_template("homepage.html", nr = catnotes(getnotes()))



if __name__ == '__main__':
    app.run()

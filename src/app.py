#!/usr/bin/env python3
#coding: utf-8
from flask import Flask, render_template, Markup, request, redirect, url_for
import markdown

#!---------- squiNotes.py ----------
# My notes-taking app
#-----------------------------!

#CLASS
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
        import datetime
        timestamp = datetime.datetime.fromtimestamp(pretimestamp)
        timestamp = timestamp.strftime("%d/%m/%Y-%H:%M:%S")
        return timestamp

    def flaskrender(self):
        """
        Render the note as html for flask, using flask.Markup
        """
        rendered = f"""
        <hr>
        <div class="notetitle">{Markup.escape(self.title)}</div>
        <form action="." method="GET" name="{self.createtime}">
        <button type="submit" name="delete" value="{self.createtime}" class="delbutton">Delete</button>|<button type="submit" name="edit" value="{self.createtime}" class="editbutton">Edit</button>
        </form>
        <div class="notetime">Created : {self.rendertime(self.createtime)}
        <br>Modified : {self.rendertime(self.modtime)}</div><br>
        <div class="notetext">{markdown.markdown(self.text, extensions=['fenced_code', 'codehilite', 'nl2br', 'smarty'])}</div><br>
        """
        return Markup(rendered)

    def __str__(self):
        return self.title

#FUNC
def dumpnotes(notes):
    """
    Get our notes list and save them as pickle to notes.pickle
    """
    import pickle
    with open('notes.pickle', 'wb') as mpf:
        pickle.dump(notes, mpf)
    
    return True

def getnotes():
    """
    Get our notes from the file notes.pickle
    """
    from os.path import exists
    import pickle

    if exists("./notes.pickle"):
        with open('notes.pickle', 'rb') as mpf:
            notes = pickle.load(mpf)
    else:
        notes = []

    return notes

def catnotes(notelist: list):
    """
    Concatenate a list of notes into a str.
    """
    final = ""
    for note in notelist:
        final += note.flaskrender()

    return final

def delnote(timestamp: int):
    """
    Delete note in our pickle file for which the createtime corresponds to timestamp
    """
    notes = getnotes()
    for note in notes:
        if int(note.createtime) == int(timestamp):
            notes.remove(note)
            dumpnotes(notes)
            return True
    return False

def findnote(createtime: int):
    """
    Find a note in our pickle file of notes by its createtime
    """
    notes = getnotes()
    for note in notes:
        if note.createtime == createtime:
            return note

def addnote(mynote: note):
    """
    Add a note to our notes pickle file (and sort it).
    """
    notes = getnotes()
    notes.append(mynote)
    notes = sorted(notes, key=lambda note: note.modtime, reverse=True)
    dumpnotes(notes)


 
#----------! MAIN
app = Flask(__name__)

@app.route('/', methods=['GET'])
def render():
    #Delete has been clicked
    try:
        todelete = request.args.get("delete")
        delnote(int(todelete))
    except Exception as e:
        pass

    #Edit has been clicked
    try:
        toedit = request.args.get("edit")
        if toedit is not None:
            return redirect(url_for('edit', notenumber=toedit))
    except Exception as e:
        pass
    
    return render_template("homepage.html", nr = catnotes(getnotes()))

#Edition mode
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    import time
    if request.method == "GET":
        notenumber = request.args.get("notenumber")
        mynote = findnote(int(notenumber))
        delnote(int(notenumber))
    return render_template("edit.html", notenumber=notenumber, ntitle=mynote.title, ntext=mynote.text)

#Basic route, allows note creation
@app.route('/', methods=['POST'])
def homepage():
    import time
    #New note
    try:
        notetitle = request.form['title']
        notetext = request.form['text']
        rightnow = int(time.time())
        newnote = note(createtime=rightnow, modtime=rightnow, title=notetitle, text=notetext)
        addnote(newnote)
    except:
        pass
    return render_template("homepage.html", nr = catnotes(getnotes()))



if __name__ == '__main__':
    app.run(host="0.0.0.0")

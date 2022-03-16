#!/usr/bin/env python3
#coding: utf-8
from flask import Flask, render_template, Markup, request
import datetime, time

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
        <div class="notetitle">{self.title}</div><br>
        <div class="notetime">Created : {self.rendertime(self.createtime)} Modified : {self.rendertime(self.modtime)}</div><br>
        <div class="notetext">{self.text}</div><br>"""
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
 


#----------! MAIN
app = Flask(__name__)

note1 = note(createtime=1647435623, modtime=1647435682, title="I love coffee", text="I love coffee. It is hot and delicious.")

note2 = note(createtime=1647435879, modtime=1647435999, title="I wanna go home", text="At first it was like dream, and then O I want to go home")

#Sort the notes ! Oldest first !
global notes
notes = [note1, note2]
notes = sorted(notes, key=lambda note: note.modtime, reverse=True)

@app.route('/')
def homepage():
    return render_template("homepage.html", nr = catnotes(notes))

@app.route('/', methods=['POST'])
def newnote():
    notetitle = request.form['title']
    notetext = request.form['text']
    rightnow = int(time.time())
    newnote = note(createtime=rightnow, modtime=rightnow, title=notetitle, text=notetext)
    notes.append(newnote)
    notes = sorted(notes, key=lambda note: note.modtime, reverse=True)
    homepage()




if __name__ == '__main__':
    app.run()

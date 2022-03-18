#!/usr/bin/env python3
#coding: utf-8
from flask import Flask, render_template, Markup, request, redirect, url_for
from classes import note
from funcs import dumpnotes, getnotes, catnotes, delnote, findnote, addnote, mknotedir, exportnotes

#!---------- squiNotes.py ----------
# My notes-taking app
#-----------------------------!


#----------! MAIN
app = Flask(__name__)
mknotedir()

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

#Export mode
@app.route('/export', methods=['GET'])
def rawnotes():
    return render_template("export.html", rawnotes = exportnotes())

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

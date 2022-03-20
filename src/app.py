#!/usr/bin/env python3
#coding: utf-8
from flask import Flask, render_template, Markup, request, redirect, url_for, make_response
from classes import note
from funcs import dumpnotes, getnotes, catnotes, delnote, findnote, addnote, mknotedir, exportnotes, getthemes
from random import choice

#!---------- squiNotes.py ----------
# My notes-taking app
#-----------------------------!


#----------! MAIN
app = Flask(__name__)
mknotedir()
#Theme variable will be made global in every flask function
#css path will then be deducted

@app.route('/', methods=['GET'])
def render():
    #Does the user have a theme ?
    #theme list
    themes = getthemes()

    #Setting default theme if the user does not have one...
    if request.cookies.get('csslink') is None:
        csslink = themes[0]
        resp = make_response(render_template("homepage.html", nr = catnotes(getnotes()), csslink = csslink))
        resp.set_cookie("csslink", csslink)
    #...or using their preferred theme if do have one
    else:
        csslink = request.cookies.get('csslink')
        resp = make_response(render_template("homepage.html", nr = catnotes(getnotes()), csslink = csslink))

    #Delete has been clicked
    try:
        todelete = request.args.get("delete")
        if todelete is not None:
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

    #Switch theme has been clicked
    try:
        switchpls = request.args.get("switchpls")
        if switchpls is not None:
            #Clicking "Change theme" switches to a random (other) theme
            current = csslink
            while csslink == current:
                csslink = choice(themes)

            #Commiting new theme, setting cookie for it, return template
            #resp = make_response(render_template("homepage.html", nr = catnotes(getnotes()), csslink = csslink))
            resp = make_response(redirect(request.path,code=302))
            resp.set_cookie('csslink', csslink)
            return resp

    except Exception as e:
        pass

    #Read has been clicked
    try:
        toread = request.args.get("toread")
        if toread is not None:
            return redirect(url_for('readmode', note=(int(toread))))
    except Exception as e: 
        pass
    
    return resp

#Export mode
@app.route('/export', methods=['GET'])
def rawnotes():
    #No theme in export
    return render_template("export.html", rawnotes = exportnotes())

#Read mode
@app.route('/readmode', methods=['GET','POST'])
def readmode():
    #theme
    csslink = request.cookies.get('csslink')


    #Render page
    if request.method == 'GET':
        notenumber = request.args.get("note")
        mynote = findnote(int(notenumber))
    return render_template("read.html", note=mynote.flaskrender(), csslink = csslink)


#Edition mode
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    import time
    #theme
    csslink = request.cookies.get('csslink') 

    #Render edition page
    if request.method == "GET":
        notenumber = request.args.get("notenumber")
        mynote = findnote(int(notenumber))
        return render_template("edit.html", notenumber=notenumber, ntitle=mynote.title, ntext=mynote.text, csslink = csslink)
    if request.method == "POST":
        notetitle = request.form['title']
        notetext = request.form['text']
        notenumber = int(request.form['notenumber'])
        delnote(notenumber)
        rightnow = int(time.time())
        newnote = note(createtime=notenumber, modtime=rightnow, title=notetitle, text=notetext)
        addnote(newnote)
        return render_template("read.html", note=newnote.flaskrender(), csslink = csslink)


#Basic route, allows note creation
@app.route('/', methods=['POST'])
def homepage():
    import time

    #theme
    csslink = request.cookies.get('csslink')

    #New note
    try:
        notetitle = request.form['title']
        notetext = request.form['text']
        rightnow = int(time.time())
        newnote = note(createtime=rightnow, modtime=rightnow, title=notetitle, text=notetext)
        addnote(newnote)
    except:
        pass
    return render_template("homepage.html", nr = catnotes(getnotes()), csslink = csslink)

if __name__ == '__main__':
    app.run(host="0.0.0.0")

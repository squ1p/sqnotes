#!/usr/bin/env python3
#coding: utf-8
from classes import note

def mknotedir():
    """
    Create our data directory if does not exist.
    """
    from os.path import exists
    from os import mkdir

    if not exists("./data"):
        mkdir("./data")

def dumpnotes(notes):
    """
    Get our notes list and save them as pickle to notes.pickle
    """
    import pickle
    with open('./data/notes.pickle', 'wb') as mpf:
        pickle.dump(notes, mpf)

    return True

def getnotes():
    """
    Get our notes from the file notes.pickle
    """
    from os.path import exists
    import pickle

    if exists("./data/notes.pickle"):
        with open('./data/notes.pickle', 'rb') as mpf:
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
        final += note.titlerender()

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

def exportnotes():
    """
    Export our notes in markdown, one after the other.
    """
    notes = getnotes()
    rawtext = ""
    for note in notes:
        rawtext += f"#{note.title}\n"
        rawtext += f"* Created: {note.rendertime(note.createtime)}\n"
        rawtext += f"* Modified: {note.rendertime(note.modtime)}\n"
        rawtext += f"{note.text}\n"
        rawtext += f"-----\n\n"

    return rawtext

    return 

def getthemes():
    """
    Find all themes present in our css folder and return a nice list of
    css links, for the user to pick into
    """
    from flask import url_for
    from os import listdir

    allfiles = listdir("./static/styles")
    themefiles, themes = [], []
    for myfile in allfiles:
        if myfile.endswith(".css"):
            themefiles.append(myfile)

    for themefile in themefiles:
        themes.append(url_for('static', filename=f'styles/{themefile}'))

    return themes


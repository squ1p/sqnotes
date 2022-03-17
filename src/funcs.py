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

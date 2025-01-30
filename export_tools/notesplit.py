#!/usr/bin/env python3
#coding: utf-8

#!---------- notesplit.py ----------
# Used for splitting notes extracted from my note-taking webapp
# into single markdown files.
# It was a good run but I am switching to obsidian.
#-----------------------------------!


#----------! FUNC
def get_args():
    '''Gets all the arguments passed to the script and returns them in a parse_args()-type object.
    No args
    Returns:
    -args : an args object containing all the optional arguments passed to the script.
    '''
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "File to split", action="store", type=str, required=True)
    parser.add_argument("-d", "--dest", help = "Folder to put the resulting files in - will overwrite anything already there !", action="store", type=str, required=True)

    #Creating the args object
    args=parser.parse_args()

    return args

def filesplit(file: str):
    '''Split the extract file and return a dict name.md : text of the note
    takes the path of the file
    '''
    import re
    with open(file, "r") as contents:
        contents = contents.read()

    res = {}
    contents = re.split(r'[^\-]\-\-\-\-\-[^\-]', contents)
    i = 0

    for note in contents:
        n = note.splitlines()
        title = f"untitled_{i}"
        i += 1

        for line in n:
            if line.startswith("#"):
                title = line[1:]
                print(f"FOUND TITLE {title} in {line}")
                break
        res[title] = note
        
    return res

def sanitize(title):
    '''Take a notetitle and make it a valid filename. Add md extension.
    '''
    title = title.replace("/", "_")
    title = title.replace(" ", "_")
    title = title.replace("\n", "_")
    title = title.replace("?", "_")
    title = title.replace("(", "_")
    title = title.replace(")", "_")
    title = title.replace(":", "_")
    title = title.replace(";", "_")
    title = title.replace('"', "_")
    title = title.replace("'", "_")
    title = f"{title}.md"

    return title

def savenotes(notes: dict, dest: str):
    '''Save notes to files in folder dest
    '''
    import os
    os.chdir(dest)
    
    for title in notes:
        text = notes[title]
        filename = sanitize(title)
        with open(filename, "w") as writer:
            writer.write(text)
        print(f"Saved {filename} in {dest}")



#----------! MAIN
args = get_args()
file = args.file
notes = filesplit(file)
savenotes(notes, args.dest)

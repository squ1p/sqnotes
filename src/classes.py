#!/usr/bin/env python3
#coding: utf-8

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

    def titlerender(self):
        """
        Render the note title and details as html for flask, using flask.Markup.
        """
        import markdown
        from flask import Markup

        rendered = f"""
        <hr>
        <div class="notetitle">{Markup.escape(self.title)}</div>
        <form action="." method="GET" name="{self.createtime}">
        <button type="submit" name="delete" value="{self.createtime}" class="delbutton" onclick="return confirm('Really ?')">Delete</button>|<button type="submit" name="edit" value="{self.createtime}" class="editbutton">Edit</button>|<button type="submit" name="toread" value="{self.createtime}" class="readbutton">Read</button>
        </form>
        <div class="notetime">Created : {self.rendertime(self.createtime)}
        <br>Modified : {self.rendertime(self.modtime)}</div><br>
        """
        return Markup(rendered)

    def flaskrender(self):
        """
        Render the note whole content as html for flask, using flask.Markup
        """
        import markdown
        from flask import Markup, url_for

        rendered = f"""
        <hr>
        <div class="notetitle">{Markup.escape(self.title)}</div>
        <form action="." method="GET" name="{self.createtime}">
        <button type="submit" name="delete" value="{self.createtime}" class="delbutton" onclick="return confirm('Really ?')">Delete</button>|<button type="submit" name="edit" value="{self.createtime}" class="editbutton">Edit</button>|<a href="{ url_for('render') }" class="backlink">Back</a>
        </form>
        <div class="notetime">Created : {self.rendertime(self.createtime)}
        <br>Modified : {self.rendertime(self.modtime)}</div><br>
        <div class="notetext">{markdown.markdown(self.text, extensions=['fenced_code', 'codehilite', 'nl2br', 'smarty'])}</div><br>
        """
        return Markup(rendered)

    def __str__(self):
        return self.title

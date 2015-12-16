# OFiction 

The purpose of Open Source Fiction (OFiction in short) is to pool together the creativity and diversity of people around the world to build unique stories. Maybe you have a great idea for a single character but no idea of how the character would fit into a story. Or maybe you have an idea for a unique plot twist but no idea of how you can incorporate it into a storyline. Or maybe you have a great first chapter to a book but simply do not have time to write the rest. OFiction is a place in which users can put forward these fragmented ideas, develop on other's ideas, and ultimately come to create a work of fiction that no one could have accomplished on their own.

## History

This project started out as Kent Shikama and Ziqi Xiong's final project for CSCI133 Databases at Pomona College.

## Development Set Up

- Clone this repository
- Install [Python 3.4+](https://www.python.org/downloads/)
- Copy `OFiction/settings.py.example` to `OFiction/settings.py` and edit as necessary
- Install all dependencies `pip3 install -r requirements.txt`
- Run the migrations `python3 manage.py migrate`
- Run the server `python3 manage.py runserver`
- Check out localhost:8000 on your browser

### A Development Small Hack

You may get an error `'latin' codec can't encode character u'\u2019'` on localhost while developing. This has to do with the fpdf library we are using.
If this isn't fixed in the near future, we might maintain a fork that permanently changes the below:

WL-198-146:fpdf kent$ pwd
/usr/local/lib/python3.5/site-packages/fpdf
WL-198-146:fpdf kent$ fpdf.py:1170: p = self.pages[n].encode("latin1") if PY3K else self.pages[n]

Change the above line to

WL-198-146:fpdf kent$ fpdf.py:1170: p = self.pages[n].encode("latin1", errors="ignore") if PY3K else self.pages[n]
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
# from models import Note

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(500), nullable=False)

    def __init__(self, title, text):
        self.title = title
        self.text = text

@app.route('/notes')
def notes():
    notes = Note.query.all()
    return render_template('notes.html', notes=notes)

@app.route('/notetext/<int:id>')
def notetext(id):
    notes = Note.query.get(id)
    return render_template('note_text.html', notes=notes)


@app.route('/addnote', methods = ['GET', 'POST'])
def addnote():
    if request.method == 'GET':
        return render_template('add_note.html')
    else:
        title = request.form['title']
        text = request.form['text']
        note = Note(title, text)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('notes'))


@app.route('/deletenote/<int:id>')
def deletenote(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import json
from . import db
from .validations import *
from .models import Note


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        print('in here')
        data = dict()
        
        data['note'] = request.form.get('note')
        
        _, err = validate_note_added(data)
        if err:
            flast(err, category="error")
            return render_template("home.html", user=current_user)
        
        print('in here')
        new_note = Note(data = data['note'], user_id=current_user.id)
        print(new_note)
        db.session.add(new_note)
        db.session.commit()
        flash('Successfully added a Note!', category="success")
        
    return render_template("home.html", user=current_user)


@views.route('/delete_note', methods=['POST'])
def delete_note():  
    print(request.data)
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


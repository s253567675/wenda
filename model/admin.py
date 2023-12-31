# encoding: utf-8
from flask import Blueprint, request, render_template, session, redirect, url_for

import dbhelper
from decorators import login_required, admin_required

admin_blu = Blueprint('admin', __name__)


@admin_blu.route('/right/<author_id>/', methods=['GET', 'POST'])
@admin_required
def right(author_id):
    if request.method == 'GET':
        user = dbhelper.fetch_user_by_id(author_id)
        if user["UserMute"] == '1':
            user["mute_text"] = "解禁"
        else:
            user["mute_text"] = "禁言"
        return render_template('user_right_manage.html', user_muted=user)
    else:
        user_id = request.form.get('user_id')
        user_mute = request.form.get('user_mute')
        dbhelper.update_user_mute(user_id, user_mute)
        user = dbhelper.fetch_user_by_id(user_id)
        if user["UserMute"] == '1':
            user["mute_text"] = "解禁"
        else:
            user["mute_text"] = "禁言"
        return render_template('user_right_manage.html', user_muted=user)


@admin_blu.route('/delete_question/', methods=['POST'])
@admin_required
def delete_question():
    question_id_delete = request.form.get('question_id_delete')
    dbhelper.delete_answers_by_questionID(question_id_delete)
    dbhelper.delete_question_by_questionId(question_id_delete)
    return redirect('/')

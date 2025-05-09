import os
from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from datetime import datetime, timezone
from ..db import db
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    
    try:
        tid = int(task_id)
    except ValueError:
        abort(make_response(
            {"message": f"Task id '{task_id}' is invalid. Must be an integer."},
            400
        ))

    task = db.session.get(Task, tid)
    if not task:
        not_found = {"message": f"Task with id '{task_id}' not found."}
        abort(make_response(not_found, 404))

    return task

@tasks_bp.post("")
def create_task():
    request_body = request.get_json() or {}
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.get("")
def get_all_tasks():

    query = db.select(Task)

    sort_param = request.args.get("sort") #Checks the URL for ?sort=asc or ?sort=desc
    if sort_param == "asc":
        query = query.order_by(Task.title)
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query) #Executes the query

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id":          task.id,
            "title":       task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })

    return tasks_response, 200

@tasks_bp.patch("/<id>/mark_complete")
def mark_complete(id):
    task = validate_task(id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    token = os.environ.get('SLACK_BOT_TOKEN', "")

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": "test-slack-api",
        "text": "Someone just completed the task: " + task.title
    }

    requests.post(url, headers=headers, json=payload)
    
    return Response(status=204, mimetype="application/json")
    
@tasks_bp.patch("/<id>/mark_incomplete")
def mark_incomplete(id):
    task = validate_task(id)

    # clear completed_at
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.get("/<id>")
def get_one_task(id):
    task = validate_task(id)

    task_data = {
        "id":           task.id,
        "title":        task.title,
        "description":  task.description,
        "is_complete":  bool(task.completed_at)
    }

    if task.goal_id is not None:
        task_data["goal_id"] = task.goal_id

    return {"task": task_data}, 200

@tasks_bp.put("/<id>")
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json() or {}
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    task.title       = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<id>")
def delete_task(id):
    task = validate_task(id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")
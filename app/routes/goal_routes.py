from flask import Blueprint, abort, make_response, request, Response
from ..models.goal import Goal
from ..models.task import Task
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        gid = int(goal_id)
    except ValueError:
        invalid = {"message": f"Goal id '{goal_id}' is invalid. Must be an integer."}
        abort(make_response(invalid, 400))

    goal = db.session.get(Goal, gid)
    if not goal:
        not_found = {"message": f"Goal with id '{goal_id}' not found."}
        abort(make_response(not_found, 404))

    return goal

@goals_bp.post("")
def create_goal():
    request_body = request.get_json() or {}
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = [g.to_dict() for g in goals]
    return goals_response, 200

@goals_bp.get("/<id>")
def get_one_goal(id):
    goal = validate_goal(id)
    return {"goal": goal.to_dict()}, 200

@goals_bp.put("/<id>")
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json() or {}
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.delete("/<id>")
def delete_goal(id):
    goal = validate_goal(id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
#------------------Wave 6------------------------
@goals_bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)

    data = request.get_json() or {}
    if "task_ids" not in data or not isinstance(data["task_ids"], list):
        return make_response({"details": "Invalid data"}, 400)

    tasks_to_assign = []
    for tid in data["task_ids"]:
        task = db.session.get(Task, tid)
        if not task:
            abort(make_response(
                {"message": f"Task with id '{tid}' not found."},
                404
            ))
        tasks_to_assign.append(task)

    goal.tasks = tasks_to_assign
    db.session.commit()

    return {"id": goal.id, "task_ids": data["task_ids"]}, 200

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)

    tasks_list = []
    for t in goal.tasks:
        tasks_list.append({
            "id":           t.id,
            "goal_id":      t.goal_id,        
            "title":        t.title,
            "description":  t.description,
            "is_complete":  bool(t.completed_at)
        })

    return {
        "id":    goal.id,
        "title": goal.title,
        "tasks": tasks_list
    }, 200
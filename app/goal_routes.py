from app import db
from app.models.goal import Goal
from app.models.task import Task 
from app.task_routes import validate_model
from flask import Blueprint, request, make_response, jsonify


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details" : "Invalid data"}, 400)
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    return {"goal" :new_goal.to_dict()}, 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    return jsonify([goal.to_dict() for goal in goals])

@goals_bp.route("<model_id>",methods=["GET"])
def read_one_goal(model_id):
    goal = validate_model(Goal, model_id)
    return {"goal": goal.to_dict()}

@goals_bp.route("/<model_id>", methods=["PUT"])
def update_goal(model_id):
    goal = validate_model(Goal, model_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return {
        "goal": goal.to_dict()
        }, 200

@goals_bp.route("<model_id>", methods=["DELETE"])
def delete_goal(model_id):
    goal = validate_model(Goal, model_id)
    db.session.delete(goal)
    db.session.commit()
    return {
        "details": f'Goal {model_id} "{goal.title}" successfully deleted'
        }, 200

@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)
        db.session.commit()
    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
        })), 200

@goals_bp.route("<goal_id>/tasks", methods=["GET"])
def read_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_response = [task.to_dict_with_goal() for task in goal.tasks]  
    return jsonify({
                "id": goal.goal_id,
                "title" : goal.title,
                "tasks" : task_response}), 200
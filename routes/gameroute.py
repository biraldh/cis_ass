from flask import Blueprint, render_template, request, jsonify
from controller.bananaGame import BananaGame
from controller.score import Score

game_bp = Blueprint("game", __name__)

banana_game = BananaGame(api_url="http://marcconrad.com/uob/banana/api.php")

@game_bp.route("/main")
def mainui():
    return render_template("homepage.html")

@game_bp.route("/play")
def gameui():
    image_url, _ = banana_game.get_question()
    leaderboard = Score.get_score()  
    return render_template("gameui.html", image_url=image_url, leaderboard = leaderboard)

@game_bp.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    leaderboard = Score.get_score()  # Get the leaderboard data from your Score model
    formatted_leaderboard = [{"username": entry[0], "score": entry[1]} for entry in leaderboard]
    return render_template("leaderboardui.html", leaderboard=formatted_leaderboard)

@game_bp.route("/submit", methods=["POST"])
def submit():
    user_solution = request.form.get("solution")
    question_url = request.form.get("question_url")

    score, is_correct = banana_game.submit_solution(user_solution)
    if is_correct:
        new_image_url, _ = banana_game.get_question()
        return jsonify({"message": "Correct! Moving to the next question.", 
                        "new_image_url": new_image_url, 
                        "score": score})
    else:
        return jsonify({"message": "Wrong answer. Please try again.", "score": score})

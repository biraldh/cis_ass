from flask import Flask, render_template, request, jsonify
import requests

class BananaGame:
    def __init__(self, api_url):
        self.api_url = api_url
        self.current_question_url = None
        self.current_solution = None
        self.score = 0

    def fetch_question(self):
        #get question
        response = requests.get(self.api_url)
        question_data = response.json()
        
        self.current_question_url = question_data['question']
        self.current_solution = question_data['solution']
        return self.current_question_url, self.current_solution

    def submit_solution(self, solution):
        #Checks answer
        return int(solution) == self.current_solution

    def set_score(self):
        self.score += 1
        return self.score

# initialize flask app and the BananaGame instance
app = Flask(__name__)
banana_game = BananaGame(api_url="http://marcconrad.com/uob/banana/api.php")

@app.route('/')
def gameui():
    # get the url and question
    image_url, solution = banana_game.fetch_question()
    return render_template('gameui.html', image_url=image_url)

@app.route('/submit', methods=['POST'])
def submit():
    user_solution = request.form.get('solution')
    question_url = request.form.get('question_url')

    # check if question matches current url
    if question_url != banana_game.current_question_url:
        return jsonify({"message": "Invalid question. Please try again."})

    # Check if the answer is correct
    is_correct = banana_game.submit_solution(user_solution)
    if is_correct:
        # fetc a new question if the answer is correct
        new_image_url, new_solution = banana_game.fetch_question()
        score = banana_game.set_score()
        return jsonify({"message": "Correct! Moving to the next question.", 
        "new_image_url": new_image_url, 
        "score": score
        })
    else:
        return jsonify({"message": "wrong answer please try again."})

if __name__ == '__main__':
    app.run(debug=True)

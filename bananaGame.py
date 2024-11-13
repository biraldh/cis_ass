from flask import Flask, render_template, request, jsonify
import requests


class Score:
    def set_score(self, solution):
        # Check answer
        if int(self.current_solution) == int(solution):
            self.score += 1
            self.result = True
        else:
            self.result = False
            
        return self.score, self.result

class Apicall:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_question(self):
        # get question and answer from API
        response = requests.get(self.api_url)
        question_data = response.json()
        return question_data['question'], question_data['solution']

class BananaGame(Score):
    def __init__(self, api_url):
        super().__init__()
        self.api_service = Apicall(api_url)
        self.api = api_url
        self.score = 0
        self.current_question_url = None
        self.current_solution = None

    def get_question(self):
        # fetch question and ans
        self.current_question_url, self.current_solution = self.api_service.fetch_question()
        return self.current_question_url, self.current_solution

    def submit_solution(self, solution):
        # send solution and get score and result
        return self.set_score(solution)




# initialize flask app and the BananaGame instance
app = Flask(__name__)
banana_game = BananaGame(api_url="http://marcconrad.com/uob/banana/api.php")

@app.route('/')
def gameui():
    # get the url and question
    image_url, solution = banana_game.get_question()
    return render_template('gameui.html', image_url=image_url)

@app.route('/submit', methods=['POST'])
def submit():
    user_solution = request.form.get('solution')
    question_url = request.form.get('question_url')

    # check if question matches current url
    if question_url != banana_game.current_question_url:
        return jsonify({"message": "Invalid question. Please try again."})

    # Check if the answer is correct
    score,is_correct = banana_game.submit_solution(user_solution)
    
    if is_correct:
        # fetc a new question if the answer is correct
        new_image_url, new_solution = banana_game.get_question()
        return jsonify({"message": "Correct! Moving to the next question.", 
        "new_image_url": new_image_url, 
        "score": score
        })
    else:
        return jsonify({"message": "wrong answer please try again.",
        "score": score
        })

if __name__ == '__main__':
    app.run(debug=True)

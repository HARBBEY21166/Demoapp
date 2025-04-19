from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Initialize game state
game_modes = {
    "Number Recognition": "number_recognition",
    "Letter Recognition": "letter_recognition",
    "Shape Identification": "shape_identification",
    "Color Matching": "color_matching"
}

def generate_question(game_mode):
    if game_mode == "number_recognition":
        return random.randint(1, 10)
    elif game_mode == "letter_recognition":
        return random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    elif game_mode == "shape_identification":
        return random.choice(["Circle", "Square", "Triangle", "Rectangle"])
    elif game_mode == "color_matching":
        return random.choice(["Red", "Blue", "Green", "Yellow"])

@app.route('/')
def index():
    if 'points' not in session:
        session['points'] = 0
    if 'game_mode' not in session:
        session['game_mode'] = "number_recognition"
    session['question'] = generate_question(session['game_mode'])
    return render_template('index.html', game_modes=game_modes, question=session['question'], points=session['points'])

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = request.form['answer'].strip().lower()
    correct_answer = str(session['question']).lower()
    if user_answer == correct_answer:
        session['points'] += 1
        result = "Correct! Great job!"
    else:
        result = f"Incorrect. The correct answer was {correct_answer}."
    session['question'] = generate_question(session['game_mode'])
    return render_template('index.html', game_modes=game_modes, question=session['question'], points=session['points'], result=result)

@app.route('/switch_game', methods=['POST'])
def switch_game():
    session['game_mode'] = game_modes[request.form['game_mode']]
    session['question'] = generate_question(session['game_mode'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
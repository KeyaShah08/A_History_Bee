from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

players = {}
questions = []
responses = []
scores = {}


class JudgeForm(FlaskForm):
    player1_name = StringField('Player 1 Name:', validators=[InputRequired()])
    player2_name = StringField('Player 2 Name:', validators=[InputRequired()])
    submit_settings = SubmitField('Submit Settings')


class QuestionForm(FlaskForm):
    question = StringField('Question:', validators=[InputRequired()])
    submit_question = SubmitField('Send Question')


class ResponseForm(FlaskForm):
    response = StringField('Response:', validators=[InputRequired()])
    submit_response = SubmitField('Submit Response')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = JudgeForm()
    if form.validate_on_submit():
        players['P1'] = form.player1_name.data
        players['P2'] = form.player2_name.data
        scores['P1'] = scores['P2'] = 0
        return redirect(url_for('judge'))

    return render_template('index.html', form=form)


@app.route('/judge', methods=['GET', 'POST'])
def judge():
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.question.data
        questions.append(question)
        return redirect(url_for('respond'))

    return render_template('judge.html', form=form, players=players, scores=scores)


@app.route('/respond', methods=['GET', 'POST'])
def respond():
    form = ResponseForm()
    game_log = ''

    if form.validate_on_submit():
        response = form.response.data

        if len(responses) % 2 == 0:
            # It's P1's turn
            responses.append(response)
            # Pass 'P1' as the player argument for P1's response
            game_log = judge_response(form, player='P1')
        else:
            # It's P2's turn
            responses.append(response)
            # Pass 'P2' as the player argument for P2's response
            game_log = judge_response(form, player='P2')

        form.response.data = ''  # Clear the response field after submission

    if len(responses) % 2 == 0:
        # It's P1's turn, render P1's respond.html template
        return render_template('respond.html', form=form, question=questions[-1], players=players, scores=scores, game_log=game_log)
    else:
        # It's P2's turn, render P2's respond.html template
        return render_template('p2_respond.html', form=form, question=questions[-1], players=players, scores=scores, game_log=game_log)


def judge_response(form, player):
    judge_message = ''
    question = questions[-1]
    response = responses[-1]
    judge_time = get_current_time()

    if is_correct(response, question):
        scores[player] += 1
        judge_message = f"[{judge_time}, Judge] OK"
    else:
        judge_message = f"[{judge_time}, Judge] NO"

    log_entry = f"[{judge_time}, {player}] {response}"
    log_entry_judge = f"{judge_message}\n"

    # Combine the log entry and judge message
    game_log = log_entry + log_entry_judge
    print(game_log)
    return game_log


def is_correct(response, question):
    # Add your logic here to determine if the response is correct for the given question
    # Assuming the correct answers are stored in a dictionary with questions as keys and answers as values
    correct_answers = {
        "When was the war of 1812?": "1812",
        "Where is the Alamo?": "San Antonio",
        "What is your name?": "Keya",
        "What are you doing?": "singing"
    
    
    
        # Add more questions and answers as needed
    }

    return response.strip().lower() == correct_answers.get(question.strip(), "").lower()


def get_responding_player(response):
    # Add your logic here to determine which player responded
    # Assuming players alternate their responses, starting with P1
    if len(responses) % 2 == 1:
        return 'P2'
    else:
        return 'P1'


def get_current_time():
    # Get the current time in seconds
    current_time = int(time.time())
    return current_time


if __name__ == '__main__':
    app.run()



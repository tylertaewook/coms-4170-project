from flask import Flask, render_template, request, abort, jsonify
import re
import random
app = Flask(__name__)

last_time = 0
cur_score = 0
cur_max = 0

# TODO: store images somewhere non local
hold_images = {
   "jug": ["jug/jug0.jpg","jug/jug1.jpg"],
   "crimp": ["crimp/crimp0.jpg","crimp/crimp1.jpg"],
   "sloper": ["sloper/sloper0.jpg","sloper/sloper1.jpg"],
   "pinch": ["pinch/pinch0.jpg","pinch/pinch1.jpg"],
   "pocket": ["pocket/pocket0.jpg","pocket/pocket1.jpg"]
}

explanations = {
   "jug": "Jugs are big holds that you can get most of your hand around. Any holds that are comfortable and easy to grip are called jugs.",
   "crimp": "Crimps are very small edges that can only fit a pad or two of your fingers.",
   "sloper": "Slopers are bulgy holds that don't have a positive angle for your hand to grip down on.",
   "pinch": "Pinches are exactly what they sound like - holds that you can pinch by engaging your fingers on one side and your thumb on the other.",
   "pocket": "Pockets are holes or divots that you can typically only fit a few fingers in."
}

lessons = [
   {
      "id": 0,
      "lesson_type": "question",
      "hold_type": "jug"
   },
   {
      "id": 1,
      "lesson_type": "explain",
      "hold_type": "jug"
   },
   {
      "id": 2,
      "lesson_type": "question",
      "hold_type": "crimp"
   },
   {
      "id": 3,
      "lesson_type": "explain",
      "hold_type": "crimp"
   },
   {
      "id": 4,
      "lesson_type": "question",
      "hold_type": "sloper"
   },
   {
      "id": 5,
      "lesson_type": "explain",
      "hold_type": "sloper"
   },
   {
      "id": 6,
      "lesson_type": "question",
      "hold_type": "pinch"
   },
   {
      "id": 7,
      "lesson_type": "explain",
      "hold_type": "pinch"
   },
   {
      "id": 8,
      "lesson_type": "question",
      "hold_type": "pocket"
   },
   {
      "id": 9,
      "lesson_type": "explain",
      "hold_type": "pocket"
   }
]

questions = [
   {
      "id": 0,
      "question_type": "select_image",
      "hold_type": "jug"
   },
   {
      "id": 1,
      "question_type": "select_image",
      "hold_type": "crimp"
   },
   {
      "id": 2,
      "question_type": "select_image",
      "hold_type": "sloper"
   },
   {
      "id": 3,
      "question_type": "select_image",
      "hold_type": "pinch"
   },
   {
      "id": 4,
      "question_type": "select_image",
      "hold_type": "pocket"
   },
]


@app.route('/')
def welcome():
   return render_template('homepage.html')   

def selectRandomCorrect(hold_type, num=2):
   return random.sample(hold_images[hold_type], num)


def selectRandomIncorrect(hold_type, num=2):
   global hold_images
   incorrect_imgs = sum([hold_images[key] for key in hold_images if key != hold_type], [])
   print(incorrect_imgs)
   return random.sample(incorrect_imgs, num)


@app.route('/lesson/<id>')
def lesson(id=0):
   global lessons
   global hold_images
   global explanations

   if int(id) >= len(lessons):
      return "Lesson Not Found"
   
   lesson = lessons[int(id)]
   if lesson["lesson_type"] == "question":
      # TODO: replace this with a function that randomly selects question type
      # this will probably reuse the code for the quiz portion when fully fleshed out
      # for the initial prototype, just use a multi select w/ 2 correct answers
      lesson["title"] = f'Select holds that look like {lesson["hold_type"].capitalize()}s'
      lesson["body"] = {
         "correct": selectRandomCorrect(lesson["hold_type"]),
         "incorrect": selectRandomIncorrect(lesson["hold_type"])
      }
   else:
      lesson["title"] = lesson["hold_type"].capitalize()
      lesson["body"] = {
         "text": explanations[lesson["hold_type"]],
         # TODO: add video field
      }
   
   return render_template('lesson.html', lesson=lesson, num_lessons=len(lessons))

@app.route('/datetime', methods=['GET', 'POST'])
def datetime():
    global last_time

    json_data = request.get_json()
    time = json_data['time']
    if json_data['start']:
       last_time = time
       return jsonify({})
    
   #  sends the time elapsed in ms
    return jsonify(time - last_time)

@app.route('/updateScore', methods=['GET', 'POST'])
def updateScore():
   global cur_score
   global cur_max

   json_data = request.get_json()
   cur_score += json_data['score']
   cur_max += json_data['maxScore']

    
   #  sends the current and max score
   return jsonify({ 'score': cur_score, 'max': cur_max })

@app.route('/resetScore', methods=['GET', 'POST'])
def resetScore():
   global cur_score
   global cur_max

   cur_score = 0
   cur_max = 0

   #  sends the current and max score
   return jsonify({ 'score': cur_score, 'max': cur_max })

@app.route('/quiz/<id>')
def quiz(id=0):
   global questions
   global hold_images
   global cur_score
   global cur_max

   question = questions[int(id)]
   if question["question_type"] == "select_image":
      question["title"] = f'Select holds that look like {question["hold_type"].capitalize()}s'
      question["body"] = {
         "correct": selectRandomCorrect(question["hold_type"]),
         "incorrect": selectRandomIncorrect(question["hold_type"])
      }
   # TODO: add slightly different structures for different question types

   return render_template('quiz.html', question=question, num_questions=len(questions), cur_score=cur_score, cur_max=cur_max)

@app.route('/result')
def result():
   return render_template("result.html", score=cur_score, max=cur_max)
   
if __name__ == '__main__':
   app.run(debug = True)





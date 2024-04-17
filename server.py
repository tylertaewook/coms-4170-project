from flask import Flask, render_template, request, abort, jsonify
import re
app = Flask(__name__)


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


@app.route('/')
def welcome():
   return render_template('homepage.html')   

@app.route('/lesson/<id>')
def lesson(id=0):
   global lessons
   global hold_images
   global explanations

   if int(id) >= len(lessons):
      return "Lesson Not Found"
   
   lesson = lessons[int(id)]
   if lesson["lesson_type"] == "question":
      # TODO: replace this with a function that randomly selects images and question type
      # for the initial prototype, just use a multi select w/ 2 correct answers
      lesson["title"] = f'Select holds that look like {lesson["hold_type"]}s'
      lesson["body"] = {
         "correct": [hold_images[lesson["hold_type"]][0], hold_images[lesson["hold_type"]][1]],
         "incorrect": [hold_images["sloper"][0], hold_images["crimp"][0]]
      }
   else:
      lesson["title"] = lesson["hold_type"]
      lesson["body"] = {
         "text": explanations[lesson["hold_type"]],
         # TODO: add video field
      }
   
   return render_template('lesson.html', lesson=lesson)
   
if __name__ == '__main__':
   app.run(debug = True)





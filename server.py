from flask import Flask, render_template, request, abort, jsonify
from datetime import datetime
import re
import random
app = Flask(__name__)

last_time = 0
cur_score = 0
cur_max = 0
start_time = None
end_time = None

# TODO: store images somewhere non local
hold_images = {
   "jug": ["jug/jug0.jpg","jug/jug1.jpg", "jug/jug2.jpg","jug/jug3.jpg"],
   "crimp": ["crimp/crimp0.jpg","crimp/crimp1.jpg", "crimp/crimp2.jpg","crimp/crimp3.jpg"],
   "sloper": ["sloper/sloper0.jpg","sloper/sloper1.jpg", "sloper/sloper2.jpg","sloper/sloper3.jpg"],
   "pinch": ["pinch/pinch0.jpg","pinch/pinch1.jpg", "pinch/pinch2.jpg","pinch/pinch3.jpg"],
   "pocket": ["pocket/pocket0.jpg","pocket/pocket1.jpg", "pocket/pocket2.jpg","pocket/pocket3.jpg"],
   "undercling": ["undercling/undercling0.jpg","undercling/undercling1.jpg", "undercling/undercling2.jpg","undercling/undercling3.jpg"]
}

compound_images = [
   {
      "id": 0,
      "image": "compound/akiyo0.jpg",
      "hold_types": {
         "left": ["pinch"],
         "right": ["crimp"]
      }
   },
   {
      "id": 1,
      "image": "compound/underclingjug0.jpg",
      "hold_types": {
         "left": ["undercling", "jug"],
         "right": ["undercling", "jug"]
      }
   },
   {
      "id": 2,
      "image": "compound/janja0.jpg",
      "hold_types": {
         "left": ["crimp", "pinch"],
         "right": ["crimp"]
      }
   },
   {
      "id": 3,
      "image": "compound/tomoa0.jpg",
      "hold_types": {
         "left": ["pinch"],
         "right": ["pinch", "sloper"]
      }
   },
   {
      "id": 4,
      "image": "compound/jakob0.jpg",
      "hold_types": {
         "left": ["sloper", "pinch"],
         "right": ["crimp"]
      }
   },
]

hold_info = {
   "jug": {
      "explanation": "Jugs are big holds that you can get most of your hand around. Any holds that are comfortable and easy to grip are called jugs.",
      "video-info" : {
         "id" :"rPCS1dkiu3k",
         "start": 128,
         "end": 179
      }
   },
   "crimp" :{
      "explanation": "Crimps are very small edges that can only fit a pad or two of your fingers.",
      "video-info" : {
         "id" :"rPCS1dkiu3k",
         "start": 281,
         "end": 325
      }
   },
   "sloper" :{
      "explanation": "Slopers are bulgy holds that don't have a positive angle for your hand to grip down on.",
      "video-info" : {
         "id" :"rPCS1dkiu3k",
         "start": 223,
         "end": 279
      }
   },
   "pinch" :{
      "explanation": "Pinches are exactly what they sound like - holds that you can pinch by engaging your fingers on one side and your thumb on the other.",
      "video-info" : {
         "id" :"rPCS1dkiu3k",
         "start": 367,
         "end": 405
      }
   },
   "pocket" :{
      "explanation": "Pockets are holes or divots that you can typically only fit a few fingers in.",
      "video-info" : {
         "id" :"rPCS1dkiu3k",
         "start": 407,
         "end": 465
      }
   },
   "undercling": {
      "explanation": "Underclings are holds that are oriented downwards, so that you grab them from underneath instead of on top of them.",
      "video-info" : {
         "id" :"rPCS1dkiu3k",
         "start": 180,
         "end": 222
      }
   }
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
      "hold_type": "undercling"
   },
   {
      "id": 3,
      "lesson_type": "explain",
      "hold_type": "undercling"
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
      "hold_type": "crimp"
   },
   {
      "id": 7,
      "lesson_type": "explain",
      "hold_type": "crimp"
   },
   {
      "id": 8,
      "lesson_type": "question",
      "hold_type": "pinch"
   },
   {
      "id": 9,
      "lesson_type": "explain",
      "hold_type": "pinch"
   },
   {
      "id": 10,
      "lesson_type": "question",
      "hold_type": "pocket"
   },
   {
      "id": 11,
      "lesson_type": "explain",
      "hold_type": "pocket"
   }
]

question_types = ["select_images", "dropdowns"]

questions = [
   {
      "id": 0,
      "question_type": "select_images",
      "hold_type": "jug"
   },
   {
      "id": 1,
      "question_type": "dropdowns"
   },
   {
      "id": 2,
      "question_type": "dropdowns"
   },
   {
      "id": 3,
      "question_type": "dropdowns"
   },
   {
      "id": 4,
      "question_type": "select_images",
      "hold_type": "pocket"
   },
]

used_images = set()


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
   global hold_info

   if int(id) >= len(lessons):
      return "Lesson Not Found"
   
   lesson = lessons[int(id)]
   if lesson["lesson_type"] == "question":
      lesson["title"] = f'Select holds that look like {lesson["hold_type"].capitalize()}s'
      lesson["body"] = {
         "correct": selectRandomCorrect(lesson["hold_type"]),
         "incorrect": selectRandomIncorrect(lesson["hold_type"])
      }
   else:
      lesson["title"] = lesson["hold_type"].capitalize()
      lesson["body"] = {
         "text": hold_info[lesson["hold_type"]]["explanation"],
         "video": hold_info[lesson["hold_type"]]["video-info"]
      }
   
   return render_template('lesson.html', lesson=lesson, num_lessons=len(lessons))

# @app.route('/datetime', methods=['GET', 'POST'])
# def datetime():
#     global last_time

#     json_data = request.get_json()
#     time = json_data['time']
#     if json_data['start']:
#        last_time = time
#        return jsonify({})
    
#    #  sends the time elapsed in ms
#     return jsonify(time - last_time)

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
   global start_time
   global used_images

   cur_score = 0
   cur_max = 0
   start_time = None
   used_images = set()
   #  sends the current and max score
   return jsonify({ 'score': cur_score, 'max': cur_max })

@app.route('/quiz/<id>')
def quiz(id=0):
   global questions
   global hold_images
   global cur_score
   global cur_max
   global start_time
   global used_images
   id = int(id)

   if id == 0: 
        start_time = datetime.now()

   question = questions[int(id)]
   if question["question_type"] == "select_images":
      question["title"] = f'Select holds that look like {question["hold_type"].capitalize()}s'
      question["body"] = {
         "correct": selectRandomCorrect(question["hold_type"]),
         "incorrect": selectRandomIncorrect(question["hold_type"])
      }
   elif question["question_type"] == "dropdowns":
      compound_image = random.choice([image for image in compound_images if image["id"] not in used_images])
      used_images.add(compound_image["id"])
      question["title"] = "Select the hold corresponding to each hand"
      question["body"] = {
         "image": compound_image["image"],
         "options": list(hold_info.keys()),
         "left": compound_image["hold_types"]["left"],
         "right": compound_image["hold_types"]["right"]
      }
   # TODO: add more question types

   return render_template('quiz.html', question=question, num_questions=len(questions), cur_score=cur_score, cur_max=cur_max)

@app.route('/result')
def result():
   global start_time
   global end_time
   global cur_score
   global cur_max

   end_time = datetime.now()
   duration = (end_time - start_time).total_seconds() if start_time else 0
   duration_str = str(int(duration // 3600)).zfill(2) + ":" + str(int((duration % 3600) // 60)).zfill(2) + ":" + str(int(duration % 60)).zfill(2)


   return render_template("result.html", score=cur_score, max=cur_max, duration=duration_str)
  

   
if __name__ == '__main__':
   app.run(debug = True)





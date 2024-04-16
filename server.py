from flask import Flask, render_template, request, abort, jsonify
import re
app = Flask(__name__)


@app.route('/')
def welcome():
   return render_template('homepage.html')   

if __name__ == '__main__':
   app.run(debug = True)





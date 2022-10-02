import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/results')
def my_link():
  print(os.getcwd())
  os.system("python Drowsiness_Detection.py")
  return render_template('analysis.html')

if __name__ == '__main__':
  app.run(debug=True)

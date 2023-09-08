from flask import Flask, render_template, request
import pika
import sys
import os
from sendQuestion_receiveAnswer import consumer, producer
  
app = Flask(__name__)
user_input = "ui"
received_ans = "default"
  
@app.route('/')
def home():
    return render_template("index.html")
  
@app.route('/answer', methods=['POST'])
def process_msg():
    global received_ans, user_input
    user_input = request.form['inputText']
    producer(user_input)
    received_ans = consumer()
    return render_template("answer.html", ans=received_ans, que=user_input)
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)

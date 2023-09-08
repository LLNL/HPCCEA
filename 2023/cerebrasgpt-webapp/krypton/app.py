#Might need to edit paths below so that you are able to access the data files
from flask import Flask, render_template, request
from rabbit import rconsume_analytics, rconsume_answer, rproduce_question
import re

app = Flask(__name__)

#Global variables used for Flask
user_input = ""
received_ans = ""
time = 0
thumbs_up_points = 0
thumbs_down_points = 0
thumbs_up_p = 0
thumbs_down_p = 0
sentiment = 'Sentiment(polarity=10, subjectivity=10) : Sentiment(polarity=10, subjectivity=10)'

#load in satisfaction rating variables from sat.txt
file_path = './data/sat.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

#Keep old thumbs up and thumbs down ratings (loading in from a file)
thumbs_up_points = int(lines[0].strip())
thumbs_down_points = int(lines[1].strip())

#Home page
@app.route('/')
def home():
    return render_template("index.html")

#About page
@app.route('/about')
def about():
    return render_template("about.html")

#Returns answer page
@app.route('/answer', methods=['GET'])
def process_msg():
    global time, received_ans, sentiment
    
    #receive answer from LLM
    received_ans = rconsume_answer()
    elements = received_ans.split(" : ")
    received_ans = elements[0]
    time = elements[1]

    #receive sentiment from Kafka analytics
    sentiment = rconsume_analytics()

    #write response time received to file for graph use
    file_path = './data/rt.txt'
    with open(file_path, 'a') as file:
        file.write(time + '\n')

    return render_template("answer.html", ans=received_ans, que=user_input)

    
#Rabbit gif loading for loading page
@app.route('/loading', methods=['POST'])
def loading():
    global user_input
    #receive question input from user and produce it to LLM
    user_input = request.form['inputText']
    rproduce_question(user_input)

    return render_template("loading.html")

#When thumbs up or thumbs down is clicked, it is sent here to update the user satisfaction ratings
@app.route('/thumbs', methods=['GET'])
def thumbs_up():
    global thumbs_up_points, thumbs_down_points, thumbs_down_p, thumbs_up_p, user_input, received_ans

    thumbs = request.args.get('thumbs')
    if thumbs and thumbs.lower() == 'up':
        thumbs_up_points += 1
    elif thumbs and thumbs.lower() == 'down':
        thumbs_down_points += 1

    return render_template("answer.html", que=user_input, ans=received_ans)


#Displays all of our analytics + graphs on analytics page
@app.route('/analytics')
def analytics():
    global thumbs_up_p, thumbs_down_p, sentiment, time

    #Calculate user satisfaction percentage and write to file to create a graph
    total_points = thumbs_down_points + thumbs_up_points
    thumbs_up_p = (thumbs_up_points / total_points) * 100 if total_points > 0 else 0
    thumbs_down_p = (thumbs_down_points / total_points) * 100 if total_points > 0 else 0

    with open(file_path, 'w') as file:
        file.write(str(thumbs_up_points) + '\n')
        file.write(str(thumbs_down_points) + '\n')

    #Getting question and answer sentiment (split them up based off of delimiter we defined)
    elements = sentiment.split(" : ")

    qsent = elements[0]
    asent = elements[1]
    qpol = str(float(re.search(r'polarity=(-?\d+\.\d+)', qsent).group(1)))
    qsub = str(float(re.search(r'subjectivity=(-?\d+\.\d+)', qsent).group(1)))

    apol = str(float(re.search(r'polarity=(-?\d+\.\d+)', asent).group(1)))
    asub = str(float(re.search(r'subjectivity=(-?\d+\.\d+)', asent).group(1)))

    #If valid sentiment values, write and read them to a file for graph (default is 10, so if 10, do not include)
    if qpol != "10":

        #Writing values of sentiment to text file
        with open('./data/qpol.txt', 'a') as file:
            file.write(qpol + '\n')

        with open('./data/apol.txt', 'a') as file:
            file.write(apol + '\n')

        with open('./data/qsub.txt', 'a') as file:
            file.write(qsub + '\n')

        with open('./data/asub.txt', 'a') as file:
            file.write(asub + '\n')

        #Reading values of different analytics from text file to use for graphs 
        with open('./data/qpol.txt', 'r') as file:
            qpoldata = file.readlines()

        with open('./data/apol.txt', 'r') as file:
            apoldata = file.readlines()

        with open('./data/qsub.txt', 'r') as file:
            qsubdata = file.readlines()

        with open('./data/asub.txt', 'r') as file:
            asubdata = file.readlines()
        
        with open('./data/rt.txt', 'r') as file:
            tdata = file.readlines()
        labels = list(range(1, len(tdata) + 1))

    #Returning with all of our analytics for analytics page to correctly display information
    return render_template("analytics.html",
                           tdata=tdata,
                           labels=labels,
                           up=thumbs_up_p,
                           down=thumbs_down_p,
                           rt=time,
                           qpol=qpol,
                           qsub=qsub,
                           apol=apol,
                           asub=asub,
                           qpoldata=qpoldata,
                           apoldata=apoldata,
                           qsubdata=qsubdata,
                           asubdata=asubdata) 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
    

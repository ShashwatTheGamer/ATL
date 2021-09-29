from flask import Flask,send_from_directory,render_template, request,redirect
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

f = open('data.json',)
data = json.load(f)
f.close()


# @cross_origin()
# @app.route('/images/<path:path>')
# def send_images(path):
#     return send_from_directory('images', path)

# Custom static data
@cross_origin()
@app.route('/images/<path:filename>')
def custom_static(filename):
    return send_from_directory('images', filename)

@cross_origin()
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/planets')
def Planets():
    
    planet = request.args.get('planet')
    if planet == None:
        planet="earth"
    Planet=planet.capitalize()
    planetdata=data[planet]

    mass = planetdata["mass10_24Kg"]
    volume = planetdata["volume10_10Km3"]
    escape = planetdata["escapeVelocityKmS"]
    rotation = planetdata["siderealRotationPeriodHrs"]
    length = planetdata["lengthOfDayHrs"]
    dist = planetdata["semimajorAxis10_6Km"]
    temp = planetdata["blackBodyTemperatureK"]

    fact = facts[planet]
    # surfaceGravityMS2
    # surfaceGravityEqMS2


    return render_template('Info.html',planet=planet,Planet=Planet,
    mass=mass,volume=volume,fact=fact,escape=escape,
    rotation=rotation,length=length,dist=dist,temp=temp)

@app.route('/levelup')
def LevelUp():
	
	coins = request.args.get('coins')
	planet = request.args.get('planet')
	if coins == None:
		coins=0
	else:
		coins = int(coins)

	if planet == None:
		newlevel=planetslist[0]
	elif planet == planetslist[-1]:
		newlevel= planetslist[0]
	else:
		newlevel= planetslist[planetslist.index(planet)+1]

	if coins < 100:
		screen = "images/level%20up/level%20up%200.png"
	elif coins < 200:
		screen = "images/level%20up/level%20up%201.png"
	elif coins < 300:
		screen = "images/level%20up/level%20up%202.png"
	else:
		screen = "images/level%20up/level%20up%203.png"

	if coins >= 1000:
		coins=str(coins/1000)[0:3]+"k"

	return render_template('LevelUp.html',coins=str(coins),screen=screen,newlevel=newlevel)

@app.route('/quiz')
def Quiz():
    
	planet = request.args.get('planet')
	question = request.args.get('question')
	coins = request.args.get('coins')

	if planet == None:
		planet="earth"
	if question == None:
		question="Q1"
	if coins == None:
		coins="0"

	if int(question[1:]) == 3:
		nexturl = f"levelup?planet={planet}&coins="
	else:
		questionnext = question[0]+str(int(question[1:])+1)
		nexturl = f"quiz?planet={planet}&question={questionnext}&coins="

	questionJson = questions[planet][question]
	questionText = questionJson["question"]
	correctOption = questionJson[questionJson["correctoption"]]
	option1 = questionJson["option1"]
	option2 = questionJson["option2"]
	option3 = questionJson["option3"]
	return render_template('quiz.html',
		planet=planet, 
		coins=coins,
		nexturl=nexturl,
		questionText=questionText,
		correctOption=correctOption,
		option1=option1,
		option2=option2,
		option3=option3,
		question=question)


@app.route('/library1')
def Library1():
    return render_template('NewPage1.html')


@app.route('/library2')
def Library2():
    return render_template('NewPage2.html')

@app.route('/start')
def Start():
    return render_template('StartPage.html')

@app.route('/')
def Home():
    return render_template('Main.html')

@app.route('/game')
def Game():
    return render_template('game.html')

planetslist = [
	"mercury",
	"venus",
	"earth",
	"mars",
	"jupiter",
	"saturn",
	"uranus",
	"neptune",
]

facts = {
	"mercury":"Mercury is hot, but not too hot for ice.",
	"venus":"Venus doesn’t have any moons, and we aren’t sure why.",
	"earth":"You can see Earth’s magnetic field at work during light shows.",
	"mars":"Mars had a thicker atmosphere in the past.",
	"jupiter":"Jupiter is a great comet catcher.",
	"saturn":"No one knows how old Saturn’s rings are.",
	"uranus":"Uranus is more stormy than we thought.",
	"neptune":"Neptune has supersonic winds."
}

questions = {
    "mercury" : {
        "Q1" : {
            "question":"What is Mercury's proximity to the Sun?",
            "option1":"8th planet furthest from sun",
            "option2":"First planet closest to the Sun",
            "option3":"5th planet at some distance from the sun",
            "correctoption":"option2",
        },
		"Q2" : {
            "question":"Mercury has many craters on its surface. Which is the largest in diameter?",
            "option1":"Caloris Basin",
            "option2":"ligma segment",
            "option3":"flarina",
            "correctoption":"option1",
        },
		"Q3" : {
            "question":"Mercury is named after a Roman God. Which of the planet's attributes match that of the god it was named after?",
            "option1":"its strength",
            "option2":"its behaviour",
            "option3":"its speed",
            "correctoption":"option3",
        },
    },
	"venus" : {
        "Q1" : {
            "question":"What temperature would be typical for the planet Venus?",
            "option1":"860°F",
            "option2":"150°C",
            "option3":"540°F",
            "correctoption":"option1",
        },
		"Q2" : {
            "question":"Venus is often called the Earth's 'sister planet'. Why is this?",
            "option1":"They are of similar size and mass",
            "option2":"they both are girls",
            "option3":"option 1 and 2",
            "correctoption":"option1",
        },
		"Q3" : {
            "question":"From Earth, which planet is brighter than Venus?",
            "option1":"mars",
            "option2":"jupiter",
            "option3":"none",
            "correctoption":"option3",
        },
    },
	"earth" : {
        "Q1" : {
            "question":"When can the Earth's magnetic field be seen?",
            "option1":"aurora boriealis",
            "option2":"during an eclipse",
            "option3":"during summer solstice",
            "correctoption":"option1",
        },
		"Q2" : {
            "question":"Which planet(s) is/are in between Earth and the Sun?",
            "option1":"Mercury and Mars",
            "option2":"Mercury and Venus",
            "option3":"Just Mercury",
            "correctoption":"option2",
        },
		"Q3" : {
            "question":"How big is Earth’s radius?",
            "option1":"6,000 miles",
            "option2":"5,000 miles",
            "option3":"4,000 miles",
            "correctoption":"option3",
        },
    },
	"mars" : {
        "Q1" : {
            "question":"The presence of what makes Mars red?",
            "option1":"Sulphide Vapours",
            "option2":"Iron Oxides",
            "option3":"Phosphate ions",
            "correctoption":"option2",
        },
		"Q2" : {
            "question":"What kind of atmosphere does Mars have?",
            "option1":"medium",
            "option2":"thick",
            "option3":"thin",
            "correctoption":"option3",
        },
		"Q3" : {
            "question":"Why can’t water exist on Mars as liquid?",
            "option1":"Because of the low atmospheric presssure",
            "option2":"Because of the high atmospheric presssure",
            "option3":"Because of the high temperature",
            "correctoption":"option1",
        },
    },
	"jupiter" : {
        "Q1" : {
            "question":"By how many degrees is Jupiter's axis tilted?",
            "option1":"3.1°",
            "option2":"24.5°",
            "option3":"It is not tilted",
            "correctoption":"option1",
        },
		"Q2" : {
            "question":"What is the surface magnetic field of Jupiter (relative to Earth)?",
            "option1":"5",
            "option2":"14",
            "option3":"0",
            "correctoption":"option2",
        },
		"Q3" : {
            "question":" What is the surface gravity of Jupiter (relative to Earth)?",
            "option1":"1.15",
            "option2":"5.75",
            "option3":"2.53",
            "correctoption":"option3",
        },
    },
	"saturn" : {
        "Q1" : {
            "question":"What is the density of Saturn in g/cm^3?",
            "option1":"0.132",
            "option2":"0.678°C",
            "option3":"3.154",
            "correctoption":"option2",
        },
		"Q2" : {
            "question":"What is the radius of the planet Saturn?",
            "option1":"37,200 miles",
            "option2":"12,000 miles",
            "option3":"57,000 miles",
            "correctoption":"option1",
        },
		"Q3" : {
            "question":"What do Saturn's rings consist of?",
            "option1":"dense metal",
            "option2":"thin fog",
            "option3":"Chunks of ice and dust",
            "correctoption":"option3",
        },
    },
	"uranus" : {
        "Q1" : {
            "question":" What is the radius of the planet Uranus?",
            "option1":"85,560 miles",
            "option2":"157,000 miles",
            "option3":"16,120 miles",
            "correctoption":"option3",
        },
		"Q2" : {
            "question":"By 2020, how many rings was Uranus known to have?",
            "option1":"2",
            "option2":"13",
            "option3":"27",
            "correctoption":"option2",
        },
		"Q3" : {
            "question":"Uranus was found by––?",
            "option1":"Sir William Herschel",
            "option2":"Sir James Halones",
            "option3":"Madam Barbara Antony",
            "correctoption":"option1",
        },
    },
	"neptune" : {
        "Q1" : {
            "question":"In terms of the overall size of the planets, where does Neptune rank?",
            "option1":"second largest",
            "option2":"third largest",
            "option3":"fourth largest",
            "correctoption":"option3",
        },
		"Q2" : {
            "question":"Which color does Neptune appear to be?",
            "option1":"blue",
            "option2":"red",
            "option3":"green",
            "correctoption":"option1",
        },
		"Q3" : {
            "question":"What is the main component of Neptune's atmosphere?",
            "option1":"helium",
            "option2":"hydrogen",
            "option3":"nitrogen",
            "correctoption":"option2",
        },
    },
}
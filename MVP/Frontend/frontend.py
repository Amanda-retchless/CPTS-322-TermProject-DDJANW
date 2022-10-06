from flask import Flask, render_template, redirect
import requests, json

app = Flask(__name__)


def addImages():

    APIResponse = requests.get("http://localhost:105/landscape/")     
    landscape_data = json.loads(APIResponse.text)
    temp = landscape_data["data"]

    imageLocalURLs = []
    for i in range(1,15):
        imageLocalURLs.append('images/' + str(i) +'.jpg')
    
    for index, landscape in enumerate(temp):
        temp[index]["image"] = imageLocalURLs[index % len(imageLocalURLs)]
    return temp


@app.route("/", methods=["GET", "POST"])
def home():

    return render_template('landscapes.html', data = addImages())


@app.route("/<landscape_id>")
def business_info(landscape_id):

    APIResponse = requests.get("http://localhost:105/comment/" + landscape_id) 
    comments = json.loads(APIResponse.text)


    data = addImages()
    target = list(filter(lambda x: x["id"] == landscape_id, data))[0]

    if target == []:
        return """
        <h1>404</h1>
        <p>Invalid landscape ID! Please try your request again!</p>"""

    return render_template('Page-2.html', landscape = target, comments = comments["data"])

@app.route("/newuser/")
def add_user():
    return render_template('newuser.html')

@app.route("/thankyou/", methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')

@app.route("/quote")
def getQuote():
    return render_template("getQuote.html")


@app.route("/contact")
def getintouch():
    return render_template("emailContact.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)

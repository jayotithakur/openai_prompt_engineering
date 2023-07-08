import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        review = request.form["email"]
        spam_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_spam_prompt(review),
            temperature=0.6,
        )
        spam_label = spam_response.choices[0].text.strip().lower()

        if spam_label == "spam":
            result = "This email is classified as spam."
        else:
            result = "This email is not spam."

        return redirect(url_for("index", result=result))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/sentiment", methods=("GET", "POST"))
def sentiment():
    if request.method == "POST":
        review = request.form["review"]
        sentiment_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_sentiment_prompt(review),
            temperature=0.6,
        )
        sentiment_label = sentiment_response.choices[0].text.strip().lower()

        return redirect(url_for("sentiment", result=sentiment_label))

    result = request.args.get("result")
    return render_template("sentiment.html", result=result)

def generate_spam_prompt(email):
    return f"""Classify the following review as 'spam' or 'not spam':

Email: {email}"""

def generate_sentiment_prompt(review):
    return f"""Determine the sentiment of the following review:

Review: {review}"""

if __name__ == "__main__":
    app.run()

import numpy as np
import time
import string
import re
from nltk.corpus import stopwords
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import pickle
from titletest import *
import requests
from urllib.parse import urlparse
from GoogleNews import GoogleNews

from bs4 import BeautifulSoup
import easyocr
from chatbot import chatBot
from PIL import Image
from contactmail import findMail
from urlsecurity import urlSecurity
from newsfeed import newsFeed
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from countrycodes import country_codes

app = Flask(__name__)
Bootstrap(app)

newstitle_object = checkTitle("")
processes = [
    newstitle_object.spelling_mistakes,
    newstitle_object.classify_clickbait,
    newstitle_object.subjective_test,
    newstitle_object.is_newstitle,
    newstitle_object.present_on_google,
]
names = [
    "Checkingforspellingmistakes",
    "Checkingforclickbaittitle",
    "Checkingforsubjectivetitles",
    "Checkingforvalidnewstitle",
    "Checkingforwebavailability",
]
index = -1
pages = [
    "spellfail.html",
    "clickfail.html",
    "subjecfail.html",
    "newtitilefail.html",
    "availweb.html",
]
headline = ""
last_executed = True
inputurl = ""


def scrape_links(text):
    pattern = r"\b(?:(?:https?|ftp):\/\/|www\.)[-a-zA-Z0-9+&@#\/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#\/%=~_|]"
    links = re.findall(pattern, text)
    return links


def present_on_google_news_2(domain):
    domain = domain.replace("www.", "")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    ggl_news_link = f"https://www.google.com/search?q={domain}&tbm=nws"
    req = requests.get(ggl_news_link)
    sup = BeautifulSoup(req.content, "html.parser")
    link = sup.find("a", attrs={"jsname": "ACyKwe"})
    li = link["href"]
    li = li.replace("/url?q=", "")
    if link:
        nd_domain = urlparse(li)
        domain_name = nd_domain.netloc
        domain_name = domain_name.replace("www.", "")
        print(domain_name)
        print(domain)
        if domain in domain_name:
            return True
    return False


def is_url(text):
    pattern = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(pattern, text) is not None


def checkbox_activate1():
    global processes
    global names
    global pages
    processes = [
        newstitle_object.classify_clickbait,
        newstitle_object.subjective_test,
        newstitle_object.is_newstitle,
        newstitle_object.present_on_google,
    ]
    names = [
        "Checkingforclickbaittitle",
        "Checkingforsubjectivetitles",
        "Checkingforvalidnewstitle",
        "Checkingforwebavailability",
    ]
    pages = ["clickfail.html", "subjecfail.html", "newtitilefail.html", "availweb.html"]


def checkbox_activate2():
    global processes
    global names
    global pages
    processes = [newstitle_object.subjective_test, newstitle_object.present_on_google]
    names = ["Checkingforsubjectivetitles", "Checkingforwebavailability"]
    pages = ["subjecfail.html", "availweb.html"]


def checkbox_activate3():
    global processes
    global names
    global pages
    processes = [newstitle_object.present_on_google]
    names = ["Checkingforwebavailability"]
    pages = ["availweb.html"]


def checkbox_activate4():
    global processes
    global names
    global pages
    processes = [
        newstitle_object.spelling_mistakes,
        newstitle_object.subjective_test,
        newstitle_object.present_on_google,
    ]
    names = [
        "Checkingforspellingmistakes",
        "Checkingforsubjectivetitles",
        "Checkingforwebavailability",
    ]
    pages = ["spellfail.html", "subjecfail.html", "availweb.html"]


def set_all():
    global processes
    global names
    global index
    global pages
    global headline
    global newstitle_object
    headline = ""
    newstitle_object = checkTitle("")
    processes = [
        newstitle_object.spelling_mistakes,
        newstitle_object.classify_clickbait,
        newstitle_object.subjective_test,
        newstitle_object.is_newstitle,
        newstitle_object.present_on_google,
    ]
    names = [
        "Checkingforspellingmistakes",
        "Checkingforclickbaittitle",
        "Checkingforsubjectivetitles",
        "Checkingforvalidnewstitle",
        "Checkingforwebavailability",
    ]
    index = -1
    pages = [
        "spellfail.html",
        "clickfail.html",
        "subjecfail.html",
        "newtitilefail.html",
        "availweb.html",
    ]


@app.route("/")
def home():
    global index
    global headline
    headline = ""
    index = -1
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/newsfeed", methods=["POST", "GET"])
def news():
    if request.method == "POST":
        news_obj = newsFeed()
        query = request.form.get("search")
        dat = request.form.get("date")
        if dat is not None and dat != "":
            dat = dat.split("-")
        location = request.form.get("location")
        location = location.lower().capitalize()
        if location in country_codes:
            location = country_codes[location]
        else:
            location = "IN"
        x, y = news_obj.run(query=query, give_date=dat, location=location)
        return render_template("newsfeed.html", news_data=y)
    else:
        news_obj = newsFeed()
        x, y = news_obj.get_top_news()
        return render_template("newsfeed.html", news_data=y)


@app.route("/gettrue", methods=["POST", "GET"])
def getrtrue():
    global headline
    print("hii  " + headline)
    news_obj = newsFeed()
    x, y = news_obj.run(query=headline, give_date="", location="")
    return render_template("newsfeed.html", news_data=y)


@app.route("/detect", methods=["POST", "GET"])
def detect():
    global headline
    set_all()
    if request.method == "POST":
        input_text = request.form.get("text")
        if "image" in request.files:
            input_image = request.files["image"]
        input_url = request.form.get("texturl")
        print(input_url)

        if input_text != None:
            print(input_text)
            checkbox1 = request.form.get("check1")
            checkbox2 = request.form.get("check2")
            if checkbox1:
                checkbox_activate1()
            if checkbox2:
                checkbox_activate2()
            links = scrape_links(input_text)
            print(links)
            if len(links):
                for i in links:
                    input_text = input_text.replace(i, "")
                    if not urlSecurity(i).run():
                        return render_template("mal.html")
            if headline == "":
                headline = input_text
                newstitle_object.headline = headline
            return redirect(
                url_for("given_is_text", text=input_text, progress_name=names[0], num=1)
            )

        elif input_url is not None:
            if not is_url(input_url):
                return render_template("detect.html", prblm="Please enter valid url")
            try:
                req = requests.get(input_url)
            except:
                return render_template("notaccessible.html")
            soup = BeautifulSoup(req.content, "html.parser")
            text = soup.find("h1")
            if text == None:
                return render_template(
                    "detect.html",
                    prblm="the given website has no Headline text, please avoid using social media website urls",
                )
            nd_domain = urlparse(input_url)
            domain_name = nd_domain.netloc
            domain_name = domain_name.replace("www.", "")
            if not urlSecurity(input_url).run():
                return render_template("mal.html")
            # if present_on_google_news_2(domain_name) == False:
            #     return render_template("detect.html",
            #                            prblm="the given domain is not present on google news, Please give only news websites url, if a news website is not present on google news there is a high possibility that the news pubished by that specific news website if fake")
            checkbox_activate3()
            text_input = text.text
            links = scrape_links(text_input)
            if len(links):
                for i in links:
                    text_input = text_input.replace(i, "")
                    if not urlSecurity(i).run():
                        return render_template("mal.html")
            if headline == "":
                headline = text_input
                print(headline)
                newstitle_object.headline = headline
                if headline == " Access Denied" or headline == "Access Denied":
                    return render_template("notaccessible.html")

            return redirect(
                url_for("given_is_text", text=headline, progress_name=names[0], num=1)
            )

        elif input_image != None:
            checkbox4 = request.form.get("check4")
            temp_path = "images/image.jpg"
            input_image.save(temp_path)
            x = int(float(request.form["x"]))
            y = int(float(request.form["y"]))
            width = int(float(request.form["width"]))
            height = int(float(request.form["height"]))
            print(x, y, width, height)
            img = Image.open(temp_path)
            cropped_img = img.crop((x, y, x + width, y + height))
            cropped_img = cropped_img.convert("RGB")
            cropped_img.save("images/cropped_image.jpg")
            reader = easyocr.Reader(["en"])
            result = reader.readtext("images/cropped_image.jpg")
            extracted_text = [entry[1] for entry in result]
            x = ""
            x = " ".join(extracted_text)
            if x == "":
                return render_template(
                    "detect.html", prblm="please input images containing text"
                )
            checkbox_activate4()
            if checkbox4:
                checkbox_activate2()

            links = scrape_links(x)
            if len(links):
                for i in links:
                    x = x.replace(i, "")
                    if not urlSecurity(i).run():
                        return render_template("mal.html")

            if headline == "":
                headline = x
                newstitle_object.headline = headline

            return redirect(
                url_for("given_is_text", text=x, progress_name=names[0], num=1)
            )

    return render_template("detect.html")


@app.route("/truenews", methods=["GET", "POST"])
def true_news():
    return render_template("true_news.html", link=newstitle_object.recom_link)


@app.route("/autopopulate", methods=["GET", "POST"])
def autopopulate():
    url = request.json.get("url")
    print(url)
    findMail(
        url,
        newstitle_object.article + f"\n{newstitle_object.recom_link}+\n",
        newstitle_object.headline,
    ).run()
    return jsonify({"yes": True})


@app.route("/listen")
def listen():
    global index
    global headline
    index += 1
    newstitle_object.headline = headline
    val = processes[index]()
    print(val)
    if val == True:
        return jsonify({"value": True})
    else:
        return jsonify({"value": False})


@app.route("/chatbot/<string:question>")
def chatbot(question):
    print(question)
    cb = chatBot()
    if question:
        answer = cb.get_answer(question)
    return jsonify({"answer": answer})


@app.route(
    "/progress/<string:text>/<string:progress_name>/<int:num>", methods=["GET", "POST"]
)
def given_is_text(text, progress_name, num):
    global last_executed
    global headline
    global names
    global pages
    print(num)
    if num == 0:
        page = pages[names.index(progress_name)]  # Modify this line
        return render_template(page)
    else:
        ind = names.index(progress_name)

        if progress_name == "Checkingforspellingmistakes":
            return render_template(
                "new.html",
                input_data="Checking if given text contains any spelling mistakes",
                my_list=names,
            )
        if progress_name == "Checkingforclickbaittitle":
            return render_template(
                "new.html",
                input_data="Checking for clickbait title in given text",
                my_list=names,
            )
        if progress_name == "Checkingforsubjectivetitles":
            return render_template(
                "new.html",
                input_data="Checking the given text is Subjective or Objective",
                my_list=names,
            )
        if progress_name == "Checkingforvalidnewstitle":
            return render_template(
                "new.html",
                input_data="Checking the given textis Valid News Title or Not",
                my_list=names,
            )
        if progress_name == "Checkingforwebavailability":
            return render_template(
                "new.html",
                input_data="Checking the availability of given news in the Web",
                my_list=names,
            )


@app.route("/similar")
def similar():
    global newstitle_object
    print(newstitle_object.max_similarity)
    return jsonify({"similar": int(newstitle_object.max_similarity * 100)})


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        input_text = request.form.get("text")
        if input_text:
            print("hello" + input_text)
    test = request.form.values()
    test_ser = pd.Series(test)
    return render_template(
        "detect.html",
        prediction_text="Given News is {}!".format("true"),
        result="RESULT:",
    )


@app.route("/names")
def names():
    global names
    num = 1
    if len(names) == 5:
        num = 1
    if len(names) == 4:
        num = 2
    if len(names) == 2:
        num = 3
    if len(names) == 1:
        num = 4
    if len(names) == 3:
        num = 5
    return jsonify({"number": num})


@app.route("/checkasyoureadd", methods=["POST", "GET"])
def dblclick():
    driver = Chrome(service=Service(ChromeDriverManager().install()))
    global headline
    global inputurl
    set_all()
    driver.get(inputurl)
    time.sleep(1)
    inputurl = driver.current_url
    print(inputurl)
    req = ""
    try:
        req = requests.get(inputurl)
    except:
        return render_template("notaccessible.html")
    soup = BeautifulSoup(req.content, "html.parser")
    text = soup.find("h1")
    if not text:
        text = soup.find("title")

    # nd_domain = urlparse(inputurl)
    # domain_name = nd_domain.netloc
    # domain_name = domain_name.replace("www.", "")
    checkbox_activate3()
    if headline == "":
        headline = text.text
        if headline == " Access Denied" or headline == "Access Denied":
            return render_template("notaccessible.html")
        newstitle_object.headline = headline
    return redirect(
        url_for("given_is_text", text=headline, progress_name=names[0], num=1)
    )


@app.route("/givenews", methods=["POST", "GET"])
def givenews():
    global inputurl
    inputurl = request.form.get("input")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

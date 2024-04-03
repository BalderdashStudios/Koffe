from flask import Flask, url_for, render_template
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route('/p1')
def page1():
    countrys = get_country_options()
    #print(states)
    return render_template('page1.html', Country_options=countrys)

def get_country_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('coffee.json') as coffee_data:
        countrys = json.load(coffee_data)
    countrysList=[] 
    for c in countrys:
        if c["Location"] ["Country"] not in countrysList:
            countrysList.append(c ["Location"]["Country"])
    print(countrys)
    options=""
    for c in countrysList:
        options += Markup("<option value=\"" + c + "\">" + c + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_beans_options(countrys):
    with open('coffee.json') as coffee_data:
        beans = json.load(coffee_data)
    beansList=[]
    for c in countrys:
        if c[""]
    

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p2")
def render_page2():
    return render_template('page2.html')
    
@app.route("/p3")
def render_page3():
    return render_template('page3.html')
    
if __name__=="__main__":
    app.run(debug=False)

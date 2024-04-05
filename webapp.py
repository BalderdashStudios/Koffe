from flask import Flask, request, url_for, render_template
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route('/p1')
def page1():
    countrys = get_options("Location","Country")
    country = request.args.get('country')
    #print(states)
    return render_template('page1.html', Country_options=countrys)

@app.route('/countrys')
def render_beans_selCountry():
    country = request.args.get('country')
    beans = get_beans_options(country)
    highestTotal = get_highest_rated_beans(country)
    
    displayHighestTotal = "In " + country + ", the highest overall rated coffee bean is " + str(highestTotal) + "."
    
    return render_template('page1.html', beans_options=beans, highest_rated=displayHighestTotal)
    
@app.route('/showBeansBySelCountry')
def render_bean_info():
    selected_bean = request.args.get('beans')
    beanInfo = get_bean_info(selected_bean)
    
    displayBeanInfo = "Aroma:" + str(beanInfo) + "."
    return render_template('page1.html', bean_info=beanInfo)

def get_options(first_level,second_level):
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('coffee.json') as coffee_data:
        countrys = json.load(coffee_data)
    countrysList=[] 
    for c in countrys:
        if c[first_level] [second_level] not in countrysList:
            countrysList.append(c [first_level][second_level])
    options=""
    for c in countrysList:
        options += Markup("<option value=\"" + c + "\">" + c + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
    
def get_beans_options(country):
    with open('coffee.json') as coffee_data:
        beans = json.load(coffee_data)
    beansList=[]
    for c in beans:
        if c["Location"] ["Country"] == country:
            beansList.append(c["Data"] ["Owner"] + str(", Year made: ") + str(c["Year"]) + str(", Location: ") + c["Location"]["Region"] + str(", Species: ") + c["Data"]["Type"]["Species"]) 
    options=""
    for b in beansList:
        options += Markup("<option value=\"" + b + "\">" + b + "</option>")
    return options
    
def get_highest_rated_beans(country):
    with open('coffee.json') as coffee_data:
        beans = json.load(coffee_data)
    max = 0;
    for c in beans:
        if c["Location"] ["Country"] == country:
            if c["Data"] ["Scores"] ["Total"] > max:
                max = c["Data"] ["Scores"] ["Total"]
    return max
    
def get_bean_info(selected_bean):
    with open('coffee.json') as coffee_data:
        data = json.load(coffee_data)
    for d in data:
        if d["Data"] ["Owner"] + ["Year"] + ["Location"] ["Region"] + ["Data"]["Type"]["Species"]  == selected_bean:
            return d["Data"]["Scores"]
    return null;

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

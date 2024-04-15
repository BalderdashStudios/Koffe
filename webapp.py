from flask import Flask, request, url_for, render_template
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route('/p1')
def page1():
    countrys = get_countrys("Location","Country")
    country = request.args.get('country')
    #print(states)
    return render_template('page1.html', Country_options=countrys)

@app.route('/countrys')
def render_beans_selCountry():
    country = request.args.get('country')
    yearInfo = get_beans_options_one_level("Year", country)
    beans = get_beans_options("Data", "Owner",country)
    highestTotal = get_highest_rated_beans(country)
    ownerInfo = get_owners("Data", "Owner", country)
    
    displayHighestTotal = "In " + country + ", the highest overall rated coffee bean is " + str(highestTotal) + "."
    
    return render_template('page1.html', owners_options=ownerInfo,highest_rated=displayHighestTotal, selected_country=country)
    
@app.route('/showBeanOwners')
def render_bean_owner():
    country = request.args.get('selectedCountry')
    owner = request.args.get('owners')
    print(owner)
    regionInfo = get_regions_options("Location", "Region", country, owner)
    return render_template('page1.html', region_options=regionInfo, selected_country=country, selected_owner=owner)

@app.route('/showBeanRegions')
def render_bean_region():
    country = request.args.get('selectedCountry')
    owner = request.args.get('selectedOwner')
    print(owner)
    region = request.args.get('regions')
    yearInfo = get_years_options("Year",region, country, owner)
    return render_template('page1.html', year_options=yearInfo, selected_country=country, selected_owner=owner, selected_region=region)  

@app.route('/showYearOptions')
def render_bean_years():
    country = request.args.get('selectedCountry')
    owner = request.args.get('selectedOwner')
    region = request.args.get('selectedRegion')
    year = int(request.args.get('years'))
    
    
    speciesInfo = get_species_options("Data", "Type", "Species", country, region, owner, year)
    return render_template('page1.html', species_options=speciesInfo, selected_owner=owner, selected_country=country, selected_region=region,  selected_year=year)

@app.route('/showSpeciesOptions')
def render_bean_species():
    country = request.args.get('selectedCountry')
    owner = request.args.get('selectedOwner')
    region = request.args.get('selectedRegion')
    year = int(request.args.get('selectedYear'))
    species = request.args.get('species')
    
    totalScore = get_bean_score(species, country, region, owner, year)
    
    return render_template('page1.html', bean_species_name=species, bean_country=country, bean_total=totalScore)          
    
def get_species_options(data, type, species, country, region, owner, year):  
    with open('coffee.json') as coffee_data:
        beans = json.load(coffee_data)
    beansList=[]
    for c in beans:
        if c["Location"] ["Country"] == country and c["Location"] ["Region"] == region and c["Data"] ["Owner"] == owner and c["Year"] == year and c[data] [type] [species] not in beansList:
            beansList.append(c[data][type][species]) 
    options=""
    for b in beansList:
        options += Markup("<option value=\"" + str(b) + "\">" + str(b) + "</option>")
    return options



   
@app.route('/showBeansBySelCountry')
def render_bean_info():
    selected_bean = request.args.get('beans')
    beanInfo = get_bean_info(selected_bean)
    
    displayBeanInfo = "Aroma:" + str(beanInfo) + "."
    return render_template('page1.html', bean_info=beanInfo)

def get_countrys(first_level,second_level):
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('coffee.json') as coffee_data:
        countrys = json.load(coffee_data)
    countrysList=[] 
    for c in countrys:
        if c[first_level] [second_level] not in countrysList:
            countrysList.append(c [first_level][second_level])
    print(countrysList)
    options=""
    for c in countrysList:
        options += Markup("<option value=\"" + c + "\">" + c + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_owners(first_level,second_level,country):
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('coffee.json') as coffee_data:
        owners = json.load(coffee_data)
    ownersList=[] 
    for o in owners:
        if o["Location"] ["Country"] == country and o[first_level] [second_level] not in ownersList:
            ownersList.append(o [first_level][second_level])
    options=""
    for c in ownersList:
        options += Markup("<option value=\"" + c + "\">" + c + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
    
def get_beans_options(first_level,second_level,country):
    with open('coffee.json') as coffee_data:
        beans = json.load(coffee_data)
    beansList=[]
    for c in beans:
        if c["Location"] ["Country"] == country and c[first_level] [second_level] not in beansList:
            beansList.append(c[first_level] [second_level]) 
    options=""
    for b in beansList:
        options += Markup("<option value=\"" + b + "\">" + b + "</option>")
    print(options)
    return options
    
def get_regions_options(first_level,second_level,country,owner):
    with open('coffee.json') as coffee_data:
        beans = json.load(coffee_data)
    beansList=[]
    
    for c in beans:
        if c["Location"] ["Country"] == country and c["Data"] ["Owner"] == owner and c[first_level] [second_level] not in beansList:
            beansList.append(c[first_level] [second_level]) 
    print(beansList)
    options=""
    for b in beansList:
        options += Markup("<option value=\"" + b + "\">" + b + "</option>")
    return options
    
def get_years_options(first_level,region, country, owner):
    with open('coffee.json') as coffee_data:
        beans = json.load(coffee_data)
    beansList=[]
    for c in beans:
        if c["Location"] ["Country"] == country and c["Location"] ["Region"] == region and c["Data"] ["Owner"] == owner and c[first_level] not in beansList:
            beansList.append(c[first_level]) 
    options=""
    for b in beansList:
        options += Markup("<option value=\"" + str(b) + "\">" + str(b) + "</option>")
    return options
    
def get_beans_options_one_level(first_level,country):
    with open('coffee.json') as coffee_data:
        beans = json.load(coffee_data)
    beansList=[]
    for c in beans:
        if c["Location"] ["Country"] == country and c[first_level] not in beansList:
            beansList.append(c[first_level]) 
    options=""
    for b in beansList:
        options += Markup("<option value=\"" + str(b) + "\">" + str(b) + "</option>")
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
    
def get_bean_score(species, country, region, owner, year):
    with open('coffee.json') as coffee_data:
        data = json.load(coffee_data)
    score = "0";
    print(species)
    print(region)
    print(owner)
    print(year)
    print(country)
    for c in data:
        if c["Location"] ["Country"] == country and c["Location"] ["Region"] == region and c["Data"] ["Owner"] == owner and c["Year"] == year and c["Data"] ["Type"] ["Species"] == species:
             score = c["Data"]["Scores"]
             print(score)
    return score
    
    
def get_bean_scoreGraph(country):
    with open('coffee.json') as coffee_data:
        data = json.load(coffee_data)
    beanAverageYear = {}
    totalBeanYear = {}
    for c in data:
        if c["Location"] ["Country"] == country:
            if c["Year"] in beanAverageYear:
                beanAverageYear[c["Year"]] += c["Data"]["Scores"]["Total"]
            else:
                beanAverageYear[c["Year"]] = c["Data"]["Scores"]["Total"]
    for c in data:
        if c["Location"] ["Country"] == country:
            if c["Year"] in totalBeanYear:
                totalBeanYear[c["Year"]] += 1
            else:
                totalBeanYear[c["Year"]] = 1
                
    print(beanAverageYear)
    print(totalBeanYear)
    return beanAverageYear
    

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p2")
def render_page2():
    return render_template('page2.html')
    
@app.route("/p3")
def render_page3():
    countrys = get_countrys("Location","Country")
    country = request.args.get('country')
    #print(states)
    return render_template('page3.html', Country_options=countrys)
    
@app.route("/countrysGraph")
def render_graph():
    country = request.args.get('country')
    scores = get_bean_scoreGraph(country)
    return render_template('page3.html', Country_options=country)


if __name__=="__main__":
    app.run(debug=True)

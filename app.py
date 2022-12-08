#--------IMPORTS-----------
import collections

import matplotlib.pyplot as plt
import pandas as pd
import requests
import yfinance as yf
from flask import Flask, render_template
from flask import request
from flask import send_file
from flask_navigation import Navigation

collections.MutableSequence = collections.abc.MutableSequence
collections.Iterable = collections.abc.Iterable
from io import BytesIO
import PIL


#-------------------------------------




#-----First NEWS API---------- 

def getNewsTime (ticker, date):


    #API_KEY = "76a9ddfc65eb4de7abf122dd0e4b5a79"
    #API_KEY = "e99b6f6b19f34a8481032168353a38c1"
    API_KEY = "adbf07961127428f81541d29606150c8"
    
    params = {
        'q': ticker,
        'source': 'google-news',
        'sortBy': 'publishedAt',
        'pageSize': '5',
        'language': 'en',

    }

    headers = {
       'X-Api-Key': API_KEY,  # KEY in header to hide it from url
    }

    url = 'https://newsapi.org/v2/everything?q=' + ticker + '&from=' + date + '&to=' + date +'&sortBy=publishedAt&apiKey='+ API_KEY

    response = requests.get(url, params=params, headers=headers)

    data = response.json()

   
    
    articles = data["articles"] 
    result = [arr["title"] for arr in articles]
    links = [arr["url"] for arr in articles]

    
    return(result, links) 

#-------------------------------------


#-----Second NEWS API---------- 
def getNews (sym):
    API_KEY = "37404635d8f24e5689c288281204c8d6"

    q = sym
                             
    params = {
        'q': q,
        'source': 'google-news',
        'sortBy': 'popularity',
        'pageSize': '10',

    }

    headers = {
       'X-Api-Key': API_KEY,  # KEY in header to hide it from url
    }

    url = 'https://newsapi.org/v2/everything?q=' + q + '&apiKey=37404635d8f24e5689c288281204c8d6'

    response = requests.get(url, params=params, headers=headers)
    
    data = response.json()


    articles1 = data["articles"] 
    results = [arr["title"] for arr in articles1]
    Links1 = [arr["url"] for arr in articles1]

 
    return (results, Links1)

    
#-------------------------------------


#-----Third NEWS API----------

   #https://newsapi.org/v2/everything?q=tesla&from=2022-10-01&sortBy=publishedAt&apiKey=76a9ddfc65eb4de7abf122dd0e4b5a79

#-------------------------------------

#-------YFinance API---------------------


def yFincall(sym):
    
    stock_datas = yf.Ticker(sym).history(period='1d', interval='1h')
    stock_lists = list(stock_datas["Close"])
    stock_time = list(stock_datas.index)

    string_stock_time = []

    for time in stock_time:
        string_stock_time.append(str(time)[11:19])

    
    return(stock_lists, string_stock_time)
#-------------------------------------

#-------Interactive Graph YFinance API---------------------

def yFincalls(sym1):
    
    stock_data = yf.Ticker(sym1).history(period='7d', interval='1d')
    stock_list = list(stock_data["Close"])
    stock_times = list(stock_data.index)

    string_stock_times = []

    for time in stock_times:
        string_stock_times.append(str(time)[0:10])


    return(stock_list, string_stock_times)



#-------------------------------------

#-------Previous Data CSV---------------------


def stockcsv(tickersymbol, timeperiod):

    tesla = yf.Ticker(tickersymbol)
    tesla.info
    hist = tesla.history(period= timeperiod + "d")
    hist.reset_index(inplace=True)
    hist.to_csv('teslaTable.csv', index=False)
    #open('teslaTable.csv')

    
   
    
#-------------------------------------

#--------FLASK-------------------

app = Flask(__name__) #app needs to match wsgi from app import app
nav = Navigation(app)
#-------------------------------------


#----initializing Navigations----
nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('timeline', 'timeline'),
    nav.Item('previousdata', 'previousdata'),
    nav.Item('currentdata', 'currentdata'),
    nav.Item('comparison', 'comparison'),
])


plt.rcParams["figure.figsize"] = [6, 4]
plt.rcParams["figure.autolayout"] = True

#-------------------------------------


#-------Graph ------

def serve_figure(fig):
    fig.canvas.draw()
    pil_img = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(),fig.canvas.tostring_rgb())
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/jpeg')



def plot_png(x_and_y):
   
   x = x_and_y[1]
   y = x_and_y[0]
   fig = plt.figure()
   axis = fig.add_subplot(1, 1, 1)
  
  
  
   axis.plot(x, y)
   
   
   
   plt.xticks(rotation = 45)
   
   return serve_figure(fig)
#-------------------------------------
#--------------TWO LINE GRAPH ---------------
def plot_png_two_lines(x_and_y1, x_and_y2 ):
   #print(x_and_y)
   x1 = x_and_y1[1]
   y1 = x_and_y1[0]
   x2 = x_and_y2[1]
   y2 = x_and_y2[0]
   fig = plt.figure()
   axis = fig.add_subplot(1, 1, 1)
   
   
   axis.plot(x1, y1, label = comparison_symbol1)
   axis.plot(x2, y2, label = comparison_symbol2)
   axis.legend()
   
   plt.xticks(rotation = 45)
   
   return serve_figure(fig)

#-------------------------------------


@app.route('/indexgraph.jpeg')
def index_graph():

    return plot_png(yFincall('VTI'))

current_data_symbol = ''

@app.route('/currentdatagraph.jpeg')
def currentdata_graph():

    
   
    return plot_png(yFincall(current_data_symbol))    

comparison_symbol1 = ''

@app.route('/comparison1graph.jpeg')
def comparison1_graph():

    
   
    return plot_png(yFincall(comparison_symbol1))

comparison_symbol2 = ''

@app.route('/comparison2graph.jpeg')
def comparison2_graph():

    
   
    return plot_png(yFincall(comparison_symbol2))

@app.route('/comparison3graph.jpeg')
def comparison3_graph():

    
   
    return plot_png_two_lines(yFincall(comparison_symbol1),yFincall(comparison_symbol2)) 

interactivegraph_symbol = ''

@app.route('/interactivegraphgraph.jpeg')
def interactive_graph():

    
   
    return plot_png(yFincalls(interactivegraph_symbol))

#--------------------


#------ Ticker to Name ----
def symbol_to_name(sym):
    
    import json
    with open('company_tickers.json') as json_file:

        data = json.load(json_file)
        for i in list(data.values()):
            if i['ticker'] == sym:
                return i['title']
                break
#--------------------------

#-------HOME PAGE-------------
@app.route("/")
def index():

    
    index_graph()
    result, links = getNews('Stock')
    
    return render_template("index.html", result = result, links = links)

#--------------------------

#------TIME LINE-------------
@app.route('/timeline')
def timeline():
    return render_template('timeline.html')
#--------------------------  

#---------Prevoius Data--------------
@app.route('/previousdata', methods = ['POST', 'GET'])
def previousdata():

    
    
    global stocktickersym
    global timeperiod
    
    try:
        form_data = request.form
         
        stocktickersym = form_data["StockCSV"]
        timeperiod = form_data["Stocktimeperiod"]

        stockcsv(str(stocktickersym), str(timeperiod)) 

       
        
        data = pd.read_csv('teslaTable.csv')

        return render_template('previousdata.html', tables=[data.to_html()], titles=[''])
    
    except:

        
        stocktickersym = ""
        timeperiod = ""            
        return render_template('previousdata.html')

    
#--------------------------

#-----------Current Data-----------
@app.route('/currentdata', methods = ['POST', 'GET'])
def currentdata():

    
    
    global current_data_symbol


    try:
        
        form_data = request.form
        current_data_symbol = form_data["Stock"]
        
        currentdata_graph()

        results , Links1 = getNews(symbol_to_name(current_data_symbol))

        stocksym = symbol_to_name(current_data_symbol)
        
    except:
        
        stocksym = "Stock"
        results = ""
        Links1 = ""

    
    return render_template('currentdata.html', results = results, Links1 = Links1, stocksym = stocksym)

#--------------------------

#---------COMPARISON PAGE------------
@app.route('/comparison', methods = ['POST', 'GET'])
def comparison():

    global comparison_symbol1
    global comparison_symbol2

    
    try:
        
        form_data = request.form
        comparison_symbol1 = form_data["Stock1"]   
        

        results1 , Links2 = getNews(symbol_to_name(comparison_symbol1))

        stocksym1 = symbol_to_name(comparison_symbol1)

        comparison_symbol2 = form_data["Stock2"]
        

        results2 , Links3 = getNews(symbol_to_name(comparison_symbol2))

        stocksym2 = symbol_to_name(comparison_symbol2)

        
        comparison1_graph()
               
        comparison2_graph()

        comparison3_graph()
        
        

        
       
    
        

        

    except:
       
        stocksym1 = "Stock 1"
        stocksym2 = "Stock 2"
        results1 = ""
        results2 = ""
        Links2 = ""
        Links3 = ""
    
    return render_template('comparison.html', results1 = results1, results2 = results2, Links2 = Links2, Links3 = Links3, stocksym1 = stocksym1, stocksym2 = stocksym2)
  
#--------------------------

#---------Interactive Graph--------------


newsList = ["","","","",""]
newsLinksList = ["","","","",""]

@app.route('/button0', methods = ['POST', 'GET']) 
def button_zero():
    global newsList
    global newsLinksList
    newsList = newsDict[stocktimes[0]]
    newsLinksList = newsLinks[stocktimes[0]]

    return interactivegraph()
    
@app.route('/button1', methods = ['POST', 'GET']) 
def button_one():
    global newsList
    global newsLinksList
    newsList = newsDict[stocktimes[1]]    
    newsLinksList = newsLinks[stocktimes[1]]

    return interactivegraph()
    
@app.route('/button2', methods = ['POST', 'GET']) 
def button_two():
    global newsList
    global newsLinksList
    newsList = newsDict[stocktimes[2]]    
    newsLinksList = newsLinks[stocktimes[2]]

    return interactivegraph()
    
@app.route('/button3', methods = ['POST', 'GET']) 
def button_three():
    global newsList
    global newsLinksList
    newsList = newsDict[stocktimes[3]]    
    newsLinksList = newsLinks[stocktimes[3]]
    
    return interactivegraph()
    
@app.route('/button4', methods = ['POST', 'GET']) 
def button_four():
    global newsList
    global newsLinksList
    newsList = newsDict[stocktimes[4]]   
    newsLinksList = newsLinks[stocktimes[4]]
    
    return interactivegraph()
   
@app.route('/button5', methods = ['POST', 'GET']) 
def button_five():
    global newsList
    global newsLinksList
    newsList = newsDict[stocktimes[5]]
    newsLinksList = newsLinks[stocktimes[5]]

    return interactivegraph()
    
@app.route('/button6', methods = ['POST', 'GET']) 
def button_six():
    global newsList
    global newsLinksList
    newsList = newsDict[stocktimes[6]]
    newsLinksList = newsLinks[stocktimes[6]]
    
    return interactivegraph()


stocktimes = []
newsDict = {}
newsLinks = {}

@app.route('/interactivegraph', methods = ['POST', 'GET'])
def interactivegraph():

    global interactivegraph_symbol
    global stocktimes
    global newsDict
    global newsLinks
    global newsLinksList

    theerror = ""
    try:

        

        

        form_data = request.form

        formdata = form_data["Stock3"]
        
        error = ""
        
        if formdata != "":
            
            if interactivegraph_symbol != formdata:
                
                interactivegraph_symbol = formdata

        

            

     
        #interactivegraph_symbol = "TSLA"

        
        interactive_graph()

        prices, stocktimes = yFincalls(interactivegraph_symbol)

        

        results3 , Links4 = getNewsTime(symbol_to_name(interactivegraph_symbol), stocktimes[0] )

        for i in range(7):

            newsOutput = getNewsTime(symbol_to_name(interactivegraph_symbol), stocktimes[i])
            newsDict[stocktimes[i]] = newsOutput[0]
            newsLinks[stocktimes[i]] = newsOutput[1]


        
            

        stocksym4 = symbol_to_name(interactivegraph_symbol)

        
    except Exception as e:
        theerror = str(repr(e))
        error = "error"
        print(newsDict)
        stocksym4 = "Stock"
        results3 = ""
        Links4 = ""
        prices = ""
        #newsDict = {}
        #stocktimes = ""
        
        

    
    ##return render_template('interactivegraph.html', results3 = results3,
                           ##Links4 = Links4, stocksym4 = stocksym4, stocktimes = stocktimes, prices = prices,
                          ## newsDict = newsDict, stocktimeindex = stocktimeindex)

    return render_template('interactivegraph.html', stocktimes = stocktimes,
                           newsDict = newsDict, error = theerror,
                           interactivegraph_symbol = interactivegraph_symbol, newsList = newsList, newsLinksList = newsLinksList)


#--------------------------




    
if __name__ == "__main__":
    app.run(debug=True)


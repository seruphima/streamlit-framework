import requests
import pandas as pd
from flask import Flask, render_template, request
from bokeh.plotting import figure
from bokeh.embed import components
import yfinance as yf
from icecream import ic

app = Flask(__name__)
	
def dataSent(ticker, year, price):
	datestart = '%d-01-01' %year
	dateend = '%d-12-31' %year
	r = yf.download(ticker, start=datestart, end=dateend)
	ic(r)
	return r

def makePlot (df, ticker, year, price):
	plot = figure(x_axis_type="datetime", title="%d" %year)
	plot.grid.grid_line_alpha=1.0
	plot.xaxis.axis_label = 'Date'
	plot.yaxis.axis_label = 'Close'
	plot.line(df.index, df[price], color='#3EB489', legend='%s: %s' %(ticker,price))
	plot.legend.location = "top_left"
	script, div = components(plot)
	return script, div

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/graph', methods=['POST'])
def graph():
	ticker, price, year = request.form['tickerInput'].upper(), request.form['priceInput'], request.form['yearInput']
	
	if ticker == '' or year == '':
		df = None
	else:
		year = int(year)	
		df = dataSent(ticker, year, price)

	if type(df) == pd.DataFrame:
		script, div = makePlot(df, ticker, year, price)
		return render_template('graph.html', div = div, script = script)
		
	else:
		err = 'Ticker and/or Year are missing. Please fill out both forms.'
		return render_template('index.html', err=err)

if __name__ == '__main__':
	app.run(port=33508, debug=True)

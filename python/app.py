#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from model import Model
import pickle
from pathlib import Path
import datetime
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
from config import *
#db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/train')
def train():
    daterange = 30
    global model
    model = Model(features,results,daterange)
    model.train()
    '''
    fname = f'/var/tmp/greengob_model.{datetime.datetime.now().strftime("%Y%m%d-%h.%m")}.pkl'
    Path(fname).touch()
    pickle.dump(model, fname)
    try:
        os.link('/var/tmp/greengob_model.LATEST.pkl', fname)
    except FileNotFoundError as ex:
        logging.info('Didnt find LATEST model file to link from. Creating new one.')
        Path('/var/tmp/greengob_model.LATEST.pkl').touch()
        os.link('/var/tmp/greengob_model.LATEST.pkl', fname)
    '''
    return "Model trained and exported successfully!"


@app.route('/fetch')
def fetch():
    global model
    spot_values = {}
    for metric in list(features.keys()):
        try:
           val = request.args.get(metric)
           logging.info(f'{metric} value is {val}')
           spot_values[metric] = val
        except Exception:
            logging.error(f'{metric}- mandatory parameter not defined!')
            return f'{metric}- mandatory parameter not defined!'
    '''
    try:
        model = pickle.load('/var/tmp/greengob_model.LATEST.pkl')
    except FileNotFoundError:
        return 'No pickle LATEST file found - try training the model first'
    '''
    params = model.params
    vol_prediction =  model.fetch(spot_values,params)
    slippage_prediction = vol_prediction*0.7
    logging.info(f'vol prediction is {slippage_prediction} - using coeff of 0.7, slippage prediction is {slippage_prediction}')
    price_prediction = float(request.args.get('BTC')) + (float(request.args.get('BTC'))*0.7) #assume we are buying only, slippage unfavourable upwards
    return f'Predicted price @ {price_prediction}'



if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter
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
    model = Model(features,results,daterange)
    model.train()
    fname = f'/var/tmp/greengob_model.{datetime.datetime.now().strftime("%Y%m%d-%h:%m")}.pkl'
    pickle.dumps(model, fname)
    try:
        os.link('/var/tmp/greengob_model.LATEST.pkl', fname)
    except FileNotFoundError as ex:
        logging.info('Didnt find LATEST model file to link from. Creating new one.')
        Path('/var/tmp/greengob_model.LATEST.pkl').touch()
        os.link('/var/tmp/greengob_model.LATEST.pkl', fname)
    return "Model trained and exported successfully!"


@app.route('/fetch')
def fetch():
    spot_values = {}
    for metric in list(metrics.keys()):
        try:
           val = request.args.get(metric)
           logging.info(f'{metric} value is {val}')
           spot_values[metric] = val
        except Exception:
            logging.error(f'{metric}- mandatory parameter not defined!')
            return f'{metric}- mandatory parameter not defined!'
    try:
        model = pickle.load('/var/tmp/greengob_model.LATEST.pkl')
    except FileNotFoundError:
        return 'No pickle LATEST file found - try training the model first'
    prediction =  model.fetch(spot_values)
    return prediction



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
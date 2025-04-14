#! /usr/bin/env python
import datetime, time, json, os, sys, logging, threading, socket, traceback
from pprint import pprint
from flask import Flask, jsonify, request, Response

logging.getLogger('werkzeug').disabled = True
#os.environ['WERKZEUG_RUN_MAIN'] = 'true'

FLASK_APP_PORT = os.getenv('FLASK_APP_PORT', 9999) # get from "app.env" or 9999 by default

def get_now():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

def get_now_utc():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

def get_now_utc_iso():
    return datetime.datetime.utcnow().isoformat()

def get_epoch():
	return time.time()

def get_epoch_nanoseconds():
	return time.time_ns()

def get_pid():
	return os.getpid()

def get_hostname():
	return socket.gethostname()

def get_appname():
	return APP_NAME

def get_app_uptime():
    secs = get_epoch() - app_start_time
    result = datetime.timedelta(seconds=secs)
    return str(result)

def get_datetime_from_epoch(seconds):
    return datetime.datetime.fromtimestamp(seconds).strftime("%Y-%m-%d %H:%M:%S")

def log(message, level="INFO", **extra):
	out = {"timestamp": get_now(), "epoch": get_epoch(), "pid": get_pid(), "level": level, "message": message}
	if extra: out |= extra
	print(json.dumps(out), flush=True)
	return True

#
APP_NAME="flask:101"
__version__ = get_datetime_from_epoch(os.path.getmtime(os.path.basename(__file__)))
app = Flask(__name__)
app_start_time = get_epoch()


@app.after_request
def after_request(response):
	return response


@app.route('/info', methods=['GET'])
def info():
    data = { 
    'hostname': get_hostname(),
    'app-name': get_appname(),
    'app-start-time': app_start_time,
    'app-uptime': get_app_uptime(),
    'pid': get_pid(),
    'now': get_now(),
    'now_utc': get_now_utc(),
    'request-ts': get_epoch(),
    'request-ns': get_epoch_nanoseconds(),
    'version': __version__
    }
    log("/info", "DEBUG", data=data)
    return data, 200

if __name__ == "__main__":
    
    log(f"{APP_NAME} - Started")

    app.run(host='0.0.0.0', port=FLASK_APP_PORT, debug=True)
    

import typing
from typing import Optional
from typing import Tuple
from typing import Dict
from typing import Any
import tkinter as tk
from tkinter import ttk
import myNotebook as nb
import requests 
import logging
import os

from config import appname


plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f'{appname}.{plugin_name}')


if not logger.hasHandlers():
    level = logging.INFO 

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

frame: Optional[tk.Frame] = None
valueLabel: Optional[tk.Label] = None

value = ""

def plugin_start3(plugin_dir: str) -> str:
   """
   Load this plugin into EDMC
   """
   return "SysValue"

def plugin_app(parent: tk.Frame) -> tk.Frame:
	"""
	Create a frame for the EDMC main window
	"""
	global frame
	global valueLabel
	frame = tk.Frame(parent)
	row = frame.grid_size()[1]
	valueLabel = tk.Label(frame, text="System Value: " + value, justify=tk.RIGHT)
	valueLabel.grid(row=0, column=0, sticky=tk.W)
	return frame

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

APIpath = "https://www.edsm.net/api-system-v1/estimated-value"

def journal_entry(
	cmdr: str, is_beta: bool, system: str, station: str, entry: Dict[str, Any], state: Dict[str, Any]
) -> None:
	if entry['event'] == 'FSDJump':
		# We arrived at a new system!
		responseRaw = requests.get(url = APIpath + "?systemName=" + entry["StarSystem"]) 
		response = responseRaw.json()
		value = human_format(response["estimatedValue"]) + " - " + human_format(response["estimatedValueMapped"])
		valueLabel["text"] = "System Value: " + value

#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import datetime

def __rotate_records(directory, rotation):
	directory = os.path.abspath(os.path.expanduser(directory))
	files = os.listdir(directory)
	limit = datetime.date.today() - datetime.timedelta(rotation)
	p = re.compile("([0-9]{8})(_[0-9]{4}){2}\..{2,4}")
	
	for f in files:
		m = p.match(f)
		if os.path.isfile(os.path.join(directory,f)) and m:
			date = m.group(1)
			date = datetime.date(int(date[0:4]),int(date[4:6]),int(date[6:8]))

			if date < limit:
				os.remove(os.path.join(directory,f))
	
def __rotate_logs(size):
	log = os.path.expanduser("~/logs")
	home = os.path.abspath(os.path.expanduser("~"))
	
	if os.path.isfile(log) and os.path.getsize(log) >= size:
		files = os.listdir(home)
		p = re.compile("logs\.([0-9]*)?")
		n = None;
		
		for f in files:
			m = p.match(f)
			if os.path.isfile(os.path.join(home,f)) and m:
				if n == None or int(m.group(1)) > n:
					n = int(m.group(1))
		
		if n != None:
			for i in reversed(range(0,n+1)):
				if os.path.isfile(os.path.join(home,"logs."+str(i))):
					os.rename(os.path.join(home,"logs."+str(i)),os.path.join(home,"logs."+str(i+1)))
		os.rename(log,os.path.join(home,"logs.0"))
		

parser = argparse.ArgumentParser(description="Logs and records rotation.")
parser.add_argument('directory',type=str,help='Directory where the recorded files are stored.')
parser.add_argument('rotation',type=int,help='Rotation period (in days).')
parser.add_argument('size',type=int,help='Maximal size for log files (in bytes).')

args = parser.parse_args()

__rotate_records(args.directory,args.rotation)
__rotate_logs(args.size)

exit(0)

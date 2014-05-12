#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Guilhem Tiennot
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
from os.path import expanduser,join,isfile,abspath, getsize
from os import remove,rename,listdir
import re
import datetime
from const import LOG_FILE

def __list_files(directory):
	return listdir(abspath(expanduser(directory)))

def rotate_records(directory, rotation):
	files = __list_files(directory)
	limit = datetime.date.today() - datetime.timedelta(rotation)
	p = re.compile("([0-9]{8})(_[0-9]{4}){2}\..{2,4}")
	
	for f in files:
		m = p.match(f)
		if isfile(join(directory,f)) and m:
			date = m.group(1)
			date = datetime.date(int(date[0:4]),int(date[4:6]),int(date[6:8]))

			if date < limit:
				remove(join(directory,f))
	
def rotate_logs(directory, size):
	directory = abspath(expanduser(directory))
	log = expanduser(join(directory,LOG_FILE))
	
	if isfile(log) and getsize(log) >= size:
		files = __list_files(directory)
		p = re.compile(LOG_FILE+"\.([0-9]*)?")
		n = None;
		
		for f in files:
			m = p.match(f)
			if isfile(join(directory,f)) and m:
				if n == None or int(m.group(1)) > n:
					n = int(m.group(1))
		
		if n != None:
			for i in reversed(range(0,n+1)):
				if isfile(join(directory,LOG_FILE+"."+str(i))):
					rename(join(directory,LOG_FILE+"."+str(i)),join(directory,LOG_FILE+"."+str(i+1)))
		rename(log,join(directory,LOG_FILE+".0"))
		

parser = argparse.ArgumentParser(description="Logs and records rotation.")
parser.add_argument('directory',type=str,help='Directory where the recorded files are stored.')
parser.add_argument('rotation',type=int,help='Rotation period (in days).')
parser.add_argument('size',type=int,help='Maximal size for log files (in bytes).')
parser.add_argument('--log-dir',type=str,default="~",help="Directory where logs are stored. Default: $HOME.")

args = parser.parse_args()

rotate_records(args.directory,args.rotation)
rotate_logs(args.log_dir,args.size)

exit(0)

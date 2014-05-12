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

from os import rename,remove
from os.path import isdir,abspath,join,isfile
from subprocess import Popen,PIPE,STDOUT
import socket
import logging
import warnings
import time
from datetime import datetime
from const import HOST,PORT

class Recorder:
	
	def __start_client(self):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((HOST, PORT))
		except Exception as e:
			logging.warning("Connection to "+HOST+" on port "+str(PORT)+" failed. "+str(e.args))
			self.s = False
	
	def __find_rec_dir(self, rec_dir):
		if not rec_dir:
			return self.pige_dir
		elif not isdir(rec_dir):
			logging.warning("Using '"+self.pige_dir+"' instead of '"+rec_dir+"'")
			return self.pige_dir
		else:
			return abspath(rec_dir)
	
	def __build_file_name(self, duration):
		start_time = datetime.fromtimestamp(time.time())
		end_time = datetime.fromtimestamp(time.time() + duration);
		return start_time.strftime('%Y%m%d_%H%M')+'_'+end_time.strftime('%H%M')+".wav"
	
	def __change_file_name_if_exists(self, filename):
		if isfile(filename):
			logging.warning("file '"+filename+"' already exists. Saving into '"+filename+".new'.")
			return self.__change_file_name_if_exists(filename + ".new")
		else:
			return filename
		
	def __exec(self, args):
		process = Popen(args,stdout=PIPE,stderr=STDOUT)
		
		newline = process.stdout.readline()
		try_reco = 0
		while newline:
			line = newline
			
			# Lines with the '%' char are related to sound level
			if self.s and b'%' in line:
				try:
					self.s.send(line[-4:])
				except Exception as e:
					logging.warning(str(e.args))
					self.s = False
			elif not self.s:
				try_reco = try_reco + 1
				if try_reco >= 200:
					try_reco = 0
					self.__start_client()
			newline = process.stdout.readline()
		
		process.wait()
		
		if process.returncode != 0:
			logging.error(line = line.decode('utf-8','ignore'))
			raise Exception("Error",args[0]+" returns an error. Check logs.")
			
	def __init__(self, pige_dir):
		if isdir(pige_dir):
			self.pige_dir = abspath(pige_dir)
		else:
			logging.error("Directory '"+pige_dir+"' does not exist!")
			raise Exception("Error","Directory does not exist!")
		
		self.__start_client()

	def record(self, duration, rec_dir=""):
		logging.info('Starting new record')
		
		cue_file = join(self.__find_rec_dir(rec_dir),"cue.wav")
		final_file = join(self.pige_dir, self.__build_file_name(duration))
		
		cue_file = self.__change_file_name_if_exists(cue_file)
		
		self.__exec([
			"arecord",
			"-d",str(duration),
			"-f","cd",
			"-t","wav",
			"-vvv",
			cue_file])
		
		logging.info('Moving recorded file to '+final_file)
		final_file = self.__change_file_name_if_exists(final_file)
		rename(cue_file, final_file)
		
		logging.info('Record ended.')
		self.last_file = final_file
		
		if self.s:
			self.s.close()
		
	def compress(self, format, bitrate):
		if format == "mp3":
			new_file = self.__change_file_name_if_exists(self.last_file.replace(".wav",".mp3"))
			self.__exec([
				"lame",
				"-b", str(bitrate),
				self.last_file,
				new_file])
			remove(self.last_file)
			self.last_file = new_file
		elif format == "ogg":
			new_file = self.__change_file_name_if_exists(self.last_file.replace(".wav",".ogg"))
			self.__exec([
				"oggenc",
				"-b", str(bitrate),
				"-o", new_file,
				self.last_file])
			remove(self.last_file)
			self.last_file = new_file
		else:
			logging.error("File format '"+format+"' not found.")
			raise Exception("Error","File format '"+format+"' not found.")

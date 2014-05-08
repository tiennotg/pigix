#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import select
import multiprocessing
from const import HOST,PORT

# Try to import Gtk for Python 3
try:
	from gi.repository import Gtk
	from gi.repository import GObject
except:
# If it doesn't work, try to import for Python 2
	import gtk as Gtk
	import gobject as GObject

class StatusWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.set_title("Contrôle de la pige")
		self.set_size_request(600, 150)
		self.set_resizable(False)
		
		self.psbar = Gtk.ProgressBar()
		self.label = Gtk.Label()
		self.__label_set_status(False)
		self.level = multiprocessing.Value('d',0.0)
		self.running = multiprocessing.Value('b',False)
		
		self.vbox = Gtk.VBox(spacing=8)
		self.add(self.vbox)
		self.vbox.pack_start(self.psbar, True, True, 8)
		self.vbox.pack_start(self.label, False, False, 8)
		
		self.timer = GObject.timeout_add(20, self.__refresh)
		
		self.run_thread = multiprocessing.Value('b',True)
		multiprocessing.Process(target=self.__server_loop,args=(self.level,self.running,self.run_thread)).start()
		
	def stop_threads(self):
		self.run_thread.value = False
		
	def __refresh(self):
		self.__label_set_status(self.running.value)
		self.psbar.set_fraction(self.level.value)
		return True
	
	def __label_set_status(self,b):
		if b:
			self.label.set_markup("<big><span foreground='green' font-weight='bold'>Enregistrement...</span></big>")
		else:
			self.label.set_markup("<big><span foreground='red' font-weight='bold'>Pige stoppée</span></big>")
	
	def __server_loop(self, level_value, running_recorder, run_thread):
		def read_line(s):
			ret = ''
			while True:
				c = s.recv(1).decode('utf-8','ignore')
				if c == '\n' or c =='\r' or c == '':
					break
				else:
					ret += c
			return ret
		
		client_count = 0
		
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((HOST, PORT))
		self.s.listen(5)
		self.s.settimeout(1)
		
		while run_thread.value:
			try:
				conn, addr = self.s.accept()
				if conn:
					running_recorder.value = True
					while run_thread.value:
						data = read_line(conn)
						if not data:
							break
						level = float(data[:-1])/100
						level_value.value = level
					conn.close()
					level_value.value = 0
					running_recorder.value = False
			except:
				running_recorder.value = False

win = StatusWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
win.stop_threads()
exit(0)

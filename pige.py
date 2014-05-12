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

import recorder
import logging
import argparse
from os.path import expanduser,join
from const import LOG_FILE

parser = argparse.ArgumentParser(description="Radio recorder.")
parser.add_argument('duration',type=int,help='Duration of the recorded file.')
parser.add_argument('directory',type=str,help='Directory where the recorded files are stored.')
parser.add_argument('--rec-dir',type=str,help="Directory where the cue file is recorded.")
parser.add_argument('--log-dir',type=str,default="~",help="Directory where logs are stored. Default: $HOME.")
parser.add_argument('--compress',nargs=2,metavar=("FORMAT","BITRATE"),
					default=("ogg",128),help="Compress recorded files.")
parser.add_argument('--no-compress',action='store_true',help="Disable compression.")

args = parser.parse_args()

logging.basicConfig(filename=join(expanduser(args.log_dir),LOG_FILE),
					format='[%(asctime)s] %(levelname)s: %(message)s',
					level=logging.INFO)

record = recorder.Recorder(args.directory)
record.record(args.duration, args.rec_dir)
if not args.no_compress:
	record.compress(args.compress[0],args.compress[1])
exit(0)

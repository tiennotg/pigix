#!/usr/bin/python
# -*- coding: utf-8 -*-

import recorder
import logging
import argparse
from os.path import expanduser,join

parser = argparse.ArgumentParser(description="Radio recorder.")
parser.add_argument('duration',type=int,help='Duration of the recorded file.')
parser.add_argument('directory',type=str,help='Directory where the recorded files are stored.')
parser.add_argument('--rec-dir',type=str,help="Directory where the cue file is recorded.")
parser.add_argument('--log-dir',type=str,default="~",help="Directory where logs are stored. Default: $HOME.")
parser.add_argument('--compress',nargs=2,metavar=("FORMAT","BITRATE"),
					default=("mp3",128),help="Compress recorded files.")
parser.add_argument('--no-compress',action='store_true',help="Disable compression.")

args = parser.parse_args()

logging.basicConfig(filename=join(expanduser(args.log_dir),'logs'),
					format='[%(asctime)s] %(levelname)s: %(message)s',
					level=logging.INFO)

record = recorder.Recorder(args.directory)
record.record(args.duration, args.rec_dir)
if not args.no_compress:
	record.compress(args.compress[0],args.compress[1])
exit(0)

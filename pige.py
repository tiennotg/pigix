#!/usr/bin/python
# -*- coding: utf-8 -*-

import recorder
import logging
import argparse
from os.path import expanduser

logging.basicConfig(filename=expanduser('~/logs'), format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="Radio recorder.")
parser.add_argument('duration',type=int,help='Duration of the recorded file.')
parser.add_argument('directory',type=str,help='Directory where the recorded files are stored.')
parser.add_argument('--rec-dir',help="Directory where the cue file is recorded.")

args = parser.parse_args()
record = recorder.Recorder(args.directory)
record.record(args.duration, args.rec_dir)
record.compress("mp3",128)
exit(0)

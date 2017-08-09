#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# podupdater.py
#
# Copyright (C) 2017
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import glob
import requests
import feedparser

PLAYER = '<audio id="audio" preload="auto" controls="" src="{0}"></audio>'
REP_START = '<!--reproductor-start-->\n'
REP_END = '\n<!--reproductor-end-->\n'


def update_podcast(url):
    try:
        r = requests.get(url, verify=False)
        if r.status_code == 200:
            d = feedparser.parse(r.text)
            last_podcast = d.entries[0]
            return last_podcast.enclosures[0]['href']
    except Exception as e:
        print('Error', e)
    return None


if __name__ == '__main__':
    for afile in glob.glob('*.markdown'):
        with open(afile, 'r') as rf:
            data = rf.read()
        if data is not None and len(data) > 0:
            start_feed = data.find('<!--reproductor-feed=')
            if start_feed > -1:
                end_feed = data.find('-->', start_feed)
                feed = data[start_feed + 21:end_feed]
                last_podcast = update_podcast(feed)
                if last_podcast is not None:
                    start_player = data.find(REP_START)
                    end_player = data.find(REP_END)
                    if start_player > -1 and end_player > -1:
                        player = data[
                            start_player + len(REP_START): end_player]
                        data = data.replace(REP_START + player + REP_END,
                                            REP_START +
                                            PLAYER.format(last_podcast) +
                                            REP_END)
                        if data is not None and len(data) > 0:
                            print('Actualizando: {0}'.format(afile))
                            with open(afile, 'w') as wf:
                                wf.write(data)

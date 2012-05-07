#!/usr/bin/env python3.2
# -*- coding: utf-8 -*-
from pytvdbapi import api
import argparse,sys

tvdb_api_key = "083D567677C1B555"

#
## main
def main():
    # Define of variables
    global args

    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tvshow', help='Name of the tv show', required=True)
    parser.add_argument('-lang', '--language',  help='Only search for results in this language', required=True)
    parser.add_argument('-w', '--write', help='Write output to episode file', action='store_true')
    parser.add_argument('-d', '--directory',  help='Output directory for episode file', required=False, default='/var/cache/eplists/episodes')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()

	# use new pytvdbapi
    db = api.TVDB(tvdb_api_key)
    dbsearch = db.search(args.tvshow, args.language)
    show = dbsearch[0]

    # clean episode counter
    count = int(0)

    # open episode file for writing if wished
    if args.write:
        filename = args.directory + "/" + show.SeriesName + ".episodes"
        try:
        	episodefile=open(filename, mode="w", encoding="utf-8")
        except:
        	sys.stderr.write("Could not open output file. Does the directory " + args.directory + " exist and is writeable?\n")
        	sys.exit(1)

    print("Warning: The output will contain all episode titles not only the localized ones, because of a limit of the api!")
    print()

    # loop through the episodes to find matching
    for season in show:
        for episode in season:
            # increment episode counter
            count = count + 1

            # Output to file or to screen
            if args.write:
                print("%02d" % episode.SeasonNumber + "\t" +  "%02d" % episode.EpisodeNumber + "\t" + "%02d" % count + "\t" + episode.EpisodeName, file=episodefile)
            else:
                print("%02d" % episode.SeasonNumber + "\t" +  "%02d" % episode.EpisodeNumber + "\t" + "%02d" % count + "\t" + episode.EpisodeName)

	# close now unneeded file
    if args.write:
        episodefile.close()


if __name__ == "__main__":
    main()
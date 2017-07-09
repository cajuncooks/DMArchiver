# -*- coding: utf-8 -*-

"""
    Direct Messages Archiver - Command Line

    Usage:
    # dmarchiver [-h] [-id CONVERSATION_ID] [-u] [-p] [-di] [-dg] [-dv]

    optional arguments:
      -h, --help            show this help message and exit
      -id CONVERSATION_ID, --conversation_id CONVERSATION_ID
                            Conversation ID
      -u,  --username       Username (e-mail or handle)
      -p,  --password       Password
      -di, --download-images
                            Download images
      -dg, --download-gifs  Download GIFs (as MP4)
      -dv, --download-videos
                            Download videos (as MP4)
      -r, --raw-output  Write the raw HTML to a file
"""

import os
import argparse
import getpass
import sys
from dmarchiver import __version__
from dmarchiver.core import Crawler


def main():
    print("DMArchiver {0}".format(__version__))
    print("Running on Python {0}{1}".format(sys.version, os.linesep))
    parser = argparse.ArgumentParser()

    parser.add_argument("-id", "--conversation_id", help="Conversation ID")
    parser.add_argument("-u", "--username", help="Username (e-mail or handle)")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument(
        "-di",
        "--download-images",
        help="Download images",
        action="store_true")
    parser.add_argument(
        "-dg",
        "--download-gifs",
        help="Download GIFs (as MP4)",
        action="store_true")
    parser.add_argument(
        "-dv",
        "--download-videos",
        help="Download videos (as MP4)",
        action="store_true")
    parser.add_argument(
        "-r",
        "--raw-output",
        help="Write the raw HTML to a file",
        action="store_true")

    args = parser.parse_args()

    if args.username is None:
        username = input('Enter your username or email: ')
    else:
        username = args.username

    if args.password is None:
        password = getpass.getpass(
            'Enter your password (characters will not be displayed): ')
    else:
        password = args.password

    crawler = Crawler()
    try:
        crawler.authenticate(username, password)
    except PermissionError as err:
        print('Error: {0}'.format(err.args[0]))
        print('Exiting.')
        sys.exit()
    
    print('Press Ctrl+C at anytime to write the current conversation and skip to the next one.\n Keep it pressed to exit the script.\n')

    try:
        if args.conversation_id is not None:
            # Prevent error when using '' instead of ""
            conversation_id = args.conversation_id.strip('\'')
            print(
                'Conversation ID specified ({0}). Retrieving only one thread.'.format(
                    args.conversation_id))
            crawler.crawl(
                conversation_id,
                args.download_images,
                args.download_gifs, args.raw_output)
        else:
            print('Conversation ID not specified. Retrieving all the threads.')
            threads = crawler.get_threads()
            print('{0} thread(s) found.'.format(len(threads)))

            for thread_id in threads:
                crawler.crawl(thread_id, args.download_images,
                              args.download_gifs, args.download_videos, args.raw_output)
    except KeyboardInterrupt:
        print('Script execution interruption requested. Exiting.')
        sys.exit()

if __name__ == "__main__":
    main()

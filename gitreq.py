#!/usr/bin/env python3

'''gitreq.py: a script that allows you to define fields and '''
__author__ = "Jack Fox"
__email__ = "jfox13@nd.edu"

import sys
import subprocess
import os
import re

TEMPFILE = 'tempfile.tmp'
EDITOR = os.environ.get('EDITOR','vim')
PREREQFILE = 'gitreq.txt'

def prepare_commit_file(req_list: list) -> None:
    with open(TEMPFILE, 'w') as message_file:
        with open(PREREQFILE, 'r') as prereq_file:
            prereq_content = prereq_file.readlines()
            for line in prereq_content:
                message_file.write("####################\n{}:\n\n####################\n".format(line))
                req_list.append(line)

def handle_commit_no_arg(lines: list) -> None:
    ''' handles commit message '''
    req_list = list()
    prepare_commit_file(req_list)
    subprocess.call([EDITOR,TEMPFILE])

    with open(TEMPFILE, 'r') as message_file:
        message_content = message_file.read()

    if not check_prereq(req_list,message_content):
        subprocess.call(['rm',TEMPFILE])
        return

    comment_index = lines.index('commit') + 1
    lines.insert(comment_index,TEMPFILE)
    lines.insert(comment_index,'-F')
    subprocess.call(lines)
    subprocess.call(['rm',TEMPFILE])

def check_prereq(req_list: list, message_content: str) -> None:
    ''' checks all prereqs are in message '''
    for req in req_list:
        if not re.search("{}:(?!####################)*####################\n".format(req), message_content).group(1).strip():
            print("Error, did not include prereq: {}".format(req))
            return False
    return True

if __name__ == '__main__':
    args = sys.argv
    args[0] = 'git'

    if '-m' in args and 'commit' in args:
        # add into temp file
        args.remove('-m')

    if 'commit' in args:
        handle_commit_no_arg(args)
    else:
        subprocess.call(args)
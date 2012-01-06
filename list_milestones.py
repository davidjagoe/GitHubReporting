#!/usr/bin/env python

import os
import requests
import simplejson

# This URL lists the milestones by due data by default
MILESTONE_URL = "https://api.github.com/repos/fidelis-technology/Drillers-Dashboard/milestones"
PASSWORD_FILE = os.path.join(os.environ["HOME"], ".github_password")


def print_milestone(milestone):
    print milestone["title"]
    print "-------"
    print "    " + milestone["description"]
    print
    print


def _read_basic_auth():
    with open(PASSWORD_FILE) as f:
        return tuple(f.read().strip().split(","))


def main():
    resp = requests.get(MILESTONE_URL, auth=_read_basic_auth())
    if resp.status_code == 200:
        milestones = simplejson.loads(resp.content)
        for milestone in milestones:
            print_milestone(milestone)
    else:
        print "Unexpected reponse"
        print "Status: %s" % resp.status_code


if __name__ == "__main__":
    main()

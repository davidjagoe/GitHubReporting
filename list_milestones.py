#!/usr/bin/env python

import codecs
import os
import requests
import simplejson

CONFIG_FILE = os.path.join(os.environ["HOME"], ".github_reporting/config.json")
OUT = None

def newline():
    OUT.write("\n")

def _h(heading, underline_char):
    OUT.write(heading + "\n")
    OUT.write(underline_char * len(heading) + "\n")
    newline()
    newline()
    
def h1(heading):
    _h(heading, "=")

def h2(heading):
    _h(heading, "-")

def paragraph(text):
    OUT.write(text + "\n")
    newline()
    newline()

def rule():
    OUT.write("-" * 80)
    OUT.write("\n")

def print_milestone(milestone):
    title = milestone["title"]
    description = milestone["description"]
    h2(title)
    paragraph(description)
    rule()

def _read_config():
    with open(CONFIG_FILE) as f:
        return simplejson.load(f)

def get_basic_auth_credentials(config):
    return (config["username"], config["password"])

def get_milestone_url(config):
    return config["repository"] + "/milestones"

def main():
    global OUT
    try:
        OUT = codecs.open("roadmap.md", encoding="utf-8", mode="w+")
        config = _read_config()
        resp = requests.get(get_milestone_url(config), auth=get_basic_auth_credentials(config))
        if resp.status_code == 200:
            h1("Technology Roadmap")
            milestones = simplejson.loads(resp.content)
            for milestone in milestones:
                print_milestone(milestone)
        else:
            print "Unexpected reponse"
            print "Status: %s" % resp.status_code
    finally:
        OUT.close()
        OUT = None


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import codecs
import os
import requests
import simplejson

CONFIG_FILE = os.path.join(os.environ["HOME"], ".github_reporting/config.json")

# "dynamic" variables
_OUT_    = None
_CONFIG_ = None

### CONFIGURATION

def _read_config():
    with open(CONFIG_FILE) as f:
        return simplejson.load(f)

def get_basic_auth_credentials(config):
    return (config["username"], config["password"])

def get_milestone_url(config):
    return config["repository"] + "/milestones"

def get_issues_url(config):
    return config["repository"] + "/issues"

### MARKDOWN

def newline():
    _OUT_.write("\n")

def _h(heading, underline_char):
    _OUT_.write(heading + "\n")
    _OUT_.write(underline_char * len(heading) + "\n")
    newline()
    newline()
    
def h1(heading):
    _h(heading, "=")

def h2(heading):
    _h(heading, "-")

def h3(heading):
    _OUT_.write("### " + heading + " ###")
    newline()

def paragraph(text):
    _OUT_.write(text)
    newline()
    newline()
    newline()

def rule():
    _OUT_.write("-" * 80)
    newline()

def list_item(text):
    _OUT_.write("* {0}".format(text))
    newline()

### WRITER

def write_issue(issue):
    list_item(issue["title"])
    newline()

def write_issues(milestone):
    milestone_number = milestone["number"]
    issues_url = "{0}?milestone={1}".format(get_issues_url(_CONFIG_), milestone_number)
    resp = requests.get(issues_url, auth=get_basic_auth_credentials(_CONFIG_))
    if resp.status_code == 200:
        issues = simplejson.loads(resp.content)
        for issue in issues:
            write_issue(issue)
    else:
        raise Exception("Error reading issues. Response: {0}".format(resp.status_code))

def write_milestone(milestone):
    title = milestone["title"]
    description = milestone["description"]
    h2(title)
    paragraph(description)
    write_issues(milestone)
    rule()

### MAIN

def main():
    global _OUT_
    global _CONFIG_
    try:
        _OUT_ = codecs.open("roadmap.md", encoding="utf-8", mode="w+")
        _CONFIG_ = _read_config()
        resp = requests.get(get_milestone_url(_CONFIG_), auth=get_basic_auth_credentials(_CONFIG_))
        if resp.status_code == 200:
            h1("Technology Roadmap")
            milestones = simplejson.loads(resp.content)
            for milestone in milestones:
                write_milestone(milestone)
            print "Done."
        else:
            print "Unexpected reponse"
            print "Status: %s" % resp.status_code
    finally:
        _OUT_.close()
        _OUT_    = None
        _CONFIG_ = None


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import requests
import simplejson
import sys

import config   as c
import markdown as fmt
import vars     as v

### WRITER

def write_issue(issue):
    title      = issue["title"]
    labels_str = ",".join([l["name"] for l in issue["labels"]])
    body       = issue["body"]

    fmt.h2(title + " -- " + labels_str)
    fmt.paragraph(body)
    fmt.rule()

### MAIN

def main(milestone):
    try:
        c.setup("issues.md")
        resp = requests.get(c.get_issues_url(v._CONFIG_), 
                            auth=c.get_basic_auth_credentials(v._CONFIG_),
                            params={'milestone': milestone})
        if resp.status_code == 200:
            fmt.h1("Issues")
            issues = simplejson.loads(resp.content)
            for issue in issues:
                write_issue(issue)
            print "Done."
        else:
            print "Unexpected reponse"
            print "Status: %s" % resp.status_code
    finally:
        c.teardown()


if __name__ == "__main__":
    # Usage: list_issues.py milestone1 ; milestone is a number
    milestone = sys.argv[1]
    main(milestone)

#!/usr/bin/env python

import requests
import simplejson

import config   as c
import markdown as fmt
import vars     as v

### WRITER

def write_issue(issue):
    fmt.list_item(issue["title"])
    fmt.newline()

def write_issues(milestone):
    milestone_number = milestone["number"]
    issues_url = "{0}?milestone={1}".format(c.get_issues_url(v._CONFIG_), milestone_number)
    resp = requests.get(issues_url, auth=c.get_basic_auth_credentials(v._CONFIG_))
    if resp.status_code == 200:
        issues = simplejson.loads(resp.content)
        for issue in issues:
            write_issue(issue)
    else:
        raise Exception("Error reading issues. Response: {0}".format(resp.status_code))

def write_milestone(milestone):
    title = milestone["title"]
    description = milestone["description"]
    fmt.h2(title)
    fmt.paragraph(description)
    write_issues(milestone)
    fmt.rule()

### MAIN

def main():
    try:
        c.setup("issues.md")
        resp = requests.get(c.get_issues_url(v._CONFIG_), auth=c.get_basic_auth_credentials(v._CONFIG_))
        if resp.status_code == 200:
            fmt.h1("Issues")
            issues = simplejson.loads(resp.content)
            for issue in milestones:
                write_issue(issue)
            print "Done."
        else:
            print "Unexpected reponse"
            print "Status: %s" % resp.status_code
    finally:
        c.teardown()


if __name__ == "__main__":
    main()

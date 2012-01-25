#!/usr/bin/env python

import pickle
import requests
import simplejson
import sys

import config   as c
import markdown as fmt
import vars     as v

### WRITER

def write_issue(issue):
    fmt.list_item(issue['title'])
    fmt.newline()

def write_issues(issues):
    for issue in issues:
        write_issue(issue)

def write_milestone(milestone):
    due = milestone['due']
    due = due.split('T')[0] if due else 'LATER'
    title = milestone['title'] + ' ' + '<span style="float: right; font-size: 75%">(Due: ' + due + ')</span>'
    description = milestone['description']

    fmt.h2(title)
    fmt.paragraph(description)
    write_issues(milestone['issues'])
    fmt.rule()

def write_milestones(milestones):
    for k, issues in milestones:
        _, title, description, due = k
        write_milestone({'title': title, 
                         'description': description, 
                         'due': due, 
                         'issues': issues})
        

def get_milestone_tuple(issue):
    ms = issue['milestone']
    if ms is None:
        return (None, 'MISCELLANEOUS', '', None)
    else:
        return (ms['number'], ms['title'], ms['description'], ms['due_on'])

def into_milestones(issues):
    milestones = {}
    for issue in issues:
        milestones.setdefault(get_milestone_tuple(issue), []).append(issue)
    return milestones

def add_milestones_with_no_issues(milestones):
    output = milestones.copy()
    resp = requests.get(c.get_milestone_url(v._CONFIG_), auth=c.get_basic_auth_credentials(v._CONFIG_))
    if resp.status_code == 200:
        empty_milestones = [m for m in simplejson.loads(resp.content) if m['open_issues'] == 0]
        for ms in empty_milestones:
            output[(ms['number'], ms['title'], ms['description'], ms['due_on'])] = []
    else:
        print 'Unexpected reponse'
    return output

def cmp_due_dates(a, b):
    ka, va = a
    kb, vb = b
    _, _, _, a_due = ka
    _, _, _, b_due = kb
    if a_due == b_due:
        return 0
    if a_due is None:
        return 1
    if b_due is None:
        return -1
    if a_due < b_due:
        return -1
    if b_due < a_due:
        return 1
    else:
        raise RuntimeError()


def fetch_issues():
    
    def error():
        print 'Unexpected reponse'
        print 'Status: %s' % resp.status_code
        sys.exit(1)

    resp = requests.get(c.get_issues_url(v._CONFIG_), auth=c.get_basic_auth_credentials(v._CONFIG_))
    if resp.status_code == 200:
        issues = simplejson.loads(resp.content)
        resp = requests.get(c.get_issues_url(v._CONFIG_), 
                            auth=c.get_basic_auth_credentials(v._CONFIG_),
                            params={'state': 'closed'})
        if resp.status_code == 200:
            issues = issues + simplejson.loads(resp.content)
        else:
            error()
    else:
        error()
    return issues
        
### MAIN

def main(use_cache):
    try:
        c.setup('roadmap.md')
        if use_cache:
            with open('milestones.pickle') as f:
                milestones = pickle.load(f)
        else:
            issues = fetch_issues()
            milestones = add_milestones_with_no_issues(into_milestones(issues))
            milestones = sorted(milestones.iteritems(), cmp_due_dates)
            with open('milestones.pickle', 'w') as f:
                pickle.dump(milestones, f)
        fmt.h1('Technology Roadmap')
        write_milestones(milestones)
        print 'Done.'
    finally:
        c.teardown()

def main2():
    try:
        c.setup('roadmap.md')
        resp = requests.get(c.get_milestone_url(v._CONFIG_), auth=c.get_basic_auth_credentials(v._CONFIG_))
        if resp.status_code == 200:
            fmt.h1('Technology Roadmap')
            milestones = simplejson.loads(resp.content)
            for milestone in milestones:
                write_milestone(milestone)
            print 'Done.'
        else:
            print 'Unexpected reponse'
            print 'Status: %s' % resp.status_code
    finally:
        c.teardown()


if __name__ == '__main__':
    use_cache = len(sys.argv) > 1 and sys.argv[1] == 'cached'
    main(use_cache)

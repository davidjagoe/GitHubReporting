
import codecs
import os
import simplejson

import vars as v

CONFIG_FILE = os.path.join(os.environ["HOME"], ".github_reporting/config.json")

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

### SETUP AND TEAR DOWN

def setup(output_filename):
    v._OUT_ = codecs.open(output_filename, encoding="utf-8", mode="w+")
    v._CONFIG_ = _read_config()

def teardown():
    try:
        v._OUT_.close()
    except Exception:
        pass
    v._OUT_ = None
    v._CONFIG_ = None

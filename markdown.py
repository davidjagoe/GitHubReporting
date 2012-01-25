
import vars as v

### MARKDOWN

def newline():
    v._OUT_.write("\n")

def _h(heading, underline_char):
    v._OUT_.write(heading + "\n")
    v._OUT_.write(underline_char * len(heading) + "\n")
    newline()
    newline()
    
def h1(heading):
    _h(heading, "=")

def h2(heading):
    _h(heading, "-")

def h3(heading):
    v._OUT_.write("### " + heading + " ###")
    newline()

def paragraph(text):
    v._OUT_.write(text)
    newline()
    newline()
    newline()

def rule():
    v._OUT_.write("-" * 80)
    newline()
    newline()
    newline()

def list_item(text):
    v._OUT_.write("* {0}".format(text))
    newline()


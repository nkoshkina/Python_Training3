from model.contact import Contact
import random
import string
import os.path
import getopt
import sys
import jsonpickle

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of groups", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 3
f = "data/contacts.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_sign_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def random_email(prefix, maxlen1, maxlen2):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen1))]) \
            +"@" + "".join([random.choice(symbols) for i in range(random.randrange(maxlen1))]) \
            +"." + "".join([random.choice(symbols) for i in range(2)])

def random_number(prefix, maxlen):
        symbols = string.digits
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [ Contact(firstname="")] + \
        [
       Contact(firstname=random_string("", 8), middlename=random_string("", 10), lastname=random_string("", 15),
            nickname=random_string("", 8),
            title=random_string("", 10), company=random_string("", 15), address=random_string("", 20),
            home=random_number("+7",10), mobile=random_number("+",11), work=random_number("+7",10),
            fax=random_number("+7",10),
            email=random_email("", 7,5), email2=random_email("", 7,5), email3=random_email("", 7,5),
            homepage=random_string("", 15),
            saddress=random_string("", 20), phone2=random_number("+",11), snotes=random_string("", 30))
    for i in range(n)]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as fout:
    fout.write(jsonpickle.encode(testdata, indent=2))
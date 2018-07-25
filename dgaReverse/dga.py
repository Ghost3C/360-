import argparse
from datetime import datetime
import hashlib
import os
 
def char_remove(A, B):
  C = []
  for x in A:
    d = 1
    for y in list(B):
      if x[0:1] == y:
        d = 0
        break
    if d > 0:
      C.append(x)
  return C
 
def dga(year, month):
    x_year = 2016
    x_month = 7
    x_add = 0
 
    delta_months = 11 * (year - 2016) + (month - 7)
    if delta_months < 0 or delta_months > 12:
        delta_months = 12
   
    domains = []
    for i in xrange(delta_months, -1, -1):
        domains += _dga(i + 12 * x_add)
    return domains
 
def _dga(delta_months):
 
    # init
    tlds = ["ru", "ua", "pw", "rocks", "biz", "org", "com", "link", "xyz", "space", "in"]
 
    A = "abcdefghijklmnopqrstuvwxyz"
 
    B = char_remove(list(A), "aeiouqxc")
    B+= ["bl", "br", "cl", "cr", "dr", "fl", "fr", "gl", "gr", "pl", "pr", "sk", "sl", "sm", "sn", "sp", "st", "str", "sw", "tr", "ch"]#, "sh"
 
    C = char_remove(list(A), "aeiouqxcsj")
    C+= ["ct", "ft", "mp", "nd", "ng", "nk", "nt", "pt", "sk", "sp", "ss", "st", "ch"]#, "sh"

    E = "aeiou"
 
    D = []
    #for i in xrange(0, len(B) * len(E) * len(C)):
    #  D.append((i % len(B), (i / len(B)) % len(E), (i / len(B) / len(E)) % len(C)))
    for i in xrange(0, len(C)):
        for j in xrange(0, len(E)):
            for k in xrange(0, len(B)):
                D.append((k, j, i))
 
    # generate
    tld_index = 33 * delta_months
    for _ in xrange(0, 33):
        t = []
        j = tld_index
        for i in xrange(0, 3):
            t.append(D[j % len(D)])
            j /= len(D)
        parts = []
        for (a,b,c) in t:
            parts.append(B[a % len(B)] + E[b % len(E)] + C[c % len(C)])
        domain = parts[2] + parts[0] + parts[1] + '.' + tlds[tld_index % len(tlds)]
        tld_index += 1
        yield _, domain
 
 
def resolve(domain):
 
  cmd = os.popen("proxychains nc %s 2>&1" % domain, "r").read()
  if cmd.find("198.105.244.11") != -1 or cmd.find("198.105.254.11") != -1 or cmd.find("104.239.213.7") != -1 or cmd.find("does not exist") != -1 or cmd.find("192.42.116.41") != -1:
    return 0
  return 1
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m")
    else:
        d = datetime.now()
 
#    for x in xrange(0, 1000):
#        for _, domain in _dga(x):
#              print "%d / %d / %s" % (x, _, domain)
    for _, domain in dga(d.year, d.month):
        #if resolve(domain) != 0:
        print "%04d-%02d / %d / %s" % (d.year, d.month, _, domain)

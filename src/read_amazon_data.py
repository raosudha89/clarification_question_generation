import gzip
import pdb
import sys

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)

path = sys.argv[1]
total = 0
has_desc = 0
for v in parse(path):
	total += 1
	if v.has_key('description'):
		has_desc += 1

print total
print has_desc

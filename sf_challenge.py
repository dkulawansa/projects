import argparse
import re
import six
import sys
import urllib.request
import urllib.parse as urlparse
import xml.parsers.expat
from collections import defaultdict
from urllib.parse import urlencode

def main():
	"""This main function retrieves sequence data, parse it and write to an external file"""
	parser = argparse.ArgumentParser()
	parser.add_argument("database", type=str, help="the database name (string)")
	parser.add_argument("id", type=int, help="the database identifier (numeric)")
	parser.add_argument("output_filename", type=str, help="the output filename (string)")
	parser.add_argument("regex_pattern", type=str, help="the regular expression pattern (string)")

	args = parser.parse_args()
	para={}
	para["db"] = args.database
	para["id"] = args.id
	para["rettype"] = 'fasta'
	para["retmode"] = 'xml'

	req = urllib.request.Request('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{}'.format(urlencode(para)))
	with open(args.output_filename, 'w') as fh:
		try:
			with urllib.request.urlopen(req) as response:
				events = []
				p = xml.parsers.expat.ParserCreate()
				p.StartElementHandler = lambda name, attrs: events.append(name)
				p.CharacterDataHandler = lambda data:char_data(data, events, args.regex_pattern, fh) 
				p.Parse(response.read(), 1)	
		except urllib.error.HTTPError as ex:
			sys.stderr.write("Error occured while retriving sequence data. Error details: {}".format(six.text_type(ex)))
	
def char_data(data, events, pattern, fh):
	""" This function write data to file stream and stdout stream"""
	if'TSeq_sequence' in events and len(data) > 1:
		hits = defaultdict(int)
		try:
			for m in re.finditer(pattern, data):
				fh.write( "{},{},{}\n".format(m.group(), m.start()+1, m.end()))
				hits[m.group()] += 1
		except Exception as ex:
			sys.stderr.write("Error occured while writing data into a file. Error details: {}".format(six.text_type(ex)))
			
		hits_sorted = sorted(hits.items(), key=lambda x: (x[0], x[1]))
		for k, v in hits_sorted:
			sys.stdout.write("{}\t{}\n".format(k, v))
if __name__ == '__main__':
	main()	
	
	
	
	



		

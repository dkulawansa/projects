sf_challenge.py is a python command-line utility to retrieve sequence data 
and perform a simple string-based analysis of the data 
=====================================================
This utility has been implemented using python version 3.6 in windows environment.

a)	What design choices you made, and why:

Tried various libraries to parse the input xml data. This include lxml, xml.etree.ElementTree, 
xml.etree.cElementTree and xml.expat.  All but xml.expat was able to work with large xml file. 
Due to the memory concerns, choices were made to process the input data while retrieving and 
writing only the process data into a file.

b)	How to run your application 
The following provids some details about input parameters
>python sf_challenge.py --help

usage: sf_challenge.py [-h] database id output_filename regex_pattern

positional arguments:
  database         the database name (string)
  id               the database identifier (numeric)
  output_filename  the output filename (string)
  regex_pattern    the regular expression pattern (string)

optional arguments:
  -h, --help       show this help message and exit
 


To run the application please provide valid positional arguments. The application accepts four input 
parameters: a database name, a database identifier, a regular expression (regex) string, and an output file name.  
The identifier and database name correspond to a sequence record in the GenBank databases for DNA and protein sequences
Please pass string values using double quotes if the operating system can not identify the command.

Sample command:
===============
>python sf_challenge.py nucleotide 30271926 output.txt "(A|C|G|T)"


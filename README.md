appscan_scripts
===============

scripts that help with IBM Rational Appscan

this is a bunch of scripts I use with appscan:

1) extract_url.py == sometimes I run a report and I want to extract URLs and parameters to a text file

2) import_url.py == sometimes I want to digest a war file and import the urls this script finds into appscan

3) import_params.py == sometimes I want to search a war file or a source tree for hidden parameters or action URLs and import those into appscan.

4) import_veracode.py Import from veracode.  Sometimes I want to parse a veracode report and import the results into appscan.

5) custom_strings.txt  These are attempts at custom attacks (OGNL, coldfusion, hacking techniques from whitehat lists)

6) what_happened.py  This is a script to read the appscan logs and compare to crashes (both of appscan and the application being attacked) to see if a particular request was to blame.  If there is already a way to do this, then this file will turn into text document of instructions for doing it.

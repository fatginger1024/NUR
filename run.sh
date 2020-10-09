#!/bin/bash

echo "Run handin template"


# Script that returns a plot
echo "Run the first script ..."
python3 problem2a.py 
python3 problem2b.py 

# Script that pipes output to a file
echo "Run the second script ..."
python3 problem3a.py 
python3 problem3b.py 
python3 problem3c.py 


echo "Generating the pdf"

pdflatex template.tex



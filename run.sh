#!/bin/bash

echo "Download image for in report..."
if [ ! -e wgs.dat ]; then
  wget https://home.strw.leidenuniv.nl/~daalen/Handin_files/wgs.dat
fi
  
if [ ! -e wss.dat ]; then
  wget https://home.strw.leidenuniv.nl/~daalen/Handin_files/wss.dat
fi

if [ ! -e coolingtables_highres.tar.gz ]; then
  wget https://www.strw.leidenuniv.nl/WSS08/coolingtables_highres.tar.gz
  tar -zxvf coolingtables_highres.tar.gz
fi

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



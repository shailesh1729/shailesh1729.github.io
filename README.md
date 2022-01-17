# Commands


pelican --autoreload --listen



Build for publishing:

pelican content -s publishconf.py
cp CNAME output

The CNAME file must be copied inside gh-page branch. 
Otherwise, Github Pages will stop recognizing the website.




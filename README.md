# Commands


Development

```shell
pelican --autoreload --listen
```

Or try with

```shell
make html
make serve
```


Build for publishing:

```shell
pelican content -s publishconf.py
cp CNAME output
```

The CNAME file must be copied inside gh-page branch. 
Otherwise, Github Pages will stop recognizing the website.

Alternatively, use the `build.bat` script.


Publishing
```shell
publish.bat
```

## Dependencies

```shell
pip install pelican
pip install ghp-import
```

Configure the elegant theme

```shell
# clone the theme code
git clone https://github.com/Pelican-Elegant/elegant.git
# install the theme
pelican-themes -i <path-to-theme>
```
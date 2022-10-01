# Commands


Development

```shell
hugo server
```

The site can be seen locally at http://localhost:1313.

Build for publishing:

```shell
hugo --minify
```

Alternatively, use the `build.bat` script.


Publishing
```shell
publish.bat
```

## Dependencies

I use `hugo` static site builder. Please install it.

For publishing to `gh-pages` branch, I use `ghp-import`.

```shell
pip install ghp-import
```
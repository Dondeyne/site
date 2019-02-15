# Dondeyne Site

## Installing

```sh
git clone https://github.com/Dondeyne/site
cd site
pip3 install -r requirements.txt
pybabel compile -d translations
```


## Running

Generally it depends on what server (Apache, NGinx ...) you are using but
it can be run stand-alone with `./app.py`.


## Translating

If you have added sentences to the source code or templates, run

```sh
pybabel extract -F babel.cfg -o messages.pot --omit-header .
pybabel update -i messages.pot
```

Translations can be added in `translations/<locale>/LC_MESSAGES/messages.po`.
After adding them, run

```sh
pybabel compile -f -d translations
```

If you want to add a new locale, run

```
pybabel init -d translations -l <locale>
```

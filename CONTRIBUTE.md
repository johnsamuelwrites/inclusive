# inclusive

## Contribute
There are three ways to contribute:
* Add a missing language in [resources](./resources) folder and add it to [configuration.json](./configuration.json).
* Update existing lists of already existing languages. For example, in [English](./resources/en/lists.json).
* Translate `inclusive`. Check existing or add new [locales](./locales).

## Configuration file

## Language suggestion

## Translate the application

### Add a new language
If a language is missing from `inclusive`, it can be added in the following way.
For example, to add a new language like French, the following steps were followed:

```
pybabel init -i locales/inclusive.bot -d locales/ -D inclusive -l fr
```
and

```
pybabel init -i locales/inclusive.bot -d locales/ -D inclusive -l fr_FR
```

Note that both `fr` and `fr_FR` are the locales supported by `pybabel`.

The above commands created the following files:
1. `locales/fr_FR/LC_MESSAGES/inclusive.po
2. `locales/fr/LC_MESSAGES/inclusive.po

An example translation from the above files is given below:
```
msgid "Enter [bold magenta]a text[/bold magenta]:"
msgstr "Saisir [bold magenta]un texte[/bold magenta]:"
```

Once the translation in the above files is completed (or partially completed), run the following command to generate `*.mo` files

```
pybabel compile -d locales -D inclusive
```

### Update missing and existing translations
For checking the existing locales in `inclusive`, run
```
ls locales
```

Check the current translation in the `.po` files, for example, `locales/fr_FR/LC_MESSAGES/inclusive.po`.
An example translation from the above files is given below:
```
msgid "Enter [bold magenta]a text[/bold magenta]:"
msgstr "Saisir [bold magenta]un texte[/bold magenta]:"
```
The translation for the phrase represented by `msgid` is the phrase associated with `msgstr`. A new value can be added or an existing value can be modified.

Once the translation in the `*.po` files is completed (or partially completed), run the following command to generate `*.mo` files

```
pybabel compile -d locales -D inclusive
```

# inclusive

## Contribute
There are three ways to contribute:
* Update existing lists of already existing languages. For example, in [English](./resources/en/list.json).
* Add a missing language in [resources](./resources) folder and add it to [configuration.json](./configuration.json).
* Translate `inclusive`. Check existing or add new [locales](./locales).

## Configuration file
To add suggestions resources for any language (or locale), add it to [configuration.json](./configuration.json)

```
{
        "en": [
                "./resources/en/list.json",
                "./resources/en/pronouns.json"
        ],
        "en_US": [
                "./resources/en/list.json",
                "./resources/en/pronouns.json"
        ]
}

```

Here, `en` and `en_US` are two locales and the associated list of resources are the files:
1. `./resources/en/list.json`
2. `./resources/en/pronouns.json`

In this case, the two locales share the same resources. But this may not be the case for all locales.

## Language suggestion

## Translate the application

### Add a new language
If a language is missing from `inclusive`, it can be added in the following way.

First check, all the locales supported by `pybabel`:

```
pybabel --list-locales
```

For example, to add a new language like French, the following steps were followed:

Find and choose the locales related to French:

```
pybabel --list-locales|grep -i French
```
which gave the following output:
```
b'fr              French'
b'fr_BE           French (Belgium)'
...
b'fr_FR           French (France)'
...
```

Two locales like `fr` and `fr_FR` are chosen to illustrate the process.

```
pybabel init -i locales/inclusive.bot -d locales/ -D inclusive -l fr
```
and

```
pybabel init -i locales/inclusive.bot -d locales/ -D inclusive -l fr_FR
```

The above commands created the following files:
1. `locales/fr_FR/LC_MESSAGES/inclusive.po`
2. `locales/fr/LC_MESSAGES/inclusive.po`

An example translation from the above files is given below:
```
msgid "Enter [bold magenta]a text[/bold magenta]:"
msgstr "Saisir [bold magenta]un texte[/bold magenta]:"
```

Once the translation in the above files is completed (or partially completed), run the following command to generate `*.mo` files: 

```
pybabel compile -d locales -D inclusive
```

Now the application will be able to show messages in this language.

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

Now the application will be able to show the updated messages in this language.

# inclusivewriting

## Contribute
There are three ways to contribute:
* Update existing lists of already existing languages. For example, in [English](./inclusivewriting/resources/en/list.json).
* Add a missing language in [resources](./resources) folder and add it to [configuration.json](./inclusivewriting/configuration.json).
* Translate `inclusivewriting`. Check existing or add new [locales](./inclusivewriting/locales).

## Development architecture
The current development model is based on:
* Rule definitions loaded from JSON resource files (rule-packs)
* Rule-pack loading and validation in `inclusivewriting/rulepacks.py`
* Context-aware detection in `inclusivewriting/rules.py`

Contributors changing suggestion resources should run:
```
python -m unittest tests.resource_schema_test
python -m tests.tests
```

## Configuration file
To add suggestions resources for any language (or locale), add it to [configuration.json](./inclusivewriting/configuration.json)

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
A new suggestion for a phrase has the following form. For every phrase (or lexeme), following informations are required:
1. Links to sources (like Wikidata, Wikitionary or any other dictionary)
2. One or more replacement suggestions. Each replacement has the following information
  a. Links to sources (like Wikidata, Wikitionary or any other dictionary)
  b. One or more eferences to sources (news article, community discussions etc.) which suggest this replacement.

The validator accepts `lexeme` values as either a string or a list of strings, but a list is recommended for consistency.
`replacement.references` may also be a string or a list of strings.

In the following example, *they* is suggested as a replacement for the lexeme *he*. 
The links for both lexemes are given along with a reference for the suggested replacement.
```
{
        "he": {
                "lexeme": ["https://www.wikidata.org/wiki/Lexeme:L485"],
                "replacement": {
                        "they": {
                                "lexeme": "https://www.wikidata.org/wiki/Lexeme:L371",
                                "references": [
                                        "https://www.cnet.com/news/twitter-engineers-replace-racially-loaded-tech-terms-like-master-slave/"
                                ]
                        }
                }
        },
	...

```

### Style guidance for suggestions
* Keep each phrase as a top-level key (avoid nested phrase entries inside another phrase).
* Prefer lower-case phrase keys for stable matching.
* Add at least one reference for each replacement.

## Translate the application

### Add a new language
If a language is missing from `inclusivewriting`, it can be added in the following way.

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
pybabel init -i locales/inclusivewriting.bot -d locales/ -D inclusivewriting -l fr
```
and

```
pybabel init -i locales/inclusivewriting.bot -d locales/ -D inclusivewriting -l fr_FR
```

The above commands created the following files:
1. `locales/fr_FR/LC_MESSAGES/inclusivewriting.po`
2. `locales/fr/LC_MESSAGES/inclusivewriting.po`

An example translation from the above files is given below:
```
msgid "Enter [bold magenta]a text[/bold magenta]:"
msgstr "Saisir [bold magenta]un texte[/bold magenta]:"
```

Once the translation in the above files is completed (or partially completed), run the following command to generate `*.mo` files: 

```
pybabel compile -d locales -D inclusivewriting
```

Now the application will be able to show messages in this language.

### Update missing and existing translations
For checking the existing locales in `inclusivewriting`, run
```
ls locales
```

Check the current translation in the `.po` files, for example, `locales/fr_FR/LC_MESSAGES/inclusivewriting.po`.
An example translation from the above files is given below:
```
msgid "Enter [bold magenta]a text[/bold magenta]:"
msgstr "Saisir [bold magenta]un texte[/bold magenta]:"
```
The translation for the phrase represented by `msgid` is the phrase associated with `msgstr`. A new value can be added or an existing value can be modified.

Once the translation in the `*.po` files is completed (or partially completed), run the following command to generate `*.mo` files

```
pybabel compile -d locales -D inclusivewriting
```

Now the application will be able to show the updated messages in this language.

Finally, if the code requires new textual strings, these could be extracted for further translation with the folliwing command: 

```
pybabel extract . -o locales/inclusivewriting.bot
```


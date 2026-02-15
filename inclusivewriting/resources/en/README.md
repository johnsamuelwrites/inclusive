# English Resource Pack

This folder contains English rule resources used by `inclusivewriting`:
* `list.json`: general inclusive terminology replacements
* `pronouns.json`: pronoun-focused suggestions

## Rule format
Each top-level key is a phrase. Each phrase has:
* `lexeme`: list of source links for the phrase (Wikidata/Wiktionary/etc.)
* `replacement`: one or more replacement entries

Each replacement contains:
* `lexeme`: list of source links for the replacement
* `references`: supporting references for usage guidance

## Examples
### Resource entry example
```json
{
  "chairman": {
    "lexeme": ["https://www.wikidata.org/wiki/Lexeme:L249635"],
    "replacement": {
      "chairperson": {
        "lexeme": ["https://www.wikidata.org/wiki/Lexeme:L90937"],
        "references": ["https://inclusivenaming.org/word-lists/"]
      },
      "chair": {
        "lexeme": ["https://www.wikidata.org/wiki/Lexeme:L17326"],
        "references": ["https://inclusivenaming.org/word-lists/"]
      }
    }
  }
}
```

### Text detection example
Input text:
`The chairman asked for more manpower from mankind.`

Detected phrases include:
* `chairman`
* `manpower`
* `mankind`

Additional examples included in this resource pack:
* `freshman` -> `first-year student`
* `middleman` -> `intermediary`, `go-between`
* `man-made` -> `artificial`, `synthetic`
* `grandfathered` -> `legacy`, `exempted`
* `sanity check` -> `quick check`, `confidence check`
* `he/she`, `s/he` -> `they`

## Guidelines
* [Linux kernel coding style](https://github.com/torvalds/linux/blob/master/Documentation/process/coding-style.rst)
* [Inclusive Chromium code](https://chromium.googlesource.com/chromium/src/+/master/styleguide/inclusive_code.md)
* [The Inclusive Naming Word Lists](https://inclusivenaming.org/word-lists/) suggested in issue [#1](https://github.com/johnsamuelwrites/inclusive/issues/1)

## Validation
Run validation after updating the English resource files:
* `python -m unittest tests.resource_schema_test`
* `python -m tests.tests`

## References
* [Inclusive language](https://en.wikipedia.org/wiki/Inclusive_language)
* [Twitter engineers replacing racially loaded tech terms like 'master,' 'slave'](https://www.cnet.com/news/twitter-engineers-replace-racially-loaded-tech-terms-like-master-slave/)
* [Tech confronts its use of the labels 'master' and 'slave'](https://www.wired.com/story/tech-confronts-use-labels-master-slave/)
* [Linux kernel coders propose inclusive terminology coding guidelines](https://www.theregister.com/2020/07/06/linux_kernel_coders_propose_inclusive/)

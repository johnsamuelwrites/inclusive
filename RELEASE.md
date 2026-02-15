# v0.9 (unreleased)
===============================================================================
* Add context-aware rule engine (`inclusivewriting/rules.py`)
* Add multilingual rule-pack loader/validator (`inclusivewriting/rulepacks.py`)
* Migrate detection flow to rule engine while preserving suggestion API compatibility
* Add structured CLI JSON output with match metadata and spans
* Add CLI options: `--format`, `--quiet`, `--no-color`
* Add explicit CLI exit codes (`0`, `1`, `2`)
* Add resource schema validation tests and CI validation step
* Modernize CI workflows and add Python dependency caching
* Add `pyproject.toml` packaging metadata

# v0.8
===============================================================================
* Update setup.py to correct the handling of locales

# v0.7
===============================================================================
* Update package to include default configuration file and language resources

# v0.3
===============================================================================
* Use of Flit for Python packaging
* Update package name from `inclusive` to `inclusivewriting`
* Add option to read user-defined configuration file

# v0.1
===============================================================================
* A configurable multilingual version for inclusive writing, permitting the users to add 
  * support for new languages
  * add new suggestions to existing languages
  * update suggestions
* Test cases and code coverage
* Suport for `en`, `en_US`, `fr` and `fr_FR` locales


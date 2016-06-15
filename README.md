# poisonpen
Find out if people are copy/pasting their diatribes

## Installation
- This project has no external dependencies

## Usage
- Include the names of files that you wish to compare (best results on ASCII/Unicode text files)
- You may optionally include the number of words to compare at a time (larger values will provide marginally faster output, but a less precise calculation)

`python poisonpen.py original_filename comparison_filename [number_of_word_tuples]`

## Output
- The filename 

as in:

`original_filename|comparison_filename: 50% similar`

## Other Solutions
- The [ssdeep](http://ssdeep.sourceforge.net/usage.html) and [sdhash](http://roussev.net/sdhash/tutorial/03-quick.html) fuzzy hash algorithms address a similar (identical?) use case to this project.

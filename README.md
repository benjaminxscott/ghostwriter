[![Build Status](https://travis-ci.org/bschmoker/ghostwriter.svg?branch=master)](https://travis-ci.org/bschmoker/ghostwriter)

# ghostwriter
Find out if people are copy/pasting their auto-biographies

## Installation
- This project has no external dependencies and can be executed directly

## Usage
`ghostwriter.py [-h] [--num_tuples NUM_TUPLES] synonym_file original_file comparison_file`

- Include the names of files that you wish to compare (best results on ASCII/Unicode text files)
- Also include a list of synonyms which will be treated as identical (expected to be a newline-seperated file with synonyms seperated by spaces on the same line)
- You may optionally include the number of word tuples to compare - defaulting to 3 words at a time (larger values will provide marginally faster output, but a less precise calculation)


## Output
- For each comparison, the script emits the percentage of word tuples which appear both in `original_file` `comparison_file`
- Synonyms are treated as identical, and punctuation/whitespace are ignored

## Example

`python ghostwriter.py synonym_file original_file comparison_file -n 3`

```
  original_file and comparison_file are 50% similar
```

`cat synonym_file`
> run jog

`cat original_file`
> went for a jog

`cat comparison_file`
> go for a run 


## Other Solutions
- The [ssdeep](http://ssdeep.sourceforge.net/usage.html) and [sdhash](http://roussev.net/sdhash/tutorial/03-quick.html) fuzzy hash algorithms address a similar use case, although they are intended to operate on binary input as opposed to prose text

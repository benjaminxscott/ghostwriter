[![Build Status](https://travis-ci.org/bschmoker/ghostwriter.svg?branch=master)](https://travis-ci.org/bschmoker/ghostwriter)

# ghostwriter
Find out if people are copy/pasting their auto-biographies

## Installation
- This project has no external dependencies and can be executed directly

## Usage
```
ghostwriter.py [-h] [--num_tuples NUM_TUPLES] [--verbose]
                      synonyms original_file comparison_file

positional arguments:
  synonyms              list of space-seperated synonyms, (each list on a
                        newline) to be treated identically in comparisons
  original_file         file to compare
  comparison_file       file to compare

optional arguments:
  -h, --help            show this help message and exit
  --num_tuples NUM_TUPLES, -n NUM_TUPLES
                        (advanced) number of words to compare at a time (a
                        positive integer) (default: 3)
  --verbose, -v         Emit more details (default: False)
```

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

## Related GIF
[![ghostwriter.gif](https://67.media.tumblr.com/347d3a152112d06d95120c4c2360f498/tumblr_n2ch03z8va1ro8ysbo1_r1_500.gif)](https://67.media.tumblr.com/347d3a152112d06d95120c4c2360f498/tumblr_n2ch03z8va1ro8ysbo1_r1_500.gif)

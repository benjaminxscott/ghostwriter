# poisonpen
Find out if people are copy/pasting their scathing criticisms

## Installation
- This project has no external dependencies

## Usage
- Include the names of files that you wish to compare (best results on ASCII/Unicode text files)
- You may optionally include a list of synonyms which will be treated as identical (expected to be a newline-seperated file with synonyms seperated by spaces on the same line)
- You may optionally include the number of word tuples to compare - defaulting to 3 words at a time (larger values will provide marginally faster output, but a less precise calculation)

`python poisonpen.py original_file comparison_file [-s synonym_file] [-n number_of_word_tuples]`

## Output
- For each comparison, the script emits the percentage of word tuples which appear both in `original_file` `comparison_file`
- So for the above example, the output would be one line saying "100%".  

## Example

`python poisonpen.py original_file comparison_file -s synonym_file -n 3`

```
  Replacing synonyms as defined in synonym_file
  Comparing number_of_word_tuples at a time
  original_file|comparison_file: 50% similar
```

`cat synonym_file`
> run jog

`cat original_file`
> went for a jog

`cat comparison_file`
> go for a run 


## Other Solutions
- The [ssdeep](http://ssdeep.sourceforge.net/usage.html) and [sdhash](http://roussev.net/sdhash/tutorial/03-quick.html) fuzzy hash algorithms address a similar (identical?) use case 

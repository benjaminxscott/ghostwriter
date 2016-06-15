#!/usr/bin/env python
# NOTE: for my own clarity, I've internally used the term 'wordset' to denote a 'tuple of words'
# DESIGN - Worst-case runtime of this program is expected to be somewhat less than O(N^2), as in N*M * (total_words_in_longest_file / N) 
            # for N as tuple size, M as number of synonyms for each word
            # since it's iterating over all tuples in each file (words/N) ^2 and looking for N^M number of synonym replacements on each iteration
# DESIGN - This program is expected to be memory-bounded

import argparse
import string
import hashlib

def get_tuples(infile, tuple_size, synonyms):
    # DESIGN - This approach scales poorly with large files, since it reads the whole file into memory
    words = infile.read().split(None) #split on whitespace
    occurs = {}
    wordset_count = 0
    num_words = len(words)
    
    # iterate through each tuple of words (ignoring trailing words that do not fit as part of a tuple)
    # DESIGN using range() to generate an iterator, and explicit indexes to make the array slice more readable
    
    end = (num_words +1) - tuple_size
    
    for start_index in range(0, end): 
        end_index = start_index + tuple_size
        
        word_set = words[start_index:end_index]
        
        wordset_count = wordset_count + 1
        # replace any synonyms with the first one in the list
        # DESIGN - we replace while operating on a list rather than a string, to avoid false positive replacements
        for index, word in enumerate(word_set):
            # iteratove over each list of synonyms
            for syn in synonyms: 
                if word in syn:
                    # replace our synonym with the first one in its related synonym list (since it's guaranteed to exist)
                    word_set[index] = syn[0] 
                    
        # DESIGN - we could have a more efficient data structure / lookup for these, perhaps a dictionary?
    
        # As a tradeoff, it requires more memory footprint for small input files 
        word_set = "".join(word_set)
        # strip punctuation 
        # DESIGN - using translate() instead of replace(';,.etc') for speed and readability
        word_set = word_set.translate(None, string.punctuation)
        
        # generate a hash digest of the input data, using sha1 since less likely to accidentially collide than md5 (while still being unique enough for our purposes)
        # DESIGN - This approach scales well for longer word lengths, and scales linearly and predictably with large/duplicative files. 
        digest = hashlib.sha1(word_set).hexdigest()
    
        # increment a count of the number of times each tuple has been observed in each file
        occurs[digest] = occurs.get(digest, 0) + 1
    
    # endfor
    return (occurs, wordset_count)
        
        
def positive_integer(value):
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("Tuple count must be a positive integer" )
    return ivalue

def main():
    
    # parse args (from readme)
    
    parser = argparse.ArgumentParser ( formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    description = "Calculate the percentage of word tuples which appear in two input files"\
    + "\nInclude the names of files that you wish to compare (best results on ASCII/Unicode text files)"\
    + "\nYou may optionally include a list of synonyms which will be treated as identical (expected to be a newline-seperated file with synonyms seperated by spaces on the same line)"\
    + "\nYou may optionally include the number of word tuples to compare - defaulting to 3 words at a time"
    # DESIGN - If I understand correctly, a larger tuple size will increase the true positive rate, but also increase the false negative rate (since it's looking for identical passages, but there may be smaller snippets that it misses)
    
    parser.add_argument("synonyms", type=argparse.FileType('r'), help="list of space-seperated synonyms, (each list on a newline) to be treated identically in comparisons", default='synonyms.txt')
    parser.add_argument('original_file', type=argparse.FileType('r'), help='file to compare')
    parser.add_argument('comparison_file', type=argparse.FileType('r'), help='file to compare')
    parser.add_argument("--num_tuples", '-n', type=positive_integer, help="(advanced) number of words to compare at a time (a positive integer)", default=3)
    parser.add_argument("--verbose",'-v', help="Emit more details",action='store_true')
    
    args = parser.parse_args()
    
    synonyms = []
    # parse synonym file into list of lists
    for line in args.synonyms:
        synonyms.append(line.split())
        
    unique_wordsets = 0   
    
    # open each input file and store tuples
    # DESIGN This could be extended to operate on an arbitrary list of input files
    (orig_dict, wordcount) = get_tuples(args.original_file, args.num_tuples, synonyms)
    unique_wordsets = unique_wordsets + wordcount   
    
    (comp_dict, wordcount) = get_tuples(args.comparison_file, args.num_tuples, synonyms)
    unique_wordsets = unique_wordsets + wordcount   
    
    # calculate similarity between tuples in the two files
    # DESIGN - We store the comparison dictionaries for each file rather than cleverly performing comparisons inline, which allows more readable code, with the tradeoff of requiring more memory
    shared_count = 0.0
    for key in orig_dict.keys():
        if comp_dict.get(key):
            # increment the count of "shared" tuples
            # DESIGN - handle the case where a tuple from the original document shows up multiple times in the comparison document 
            shared_count += comp_dict.get(key) + orig_dict.get(key)# count the number we've found in the comparison document, plus the one in our source document

    similarity = (shared_count / (unique_wordsets ) ) * 100
    
    # emit output
    if args.verbose:
        print "Replacing synonyms as defined in %(syn)s" %{'syn':args.synonyms.name}
        print "Comparing %(tuples)d words at a time" % {'tuples':args.num_tuples}
        print "Inspected %(wordsets)d total word tuples" %{'wordsets':unique_wordsets}
        print "%(orig)s and %(comp)s are %(percent)f percent similar" % {'orig':args.original_file.name,'comp':args.comparison_file.name, 'percent':similarity}
    else:
        print "%(percent)d" % {'percent':similarity} + '%'
    
if __name__ == '__main__':
    main()

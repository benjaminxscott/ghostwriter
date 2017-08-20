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
    occurs = {}
    wordset_count = 0
    with open(infile, 'r') as infilehandle:
        words = infilehandle.read().split(None) #split on whitespace
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
        
def compare_tuples (orig_dict, comp_dict, total_unique_wordsets):
    # calculate similarity between two sets of tuples from individual files
    shared_count = 0.0
    for key in orig_dict.keys():
        if comp_dict.get(key):
            # increment the count of "shared" tuples
            # DESIGN - handle the case where a tuple from the original document shows up multiple times in the comparison document 
            shared_count += comp_dict.get(key) + orig_dict.get(key)# count the number we've found in the comparison document, plus the one in our source document
            
    similarity_percent = (shared_count / (total_unique_wordsets ) ) * 100
    
    return similarity_percent 
    
        
def positive_integer(value):
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("Tuple count must be a positive integer" )
    return ivalue

def main():
    
    # parse args (from readme)
    
    parser = argparse.ArgumentParser ( formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    description = "Compare an original file with some number of other files to find textual equivalencies "\
    + "\n(best results on ASCII/Unicode text files)"\
    + "\nYou may optionally include a list of synonyms which will be treated as identical (expected to be a newline-seperated file with synonyms seperated by spaces on the same line)"\
    + "\nYou may optionally include the number of words per tuple to compare - default is 3 words per tuple"
    
    # DESIGN - a larger tuple size should increase the true positive rate, but also increase the false negative rate (since it's looking for identical passages, but there may be smaller snippets that it misses)
    
    parser.add_argument("--synonyms", type=argparse.FileType('r'), nargs='?', help="file with list of space-seperated synonyms to be treated identically in comparisons")
    parser.add_argument('original_file', help='comparison_filepath to original textfile ')
    parser.add_argument('comparison_files', nargs='+', help='comparison_filepath(s) to comparison textfiles')
    parser.add_argument("--num_tuples", '-n', type=positive_integer, help="(advanced) number of words to compare at a time (a positive integer)", default=3)
    parser.add_argument("--verbose",'-v', help="Emit more details",action='store_true')
    
    args = parser.parse_args()
    
    if args.verbose:
        print "DBG: Comparing %(tuples)d words at a time" % {'tuples':args.num_tuples}
    
    # Parse synonym list if provided
    synonyms = []
    if args.synonyms:
        if args.verbose:
            print "DBG: Replacing synonyms as defined in %(syn)s" %{'syn':args.synonyms.name}
        
        # parse synonym file into list of lists
        for line in args.synonyms:
            synonyms.append(line.split())
        
    # Get tuples from original file
    if args.verbose:
        print "DBG: Attempting to read tuples from: " + args.original_file
    (orig_dict, orig_wordcount) = get_tuples(args.original_file, args.num_tuples, synonyms)
    total_unique_wordsets = orig_wordcount   
    
    # Iterate over input files and generate comparison of original to others
    for comparison_filepath in args.comparison_files:
        if args.verbose:
            print "DBG: Attempting to read tuples from: " + comparison_filepath
        
        (comp_dict, wordcount) = get_tuples(comparison_filepath, args.num_tuples, synonyms)
        total_unique_wordsets = total_unique_wordsets + wordcount   
        
        # calculate similarity of two files
        similarity = compare_tuples(orig_dict,comp_dict, orig_wordcount + wordcount)
        
        if args.verbose:
            print "%(orig)s and %(comp)s are %(percent).2f percent similar" % {'orig':args.original_file,'comp':comparison_filepath, 'percent':similarity}
        else:
            print "%(percent).2f" % {'percent':similarity} + '%'
        
    # endmain
    if args.verbose:
        print "DBG: Inspected %(wordsets)d total word tuples" %{'wordsets':total_unique_wordsets}
    
if __name__ == '__main__':
    main()

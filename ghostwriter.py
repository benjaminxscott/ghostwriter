#!/usr/bin/env python
# NOTE: for my own clarity, I've internally used the term 'wordset' to denote a 'tuple of words'
# DESIGN - Runtime of this program is expected to be O(total_words / N)^2
# DESIGN - This program is expected to be memory-bounded

import argparse
import string
import hashlib

def get_tuples(infile, tuple_size):
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
        print word_set
        
        wordset_count = wordset_count + 1
        # TODO replace any synonyms with the first one in the list
    
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
    
        return (occurs, wordset_count)
        
def main():
    
    # parse args (from readme)
    
    parser = argparse.ArgumentParser ( formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    description = "Calculate the percentage of word tuples which appear in two input files"\
    + "\nInclude the names of files that you wish to compare (best results on ASCII/Unicode text files)"\
    + "\nYou may optionally include a list of synonyms which will be treated as identical (expected to be a newline-seperated file with synonyms seperated by spaces on the same line)"\
    + "\nYou may optionally include the number of word tuples to compare - defaulting to 3 words at a time (larger values will provide marginally faster output, but a less precise calculation)"
    
    parser.add_argument("synonyms", type=argparse.FileType('r'), help="list of space-seperated synonyms, (each list on a newline) to be treated identically in comparisons", default='synonyms.txt')
    parser.add_argument('original_file', type=argparse.FileType('r'), help='file to compare')
    parser.add_argument('comparison_file', type=argparse.FileType('r'), help='file to compare')
    parser.add_argument("--num_tuples", '-n', type=int, help="(advanced) number of words to compare at a time", default=3)
    parser.add_argument("--verbose",'-v', help="Emit more details",action='store_true')
    
    args = parser.parse_args()
    
    # TODO parse synonym file
    #for each in args.synonyms.readline().split():
    
    
    total_wordsets = 0   
    
    (orig_dict, wordcount) = get_tuples(args.original_file, args.num_tuples)
    total_wordsets = total_wordsets + wordcount   
    (comp_dict, wordcount) = get_tuples(args.comparison_file, args.num_tuples)
    total_wordsets = total_wordsets + wordcount   
    
        
    # calculate similarity
    # DESIGN - We store the comparison dictionaries for each file rather than cleverly performing comparisons inline, which allows more readable code, with the tradeoff of requiring more memory
    shared_count = 0   
    for key in orig_dict.keys():
        if comp_dict.get(key):
            shared_count += min(orig_dict[key], comp_dict[key])

    similarity = shared_count / (total_wordsets - shared_count) * 100
    
    # emit output
    if args.verbose:
        print "Replacing synonyms as defined in %(syn)s" %{'syn':args.synonyms.name}
        print "Comparing %(tuples)d words at a time" % {'tuples':args.num_tuples}
        print "Inspected %(wordsets)d total word tuples" %{'wordsets':total_wordsets}
        print "%(orig)s and %(comp)s are %(percent)f percent similar" % {'orig':args.original_file.name,'comp':args.comparison_file.name, 'percent':similarity}
    else:
        print "%(percent)d" % {'percent':similarity} + '%'
    
if __name__ == '__main__':
    main()
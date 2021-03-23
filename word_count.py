# Author: Max Grier
# Date: 6/6/2020
# Description: Uses the hash_map file to sort the word count of a file and return
# a list of words and their respective counts


# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")


def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500,hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                # Turn all letters lower case to avoid case sensitivity
                lower_w = w.lower()
                # Add the word to the set of keys (keys are words here)
                keys.add(lower_w)

                # Checks if the word is in the hash map
                if ht.contains_key(lower_w):
                    # If so, increase the count by 1 and add it
                    # to the hash table with it's count
                    word_count = ht.get(lower_w) + 1
                    ht.put(lower_w, word_count)
                # Otherwise, put in hash table with a count of 1
                # (since it is the first occurrence)
                else:
                    ht.put(lower_w, 1)

    # Make the list to convert the tuple
    word_count_list = []

    # Iterate through the words
    for word in keys:
        # Set the index based on the hash function being used
        index = ht._hash_function(word) % ht.capacity
        # Set the position within the bucket
        position = ht._buckets[index]
        # Set the node for the word
        node = position.contains(word)
        # Add the word and count to the list as a tuple
        word_count_list.append((node.key, node.value))

    # After adding the sets of word and count value pairs,
    # sorts the tuples in decending order base on word count.
    # Code help with this portion Source: geeksforgeeks.org
    # It reverses the order based on the count value
    word_count_list.sort(key=lambda tup: tup[1], reverse=True)

    # Return the number of words based on the user
    # input starting from the first one
    return word_count_list[0:number]


#print(top_words("alice.txt", 10))  # COMMENT THIS OUT WHEN SUBMITTING TO GRADESCOPE











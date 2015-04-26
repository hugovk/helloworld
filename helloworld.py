#!/usr/bin/env python
# encoding: utf-8
"""
Generate a poem.

Start from "Hello, world!" and repeatedly replacing a word using a synonym,
antonym, rhyme, etc., to make the next line.

Example output:

Hello, world!
Howzit, world!
Howzit, terrestrial planet!
Howzit, major planet!
Howzit, planet!
What's the craic, planet!
Hi, planet!
Hi, satellite!
Hi, solar!
Hi, solar energy!
Salutation, solar energy!
Salutation, extrasolar!

A longer one:

Excitement, bubbling!
Excitement, effervescent!
Excitement, lively!
Excitement, look lively!
Motive, look lively!
Impulsion, look lively!
Tension, look lively!
Agitation, look lively!
Bustle, look lively!
Russell, look lively!
Muscle, look lively!
Mussel, look lively!
Tussle, look lively!
Contend, look lively!
Fight, look lively!
Fighting, look lively!
Operational, look lively!
Coeducational, look lively!
Computational, look lively!
Conformational, look lively!
Conversational, look lively!
Informal, look lively!
Unofficial, look lively!
Unconventional, look lively!
Inofficial, look lively!
Irregular, look lively!
Connotational, look lively!
Confrontational, look lively!
Denominational, look lively!
Sectarian, look lively!
Aberrational, look lively!
Congregational, look lively!
Disarrange, look lively!
Combat, look lively!
Struggle, look lively!
Scrap, look lively!
Scrapped, look lively!
Scrapping, look lively!
Lapp, look lively!
Chap, look lively!
Blow, look lively!
Rap, look lively!
Rap music, look lively!
Rapped, look lively!
Rapping, look lively!
Conversation, look lively!
Strike, look lively!
Dike, look lively!
Mike, look lively!
Ike, look lively!

A shorter one:

Git, commit!
Unpleasant person, commit!
Unpleasant person, pursue!
Unpleasant person, prosecute!
Disagreeable person, prosecute!
Disagreeable person, engage!

Hack for NaPoGenMo2015, National Poetry Generation Month:
https://github.com/NaPoGenMo/NaPoGenMo2015
"""
from __future__ import print_function, unicode_literals
import argparse
import random
import sys
import yaml  # pip install PyYAML

from wordnik import swagger, WordApi  # pip install wordnik

RELATIONSHIPS = ["synonym",
                 "antonym",
                 "variant",
                 "equivalent",
                 # "cross-reference",
                 "related-word",
                 "rhyme",
                 "form",
                 "etymologically-related-term",
                 "hypernym",
                 "hyponym",
                 # "inflected-form",
                 # "primary",
                 # "same-context",
                 # "verb-form",
                 # "verb-stem",
                ]

GAPS = [" ", ", "]
ENDINGS = ["", "!"]


def print_it(text):
    """ Windows cmd.exe cannot do Unicode so encode first """
    print(text.encode('utf-8'))


def timestamp():
    """ Print a timestamp """
    import datetime
    print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))


def load_yaml(filename):
    """
    File should contain:
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
            'wordnik_api_key'}:
        sys.exit("Wordnik credentials missing from YAML: " + filename)
    return data


def make_line(word_list):
    """ Make a string from the word list """
    # line = random.choice(GAPS).join(word_list)
    # line += random.choice(ENDINGS)
    line = ", ".join(word_list) + "!"
    print(line)
    return line.capitalize()


def helloworld(seed):
    """ Generate the next line for the poem """
    while True:
        word_to_change = random.randrange(len(seed))  # an index
        print("Word to change:", seed[word_to_change])
        relationships_to_try = list(RELATIONSHIPS)  # Don't repeat if no result
        random.shuffle(relationships_to_try)

        if not relationships_to_try:
            if unused_words[word_to_change]:
                words = [unused_words[word_to_change].pop()]
                break
            return None
        print("Relationship to try:", relationships_to_try)
        # relationship = random.choice(relationships_to_try)
        relationship = relationships_to_try.pop()
        print("Try relationship:", relationship)

        print("Get words from Wordnik...")
        words = word_api.getRelatedWords(seed[word_to_change],
                                         relationshipTypes=relationship)
        if words:
            print("Found words")
            words = words[0].words
            random.shuffle(words)
            seed[word_to_change] = words.pop()
            line = make_line(seed)
            unused_words[word_to_change].extend(words)
            return line
        else:
            print("No words found, try cache")
            if unused_words[word_to_change]:
                seed[word_to_change] = unused_words[word_to_change].pop()
                line = make_line(seed)
                return line
            else:
                print("Try again")
    return None


if __name__ == "__main__":
    timestamp()

    parser = argparse.ArgumentParser(
        description="Generate a poem, starting from 'hello world'.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/helloworld.yaml',
        # default='E:/Users/hugovk/Dropbox/bin/data/helloworld.yaml',
        help="YAML file containing Wordnik keys and secrets")
    parser.add_argument(
        '-1', '--first', default="hello",
        help="First word in first line.")
    parser.add_argument(
        '-2', '--second', default="world",
        help="Second word in first line.")
    parser.add_argument(
        '-n', '--number', type=int, default=50,
        help="Number of lines to generate.")
    args = parser.parse_args()

    # Initialise
    data = load_yaml(args.yaml)
    wordnik_client = swagger.ApiClient(data['wordnik_api_key'],
                                       'http://api.wordnik.com/v4')
    word_api = WordApi.WordApi(wordnik_client)

    seed = [args.first, args.second]
    unused_words = [[], []]  # might be handy later

    output = [make_line(seed)]

    while True:
        print()
        print(len(output))
        print()
        if len(output) >= args.number:
            break
        line = helloworld(seed)
        if line and line not in output:
            # avoid duplicates
            output.append(line)

    print()
    print("Finished!")
    print()
    for line in output:
        print(line)

# End of file

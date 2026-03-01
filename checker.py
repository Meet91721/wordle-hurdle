import math
import random
import argparse

from server import correctness
with open("allowed_words.txt") as f:
    all_words = f.read().splitlines()

def generate_all_patterns(index):
    if index == 1:
        return [[1],[2],[3]]
    previous_response = generate_all_patterns(index - 1)
    final_response = []
    for i in [1, 2, 3]:
        for prev in previous_response:
            j = prev.copy()
            j.append(i)
            final_response.append(j.copy())
    return final_response 

all_patterns = generate_all_patterns(5)

def get_index(pattern):
    index = 0
    for i in pattern:
        index *= 3
        index += i - 1
    return index

def get_list_for_a_word(word):
    res = [0 for i in range(len(all_patterns))]
    for compare_word in all_words:
        index = get_index(correctness(word, compare_word))
        res[index] += 1
    return res

def get_words_for_pattern(source, pattern, invalid_chars):
    res = []
    for word in all_words:
        if correctness(word, source) == pattern:
            if invalid_chars:
                if all([c not in word for c in invalid_chars]):
                    res.append(word)
            else:
                res.append(word)
    return res

parser = argparse.ArgumentParser()
parser.add_argument("--w", type=str)
parser.add_argument("--p", type=str)
parser.add_argument("--i", type=str)
args = parser.parse_args()

def calculate_i_gain(counts):
    total = sum(counts)
    gain = 0
    for count in counts:
        if count > 0:
            p = count / total
            gain -= p * math.log2(p)
    return gain


def get_all_patterns_count(word, allowed_words):
    final_count = [0 for _ in range(len(all_patterns))]
    for compare_word in allowed_words:
        index = get_index(correctness(compare_word, word))
        final_count[index] += 1
    return final_count


def calculate_expected_gain(word, pattern, invalid_chars):
    allowed_words = get_words_for_pattern(word, pattern, invalid_chars)
    word_gain_map = {}
    for word in allowed_words:
        counts = get_all_patterns_count(word, allowed_words)
        gain = calculate_i_gain(counts)
        word_gain_map[word] = gain
    return word_gain_map

word_gain_map = calculate_expected_gain(args.w, [int(i) for i in args.p], args.i)
list_of_gains = [[g,w] for w, g in word_gain_map.items()]
list_of_gains.sort(reverse=True)
for i in range(min(10, len(list_of_gains))):
    print(list_of_gains[i])
# for i in list_of_gains:
#     print(i)







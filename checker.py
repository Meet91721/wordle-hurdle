import math
import random
import argparse

from server import correctness

with open("possible_words.txt") as f:
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
        index = get_index(correctness(compare_word, word))
        res[index] += 1
    return res

def get_words_for_pattern(source, pattern, invalid_chars, invalid_char_pos):
    res = []
    # all_words = ['devil']
    for word in all_words:
        if correctness(word, source) == pattern:
            w = str(word)
            for i in range(len(pattern)):
                if pattern[i] != 3:
                    # print(i, pattern.index(i), source[pattern.index(i)], source[i])
                    w = w.replace(source[i], "", 1)

            # print(all_words)
            # print(w)
            if all ([c not in w for c in invalid_chars]):
                for pos, char in invalid_char_pos:
                    if word[pos] == char:
                        break
                else:
                    res.append(word)
    return res

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

def depth_first_search(group) -> (str, float):
    if len(group) == 1:
        return group[0], 1
    best_guess = None
    best_avg_depth = float("inf")
    for guess in group:
        pattern_groups = {}
        for target in group:
            pattern = correctness(guess, target)
            pattern = ''.join([str(i) for i in pattern])
            # print(guess, target, pattern)
            if pattern not in pattern_groups:
                pattern_groups[pattern] = []
            pattern_groups[pattern].append(target)
        avg_depth = 0
        for pattern, sub_group in pattern_groups.items():
            avg_depth += len(sub_group) * depth_first_search(sub_group)[1]
        avg_depth /= len(group)
        if avg_depth < best_avg_depth:
            best_avg_depth = avg_depth
            best_guess = guess
    return best_guess, best_avg_depth

def calculate_expected_gain(word, pattern, invalid_chars="", invalid_char_pos=[]):
    allowed_words = get_words_for_pattern(word, pattern, invalid_chars, invalid_char_pos)
    return depth_first_search(allowed_words)[0]

def get_best_start_word():
    start_word_gain_map = {}
    for word in all_words:
        counts = get_list_for_a_word(word)
        gain = calculate_i_gain(counts)
        start_word_gain_map[word] = gain
        b = "Processed words " + str(len(start_word_gain_map)) + "/" + str(len(all_words))
        print (b, end="\r")
    list_of_gains = [[g,w] for w, g in start_word_gain_map.items()]
    list_of_gains.sort(reverse=True)
    for i in range(min(10, len(list_of_gains))):
        print(list_of_gains[i])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--get-best", type=str)
    parser.add_argument("--word", type=str)
    parser.add_argument("--pattern", type=str)
    parser.add_argument("--invalid-char", type=str)
    parser.add_argument("--invalid-posn", type=str)
    args = parser.parse_args()

    if args.get_best:
        get_best_start_word()
        exit(0)

    invalid_posn = []
    if args.invalid_posn:
        for i in range(0, len(args.invalid_posn), 2):
            invalid_posn.append([int(args.invalid_posn[i]), str(args.invalid_posn[i+1])])

    invalid_char = args.invalid_char if args.invalid_char else ""

    prediction = calculate_expected_gain(args.word, [int(i) for i in args.pattern], invalid_char, invalid_posn)





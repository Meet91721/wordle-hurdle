from checker import correctness, calculate_expected_gain

counts = {}

with open("possible_words.txt") as f:
    all_words = f.read().splitlines()

# all_words = all_words[:200]

start_word = ['arose', 'unlit']

def step_information(guess_word, pattern):
    invalid_char = ''
    invalid_posn = []
    valid_posn = []
    for i in range(len(pattern)):
        if pattern[i] == 3:
            invalid_char += guess_word[i]
        elif pattern[i] == 1:
            invalid_posn.append((i, guess_word[i]))
        else:
            valid_posn.append((i, guess_word[i]))
    return invalid_char, invalid_posn, valid_posn

for all_words_i, target_word in enumerate(all_words):
    steps = 1
    guess_word = start_word[0]
    invalid_char, invalid_posn, valid_posn = ["", [], []]
    for i in range(len(start_word) - 1):
        if guess_word == target_word:
            break
        i_char, i_posn, v_posn = step_information(guess_word, correctness(target_word, guess_word))
        invalid_char += i_char
        invalid_posn += i_posn
        valid_posn += v_posn
        steps+=1
        guess_word = str(start_word[i + 1])

    while guess_word != target_word:
        pattern = correctness(target_word, guess_word)
        i_char, i_posn, v_posn = step_information(guess_word, pattern)
        invalid_char += i_char
        invalid_posn += i_posn
        valid_posn += v_posn
        word_gain_map = calculate_expected_gain(guess_word, pattern, invalid_char, invalid_posn, valid_posn)
        # word_gain_map = calculate_expected_gain(guess_word, pattern, invalid_char, invalid_posn, [])
        list_of_gains = [[g,w] for w, g in word_gain_map.items()]
        list_of_gains.sort(reverse=True)
        if len(list_of_gains) == 0:
            print(guess_word, target_word, pattern, invalid_char, invalid_posn)
        guess_word = list_of_gains[0][1]
        steps += 1
    if steps not in counts:
        counts[steps] = 0
    counts[steps] += 1

    if all_words_i % 10 == 0:
        print(f"After {all_words_i} words:")
        for i,j in counts.items():
            print(i, j)
        print('===============')

print("Test Result:")
print("Start word:", start_word)
total = sum(counts.values())
print("Total words:", total)
print("Final counts:")
for i,j in counts.items():
    print(i, j)

expected_steps = sum([i*j for i,j in counts.items()]) / total
print("Expected steps:", expected_steps)



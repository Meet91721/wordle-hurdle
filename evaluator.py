from checker import correctness, calculate_expected_gain

counts = {}

with open("possible_words.txt") as f:
    all_words = f.read().splitlines()

# all_words = all_words[:200]

start_word = "raise"

for all_words_i, target_word in enumerate(all_words):
    guess_word = str(start_word)
    steps = 1
    invalid_char = ''
    invalid_posn = []
    while guess_word != target_word:
        # print(guess_word, target_word)
        steps += 1
        pattern = correctness(target_word, guess_word)
        for i in range(len(pattern)):
            if pattern[i] == 3:
                invalid_char += guess_word[i]
            elif pattern[i] == 1:
                invalid_posn.append((i, guess_word[i]))
        word_gain_map = calculate_expected_gain(guess_word, pattern, invalid_char, invalid_posn)
        list_of_gains = [[g,w] for w, g in word_gain_map.items()]
        list_of_gains.sort(reverse=True)
        # print(list_of_gains[:10])
        guess_word = list_of_gains[0][1]
        # print(pattern, invalid_char, invalid_posn)
    if steps not in counts:
        counts[steps] = 0
    counts[steps] += 1

    if all_words_i % 10 == 0:
        print(f"After {all_words_i} words:")
        for i,j in counts.items():
            print(i, j)
        print('===============')

print("Final counts:")
total = sum(counts.values())
for i,j in counts.items():
    print(i, j)

expected_steps = sum([i*j for i,j in counts.items()]) / total
print("Expected steps:", expected_steps)
print("Total words:", total)



import random
from sys import unraisablehook


#Open file

words = None
with open('C:\\Users\\Chloe\\Downloads\\corncob_caps.txt', 'r') as f:
    words = f.read().splitlines()

#Generate 7 unique letters at random
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
letters = set()

possible_letter_sets = []
for word in words:
    letters = set()
    for letter in word:
        letters.add(letter)
    if len(letters) == 7:
        possible_letter_sets.append(letters)

letters = random.choice(possible_letter_sets)
mandatory_letter = random.choice(list(letters))
    
useable_words = set()
panagrams = set()
for word in words:
    if len(word) < 4:
        #print("too short")
        continue
    #Make sure the word contains the mandatory letter
    if mandatory_letter not in word:
        continue
    #Make sure the word contains only the letters in the list
    word_failed = False
    is_panagram = True
    for letter in word:
        if letter not in letters:
            word_failed = True
            break
    if word_failed:
        continue
    for letter in letters:
        if letter not in word:
            is_panagram = False       
            break 
    useable_words.add(word)
    if not is_panagram:
        continue
    panagrams.add(word)

print()
print(' ' * 5, mandatory_letter)
print(" ".join(letters))
print()
print(f"{len(useable_words)} words, of which {len(panagrams)} are panagrams")
print("Commnads: \nq to quit\nh for hint\n- to forfeit and print all words\nm to print all found words\nl to print all letters")

found_words = set()
while len(useable_words) > 0:
    guess = input(">>> ").upper()
    if guess == "Q":
        break
    elif guess == "H":
        word_to_hint = random.choice(list(useable_words))
        pos_to_give = random.randint(0, len(word_to_hint) - 1)
        for i in range(len(word_to_hint)):
            if i == pos_to_give:
                print(word_to_hint[i], end=" ")
            else:
                print("_", end=" ")
        print()
        continue
    elif guess == "-":
        print("Forfeited words:")
        for word in useable_words:
            if word in panagrams:
                print("*", end=" ")
            print(word)
        break
    elif guess == "M":
        for word in found_words:
            if word in panagrams:
                print("*", end=" ")
            print(word)
        continue
    elif guess == "L":
        print()
        print(' ' * 4, mandatory_letter)
        print(" ".join(letters))
        print()
        continue
    if guess not in useable_words:
        print("Not a valid guess")
        continue
    print(f"{guess} is a word!")
    useable_words.remove(guess)
    found_words.add(guess)
    if guess in panagrams:
        print(f"{guess} is a panagram!")
if len(useable_words) == 0:
    print("Congratulations! You've found all the words!")
print("Thanks for playing!")
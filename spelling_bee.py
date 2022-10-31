import random
from sys import unraisablehook
from rich import print
from rich.console import Console

console = Console()
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

letter_set = random.choice(possible_letter_sets)
mandatory_letter = random.choice(list(letter_set))
letter_set.remove(mandatory_letter)
letters = list(letter_set)[0:3] + [mandatory_letter] + list(letter_set)[3:]

    
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

possible_score = 0
for word in useable_words:
    if len(word) == 4:
        possible_score += 1
        continue
    possible_score += len(word)
    if word in panagrams:
        possible_score += 7

tiers = {
    "Genius": int(possible_score * 0.7),
    "Amazing": int(possible_score * 0.5),
    "Great": int(possible_score * 0.4),
    "Nice": int(possible_score * 0.25),
    "Solid": int(possible_score * 0.15),
    "Good": int(possible_score * 0.08),
    "Moving Up": int(possible_score * 0.05),
    "Good Start": int(possible_score * 0.02),
    "Beginner": int(possible_score * 0.00),
}

print()
print("  __  _   _       ___       __    _   _  _   ")
print(" (_  |_) |_ |  |   |  |\ | /__   |_) |_ |_ | ")
print(" __) |   |_ |_ |_ _|_ | \| \_|   |_) |_ |_ o ")
print()

console.print("", " ".join(letters[0:2]))
console.print(letters[2], f"[bold red]{letters[3]}[/bold red]", letters[4])
console.print(""," ".join(letters[5:]))
print()
print(f"{len(useable_words)} words, of which {len(panagrams)} are panagrams")
print(f"Total possible score is {possible_score}")
print()
print("Tiers:")
for tier, points in tiers.items():
    print(f"{tier}: {points} points")
print()

print("Commands: \nq to quit\nh or ? for help\n- to forfeit and print all words\nm to print all found words\nl to print all letters\na for a hint")
print()
print("Try to make words with the letters provided!")
print("You can use each letter as many times as you like.")
print("You must include the mandatory letter in each word.")
print("You can only make words containing more than 4 letters.")
print()
print("Score is calculated as follows:")
print("For 4 letter words, 1 point is awarded.")
print("For words above 4 letters, the number of points awarded is equal to the length of the word.")
print("Additionally, if a word is a panagram (i.e. it has every letter at least once), 7 points are awarded.")
print()


found_words = set()
score = 0
while len(useable_words) > 0:
    tier = None
    for s_tier, points in tiers.items():
        if score >= points and (tier == None or tiers[s_tier] > tiers[tier]):
            tier = s_tier
        
    guess = input(f"{score}({tier})>>> ").upper()
    if guess == "Q":
        break
    elif guess == "H" or guess == "?":
        print()
        print("Commands: \nq to quit\nh or ? for help\n- to forfeit and print all words\nm to print all found words\nl to print all letters\na for a hint")
        print()
        print("Try to make words with the letters provided!")
        print("You can use each letter as many times as you like.")
        print("You must include the mandatory letter in each word.")
        print("You can only make words containing more than 4 letters.")
        print()
        print("Score is calculated as follows:")
        print("For 4 letter words, 1 point is awarded.")
        print("For words above 4 letters, the number of points awarded is equal to the length of the word.")
        print("Additionally, if a word is a panagram (i.e. it has every letter at least once), 7 points are awarded.")
        print()
        continue
    elif guess == "A":
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
                console.print(f"[bold red]{word}[/bold red]")
            else:
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
        l = letters[0:3] + letters[4:]
        random.shuffle(l)
        console.print("", " ".join(l[0:2]))
        console.print(l[2], f"[bold red]{mandatory_letter}[/bold red]", l[3])
        console.print(""," ".join(l[4:]))
        print()
        print(f"{len(useable_words) + len(found_words)} words, of which {len(panagrams)} are panagrams")
        print(f"Total possible score is {possible_score}")
        print("Tiers:")
        for tier, points in tiers.items():
            print(f"{tier}: {points} points")
        print()
        continue
    if len(guess) < 4:
        print("Too short!")
        continue
    if mandatory_letter not in guess:
        print("You must include the mandatory letter in each word.")
        continue
    for letter in guess:
        if letter not in letters:
            print("You can only use the letters provided.")
            break
    if guess not in useable_words:
        print("Not a valid guess")
        continue
    print(f"{guess} is a word!")
    if len(guess) == 4:
        score += 1
    else:
        score += len(guess)
    useable_words.remove(guess)
    found_words.add(guess)
    if guess in panagrams:
        print(f"[bold red]{guess}[/bold red] is a panagram!")
        score += 7
if len(useable_words) == 0:
    print("Congratulations! You've found all the words!")
print("Thanks for playing!")
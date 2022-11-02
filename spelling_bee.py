import random
from sys import unraisablehook
from rich import print
from rich.console import Console
import copy
import sys
import os
import IPython

console = Console()
#Open file

def help():
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

class SpellingBee:
    def __init__(self, file):
        with open(file, "r") as f:
            words = f.read().splitlines()

        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        possible_letter_sets = []

        for word in words:
            letters = set()
            for letter in word:
                letters.add(letter)
            if len(letters) == 7:
                possible_letter_sets.append(letters)

        self.letter_set = random.choice(possible_letter_sets)
        self.mandatory_letter = random.choice(list(self.letter_set))
        self.letter_set.remove(self.mandatory_letter)
        self.letters = list(self.letter_set)[0:3] + [self.mandatory_letter] + list(self.letter_set)[3:]
        self.useable_words = set()
        self.panagrams = set()
        self.possible_score = 0


        for word in words:
            if len(word) < 4:
                continue

            #Make sure the word contains the mandatory letter
            if self.mandatory_letter not in word:
                continue
            #Make sure the word contains only the letters in the list

            word_failed = False
            is_panagram = True
            for letter in word:
                if letter not in self.letters:
                    word_failed = True
                    break
            if word_failed:
                continue
            for letter in self.letters:
                if letter not in word:
                    is_panagram = False       
                    break 
            self.useable_words.add(word)
            if not is_panagram:
                continue
            self.panagrams.add(word)

        for word in self.useable_words:
            if len(word) == 4:
                self.possible_score += 1
            else:
                self.possible_score += len(word)
            if word in self.panagrams:
                self.possible_score += 7

        self.tiers = {
            "Genius": int(self.possible_score * 0.7),
            "Amazing": int(self.possible_score * 0.5),
            "Great": int(self.possible_score * 0.4),
            "Nice": int(self.possible_score * 0.25),
            "Solid": int(self.possible_score * 0.15),
            "Good": int(self.possible_score * 0.08),
            "Moving Up": int(self.possible_score * 0.05),
            "Good Start": int(self.possible_score * 0.02),
            "Beginner": int(self.possible_score * 0.00),
        }
        self._show_letters()

    def _show_letters(self):
        console.print("", " ".join(self.letters[0:2]))
        console.print(self.letters[2], f"[bold red]{self.letters[3]}[/bold red]", self.letters[4])
        console.print(""," ".join(self.letters[5:]))
        print()
        print(f"{len(self.useable_words)} words, of which {len(self.panagrams)} are panagrams")
        print(f"Total possible score is {self.possible_score}")
        print()
        print("Tiers:")
        for tier, points in self.tiers.items():
            print(f"{tier}: {points} points")
        print()
        pass

    def play(self):
        useable_words = copy.deepcopy(self.useable_words)
        found_words = set()
        score = 0
        while len(useable_words) > 0:
            tier = None
            for s_tier, points in self.tiers.items():
                if score >= points and (tier == None or self.tiers[s_tier] > self.tiers[tier]):
                    tier = s_tier
                
            guess = input(f"{score}({tier})>>> ").upper()

            if guess == "Q":
                return
            elif guess == "H" or guess == "?":
                help()
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
                    if word in self.panagrams:
                        console.print(f"[bold red]{word}[/bold red]")
                    else:
                        print(word)
                break
            elif guess == "M":
                for word in found_words:
                    if word in self.panagrams:
                        console.print(f"[bold red]{word}[/bold red]")
                    else:
                        print(word)
                continue
            elif guess == "L":
                self._show_letters()
                continue


            if len(guess) < 4:
                print("Too short!")
                continue

            if self.mandatory_letter not in guess:
                print("You must include the mandatory letter in each word.")
                continue

            for letter in guess:
                if letter not in self.letters:
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
            if guess in self.panagrams:
                print(f"[bold red]{guess}[/bold red] is a panagram!")
                score += 7
        if len(useable_words) == 0:
            print("Congratulations! You've found all the words!")
        print("Thanks for playing!")


print()
print("  __  _   _       ___       __    _   _  _   ")
print(" (_  |_) |_ |  |   |  |\ | /__   |_) |_ |_ | ")
print(" __) |   |_ |_ |_ _|_ | \| \_|   |_) |_ |_ o ")
print()

if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("Usage: python3 spelling_bee.py [wordlist]")
    help()
    sys.exit(0)
wordlist = sys.argv[1]
if not os.path.exists(wordlist):
    print(f"Wordlist {wordlist} does not exist.")
    sys.exit(1)
game = SpellingBee(wordlist)
game.play()

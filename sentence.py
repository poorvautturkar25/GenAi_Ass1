'''Q1:
Write a Python program that takes a sentence from the user and prints:

Number of characters

Number of words

Number of vowels

Hint: Use split(), loops, and vowel checking.
'''

def sentence_check(sentence):
    no_char = len(sentence)

    words = sentence.split()
    no_words = len(words)
    
    no_vowels = 0
    vowels = "aeiouAEIOU"
    for char in vowels:
        if char in vowels:
            no_vowels = no_vowels + 1
    
    print("Sentence Analyasis :")
    print("Number of Characters : ",no_char)
    print("Number of Words : ",no_words)
    print("Number of Vowels : ",no_vowels)

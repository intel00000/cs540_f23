import sys
import math
import numpy as np

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

# function to return the converted character in uppercase, ignoring non-alphabetic characters
def char_convert(char):
    if char.isalpha():
        return char.upper()
    else:
        return ''

def shred(filename):
    # Using a dictionary here. You may change this to any data structure of your choice such as lists (X=[]) etc for the assignment
    # prepopulate the dictionary with 0 counts for each letter
    X = {chr(i + ord("A")) : 0 for i in range(26)}
    with open (filename,encoding='utf-8') as f:
        for line in f:
            for char in line:
                if char.isalpha() and char.upper() in X:
                    X[char.upper()] += 1
    # return X
    return X

def print_counts(filename):
    # print the 26 character counts for letter.txt
    output_dict = shred(filename)
    for item in output_dict:
        print('{} {}'.format(item, output_dict[item]))

def Q1(filename):
    print('Q1')
    print_counts(filename)

def Q2(dict, index):
    # convert dictionary to list, ordered from A to Z
    X=[0]*26
    for item in dict:
        X[ord(item)-ord('A')] = dict[item]

    # get multinomial parameter vectors
    e, s = get_parameter_vectors()

    print('Q2')
    # control output to 4 decimal places
    print('{:.4f}'.format(X[index] * np.log(e[index])))
    print('{:.4f}'.format(X[index] * np.log(s[index])))

# 1.2 Language identification via Bayes rule
# We arrange the 26 counts into a 26-dimensional count vector
# mpv: multinomial probability vector
def get_conditional_probability(dict):
    # convert dictionary to list, ordered from A to Z
    X=[0]*26
    for item in dict:
        X[ord(item)-ord('A')] = dict[item]
    # sum of all counts
    total = sum(X)

    # define prior probabilities of letter being English or Spanish
    probability_English = 0.6
    probability_Spanish = 1 - probability_English

    # get multinomial parameter vectors
    e, s = get_parameter_vectors()

    # calculate multinomial coefficient using numpy
    coef = math.factorial(total) / np.prod([math.factorial(X[i]) for i in range(26)])

    # P(X | Y = language)
    # calculate multinomial_probability
    multinomial_probability_e = coef * np.prod([e[i] ** X[i] for i in range(26)])
    multinomial_probability_s = coef * np.prod([s[i] ** X[i] for i in range(26)])

    # P(Y = language | X)
    # calculate conditional_probability
    conditional_probability_e = (multinomial_probability_e * probability_English) / (multinomial_probability_e * probability_English + multinomial_probability_s * probability_Spanish)
    conditional_probability_s = (multinomial_probability_s * probability_Spanish) / (multinomial_probability_e * probability_English + multinomial_probability_s * probability_Spanish)

    return (conditional_probability_e, conditional_probability_s)

def get_F(dict):
    # convert dictionary to list, ordered from A to Z
    X=[0]*26
    for item in dict:
        X[ord(item)-ord('A')] = dict[item]
    # sum of all counts
    total = sum(X)

    # define prior probabilities of letter being English or Spanish
    probability_English = 0.6
    probability_Spanish = 1 - probability_English

    # get multinomial parameter vectors
    e, s = get_parameter_vectors()

    F_e = np.log(probability_English) + np.sum([X[i] * np.log(e[i]) for i in range(26)])
    F_s = np.log(probability_Spanish) + np.sum([X[i] * np.log(s[i]) for i in range(26)])

    return (F_e, F_s)

def Q3(filename):
    # control output to 4 decimal places
    print('Q3')
    F_e, F_s = get_F(shred(filename))
    print('{:.4f}'.format(F_e))
    print('{:.4f}'.format(F_s))

# 1.3
def get_conditional_probability_simplify_english(filename):
    F_e, F_s = get_F(shred(filename))
    if F_s - F_e >= 100:
        return 0
    elif F_s - F_e <= -100:
        return 1
    else:
        return 1 / (1 + np.exp(F_s - F_e))

def Q4(filename):
    print('Q4')
    print('{:.4f}'.format(get_conditional_probability_simplify_english(filename)))

def main():
    filename = 'letter.txt'
    # Q1
    Q1(filename)
    # Q2
    Q2(shred(filename), 0)
    # Q3
    Q3(filename)
    # Q4
    Q4(filename)

if __name__ == '__main__':
    main()
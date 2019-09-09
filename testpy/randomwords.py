
import csv
import random
import pandas as pd

def randomwords(n):

    # word_url = "https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-usa-no-swears-medium.txt"
    #word_path = r"C:\Users\jerryzli\Downloads\google-10000-english-master\google-20000-english-usa-no-swears-short(no less 3)-medium-long.txt"
    word_path = r"C:\Users\jerryzli\Downloads\google-10000-english-master\google-20000-english-usa-no-swears-short(no less 3)-medium-long-non-google.txt"
    words = open(word_path,"r").readlines()

    if n<=len(words) :
       wordlist = [words[random.randint(0, len(words))].replace('\n','') for i in range(n)]
       # write to csv
       df = pd.DataFrame(wordlist)
       df.to_csv(str(n) + 'randomwords.csv', header=False,index=False)
    else :
        print('not enough words to generate')


if __name__ == "__main__":
    n=10000
    randomwords(n)
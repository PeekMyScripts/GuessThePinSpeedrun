import requests
import random
import threading
from bs4 import BeautifulSoup

url = 'https://www.guessthepin.com/prg.php'

numberOfThreads = int(input("How many threads would you like to use?"))
guessedNumbers = []
correctGuesses = 0
timesReset = 0

def sendData():
    while True:
        global guessedNumbers
        global correctGuesses
        global timesReset
        if len(guessedNumbers) >= 10000:
            guessedNumbers = []
            timesReset += 1
        data = {
        'guess': format(random.randint(0, 9999), '04d')
        }
        while data['guess'] in guessedNumbers:
            data = {
            'guess': format(random.randint(0, 9999), '04d')
            }
        response = requests.post(url=url, data=data)
        soup = BeautifulSoup(response.content, 'html.parser')
        guessedNumbers.append(data['guess'])
        try:
            print(f"{data['guess']}    |   {soup.select_one('label').text}     |    Current # guessed nums: {len(guessedNumbers)}   |   Correct Guesses: {correctGuesses}     |   Times Reset: {timesReset}")
        except:
            correctGuesses += 1
            timesReset += 1
            print(f"{data['guess']} was the correct guess for a total of {correctGuesses} correct guesses")
            guessedNumbers = []
threads = []

for i in range(numberOfThreads):
    thread = threading.Thread(target=sendData, daemon=True)
    threads.append(thread)

for i in range(numberOfThreads):
    threads[i].start()

for i in range(numberOfThreads):
    threads[i].join()

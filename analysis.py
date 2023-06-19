from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import re

#stopwords resource
data_stopwords = requests.get(
  "https://gist.githubusercontent.com/larsyencken/1440509/raw/53273c6c202b35ef00194d06751d8ef630e53df2/stopwords.txt"
).text


#stopwords
def remove_stopwords(input_string):
  dict_stopwords = {}
  for val in data_stopwords.split("\n"):
    dict_stopwords[val.strip()] = 1

  output_string = ""
  for word in input_string.lower().split():
    if (word in dict_stopwords):
      continue
    output_string += word + " "
  output_string = output_string.strip()
  return output_string


#most common word frequency
def countFrequency(filename):
  #read the contents of the file
  with open(filename, 'r') as file:
    text = file.read().lower()

  words = text.split()

  word_count = {}

  for word in words:
    if word in word_count:
      word_count[word] += 1
    else:
      word_count[word] = 1

  sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

  for word, count in sorted_words[:10][::-1]:
    print(f'{word}: {count}')


def count_word_fractions(filename, words):

  def count_word(line, word):
    #check if defined word in title
    return 1 if word in line.lower() else 0

  #counter for total # titles
  num_titles = 0
  counts = {word: 0 for word in words}

  with open(filename, 'r') as file:
    for line in file:
      num_titles += 1
      for word in words:
        counts[word] += count_word(line, word)

  fractions = {word: counts[word] / num_titles for word in words}

  return fractions


words = ["flu", "virus", "death"]

fractions = count_word_fractions("titles_1918.txt", words)
fractions2 = count_word_fractions("titles_2020.txt", words)

#$ amounts discussed in articles
total_dollars = 0

with open('titles_1918.txt', 'r') as file:
  for line in file:
    matches = re.findall(r'\$([0-9]+(?:\.[0-9]{2})?)', line)
    for match in matches:
      total_dollars += float(match)

print(f'Total dollars mentioned in 1918: ${total_dollars:.2f}')

total_dollars = 0

with open('titles_2020.txt', 'r') as file:
  for line in file:
    matches = re.findall(r'\$([0-9]+(?:\.[0-9]{2})?)', line)
    for match in matches:
      total_dollars += float(match)

print(f'Total dollars mentioned in 2020: ${total_dollars:.2f}')

for word in words:
  fraction = fractions[word]
  print(
    f'The fraction of articles from 1918 that contained the word "{word}" was {fraction:.2f}'
  )

for word in words:
  fraction = fractions2[word]
  print(
    f'The fraction of articles from 2020 that contained the word "{word}" was {fraction:.2f}'
  )
#print frequencies
print(countFrequency("titles_1918.txt"))
print("******************************")
print(countFrequency("titles_2020.txt"))

#sentiment


def get_sentiment(filename):
  total_score = 0
  num_lines = 0

  analyzer = SentimentIntensityAnalyzer()

  with open(filename, 'r') as file:
    lines = file.readlines()

  for line in lines:
    try:
      vs = analyzer.polarity_scores(line)
      total_score = total_score + vs['compound']
      num_lines = num_lines + 1
    except:
      return -1

  #average sentiment score
  avg_score = total_score / num_lines

  return avg_score


#sentiment intensity average scores
avg_score1 = get_sentiment("titles_1918.txt")
print(f"Average sentiment score: {avg_score1:.2f}")

avg_score2 = get_sentiment("titles_2020.txt")
print(f"Average sentiment score: {avg_score2:.2f}")

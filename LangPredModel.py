import pickle
import math
from nltk import word_tokenize
from nltk import ngrams

#calculates probability of the argument text of being a dictionary language
def calcLanguageProbability(text, unigram_dict, bigram_dict, vocab_size):
  unigrams_test = word_tokenize(text)
  bigrams_test = list(ngrams(unigrams_test, 2))
  probability = 1

  for bigram in bigrams_test:
    #b = bigram count
    b = bigram_dict[bigram] if bigram in bigram_dict else 0
    #unigram count of the first word in bigram
    u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0

    #calculating probability of langauge
    v = vocab_size
    probability = ((b+1)/(u+v))

  return probability

#main
if __name__ == '__main__':
  #read pickled dictionaries
  eng_uni = pickle.load(open('data/eng_uni.p', 'rb'))
  fre_uni = pickle.load(open('data/fre_uni.p', 'rb'))
  ita_uni = pickle.load(open('data/ita_uni.p', 'rb'))
  eng_bi = pickle.load(open('data/eng_bi.p', 'rb'))
  fre_bi = pickle.load(open('data/fre_bi.p', 'rb'))
  ita_bi = pickle.load(open('data/ita_bi.p', 'rb'))

  #set token size as 0, and vocab size as length of dict
  eng_tokens = 0
  fre_tokens = 0
  ita_tokens = 0
  eng_vocabs = len(eng_uni)
  fre_vocabs = len(fre_uni)
  ita_vocabs = len(ita_uni)
  all_vocabs = eng_vocabs + fre_vocabs + ita_vocabs

  #get size from dictionary
  for tokens in eng_uni.values():
    eng_tokens += tokens
  for tokens in fre_uni.values():
    fre_tokens += tokens
  for tokens in ita_uni.values():
    ita_tokens += tokens

  #read test file and save as lines
  with open('data/LangId.test', 'r', encoding="utf-8") as test:
    test_lines = test.read().splitlines()
  
  #write a predict file with language prediction on each line
  with open('data/LangId.predict', 'w', encoding="utf-8") as predict:
    currentLine = 1

    #go through each line of test file and run lang probability function
    for l in test_lines:
      eng_p = calcLanguageProbability(l, eng_uni, eng_bi, all_vocabs)
      fre_p = calcLanguageProbability(l, fre_uni, fre_bi, all_vocabs)
      ita_p = calcLanguageProbability(l, ita_uni, ita_bi, all_vocabs)

      prediction = ""
      if eng_p>fre_p and eng_p>ita_p:   #if english chance is highest
        prediction = str(currentLine) + " English\n"
      elif fre_p>eng_p and fre_p>ita_p: #if french chance is highest
        prediction = str(currentLine) + " French\n"
      else:                             #else (italian chance is highest)
        prediction = str(currentLine) + " Italian\n"

      #write predictions on each line
      predict.write(prediction)
      currentLine += 1

  #now that prediction is done, open the solution file to check my accuracy
  with open('data/LangId.sol', 'r', encoding="utf-8") as soluFile:
    with open('data/LangId.predict', 'r', encoding="utf-8") as predFile:
      solutions = soluFile.readlines() 
      predictions = predFile.readlines()   

      totalPreds = 0
      correctPreds = 0
      incorrectLines = []
      
      wrongEngSol = 0
      wrongFreSol = 0
      wrongItaSol = 0 
      wrongEngPre = 0
      wrongFrePre = 0
      wrongItaPre = 0 

      #for each lines in both solution and prediction
      for s, p in enumerate(predictions):
        solutionLanguage = (solutions[s].split())[1]
        predictionLanguage = (predictions[s].split())[1]

        if solutionLanguage == predictionLanguage: #if prediction = solution
          correctPreds += 1          
        else:         #else, add just the line number
          incorrectLines.append((solutions[s].split())[0])
          if solutionLanguage == "English":
            wrongEngSol += 1
          if solutionLanguage == "French":
            wrongFreSol += 1
          if solutionLanguage == "Italian":
            wrongItaSol += 1
          if predictionLanguage == "English":
            wrongEngPre += 1
          if predictionLanguage == "French":
            wrongFrePre += 1
          if predictionLanguage == "Italian":
            wrongItaPre += 1
        totalPreds += 1   #increment total predictions

      #calc and print accuracy
      print("Language Prediction Accuracy: ", correctPreds / totalPreds)
      #print incorrectly classified items and their line number
      print("\nLine numbers of incorrectly classified items:", incorrectLines)
      print("\nEnglish solution missclassified count: ", wrongEngSol)
      print("French solution missclassified count: ", wrongFreSol)
      print("Italian solution missclassified count: ", wrongItaSol)
      print("\nEnglish wrong prediction count: ", wrongEngPre)
      print("French wrong prediction count: ", wrongFrePre)
      print("Italian wrong prediction count: ", wrongItaPre)
      print("\nBased on above results, we can conclude that some of our english and french texts are being classified as italian")
import re
import pke
extractor = pke.unsupervised.TopicRank()

# get synopses
file = open("synopses.txt", "r")
text = file.read()
synopses = re.findall(r"<synopsis>(.+)<\/synopsis>", text)
file.close()

# extract themes
file = open("synopsis_themes.txt", "w")
for synopsis in synopses:
    extractor.load_document(synopsis, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    number_of_themes = 10 #int(input("How many themes would you like? "))
    keyphrases = extractor.get_n_best(n=number_of_themes)
    for theme in keyphrases:
        file.write(str(theme[1]) + " " + theme[0] + "\n")
    file.write("\n")    
file.close()

from bs4 import BeautifulSoup
import requests
import re
import pke
extractor = pke.unsupervised.TopicRank()

try:
    url = input("Enter the URL of a Wikipedia movie article: ")
    source = requests.get(url)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, "html.parser")

    # find the "Plot" header
    span = soup.find("span", class_="mw-headline", text="Plot")
    plot_header = span.parent

    # collect all paragraphs in the "Plot" section
    paragraphs = [plot_header]
    paragraphs.append(paragraphs[-1].next_sibling)
    paragraphs.append(paragraphs[-1].next_sibling)
    while "<p>" in str(paragraphs[-1]):
        paragraphs.append(paragraphs[-1].next_sibling)

    # make it one string
    storyline = []
    for paragraph in paragraphs:
        storyline.append(str(paragraph))
    storyline = "".join(storyline)

    # remove tags
    tags = re.findall(r"<[^<>]+>", storyline)
    for i in range(len(tags)):
        storyline = re.sub(r"<[^<>]+>", r"", storyline)

    # extract themes
    extractor.load_document(storyline, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    number_of_themes = int(input("How many themes would you like? "))
    keyphrases = extractor.get_n_best(n=number_of_themes)

    print("Extracted themes:")
    print("=================")
    for keyphrase in keyphrases:
        print(f'{keyphrase[1]:.5f}   {keyphrase[0]}')
    
except Exception as e:
    print(e)

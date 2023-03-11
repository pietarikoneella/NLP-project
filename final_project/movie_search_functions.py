import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize
#nltk.download('punkt')
import pke
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt

import re

def this_is_movie_search():
    message = "NLP is great!"
    return message

def index_documents_from_text_file():
    """ This function first opens a file, reads its contents
        into a string and closes the file. Then it creates and returns a list
        of every item consisiting of an article title and the article text itself
    """
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
    
        input_file = open("synopses.txt", "r", encoding= 'Windows-1252')    

        #for line in input_file:
        #    line = line.strip()
        #    document_string += line + " "
        document_string = input_file.read()
        input_file.close()

    except FileNotFoundError:
        print(f"File was not found.")
    except OSError:
        print(f"Something went wrong reading the file.")
    except:
        print("Something went wrong.")

    article_content_string = re.sub(r"<synopsis>", "",  document_string)
    synopsis_list = article_content_string.strip().split("</synopsis>")
    
    return synopsis_list

def rewrite_token(t):
    d = {"and": "&", "or": "|",
        "not": "1 -",
        "(": "(", ")": ")"}  # operator replacements 
    #print(d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))) # N.B. This print statement shows the rewritten query!
    
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) 


def rewrite_query(query): # rewrite every token in the query
        return " ".join(rewrite_token(t) for t in query.split())

def search_b(synopsis_list, query): #boolean search
    """This function handles the Boolean search
    """
    if synopsis_list[-1] == "":
        synopsis_list = synopsis_list[:250]
    hits_list = []
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r"(?u)\b\w\w*\b") # indexing all words containing alphanumeric characters
    
    sparse_matrix = cv.fit_transform(synopsis_list)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    # There seems to be variation in these commands between scikit-learn versions - 
    # this block of code helps with that 
    try:
        terms = cv.get_feature_names_out()
    except AttributeError:
        terms = cv.get_feature_names()
    
    t2i = cv.vocabulary_
    parts = query.split()
    parts_without = parts[:]
    parts_into_string = " ".join(parts)
    try:
        hits_matrix = eval(rewrite_query(parts_into_string))
        print(hits_matrix)
    except:
        print("Oops")
    

    all_one = False

    for i, p in enumerate(parts_without):
        if p == "not" or p == "and" or p == "or":
            continue
        elif p not in terms:
            if i > 0 and parts_without[i-1] == "not":
                if i-1 == 0:
                    parts = parts[i+1:]
                elif i-1 > 0:
                    parts = parts[:i-1]
                all_one = True
            elif i != len(parts_without)-1 and parts_without[i+1] == "or":
                parts = parts[i+1:]
                all_one = False
            elif i == len(parts_without)-1 and parts_without[i-1] == "or":
                parts = parts[:i-1]
                all_one = False
            else:
                continue
            
    operator = ""
    if len(parts) > 0:
        if parts[0] == "or" or parts[0] == "and":
            operator = parts[0]
            parts = parts[1:]
            #print("And tai or alussa",parts)
        
        elif parts[-1] == "or" or parts[-1] == "and":
            operator = parts[-1]
            parts = parts[:len(parts)-1]
            #print("And tai or lopussa",parts)
    
        if operator == "or" and all_one == True:
            shape = 1, len(synopsis_list)
            hits_matrix = numpy.ones(shape, dtype=int)
    
        elif operator == "and":
            if len(parts) > 0:
                parts_into_string = " ".join(parts)
                hits_matrix = eval(rewrite_query(parts_into_string))

        else:
            parts_into_string = " ".join(parts)
            try:
                hits_matrix = eval(rewrite_query(parts_into_string))
            except KeyError:
                shape = 1, len(synopsis_list)
                hits_matrix = numpy.zeros(shape, dtype=int)
        hits_list = list(hits_matrix.nonzero()[1])
    else:
        shape = 1, len(synopsis_list)
        hits_matrix = numpy.ones(shape, dtype=int)
        hits_list = list(hits_matrix.nonzero()[1])
        
    return hits_list
    

def search_t(synopsis_list, query): #tf-idf search
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    sparse_matrix = tfv.fit_transform(synopsis_list).T.tocsr() # CSR: compressed sparse row format => order by terms

    # The query vector is a horizontal vector, so in order to sort by terms, we need to use CSC
    query_vec = tfv.transform([query]).tocsc() # CSC: compressed sparse column format

    hits = np.dot(query_vec, sparse_matrix)
    best_doc_ids = []

    try:
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

        for score, i in ranked_scores_and_doc_ids:
                best_doc_ids.append(i)

    except IndexError: # Entering an unknown word causes IndexError
        print("No matches")
    #print("Best doc ids:", best_doc_ids)
    return best_doc_ids

def stemming_documents(docs):

    ps = PorterStemmer()
    docs_tokens = [word_tokenize(i) for i in docs]
    docs = [[]]
    docs = [[ps.stem(token) for token in docs_tokens[i]] for i in range(0, len(docs_tokens))]
                         
    for i in range(0, len(docs)):
        docs[i] = " ".join(docs[i])
    return(docs)


def stem_query(q):
    ps = PorterStemmer()
    query_split = q.split(" ")
    
    for i in range(0, len(query_split)):
        if i == 0:
            q = "".join(q)
            q = ps.stem(q)

        elif i > 0:
            query_list_stem = []
            query_list_stem = [ps.stem(token) for token in query_split] 
            q = " ".join(query_list_stem)

    return q



def make_plot(keyph, title):
    if len(keyph) > 0:
        themes = []
        values = []

        if f"./static/article_{title}_plot.png":
            print(f"The plot for \"{title}\" is already in static!")
                
        for p in keyph:
            themes.append(p[1].replace(' ', '\n'))
            values.append(round(p[0], 2))

        fig = plt.figure()
        plt.title(f"Themes for movie \"{title}\"")
        colors = plt.cm.rainbow(np.linspace(0, 1, 10))
        bar = plt.bar(themes, values, color = colors)
        plt.xticks(rotation=50)
        plt.subplots_adjust(bottom=0.6, right=0.4)
        plt.tight_layout()
        labels = plt.bar_label(bar, values)
        plt.savefig(f'static/movie_{title}_plot.png')

def make_bubble_plot(keyph, title):

# Original code source: https://matplotlib.org/stable/gallery/misc/packed_bubbles.html

# The original code was modified for the purpose of Movie Search

    if len(keyph) > 0:
            themes = []
            values = []

            if f"./static/article_{title}_plot.png":
                print(f"The plot for \"{title}\" is already in static!")
                    
            for p in keyph:
                themes.append(p[1].replace(' ', '\n'))
                values.append(round(p[0], 2))

    class BubbleChart:
        def __init__(self, area, bubble_spacing=0):
            """
            Setup for bubble collapse.

            Parameters
            ----------
            area : array-like
                Area of the bubbles.
            bubble_spacing : float, default: 0
                Minimal spacing between bubbles after collapsing.

            Notes
            -----
            If "area" is sorted, the results might look weird.
            """
            area = np.asarray(area)
            r = np.sqrt(area / np.pi)

            self.bubble_spacing = bubble_spacing
            self.bubbles = np.ones((len(area), 4))
            self.bubbles[:, 2] = r
            self.bubbles[:, 3] = area
            self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
            self.step_dist = self.maxstep / 2

            # calculate initial grid layout for bubbles
            length = np.ceil(np.sqrt(len(self.bubbles)))
            grid = np.arange(length) * self.maxstep
            gx, gy = np.meshgrid(grid, grid)
            self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
            self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]

            self.com = self.center_of_mass()

        def center_of_mass(self):
            return np.average(
                self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
            )

        def center_distance(self, bubble, bubbles):
            return np.hypot(bubble[0] - bubbles[:, 0],
                            bubble[1] - bubbles[:, 1])

        def outline_distance(self, bubble, bubbles):
            center_distance = self.center_distance(bubble, bubbles)
            return center_distance - bubble[2] - \
                bubbles[:, 2] - self.bubble_spacing

        def check_collisions(self, bubble, bubbles):
            distance = self.outline_distance(bubble, bubbles)
            return len(distance[distance < 0])

        def collides_with(self, bubble, bubbles):
            distance = self.outline_distance(bubble, bubbles)
            idx_min = np.argmin(distance)
            return idx_min if type(idx_min) == np.ndarray else [idx_min]

        def collapse(self, n_iterations=50):
            """
            Move bubbles to the center of mass.

            Parameters
            ----------
            n_iterations : int, default: 50
                Number of moves to perform.
            """
            for _i in range(n_iterations):
                moves = 0
                for i in range(len(self.bubbles)):
                    rest_bub = np.delete(self.bubbles, i, 0)
                    # try to move directly towards the center of mass
                    # direction vector from bubble to the center of mass
                    dir_vec = self.com - self.bubbles[i, :2]

                    # shorten direction vector to have length of 1
                    dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                    # calculate new bubble position
                    new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                    new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                    # check whether new bubble collides with other bubbles
                    if not self.check_collisions(new_bubble, rest_bub):
                        self.bubbles[i, :] = new_bubble
                        self.com = self.center_of_mass()
                        moves += 1
                    else:
                        # try to move around a bubble that you collide with
                        # find colliding bubble
                        for colliding in self.collides_with(new_bubble, rest_bub):
                            # calculate direction vector
                            dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                            dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                            # calculate orthogonal vector
                            orth = np.array([dir_vec[1], -dir_vec[0]])
                            # test which direction to go
                            new_point1 = (self.bubbles[i, :2] + orth *
                                        self.step_dist)
                            new_point2 = (self.bubbles[i, :2] - orth *
                                        self.step_dist)
                            dist1 = self.center_distance(
                                self.com, np.array([new_point1]))
                            dist2 = self.center_distance(
                                self.com, np.array([new_point2]))
                            new_point = new_point1 if dist1 < dist2 else new_point2
                            new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                            if not self.check_collisions(new_bubble, rest_bub):
                                self.bubbles[i, :] = new_bubble
                                self.com = self.center_of_mass()

                if moves / len(self.bubbles) < 0.1:
                    self.step_dist = self.step_dist / 2

        def plot(self, ax, labels, colors):
            """
            Draw the bubble plot.

            Parameters
            ----------
            ax : matplotlib.axes.Axes
            labels : list
                Labels of the bubbles.
            colors : list
                Colors of the bubbles.
            """
            for i in range(len(self.bubbles)):
                circ = plt.Circle(
                    self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
                ax.add_patch(circ)
                ax.text(*self.bubbles[i, :2], labels[i],
                        horizontalalignment='center', verticalalignment='center')


    bubble_chart = BubbleChart(area=values,
                            bubble_spacing=0.05)

    bubble_chart.collapse()

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    colors = plt.cm.rainbow(np.linspace(0, 1, 10))
    bubble_chart.plot(
        ax, themes, colors)
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()
    #ax.set_title('Movie themes')
    plt.title(f"Themes for movie \"{title}\"")

    plt.savefig(f'static/movie_{title}_bubble_plot.png')

    #plt.show()



def search_other():
    return "This is some other search"

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

titles = ["Movie 1", "Movie 2", "Movie 3", "Movie 4"]
ratings = [2, 3, 4, 5]
synopses = ["Synopsis 1", "Synopsis 2", "Synopsis 3", "Synopsis 4"]
themes = [["Theme 1", "theme 2", "theme 3"], ["Theme 2", "Theme 4", "Theme 5"], ["Theme 2", "Theme 3", "Theme 4", "Theme 5"], ["Theme 3", "Theme 4", "Theme 5", "Theme 6", ] ]

data = zip(titles, ratings, synopses, themes)
query = ""
result_list = []

class Movie:
    def __init__(self, id, title, rating, synopsis, themes):
        self.__id = id
        self.__title = title
        self.__rating = rating
        self.__synopsis = synopsis
        self.__themes = themes
    
    def get_id(self):
        return self.__id
    
    def get_title(self):
        return self.__title
    
    def get_rating(self):
        return self.__rating
    
    def get_synopsis(self):
        return self.__synopsis
    
    def get_themes(self):
        return self.__themes

@app.route('/')
def index():
    print("Hello, world")
    return render_template('index.html')

@app.route('/index')
def search():

    query = request.args.get('query')
    i = 0
    for item in data:
        new_movie = Movie(i, item[0], item[1], item[2], item[3])
        result_list.append(new_movie)
        i+=1
    #for item in result_list:
    #    print(item.get_id())
    #    print(item.get_title())
    #    print(item.get_rating())
    #    print(item.get_synopsis())
    #    print(item.get_themes())
    
    if query:
        print('The query is "' + query +'".')

    return render_template('index.html', result_list=result_list, query=query)

@app.route('/movie/<id>')

def show_movie(id):
    print("Showing movie")
    id = int(id)
    movie_ = Movie(id, titles[id], ratings[id], synopses[id], themes[id])

    return render_template('movie.html', result_list=result_list, id=id, movie_=movie_)

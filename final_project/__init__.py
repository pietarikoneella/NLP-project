from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

titles = ["Movie 1", "Movie 2", "Movie 3", "Movie 4"]
synopses = ["Synopsis 1", "Synopsis 2", "Synopsis 3", "Synopsis 4"]
themes = [["Theme 1", "theme 2", "theme 3"], ["Theme 2", "Theme 4", "Theme 5"], ["Theme 2", "Theme 3", "Theme 4", "Theme 5"], ["Theme 3", "Theme 4", "Theme 5", "Theme 6", ] ]
data = zip(titles, synopses, themes)
query = ""

@app.route('/')
def index():
    print("Hello, world")
    return render_template('index.html')


@app.route('/index')
def search():

    query = request.args.get('query')

    
    if query:
        print('The query is "' + query +'".')

    return render_template('index.html', data=data, query=query)

@app.route('/movie/<title>')

def show_movie(title):
    print("Showing movie")

    #title = request.args.get('query')

    
    return render_template('movie.html', title=title)

#def show_movie(title, synopsis):

#    return render_template('movie.html', title=title, synopsis=synopsis)


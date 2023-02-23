from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')

def first():
    return "Movie search" 

@app.route('/search')

def search():

    #query = request.args.get('query')
    #if query:
    title = ["Great movie"]
    synopsis = "Exciting plot, world-class actors, big themes, beautifully excecuted."


    return render_template('search.html', title=title, synopsis=synopsis)

#@app.route('/movie')

#def show_movie(title, synopsis):

#    return render_template('movie.html', title=title, synopsis=synopsis)



    
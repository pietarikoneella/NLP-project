from flask import Flask

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

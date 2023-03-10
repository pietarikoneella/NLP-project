from flask import Flask

class Movie:

    def __init__(self, id, title, rating, year, themes, summary, synopsis):#, photo):
        self.__id = id
        self.__title = title
        self.__rating = rating
        self.__year = year
        self.__themes = themes
        self.__summary = summary
        self.__synopsis = synopsis
       # self.__photo = photo
    
    def get_id(self):
        return self.__id
    
    def get_title(self):
        return self.__title
    
    def get_rating(self):
        return self.__rating
    
    def get_year(self):
        return self.__year
    
    def get_themes(self):
        return self.__themes
    
    def get_summary(self):
        return self.__summary
    
    def set_synopsis(self, syn):
        self.__synopsis = syn

    def get_synopsis(self):
        return self.__synopsis

    #def get_photo(self):
    #    return self.__photo
    

    

    
    
    #def set_themes(self, theme_list):
    #    self.__themes = theme_list[:]
    


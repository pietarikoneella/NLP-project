def main():

    document = open("articles.txt", "r", encoding="utf-8")
    document.read()


    query ="*"
    while query != "":
        query = input("Type a query: ")
        if query == "":
            print("Goodbye!")
            break
        
    
main()

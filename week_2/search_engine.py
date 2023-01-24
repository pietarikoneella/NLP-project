def code_from_jupyter_notebook():
    #2 
    from sklearn.feature_extraction.text import CountVectorizer

    #1
    documents = ["This is a silly example",
                "A better example",
                "Nothing to see here",
                "This is a great and long example"]

    #3
    cv = CountVectorizer(lowercase=True, binary=True) 
    sparse_matrix = cv.fit_transform(documents)

    print("Term-document matrix: (?)\n")
    print(sparse_matrix)

    #4
    dense_matrix = sparse_matrix.todense()

    print("Term-document matrix: (?)\n")
    print(dense_matrix)

    #5
    td_matrix = dense_matrix.T   # .T transposes the matrix

    print("Term-document matrix:\n")
    print(td_matrix)

    #6
    print("\nIDX -> terms mapping:\n")
    print(cv.get_feature_names_out())

    #7
    terms = cv.get_feature_names_out()

    print("First term (with row index 0):", terms[0])
    print("Third term (with row index 2):", terms[2])

    #8
    print("\nterm -> IDX mapping:\n")
    print(cv.vocabulary_) # note the _ at the end

    #9
    print("Row index of 'example':", cv.vocabulary_["example"])
    print("Row index of 'silly':", cv.vocabulary_["silly"])

    #10
    t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index
    print("Query: example")
    print(td_matrix[t2i["example"]])

    #11
    print("Query: example AND great")
    print("example occurs in:                            ", td_matrix[t2i["example"]])
    print("great occurs in:                              ", td_matrix[t2i["great"]])
    print("Both occur in the intersection (AND operator):", td_matrix[t2i["example"]] & td_matrix[t2i["great"]])

    #12
    print("Query: is OR see")
    print("is occurs in:                            ", td_matrix[t2i["is"]])
    print("see occurs in:                           ", td_matrix[t2i["see"]])
    print("Either occurs in the union (OR operator):", td_matrix[t2i["is"]] | td_matrix[t2i["see"]])

    #13
    print("Query: NOT this")
    print("this occurs in:                     ", td_matrix[t2i["this"]])
    print("this does not occur in (complement):", 1 - td_matrix[t2i["this"]]) # 1 - x changes 1 to 0 and 0 to 1

    #14
    print("Query: ( example AND NOT this ) OR nothing")
    print("example occurs in:                  ", td_matrix[t2i["example"]])
    print("this does not occur in:             ", 1 - td_matrix[t2i["this"]])
    print("example AND NOT this:               ", td_matrix[t2i["example"]] & (1 - td_matrix[t2i["this"]]))
    print("nothing occurs in:                  ", td_matrix[t2i["nothing"]])
    print("( example AND NOT this ) OR nothing:", 
        (td_matrix[t2i["example"]] & (1 - td_matrix[t2i["this"]])) | td_matrix[t2i["nothing"]])

    #15
    ########################################################
    # Operators and/AND, or/OR, not/NOT become &, |, 1 -
    # Parentheses are left untouched
    # Everything else is interpreted as a term and fed through td_matrix[t2i["..."]]

    d = {"and": "&", "AND": "&",
        "or": "|", "OR": "|",
        "not": "1 -", "NOT": "1 -",
        "(": "(", ")": ")"}          # operator replacements

    def rewrite_token(t):
        return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

    def rewrite_query(query): # rewrite every token in the query
        return " ".join(rewrite_token(t) for t in query.split())

    def test_query(query):
        print("Query: '" + query + "'")
        print("Rewritten:", rewrite_query(query))
        print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command
        print()

    test_query("example AND NOT nothing")
    test_query("NOT example OR great")
    test_query("( NOT example OR great ) AND nothing") # AND, OR, NOT can be written either in ALLCAPS
    test_query("( not example or great ) and nothing") # ... or all small letters
    test_query("not example and not nothing")
    ########################################################

    #16
    print(sparse_matrix)

    #17
    print(sparse_matrix.tocsc()) # M: now starting with the wordnumbers

    #18
    print(sparse_matrix.T)

    #19
    sparse_td_matrix = sparse_matrix.T.tocsr()
    print(sparse_td_matrix)

    #20
    def rewrite_token(t):
        return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

    test_query("NOT example OR great")

    #21
    hits_matrix = eval(rewrite_query("NOT example OR great"))
    print("Matching documents as vector (it is actually a matrix with one single row):", hits_matrix)
    print("The coordinates of the non-zero elements:", hits_matrix.nonzero())    

    #22
    hits_list = list(hits_matrix.nonzero()[1])
    print(hits_list)

    #24
    for doc_idx in hits_list:
        print("Matching doc:", documents[doc_idx])

    #25
    for i, doc_idx in enumerate(hits_list):
        print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))




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

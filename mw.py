from operator import itemgetter
import mwclient
import sys

def get_llist(page):
    languages = page.langlinks()
    langlist = list(languages)
    return langlist

def listpages(category, limit=0): #0 means only current cat, set to 1 for one subcategory etc
    mylist = []
    for page in category:
        if page.namespace != 14:
            langlist=get_llist(page)
            langs = set([item[0] for item in langlist])
            if "en" in langs:
                print page.name, "exists on English Wikipedia."
            else:
                print page.name, "does not exist on English Wikipedia."
                mytuple = (page.name, len(langlist))
                mylist.append(mytuple)
        else:
            if limit > 0:
                mylist += listpages(page, limit-1)
    return mylist

if __name__ == '__main__':
    site = mwclient.Site('sv.wikipedia.org')
    try:
        categoryname = sys.argv[1].decode("utf8")
    except IndexError:
        categoryname = "Byggnader i Tammerfors"
    category = site.Categories[categoryname]

    data = listpages(category)
    sorteddata = sorted(data, key=itemgetter(1), reverse=True)
    for x in sorteddata:
        print x

from operator import itemgetter
import mwclient
import sys

def get_llist(page):
    languages = page.langlinks()
    langlist = list(languages)
    return langlist

def listpages(category):
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
             pass
    return mylist

if __name__ == '__main__':
    site = mwclient.Site('sv.wikipedia.org')
    try:
        categoryname = sys.argv[1]
    except IndexError:
        categoryname = "Kyrkobyggnader i Tammerfors"
    category = site.Categories[categoryname]

    data = listpages(category)
    sorteddata = sorted(data, key=itemgetter(1), reverse=True)
    for x in sorteddata:
        print x

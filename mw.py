from operator import itemgetter
import mwclient

def get_llist(page):
    languages = page.langlinks()
    langlist = list(languages)
    return langlist

def listpages(category):
    text = []
    for page in category:
        if page.namespace != 14:
            langlist=get_llist(page)
            langs = set([item[0] for item in langlist])
            if "en" in langs:
                print page.name, "exists on English Wikipedia."
            else:
                print page.name, "does not exist on English Wikipedia."
                text.append(page.name)
        else:
             pass
    return text

if __name__ == '__main__':
    site = mwclient.Site('sv.wikipedia.org')
    category = site.Categories['Kyrkobyggnader i Helsingfors']

    data = listpages(category)
    langdict = {}
    for x in data:
        page = site.Pages[x]
        langlist = get_llist(page)
        langdict[x] = len(langlist)

    sorteddict = sorted(langdict.items(), key=itemgetter(1), reverse=True)
    for x in sorteddict:
        print x

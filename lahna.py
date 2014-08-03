from operator import itemgetter
import mwclient
import sys
import codecs
import csv

def get_llist(page):
    languages = page.langlinks()
    langlist = list(languages)
    return langlist

def listpages(category, limit=0):
    """
    0 means only current cat, set to 1 for one subcategory etc
    ALSO THIS REALLY NEEDS TO BE SPLIT IN SEPARATE FUNCTIONS
    FOR LISTING PAGES AND GETTING IW LINKS
    THIS MAKES NO SENSE RIGHT NOW
    """
    mylist = []
    for page in category:
        if page.namespace != 14:
            langlist=get_llist(page)
            langs = set([item[0] for item in langlist])
            if targetlanguage in langs:
                print page.name, "exists on %s Wikipedia." % targetlanguage
            else:
                print page.name, "does not exist on %s Wikipedia." % targetlanguage
                mytuple = (page.name, len(langlist))
                mylist.append(mytuple)
        else:
            if limit > 0:
                mylist += listpages(page, limit-1)
    return mylist

def listcatscan(f):
    """
    Work on csv file from http://tools.wmflabs.org/catscan2/catscan2.php.
    """
    with codecs.open("catscan", "rt", "utf8") as f:
        reader = csv.reader(f)
        listoftitles = []
        next(reader, None)
        next(reader, None) #wtf there must be a better way...
        for row in reader:
            print row[0]
            listoftitles.append(row[0])
    return listoftitles

def wikiformat(data):
    wikioutput = []
    for x in data:
        y = "* [[:" + languagecode + ":"+ x[0] + "|" + x[0] + "]], " + str(x[1])
        wikioutput.append(y)
    return wikioutput

def saveoutput(data):
    with codecs.open("output.txt", "w", "utf8") as outputfile:
        for x in output:
            outputfile.write(x + "\n")
    return outputfile

if __name__ == '__main__':
    languagecode = "sv"
    targetlanguage = "en"
    site = mwclient.Site(languagecode + '.wikipedia.org')
    try:
        categoryname = sys.argv[1].decode("utf8")
    except IndexError:
        categoryname = "Byggnader i Tammerfors"
    category = site.Categories[categoryname]

    data = listpages(category)
    sorteddata = sorted(data, key=itemgetter(1), reverse=True)
    for x in sorteddata:
        print x
    output = wikiformat(sorteddata)
    for x in output:
        print x
    myfile = saveoutput(output)

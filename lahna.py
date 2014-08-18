import argparse
import csv
import codecs
import mwclient
from operator import itemgetter


def get_iwlist(page):
    languages = page.langlinks()
    langlist = list(languages)
    return langlist


def newlistpages(category, limit):
    """
    limit = 0 means only current cat, set to 1 for one subcategory etc
    """
    mylist = []
    for page in category:
        if page.namespace != 14:
            mylist.append(page.name)
        else:
            if limit > 0:
                mylist += newlistpages(page, limit - 1)
    return mylist


def iwprocess(data):
    outputlist = []
    for x in data:
        page = site.Pages[x]
        iwlist = get_iwlist(page)
        iw = set([item[0] for item in iwlist])
        if targetlanguage in iw:
            print page.name, "exists on %s Wikipedia." % targetlanguage
        else:
            print page.name, "does not exist on %s Wikipedia." % targetlanguage
            mytuple = (page.name, len(iwlist))
            outputlist.append(mytuple)
    return outputlist


def listcatscan(f):
    """
    Work on csv file from http://tools.wmflabs.org/catscan2/catscan2.php.
    """
    with open("catscan", "rt") as f:
        reader = csv.reader(f)
        listoftitles = []
        next(reader, None)
        next(reader, None)  # wtf there must be a better way...
        for row in reader:
            listoftitles.append(row[0].decode("utf-8"))
    return listoftitles


def sort(data):
    """
    Sort by number of iwlinks in descending order.
    """
    sorteddata = sorted(data, key=itemgetter(1), reverse=True)
    return sorteddata


def wikiformat(data):
    wikioutput = []
    for x in data:
        y = "* [[:" + languagecode + ":" + x[0] + "|" + x[0] + "]], " + \
            str(x[1])
        wikioutput.append(y)
    return wikioutput


def saveoutput(data):
    with codecs.open("output.txt", "w", "utf8") as outputfile:
        for x in data:
            outputfile.write(x + "\n")
    return outputfile


def processall(data):
    """
    Takes a list of pages as input, processes it all the way to saving
    wikiformatted output to file.
    """
    outputlist = iwprocess(data)
    sorteddata = sort(outputlist)
    formattedoutput = wikiformat(sorteddata)
    myfile = saveoutput(formattedoutput)
    return myfile


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=None)
    parser.add_argument(
        "-c", "--category", default='Tampereen kirkkorakennukset')
    parser.add_argument("-s", "--sourcelanguage", default='fi')
    parser.add_argument("-t", "--targetlanguage", default='sv')
    args = parser.parse_args()
    filename = args.file
    languagecode = args.sourcelanguage
    categoryname = args.category.decode("utf8")
    targetlanguage = args.targetlanguage
    site = mwclient.Site(languagecode + '.wikipedia.org')
    if args.file:
        data = listcatscan(filename)
    else:
        category = site.Categories[categoryname]
        data = newlistpages(category, 0)
    myfile = processall(data)

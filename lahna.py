#!/usr/bin/env python3
import argparse
import csv
import codecs
import mwclient
from operator import itemgetter
import json
from pprint import pprint

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
        namespace = page.namespace
        print(page.name)
        if namespace != 14:
            if namespace == 0:
                mylist.append(page.name)
        else:
            if limit > 0:
                cat = site.Categories[page.name.split(":")[1]]
                mylist += newlistpages(cat, limit - 1)
    return mylist


def iwprocess(data):
    outputlist = []
    for x in data:
        page = site.Pages[x]
        iwlist = get_iwlist(page)
        iw = set([item[0] for item in iwlist])
        if targetlanguage in iw:
            print(page.name, "exists on %s Wikipedia." % targetlanguage)
        else:
            print(page.name, "does not exist on %s Wikipedia." % targetlanguage)
            mytuple = (page.name, len(iwlist))
            outputlist.append(mytuple)
    return outputlist

def sort(data):
    """
    Sort by number of iwlinks in descending order.
    """
    data = list(set(data))
    sorteddata = sorted(data, key=itemgetter(1), reverse=True)
    return sorteddata


def wikiformat(data):
    wikioutput = []
    for x in data:
        y = "* [[:" + languagecode + ":" + x[0] + "|" + x[0] + "]], " + \
            str(x[1])
        wikioutput.append(y)
    return wikioutput


def saveoutput(data, filename):
    with codecs.open(filename, "w", "utf8") as outputfile:
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
    if (args.file):
        myfile = saveoutput(formattedoutput, "test.txt")
    else:
        myfile = saveoutput(formattedoutput, generateFileName(languagecode, targetlanguage, categoryname))
    return myfile

def generateFileName(source, target, category):
    return category + "_" + source + "_" + target + ".txt"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--category", required=False)
    parser.add_argument("-s", "--sourcelanguage", default='en', required=True)
    parser.add_argument("-t", "--targetlanguage", default='sv', required=True)
    parser.add_argument("-d", "--depth", default='0', required=False)
    parser.add_argument("-f", "--file", default=None)
    args = parser.parse_args()
    filename = args.file
    languagecode = args.sourcelanguage
    categoryname = args.category
    targetlanguage = args.targetlanguage
    site = mwclient.Site(('https', languagecode + '.wikipedia.org'))
    if args.file:
        with open(filename) as data_file:    
            data = json.load(data_file)
            itemList = (data["*"][0]["a"]["*"])
            titleList = []
            for item in itemList:
                print(item["title"])
                titleList.append(item["title"])
        myfile = processall(titleList)
        #data = listFromFile(filename)
    else:
        category = site.Categories[categoryname]
        data = newlistpages(category, int(args.depth))
    #myfile = processall(data)

#Lahna

Find articles with most interwiki links that are missing in a certain Wikipedia version, based on category search. Uses the [mwclient](https://github.com/mwclient/mwclient) library.

## Usage

```
python3 lahna.py -c "Finnish painters" -s en -t sv -d 0
```
-c Category in which to search for articles
-s Source Wikipedia version (the one with the category)
-t Target Wikipedia version (the one where we want to see which articles are missing)
-d Depth of category search, default is 0

The output contains a list of articles from the source Wikipedia that are missing on the target Wikipedia, ordered by most interwiki links and formated for wiki display:

```
* [[:en:Léopold Survage|Léopold Survage]], 5
* [[:en:Aleksanteri Ahola-Valo|Aleksanteri Ahola-Valo]], 5
* [[:en:Andreas Alariesto|Andreas Alariesto]], 3
* [[:en:Jorma Gallen-Kallela|Jorma Gallen-Kallela]], 3
```

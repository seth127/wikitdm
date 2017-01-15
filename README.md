# wikitdm
a Python library for wiki-weighted TF-IDF and keyword analysis

# Python version
To run in Python 2.* use `import wikitdm2`

To run in Python 3.* use `import wikitdm3`

All the functionality is the same regardless of Python version.

*Note:* **All terms are stemmed and made lower-case. Digits are also converted to `NUM`. At this time, there is no way to change this.**

# Basic Functions
### *wikitdm*(textDir, log = True, saveToCsv = True, printEach = True, noPro = False)
Returns a pandas DataFrame with terms as the index and document names as the columns.

Arguments:

`textDir` The directory where the text files to be analyzed are located. Currently designed to work with only `.txt` files encoded in `utf-8`, each file treated as a single document.

`log` Boolean: whether to use the log(IDF) or raw IDF as the multiplier.

`saveToCsv` Boolean: whether to save a .csv file of the TDM.

`printEach` Boolean: whether to print to the console the top 5 words in each document as it runs. Mostly just for keeping track of progress.

`noPro` Boolean: if `True` doesn't include any pronouns as terms.

### *wikidtm*()
The exact same as `wikitdm()` except the axes are reversed. Index is document names and columns are terms. It has all the same parameters.

### *wikiKeywords*(filename, wordCount)
Returns a list of the top ranking terms for a given document.

Arguments:

`filename` The name of (and path, if necessary) of the document.

`wordCount` The number of keywords to return.

# Sample Text and Calls
The library comes with some sample texts to try things out on. They are in the folders `sampleText` and `sampleTextTrump`.

### Some example calls
    from wikitdm3 import *
    sampleTDM = wikitdm('sampleText')

    wikiKeywords('sampleText/brain.txt')
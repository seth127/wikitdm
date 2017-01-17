# wikitdm
a Python library for wiki-weighted TF-IDF and keyword analysis

The purpose of this library is be able to extract the "important" keywords from documents, or to construct a Term Frequency-Inverse Document Frequency (TF-IDF) matrix with scores that reflect this notion of "importance." We are using the term "important" to mean the sense that those words are uniquely prevelant in a certain document, as compared to in general language use.

The more conventional TF-IDF weights words by the frequency that they appear in documents *in the corpus being analyzed*, however in many cases this is not ideal. For example, this was conceived while analyzing religious texts and attempting to find the words which were most relevant to a particular tradition's religious discourse. In this case, those words would be in *a lot* of the documents in *our corpus* and therefore would be considered "common words" and weighted down accordingly. However, these words are rare in general language usage.

This is solved by using Wikipedia as the IDF portion of the calculation. The entire dump of all of Wikipedia was downloaded (in February of 2016), and filtered to only articles containing at least 35,000 characters (in order to trim the corpus to a more manageable size, and to get rid of re-directs and disambiguations, etc.). This was then converted in a long, thin matrix with every term (stemmed and lower-cased) found in the corpus, and an IDF score indicating how many articles that term appeared in. Thus Wikipedia stands in as a proxy for "general usage" of English.

By using this number of the TF-IDF calculation, you are weighting words based on their prevalance in the document, scaled by their prevalance in Wikipedia. In our experience, this gives a very useful measure of which words are uniquely important to each document.

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
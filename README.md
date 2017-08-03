# flashcards

A command line utility (and Python module) for producing flashcards suitable for printing on [Moo](http://moo.com/) MiniCards.

This module makes use of the [ReportLab](http://www.reportlab.com/opensource/) open-source PDF Toolkit to produce .pdf files.

The module provides a minimal class definition for Moo MiniCards, and a minimal wrapper around some useful PDF generation/drawing commands from the ReportLab Toolkit.
___
The command line utility can be used to produce simple flashcards from a comma delimited list containing (Rank,Value) pairs.

I have used the command line utility to produce spelling flashcards using wordlists from [Oxford University Press](http://www.oxfordwordlist.com/).

Having generated and downloaded (as .csv) a wordlist,

```bash
$ cat oxford_wordlist.csv | ./flashcards.py ./pdfs/
```

produces one .pdf file (e.g., [rank]_[word].pdf) in ./pdfs/ for each card, containing a single word from the wordlist together with its rank. These .pdf files can be uploaded at [Moo.com](http://moo.com/) to produce high quality flashcards.

![alt text](https://github.com/cnuahs/flashcards/images/Photo_2017-08-03.jpg "Moo MiniCard Flashcards")

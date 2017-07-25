#!/opt/local/bin/python2.7

# 2017-07-25 - Shaun L. Cloherty <s.cloherty@ieee.org>

import os;

import flashcards;

from reportlab.pdfbase import pdfmetrics;
from reportlab.pdfbase.ttfonts import TTFont;
from reportlab.lib.colors import Color;

path = os.path.join(".","pdfs");

label = "";

# define colours
# colours = {'mint': Color(0.15,0.67,0.63), # green'ish
#            'plum': Color(0.67,0.13,0.35), # maroon?
#            'pink': Color(0.91,0.63,0.72), # pink
#            'gray': Color(0.42,0.55,0.62)}; # egg shell?

# colours = {'black': Color(0.0,0.0,0.0), # 000000
#            'ink': Color(0.02,0.18,0.31), # 062f4f
#            'posy': Color(0.51,0.22,0.45), # 813772
#            'embers': Color(0.72,0.15,0.0)}; # b82601

# colours = {'black': Color(0.0,0.0,0.0),
#            'pink': Color(0.93,0.34,0.42), # ec576b
#            'aqua': Color(0.31,0.77,0.76), # 4ec5c1
#            'lime': Color(0.90,0.89,0.22)}; # e5e338

# colours = {'feather': Color(0.47,0.79,0.83), # 77c9d4
#            'marine': Color(0.34,0.74,0.56), # 57bc90
#            'forest': Color(0.0,0.32,0.35), # 015259
#            'sleek_gray': Color(0.65,0.65,0.69)}; # a5a5af

colours = {'0_sleek_gray': Color(0.65,0.65,0.69), # a5a5af
           '1_forest': Color(0.0,0.32,0.35), # 015259
           '2_ink': Color(0.02,0.18,0.31), # 062f4f
           '3_posy': Color(0.51,0.22,0.45), # 813772
           '4_embers': Color(0.72,0.15,0.0)}; # b82601

# import fonts...
pdfmetrics.registerFont(TTFont('Helvetica-Bold','HelveticaBold.ttf'));
pdfmetrics.registerFont(TTFont('Helvetica-Italic','HelveticaOblique.ttf'));

for k,v in colours.iteritems():
    fname = "{0}.pdf".format(k);
    fname = os.path.join(path,fname);

    c = flashcards.ZigZag(fname,label,v);
    c.save();

#!/opt/local/bin/python2.7
'''
Make pdf flashcards for printing on Moo MiniCards.
'''

# 2017-07-25 - Shaun L. Cloherty <s.cloherty@ieee.org>

import os, sys, csv;

from reportlab.pdfgen import canvas;
from reportlab.lib.units import mm;
from reportlab.pdfbase import pdfmetrics;
from reportlab.pdfbase.ttfonts import TTFont;
from reportlab.lib.colors import Color;

from argparse import ArgumentParser;
import argparse;

import logging;

class MooMini(object):
    # Moo MiniCard dimensions are as follows:
    #
    #   bleed: 74x32mm
    #    trim: 72x30mm (i.e., finished size)
    #    safe: 66x24mm
    #
    # Min. line thickness is 0.5pt.
    def __init__(self,filename):
        self.filename = filename;
        self.width = 74.0; # mm
        self.height = 32.0;
        self.margin = 4.0; # mm

        self.showMask = False;

        # create the canvas object
        self.canvas = canvas.Canvas(filename,pagesize=(self.width*mm,self.height*mm));
        self.canvas.translate(self.margin*mm,self.margin*mm);

    def drawMask(self):
        # draw safe area boundary...
        red85 = Color(1.0,0.0,0.0,alpha = 0.15);
        white = Color(1.0,1.0,1.0);
        self.canvas.saveState();
        self.canvas.translate(-1*self.margin*mm,-1*self.margin*mm);
        self.canvas.setFillColor(red85);
        self.canvas.rect(0.0,0.0,self.width*mm,self.height*mm,stroke=0,fill=1);

        width = (self.width-2*self.margin);
        height = (self.height-2*self.margin);
        self.canvas.setFillColor(white);
        self.canvas.rect(self.margin*mm,self.margin*mm,width*mm,height*mm,stroke=0,fill=1);
        self.canvas.restoreState();

    def save(self):
        self.draw();
        self.canvas.save();


class FlashCard(MooMini):
    # Class for creating a flashcard suitable for printing on Moo MiniCards
    def __init__(self,filename,txt,head = [],foot = []):
        super(FlashCard,self).__init__(filename);

        self.txt = txt;
        self.head = head;
        self.foot = foot;

        self.gray = Color(0.7,0.7,0.7);

        self.fontSize = 24;

    def drawHeader(self,head):
        self.canvas.saveState();
        self.canvas.translate(0+1,(self.height-2*self.margin)*mm);
        self.canvas.setFont("Helvetica-Italic",10);
        self.canvas.setFillColor(self.gray);
        self.canvas.drawString(0,-10,head);
        self.canvas.restoreState();

    def drawFooter(self,foot):
        self.canvas.saveState();
        self.canvas.translate((self.width-2*self.margin)*mm-1,0.0);
        self.canvas.setFont("Helvetica-Italic",10);
        self.canvas.setFillColor(self.gray);
        self.canvas.drawRightString(0,0,foot);
        self.canvas.restoreState();

    def drawText(self,txt):
        self.canvas.saveState();
        self.canvas.translate((0.5*self.width-self.margin)*mm,(0.5*self.height-self.margin)*mm);
        self.canvas.setFont("Helvetica-Bold",self.fontSize);
        self.canvas.drawCentredString(0,-8,txt);
        self.canvas.restoreState();

    def draw(self):
        if self.showMask:
            self.drawMask();
        self.drawHeader(self.head);
        self.drawText(self.txt);
        self.drawFooter(self.foot);
        self.canvas.showPage();


class ZigZag(MooMini):
    def __init__(self,filename,label = "",colour = Color(0.5,0.5,0.5)):
        super(ZigZag,self).__init__(filename);

        self.label = label;

        self.colour = colour;
        self.lineWidth = 1.5; # pt

        self.red = Color();

    def draw(self):
        # draw the zig-zag pattern
        x = int(round(0.5*self.width/5)*5+10);
        x = range(-1*x,x,5);
        y = [2*(k % 2)-1 for k in x];

        y0 = int(round(0.5*self.height))+10;

        self.canvas.saveState();
        self.canvas.setLineWidth(self.lineWidth);
        self.canvas.setLineCap(1); # 1 = round cap, 2 = square cap
        self.canvas.setStrokeColor(self.colour);
        self.canvas.translate((0.5*self.width-self.margin)*mm,(0.5*self.height-self.margin)*mm); # center
        self.canvas.saveState();
        self.canvas.translate(0.0,-1*y0*mm); # bottom
        for jj in range(0,2*y0,1):
            self.canvas.translate(0.0,1.5*mm);
            for ii in range(len(x)-1):
                self.canvas.line(x[ii]*mm,y[ii]*mm,x[ii+1]*mm,y[ii+1]*mm);
        self.canvas.restoreState(); # center
        self.canvas.setFillColor(Color(1.0,1.0,1.0)); # white
        self.canvas.circle(0.0,0.0,10*mm+2,stroke=0,fill=1);
        self.canvas.circle(0.0,0.0,10*mm,stroke=1,fill=1);
        self.canvas.setFillColor(self.colour);
        self.canvas.circle(0.0,0.0,10*mm-2,stroke=0,fill=1);
        self.canvas.setFillColor(Color(1.0,1.0,1.0)); # white
        self.canvas.setFont("Helvetica-Italic",12);
        self.canvas.drawCentredString(0,-4,self.label);
        self.canvas.restoreState();


def main(args):
    logging.basicConfig(stream = sys.stderr,
                        format='%(levelname)s:%(message)s',
                        level = args.loglevel or logging.INFO);

    logging.debug("args = %s", args);
    logging.debug("path = %s", getattr(args,"path"));

    # register TrueType fonts for embedding... as required by moo.com
    # pdfmetrics.registerFont(TTFont('Helvetica','Helvetica.ttf'));
    pdfmetrics.registerFont(TTFont('Helvetica-Bold','HelveticaBold.ttf'));
    pdfmetrics.registerFont(TTFont('Helvetica-Italic','HelveticaOblique.ttf'));

    with getattr(args,'csvfile') as fid:
#        import pdb; pdb.set_trace();
        logging.info("Reading input from %s...", fid.name);

        dialect = 'excel';

        # note: cannot seek() on stdin, so don't attempt to
        #       determine the dialect and just use the default
        #       'excel' dialect

        if fid is not sys.stdin:
            logging.info('Sniffing csv dialect...');
            dialect = csv.Sniffer().sniff(fid.read(2*1024));
#            dialect.skipinitialspace = True;
#            csv.register_dialect(ns,dialect)

            fid.seek(0); # reset file pointer?

        reader = csv.DictReader(fid,dialect=dialect);

        cnt = 0; mx = ""; imx = 0;
        for row in reader:
            logging.debug("%i:row = %s", cnt, row);

            rank = row["Rank:"]; # rank
            word = row["Word:"]; # word

            if len(rank) == 0:
                rank = 0;
            fname = "{0}_{1}.pdf".format(rank,word);
            fname = os.path.join(getattr(args,'path'),fname);
            logging.info("fname = %s.", fname);
            myCard = FlashCard(fname,word,"",rank);
#            myCard.showMask = True;
            myCard.save();
            cnt = cnt + 1;

        logging.info("Ok. Read %i words.", cnt);

    return(0);


if __name__ == "__main__":
    prog = os.path.basename(sys.argv[0]);

    rev = 0.1; # increment this if modifying the script

    version = "%s v%s" % (prog, rev);

    p = ArgumentParser(usage = "%(prog)s [options] PTH",
                       description = __doc__,
                       conflict_handler = "resolve");

    # add arguments here
    p.add_argument("--version", action = "version", version = version);

    # control debugging output/verbosity
    group = p.add_mutually_exclusive_group();
    group.add_argument("-v","--verbose",
                    action = "store_const", const = logging.DEBUG,
                    dest = "loglevel",
                    help = "increase verbosity");
    group.add_argument("-q","--quiet",
                    action = "store_const", const = logging.WARN,
                    dest = "loglevel",
                    help = "suppress non-error messages");

    # optional arguments
    p.add_argument("path", action = "store",
                    help = argparse.SUPPRESS);

    # required arguments
    p.add_argument("-i","--input",
                   action = 'store', type = argparse.FileType('r', 0),
                   default = sys.stdin,
                   metavar = "FILE",
                   dest = "csvfile",
                   help = "read text from FILE in csv format");

    args = p.parse_args();
    exit(main(args));

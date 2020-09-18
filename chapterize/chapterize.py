import click
#https://click.palletsprojects.com/en/7.x/
import logging
import re
import os

@click.command()
@click.argument('book')
@click.option('--nochapters', is_flag=True, default=False, help="Don't actually split the book into chapters. Just extract the inner text.")
@click.option('--stats', is_flag=True, default=False, help="Don't actually split the book into chapters. Just return statistics about the chapters.")
@click.option('--verbose', is_flag=True, help='Get extra information about what\'s happening behind the scenes.')
@click.option('--debug', is_flag=True, help='Turn on debugging messages.')
@click.version_option('0.1')
def cli(book, nochapters, stats, verbose, debug):
    """ This tool breaks up a plain text book into chapters.
    It works especially well with Project Gutenberg plain text ebooks.
    This may also be used to strip metatextual text (tables of contents,
    headings, Project Gutenberg licenses) from a book, to prepare it
    for text analysis. Just use the --nochapters option.
    """

    if verbose:
        logging.basicConfig(level=logging.INFO)

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.info('Now attempting to break the file %s into chapters.' % book)

    bookObj = Book(book, nochapters, stats)

class Book():
    def __init__(self, filename, nochapters, stats):
        self.filename = filename
        self.nochapters = nochapters
        self.contents = self.getContents()
        self.lines = self.getLines()
        self.headings = self.getHeadings()
        # Alias for historical reasons. FIXME
        self.headingLocations = self.headings
        self.ignoreTOC()
        self.ignoreShort()
        logging.info('Heading locations: %s' % self.headingLocations)
        headingsPlain = [self.lines[loc] for loc in self.headingLocations]
        logging.info('Headings: %s' % headingsPlain)
        self.chapters = self.getTextBetweenHeadings()
        # logging.info('Chapters: %s' % self.chapters)
        self.numChapters = len(self.chapters)

        if stats:
            self.getStats()
        else:
            self.writeChapters()

    def getContents(self):
        """
        Reads the book into memory.
        """
        with open(self.filename, errors='ignore') as f:
            contents = f.read()
        return contents

    def getLines(self):
        """
        Breaks the book into lines.
        """
        return self.contents.split('\n')

    def getHeadings(self):

        fixed_expressions = ["^PROLEGOMENI.?$", "^Proemio.?$", "^RAGIONE DELL'OPERA$", "^Introduzione$"]
        fixedPat = '(' + '|'.join(fixed_expressions) + ')'
        
        # CASE INSENSITIVE
        # Form 1: Capitolo I, Capitolo 1, Capitolo primo, CAPITOLO 1
        # Alternative Form 1: Primo capitolo. Quarto capitolo
        # Ways of enumerating chapters, e.g.
        
        arabicNumerals = '\d+'
        romanNumerals = '(?=[MDCLXVI])M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
        
        oneDigitCardinals = ['due', 'tre', 'quattro', 'cinque', 'sei', 'sette', 'otto', 'nove']
        firstBatchCardinals = ['dieci', 'undici', 'dodici', 'tredici', 'quattordici', 'quindici', 'sedici', 'diciassette', 'diciotto', 'diciannove']
        secondBatchCardinals = ['venti', 'trenta', 'quaranta', 'cinquanta', 'sessanta','settanta', 'ottanta', 'novanta']
        onesSecondBatch = [cardinal[:-1] + 'uno' for cardinal in secondBatchCardinals]
        remainingCardinals = [two_digits + one_digit for two_digits in secondBatchCardinals for one_digit in oneDigitCardinals]
        hundreds = ['cento' + cardinal for cardinal in oneDigitCardinals] + ['cento' + cardinal for cardinal in firstBatchCardinals] + \
        ['cento' + cardinal for cardinal in secondBatchCardinals] + ['cento' + cardinal for cardinal in onesSecondBatch] + \
        ['cento' + cardinal for cardinal in remainingCardinals] + ['centouno']
        all_hundreds = [cardinal + hundred for cardinal in remainingCardinals for hundred in hundreds]
        
        numberWords = ['uno'] + oneDigitCardinals + firstBatchCardinals + secondBatchCardinals + onesSecondBatch + remainingCardinals + hundreds + all_hundreds
        numberWordsPat = '(' + '|'.join(numberWords) + ')'
        
        ordinalNumberWords = ['primo', 'secondo', 'terzo', 'quarto', 'quinto', 'sesto', 
                              'settimo', 'ottavo', 'nono', 'decimo'] + [numberWord[:-1] + 'esimo' for numberWord in numberWords]
        ordinalsPat = '(' + '|'.join(ordinalNumberWords) + ')'
        
        enumeratorsList = [arabicNumerals, romanNumerals, numberWordsPat, ordinalsPat] 
        enumerators = '(' + '|'.join(enumeratorsList) + ')'
        form1 = 'capitolo ' + enumerators
        altForm1 = ordinalsPat + 'capitolo'

        # Form 2: II. Il Postino
        enumerators = romanNumerals
        separators = '(\. | )'
        titleCase = '[A-Z][a-z]'
        form2 = enumerators + separators + titleCase

        # Form 3: II. LA STRADA APERTA
        enumerators = romanNumerals
        separators = '(\. )'
        titleCase = '[A-Z][A-Z]'
        form3 = enumerators + separators + titleCase

        # Form 4: a number on its own, e.g. 8, VIII
        arabicNumerals = '^\d{1,3}\.?$'
        romanNumerals = '(?=[MDCLXVI])M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.?$'
        enumeratorsList = [arabicNumerals, romanNumerals]
        enumerators = '(' + '|'.join(enumeratorsList) + ')'
        form4 = enumerators
        altform4 = enumerators + '(\.)'

        # Form 5: LA STRADA APERTA.
        # NOT SAFE (CHECK EFFECTS ON SUCCESFUL PARSED CHAPTERS BEFORE APPLYING)
        #form5 = '[A-Z]+ [A-Z]+\.$'

        fixedPat = re.compile(fixedPat, re.IGNORECASE)
        pat = re.compile(form1, re.IGNORECASE)
        altPat = re.compile(altForm1, re.IGNORECASE)
        # This one is case-sensitive.
        pat2 = re.compile('(%s|%s|%s|%s)' % (form2, form3, form4, altform4))
        #pat2 = re.compile('(%s|%s|%s|%s|%s)' % (form2, form3, form4, altform4, form5))

        self.endLocation = self.getEndLocation()

        # TODO: can't use .index() since not all lines are unique.
        headings = []
        for i, line in enumerate(self.lines):
            if line.lstrip() == self.lines[self.endLocation].lstrip():
                print(line)
                headings.append(i)
                break
            if fixedPat.match(line.lstrip()) is not None:
                headings.append(i)
            if pat.match(line.lstrip()) is not None:
                headings.append(i)
            if altPat.match(line.lstrip()) is not None:
                headings.append(i)
            if pat2.match(line.lstrip()) is not None:
                if pat2.match(line.lstrip()).group(0) != "DI":
                    headings.append(i)

        if len(headings) < 3:
            logging.info('Headings: %s' % headings)
            logging.error("Detected fewer than three chapters. This probably means there's something wrong with chapter detection for this book.")
            exit()

        return headings

    def ignoreTOC(self):
        """
        Filters headings out that are too close together,
        since they probably belong to a table of contents.
        """
        pairs = zip(self.headingLocations, self.headingLocations[1:])
        toBeDeleted = []
        for pair in pairs:
            delta = pair[1] - pair[0]
            if delta < 4:
                if pair[0] not in toBeDeleted:
                    toBeDeleted.append(pair[0])
                if pair[1] not in toBeDeleted:
                    toBeDeleted.append(pair[1])
        logging.debug('TOC locations to be deleted: %s' % toBeDeleted)
        for badLoc in toBeDeleted:
            index = self.headingLocations.index(badLoc)
            del self.headingLocations[index]


    def ignoreShort(self):
        """
        Filters headings out that are too close together,
        since they probably belong to a table of contents.
        """
        pairs = zip(self.headingLocations, self.headingLocations[1:])
        toBeDeleted = []
        for pair in pairs:
            delta = pair[1] - pair[0]
            if delta < 30:
                if pair[0] not in toBeDeleted:
                    toBeDeleted.append(pair[0])
        logging.debug('TOC locations to be deleted: %s' % toBeDeleted)
        for badLoc in toBeDeleted:
            index = self.headingLocations.index(badLoc)
            del self.headingLocations[index]

    def getEndLocation(self):
        """
        Tries to find where the book ends.
        """
        ends = ["^FINE.?$", "End of the Project Gutenberg EBook",
                "End of Project Gutenberg's",
                "\*\*\*END OF THE PROJECT GUTENBERG EBOOK",
                "\*\*\* END OF THIS PROJECT GUTENBERG EBOOK"]
        joined = '|'.join(ends)
        pat = re.compile(joined, re.IGNORECASE)
        endLocation = None
        for line in self.lines:
            if pat.match(line.lstrip()) is not None:
                endLocation = self.lines.index(line)
                self.endLine = self.lines[endLocation]
                break

        if endLocation is None: # Can't find the ending.
            logging.info("Can't find an ending line. Assuming that the book ends at the end of the text.")
            endLocation = len(self.lines)-1 # The end
            self.endLine = 'None'

        logging.info('End line: %s at line %s' % (self.endLine, endLocation))
        return endLocation

    def getTextBetweenHeadings(self):
        chapters = []
        lastHeading = len(self.headingLocations) - 1
        for i, headingLocation in enumerate(self.headingLocations):
            if i != lastHeading:
                nextHeadingLocation = self.headingLocations[i+1]
                chapters.append(self.lines[headingLocation:nextHeadingLocation])
        return chapters

    def zeroPad(self, numbers):
        """
        Takes a list of ints and zero-pads them, returning
        them as a list of strings.
        """
        maxNum = max(numbers)
        maxDigits = len(str(maxNum))
        numberStrs = [str(number).zfill(maxDigits) for number in numbers]
        return numberStrs

    def getStats(self):
        """
        Returns statistics about the chapters, like their length.
        """
        # TODO: Check to see if there's a log file. If not, make one.
        # Write headings to file.
        numChapters = self.numChapters
        averageChapterLength = sum([len(chapter) for chapter in self.chapters])/numChapters
        headings = ['Filename', 'Average chapter length', 'Number of chapters']
        stats = ['"' + self.filename + '"', averageChapterLength, numChapters]
        stats = [str(val) for val in stats]
        headings = ','.join(headings) + '\n'
        statsLog = ','.join(stats) + '\n'
        logging.info('Log headings: %s' % headings)
        logging.info('Log stats: %s' % statsLog)

        if not os.path.exists('log.txt'):
            logging.info('Log file does not exist. Creating it.')
            with open('log.txt', 'w') as f:
                f.write(headings)
                f.close()

        with open('log.txt', 'a') as f:
            f.write(statsLog)
            f.close()

    def writeChapters(self):
        chapterNums = self.zeroPad(range(1, len(self.chapters)+1))
        logging.debug('Writing chapter headings: %s' % chapterNums)
        basename = os.path.basename(self.filename)
        noExt = os.path.splitext(basename)[0]

        if self.nochapters:
            # Join together all the chapters and lines.
            text = ""
            for chapter in self.chapters:
                # Stitch together the lines.
                chapter = '\n'.join(chapter)
                # Stitch together the chapters.
                text += chapter + '\n'
            ext = '-extracted.txt'
            path = noExt + ext
            with open(path, 'w') as f:
                f.write(text)
        else:
            logging.info('Filename: %s' % noExt)
            outDir = noExt + '-chapters'
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            ext = '.txt'
            for num, chapter in zip(chapterNums, self.chapters):
                path = outDir + '/' + num + ext
                logging.debug(chapter)
                chapter = '\n'.join(chapter)
                with open(path, 'w') as f:
                    f.write(chapter)

if __name__ == '__main__':
    cli()

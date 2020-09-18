# It-Chapterize

<a href="https://github.com/JonathanReeve/chapterize">Chapterize</a> by <a href="https://github.com/JonathanReeve">Jonathan Reeve</a> is a command-line tool that breaks up Gutenberg Project English plain text e-books into chapters, removing both the chapter headings and the text not included between them. 

**It-Chapterize** is an adaptation of <a href="https://github.com/JonathanReeve/chapterize">Chapterize</a> for the Italian language with additional minor changes concerning the output.

* [Main Changes](#main-changes)
* [Installation and Testing](#installation-and-testing)
* [State of the Tool](#state-of-the-tool)
* [Tested on](#tested-on)
 
## Main Changes
- All regular expressions were modified so as to detect the most likely Italian chapters headings
- Chapter Headings are included at the beginning of each extracted chapter
- The value of the delta variable for removing chapter headings that are likely to be part of a Table of Contents was increased
- An additional function removes short detected chapters, that are likely to be false positive chapters/spurious text 

## Installation and Testing
```
# Clone the repository
git clone https://github.com/GiuseppeDellaCorte/It-Chapterize.git

# Grab a copy of "I tre Moschettieri - Volume 1 " from Project Gutenberg: 
wget https://www.gutenberg.org/files/60641/60641-0.txt

# Run It-Chapterize on it as it follows:  
/path-to/chapterize /path-to/60641-0.txt
```
It will output a new directory in the current working directory named `60641-0.txt-chapters`, containing files ranging from 01.txt to 16.txt.

## State of the Tool
**It-Chapterize** has been tested on a few set of Italian e-books, which means that the tool does not handle many possible Italian chapter headings.

## Tested on
**It-Chapterize** has been tested successfully on these Italian Gutenberg Project files:

* <a href="http://www.gutenberg.org/files/60641/60641-0.txt">I tre moschettieri, vol. I</a>
* <a href="http://www.gutenberg.org/files/60642/60642-0.txt">I tre moschettieri, vol. II</a>
* <a href="http://www.gutenberg.org/files/60643/60643-0.txt">I tre moschettieri, vol. III</a>
* <a href="http://www.gutenberg.org/cache/epub/28371/pg28371.txt">Le avventure d'Alice nel paese delle meraviglie</a>
* <a href="http://www.gutenberg.org/files/47102/47102-0.txt">L'arte di far debiti</a>
* <a href="http://www.gutenberg.org/files/58415/58415-0.txt">Una sfida al Polo</a>

**It-Chapterize** has also been tested on the Gutenberg Project files that follows this paragraph. It worked relatively well on them, but not perfectly: the output text files include between one and two false positives chapters. In addition, for a few of them, sometimes spurious information are included usually in the first or last detected extracted chapters. Manual correction of false negatives requires around 1/2 minutes per parsed file.  

* <a href="http://www.gutenberg.org/cache/epub/21425/pg21425.txt">Le rive della Bormida</a>
* <a href="http://www.gutenberg.org/files/38338/38338-0.txt">Top</a>
* <a href="http://www.gutenberg.org/files/46914/46914-0.txt">Il libro di Don Chisciotte</a>
* <a href="http://www.gutenberg.org/files/47786/47786-0.txt">Una Donna</a>
* <a href="http://www.gutenberg.org/files/48361/48361-0.txt">In faccia al destino</a>
* <a href="http://www.gutenberg.org/files/48779/48779-0.txt">Novelle umoristiche</a>
* <a href="http://www.gutenberg.org/files/60586/60586-0.txt">Il fantasma di Canterville e il delitto di Lord Savile</a>
* <a href="http://www.gutenberg.org/files/60644/60644-0.txt">I tre moschettieri, vol. IV</a>
* <a href="http://www.gutenberg.org/files/62047/62047-0.txt">La libertà</a>
* <a href="http://www.gutenberg.org/files/63194/63194-0.txt">Ivanhoe; ossia, Il ritorno del Crociato</a>

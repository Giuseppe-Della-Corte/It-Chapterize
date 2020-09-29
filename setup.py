from distutils.core import setup
from sys import version_info as ver

if ver[0] < 3:
    version = str(ver[0]) + '.' + str(ver[1])
    sys.exit("""
    Error: your Python version is %s, but chapterize requires at least
    Python 3. Please upgrade your Python installation, or try using pip3
    instead of pip.""" % version)

setup(
    name = 'itchapterize',
    packages = ['itchapterize'], 
    version = '0.1',
    description = 'A tool for breaking Italian etexts into chapters.',
    author = 'Giuseppe Della Corte',
    author_email = 'giuseppedellacorte95@gmail.com',
    url = 'https://github.com/Giuseppe-Della-Corte/It-Chapterize/', 
    download_url = 'https://github.com/Giuseppe-Della-Corte/It-Chapterize.git',
    install_requires = ['Click'],
    keywords = ['regex', 'regexp', 'regular-expression', 'italian', 'regex-pattern', 'digital-humanities', 'text-processing', 'italian-nlp', 'gutenberg-project'],
    entry_points='''
    [console_scripts]
    itchapterize = itchapterize.itchapterize:cli''',
)

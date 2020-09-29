from distutils.core import setup
from sys import version_info as ver

if ver[0] < 3:
    version = str(ver[0]) + '.' + str(ver[1])
    sys.exit("""
    Error: your Python version is %s, but chapterize requires at least
    Python 3. Please upgrade your Python installation, or try using pip3
    instead of pip.""" % version)

setup(
    name = 'It-Chapterize',
    packages = ['It-Chapterize'], 
    version = '0.0.1',
    description = 'A tool for breaking Italian etexts into chapters.',
    author = 'Giuseppe Della Corte',
    author_email = 'giuseppedellacorte95@gmail.com',
    url = 'https://github.com/Giuseppe-Della-Corte/It-Chapterize/', 
    download_url = 'https://github.com/Giuseppe-Della-Corte/It-Chapterize.git',
    install_requires = ['Click'],
    keywords = ['NLP', 'text', 'chapters', 'Italian],
    entry_points='''
    [console_scripts]
    chapterize = chapterize.chapterize:cli''',
)

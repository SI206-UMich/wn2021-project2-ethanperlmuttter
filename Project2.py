# By Ethan Perlmutter with Chris Hudson
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    with open(filename) as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    books = soup.find_all('a', class_ = "bookTitle")
    bk_list = []
    ac = soup.find_all('span', itemprop = "author")
    authors = []
    for a in ac:
        authors.append(a.find('span', itemprop = "name"))


    name_list  = []
    for book in books:
        bk_list.append(book.text.strip())
    for book in authors:
        name_list.append(book.text.strip())
    return list(zip(bk_list, name_list))
    




def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    link = requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc")
    soup = BeautifulSoup(link.text, 'html.parser')
    
    books = soup.find_all('tr')
    urls = []

    for book in books:
        c = book.find('a')
        complete = c['href']
        url = "https://www.goodreads.com" + str(complete)
        urls.append(url)


    return urls[:10]




def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    link = requests.get(book_url)
    soup = BeautifulSoup(link.text, 'html.parser')
    title = soup.find('h1').text
    author = soup.find('a', class_ = 'authorName').text
    pages = (soup.find('span', itemprop = 'numberOfPages').text).strip()
    pages = pages[:-5]
    return (str(title.strip()), str(author), int(pages))

    
    



def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    f = open(filepath)
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()

    books = soup.find_all('div', class_= 'category clearFix')
    total_list = []
    for book in books:
        e = book.find('a')
        i = book.find('img', class_ = 'category__winnerImage')
        cat = e.find('h4').text
        url = e['href']
        title = i['alt']


        total_list.append((str(cat.strip()),str(title), str(url)))
    return total_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w') as file:
        csv_write = csv.writer(file)
        csv_write.writerow(["Book Title", "Author Name"])
        for book in data:
            csv_write.writerow(book)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    """link  = filepath
    rsp = requests.get(link)
    soup = BeautifulSoup(rsp.content, 'html.parser')
    """
    
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    dc = soup.find('div', id = 'descriptionContainer')

    t = dc.find_all('span')[1].text
    
    regex = r'[A-Z]\w\w+(?: [A-Z]\w*)+'

    NERs = re.findall(regex, t)

    return NERs
    
    
    

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    def setUp(self):
        self.urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        tgtfsr = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(tgtfsr), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(tgtfsr), list)
        # check that each item in the list is a tuple
        for item in tgtfsr:
            self.assertEqual(type(item), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(tgtfsr[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)','J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)

        self.assertEqual(tgtfsr[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(self.urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(self.urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for url in self.urls:
            self.assertEqual(type(url), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in self.urls:
            self.assertEqual(url[0:36], "https://www.goodreads.com/book/show/")

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        bs = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in self.urls:
            bs.append(get_book_summary(url))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(bs), 10)
            # check that each item in the list is a tuple
        for item in bs:
            self.assertEqual(type(item), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(item), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(item[0]), str)
            self.assertEqual(type(item[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(item[2]), int)
            # check that the first book in the search has 337 pages
        self.assertEqual(bs[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        bb = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(len(bb), 20)
        for b in bb:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(b), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(b), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        first = ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')
        self.assertEqual(bb[0], first)
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        last = ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020')
        self.assertEqual(bb[-1], last)


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', 'r') as f:
            csv_lines = f.readlines()


        # check that there are 21 lines in the csv
            self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
            self.assertEqual(csv_lines[0].rstrip(), 'Book Title,Author Name')
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
            self.assertEqual(csv_lines[1].rstrip(), "\"Harry Potter and the Deathly Hallows (Harry Potter, #7)\",J.K. Rowling")
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
            self.assertEqual(csv_lines[-1].rstrip(), "\"Harry Potter: The Prequel (Harry Potter, #0.5)\",J.K. Rowling")


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)




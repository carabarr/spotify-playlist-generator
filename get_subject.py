import requests
import click

# takes a book title and author and constructs the search url based on it
def urlify_title(title, author):
    base = "https://openlibrary.org/search.json?"
    search_title = title.replace(" ", "+").lower()
    url = base + 'title=' + search_title
    if author:
        search_author = author.replace(" ", "+").lower()
        url = url + '&author=' + search_author
    return url

# return subject list of the first search result obtained by searching the book title
# on open library
@click.command()
@click.argument('title')
@click.argument('author', required=False)
def subject_list(title, author):
    url = urlify_title(title, author)
    response = requests.get(url).json()
    search_results = response.get('docs')
    try:
        first_result = search_results[0]
    except:
        print('Nothing matches the search! Check manually on open library.')
        exit()

    print(first_result.get('subject'))

if __name__ == '__main__':
    subject_list()
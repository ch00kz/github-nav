from datetime import datetime
import requests
from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('.'))


def app(environ, start_fn):
    start_fn('200 OK', [('Content-Type', 'text/html')])
    return router(environ)


def router(environ):
    """ Simple router method, with a list of routes and view functions
    """
    routes = [
        ('/', home),
        ('/navigator', navigator),
    ]

    path = environ.get('PATH_INFO', '/')
    for route, view in routes:
        if route == path:
            return view(environ)
    else:
        return home(environ)


# VIEW functions
def home(environ):
    """ Handles view logic for / route.
    """
    template = ENV.get_template('cover.txt')
    return create_response(template.render({}))


def navigator(environ):
    """ Handles logic for /navigator route.
    """
    query_str = environ.get('QUERY_STRING')
    # handling multiple query params
    queries = query_str.split('&')
    for query in queries:
        # getting the search_term
        if query.startswith('search_term='):
            search_term = query.split('search_term=')[1]
            break
    else:
        search_term = None

    if search_term is None:
        return home(environ)

    repository_data = get_repositories(search_term)
    repositories = build_repository_collection(repository_data)

    template = ENV.get_template('template.html')
    context = {'repositories': repositories, 'search_term': search_term}
    return create_response(template.render(context))


# HELPER functions
def create_response(response):
    """ returns response as list containing bytes """
    return [bytes(response, 'utf-8')]


def get_repositories(search_term):
    """ fetches and returns top 5 repositories matching
        supplied search_term
    """
    base_url = 'https://api.github.com/search/repositories'
    url = '{}?q={}&page=1&per_page=5'.format(base_url, search_term)
    r = requests.get(url)
    repositories = r.json().get('items', [])
    return repositories


def build_repository_collection(repos):
    """ build and return repository collection using response from 'get_repositories'
        resulting collection to be used in context when rendering template.
    """
    collection = []
    for repo in repos:
        # get latest commit
        commit_url = repo.get('commits_url').replace('{/sha}', '')
        r_commit = requests.get('{}?page=1&per_page=1'.format(commit_url))
        commit = r_commit.json()[0]
        # building and appending repo dict to collection
        created = datetime.strptime(repo.get('created_at', ''), "%Y-%m-%dT%H:%M:%SZ")
        collection.append({
            'name': repo.get('name', ''),
            'created': created.strftime('%A %b %d, %Y at %H:%M GMT'),  # format date
            'owner': {
                'login': repo.get('owner', {}).get('login', ''),
                'url': repo.get('owner', {}).get('html_url', ''),
                'avatar': repo.get('owner', {}).get('avatar_url', '')
            },
            'last_commit': {
                'sha': commit.get('sha', ''),
                'message': commit.get('commit', {}).get('message', ''),
                'author': commit.get('commit', {}).get('author', {}).get('name', '')
            }
        })
    return collection

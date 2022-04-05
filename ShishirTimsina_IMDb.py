#!/usr/bin/python3
import time
import sys

# Multi-line string variable for the main program menu.
MAIN_MENU = (
'''======================================================================
\tEnter 1 to Search for a Movie Title and See its Cast
\tEnter 2 to Search for an Actor/Actress and See their Movies
\tEnter anything else to exit.
======================================================================
Please type an option from the list above:
>>> ''')

# Filename for the IMDB database
IMDB_FILE = 'imdb_data.tsv'

def main():
    """Main program execution function.

    This is already written for you and should not be be modified.
    """
    # Two dict objects will serve as efficient data structures for look ups
    titles_index = {}
    actors_index = {}
    start = time.time()
    rows = build_indexes(titles_index, actors_index)
    print('Indexed {:,} rows from {} in {:,.2f}s'.format(
        rows, IMDB_FILE, time.time() - start))
    memory_used = sys.getsizeof(titles_index) + sys.getsizeof(actors_index)
    print('Using {:,.2f}MB of memory'.format(memory_used / 2 ** 20))

    # Stay in the loop until an invalid action is received.
    while True:
        action = input(MAIN_MENU)
        if action == '1':
            search_for_title(titles_index)
        elif action == '2':
            movies_for_actor(actors_index)
        else:
            print('"{}" is not a valid action. Goodbye!'.format(action))
            break

def build_indexes(titles_index, actors_index):
    """Processes IMDB_FILE and populates two dict data structures."""
    big_file = open(IMDB_FILE, 'r')
  
    r = 0
    for line in big_file:
        data = line.strip().split('\t')
        titles = data[1]
        names = '{} {}'.format(data[2], data[3])
        year = int(data[0])
        gender = data[4]
        character = data[5]
        title_final = titles.lower()
        names_final = names.lower()
        if titles_index.get(title_final) is not None:
            cas = titles_index[title_final][2]
            new = [{'names':names}, {'gender':gender}, {'character':character}]
            cas.append(new)
            titles_index[title_final][2] = cas
        else:
            titles_index[title_final] = [{'year':year},{'titles':titles},[[{'names':names}, {'gender':gender}, {'character':character}]]]


        if actors_index.get(names_final) is not None:
            movies_info = actors_index[names_final]
            new_movies = [{'year':year}, {'titles': titles}, {'character': character}]
            movies_info.append(new_movies)
            actors_index[names_final] = movies_info
        else:
            actors_index[names_final] = [[{'year':year}, {'titles': titles}, {'character': character}]]
        r += 1
    return r

    
    


def sort_by_name(data):
    """Helper function to be passed to the sort() method for titles_index values.

    Args:
        data: dict object
    Return:
        data['name'] Value
    """
    return data['name']


def sort_by_year(data):
    """Helper function to be passed to the sort() method for actors_index values.

    Args:
        data: dict object
    Return:
        data['year'] Value
    """
    return data['year']


def search_for_title(titles_index):
    """Lookup and print the actors/actresses from a movie by title.

    Args:
        titles_index: Dict data structure keyed by title
    """
    search_title = input('What movie title would you like to search ').lower()
    val = titles_index.get(search_title)
    if val is not None:
        year = val[0]["year"]
        title = val[1]["titles"]
        print(' {} was released in {}' .format(title, year))
        print(' Cast of {} is as follows: ' .format(title))
        for cast in val[2]:
            character = cast[2]['character']
            names = cast[0]['names']
            print('{} played {}'.format(names, character))
                          
    else:
        print('Sorry, I could not find {}' .format(search_title))
    


def movies_for_actor(actors_index):
    """Lookup and print the movies that an actor/actress starred in.

    Args:
        actors_index: Dict data structure keyed by year
    """
    search_actor = input('Which actor would you like to search ').lower()
    val = actors_index.get(search_actor)
    if val is not None:
        for cast in val:
            character = cast[2]['character']
            title = cast[1]['titles']
            year = cast[0]['year']
            print('Your actor played {} in the movie {} in {}' .format(character, title, year))
    else:
        print('Sorry, I could not find {}' .format(search_actor))
  


main()


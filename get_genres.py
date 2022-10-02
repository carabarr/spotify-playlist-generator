import requests
import click
import spacy


music_list = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 
    'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 
    'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 
    'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 
    'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 
    'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 
    'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies',
    'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 
    'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip',
    'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 
    'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 
    'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']

# takes a book title and author and constructs the search url based on it
def urlify_title(title, author):
    base = "https://openlibrary.org/search.json?"
    search_title = title.replace(" ", "+").lower()
    url = base + 'title=' + search_title
    if author != "n/a":
        search_author = author.replace(" ", "+").lower()
        url = url + '&author=' + search_author
    return url



def parse(list_in):
    input_list = list_in

    #input_list = ["Greek Mythology", "Zeus (Greek deity)", "Juvenile fiction", "Fathers and sons", "Hades (Greek deity)", "Poseidon (Greek deity)", "Camps", "Friendship", "Fantasy fiction", "Fantasy", "Young Adult Fiction", "New York Times bestseller", "nyt:series_books=2007-07-21", "Mythology, Greek", "Juvenile fiction..", "Identity (Philosophical concept)", "Identity", "Adaptations", "Greek Gods", "Comic books, strips", "Cartoons and comics", "Children's fiction", "Camps, fiction", "Friendship, fiction", "Fathers and sons, fiction", "Gods, fiction", "Large type books", "mirror", "pdf.yt", "Graphic novels", "Action & Adventure", "Fantasy & Magic", "Legends, Myths, Fables", "Voyages and travels", "Father-son relationship", "Gods and goddesses", "Literature and fiction, juvenile", "Children's Books -- Literature -- Action & Adventure", "Children's Books -- Literature -- Fairy Tales, Folk Tales & Myths -- Greek & Roman", "Children's Books -- Literature -- Popular Culture", "Children's Books -- Literature -- Science Fiction, Fantasy, Mystery & Horror -- Science Fiction, Fantasy, & Magic", "Literature & Fiction -- World Literature -- Mythology", "Child and youth fiction", "Science fiction, fantasy, horror", "New York Times reviewed", "Mythologie grecque", "Romans, nouvelles, etc. pour la jeunesse", "Colonies de vacances", "Amitié", "Pères et fils"]
    new_list = []
    alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    td = ['and', 'fiction', 'young', 'adult', 'literature', 'juvenile', 'classic', 'classics', 'children', "children's", 'books', 'book', 'science', 'york', 'times', 'new', 'of', 'the', 'character']


    for i in input_list:
        if i.startswith('pdf') or i.startswith('nyt'):
            input_list.remove(i)
        if ' ' in i:
            temp = i.split(' ')
            for k in temp:
                new_list.append(k)
        else:
            new_list.append(i)
                    
    for j in range(len(new_list)):
        if new_list[j][0] == '(':
            new_list[j] = new_list[j].replace('(', '')
        if new_list[j][-1] == ')':
            new_list[j] = new_list[j].replace(')', '')
        new_list[j] = new_list[j].lower()
        
        
    new_list2 = []
    for o in new_list:
        for m in o:
            temp = 0
            if m not in alph:
                temp += 1
        if o in td:
            temp += 1
        if temp == 0:
            new_list2.append(o)

    freqDict = {}

    for n in range (len(new_list2)):
        if new_list2[n].lower() in freqDict.keys():
            freqDict[new_list2[n].lower()] += 1
        else:
            freqDict[new_list2[n].lower()] = 1
            
    final_list = []

    count = 1
    freqDictC = freqDict.copy()

    while (len(final_list) < 5):
        final_list.clear()
        for g in freqDictC.keys():
            if freqDict.get(g) > max(freqDict.values()) - count:
                final_list.append(g)
        count += 1
            
    if len(final_list) == 0:
        for b in range(5):
            final_list.append(freqDict[b])

    return final_list
        

def genre_correlation(book_list, music_list):
    SimilarFreq = {}
    SimilarVal = {}

    # load the language model
    nlp = spacy.load('en_core_web_md')  

    for i in book_list:
        bookXmus = {}
        token1 = nlp(i)[0]
        for j in music_list:
            token2 = nlp(j)[0]
            bookXmus[j] = token1.similarity(token2)
        value = [k for k, v in bookXmus.items() if v == max(bookXmus.values())]
        SimilarVal[value[0]] = max(bookXmus.values()) #value is a music genre

        if value[0] in SimilarFreq.keys():
            SimilarFreq[value[0]] += 1
        else:
            SimilarFreq[value[0]] = 1

    final_mus_list = []

    if sum(bookXmus.values())/len(bookXmus) == 1:
        for t in range(3):
            valueM = [k for k, v in SimilarVal.items() if v == max(SimilarVal.values())]
            final_mus_list.append(valueM[0])
            del SimilarVal[valueM[0]]
    else:
        for t in range(3):
            valueM = [k for k, v in SimilarFreq.items() if v == max(SimilarFreq.values())]
            final_mus_list.append(valueM[0])
            del SimilarFreq[valueM[0]]

    return final_mus_list

# return subject list of the first search result obtained by searching the book title
# on open library
def subject_list(title, author):
    url = urlify_title(title, author)
    response = requests.get(url).json()
    search_results = response.get('docs')
    # print("printing search results")
    # print(search_results)
    try:
        first_result = search_results[0]
    except:
        print('Nothing matches the search! Check manually on open library.')
        exit()
    genres = first_result.get('subject')
    print("going into parse")
    final = parse(genres)
    return final

def music_genres(title):
    return genre_correlation(subject_list(title, "n/a"), music_list)

def book_keywords(title):
    return subject_list(title, "n/a")

if __name__ == "__main__":
    title = input("Enter book title: ")
    author = input("Enter author: ")
    booklist = subject_list(title, author)
    print(booklist)
    musiclist = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 
    'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 
    'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 
    'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 
    'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 
    'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 
    'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies',
    'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 
    'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip',
    'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 
    'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 
    'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
    print(genre_correlation(booklist, musiclist))

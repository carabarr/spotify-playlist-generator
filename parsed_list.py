input_list = ["Greek Mythology", "Zeus (Greek deity)", "Juvenile fiction", "Fathers and sons", "Hades (Greek deity)", "Poseidon (Greek deity)", "Camps", "Friendship", "Fantasy fiction", "Fantasy", "Young Adult Fiction", "New York Times bestseller", "nyt:series_books=2007-07-21", "Mythology, Greek", "Juvenile fiction..", "Identity (Philosophical concept)", "Identity", "Adaptations", "Greek Gods", "Comic books, strips", "Cartoons and comics", "Children's fiction", "Camps, fiction", "Friendship, fiction", "Fathers and sons, fiction", "Gods, fiction", "Large type books", "mirror", "pdf.yt", "Graphic novels", "Action & Adventure", "Fantasy & Magic", "Legends, Myths, Fables", "Voyages and travels", "Father-son relationship", "Gods and goddesses", "Literature and fiction, juvenile", "Children's Books -- Literature -- Action & Adventure", "Children's Books -- Literature -- Fairy Tales, Folk Tales & Myths -- Greek & Roman", "Children's Books -- Literature -- Popular Culture", "Children's Books -- Literature -- Science Fiction, Fantasy, Mystery & Horror -- Science Fiction, Fantasy, & Magic", "Literature & Fiction -- World Literature -- Mythology", "Child and youth fiction", "Science fiction, fantasy, horror", "New York Times reviewed", "Mythologie grecque", "Romans, nouvelles, etc. pour la jeunesse", "Colonies de vacances", "Amitié", "Pères et fils"]
new_list = []
alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
td = ['and', 'fiction', 'young', 'adult', 'literature', 'juvenile', 'classic', 'classics', 'children', "children's", 'books', 'book', 'science', 'york', 'times', 'new']


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

    
print(final_list)
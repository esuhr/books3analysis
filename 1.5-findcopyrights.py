import spacy
from tqdm import tqdm
import pickle

def find_entities(item):
    copyrighttags = {'COPYRIGHT', 'Copyright', 'copyright', '©'}

    entitydict = {
        'title': '',
        'copyright': [],
        'copyrightYear': '',
        'filepath': '',
    }

    fp, texts = item

    fp_stripped = fp.replace('.epub.txt', '').replace('./Bibliotik/', '').split('/', )[1]
    entitydict['title'] = fp_stripped

    if isinstance(texts, str):
        texts = [texts]

    for text in texts:
        textdoc = nlp(text)
        text = text.replace('\n', ' ')
        for ent in textdoc.ents:
            if ent.label_ in {'PERSON', 'ORG'} and any(tag in text[ent.start_char-12:ent.start_char] for tag in copyrighttags):
                entitydict['copyright'].append(ent.text)
                entitydict['copyright'] = list(set(entitydict['copyright']))
            elif ent.label_ == 'DATE' and any(tag in text[ent.start_char-12:ent.start_char] for tag in copyrighttags):
                entitydict['copyrightYear'] = ent.text

    entitydict['filepath'] = fp
    return entitydict

def main():
    for item in tqdm(copyrightextracts):
        if not item:
            continue
        else:
            entitylist = find_entities(item)
            with open('entitylist.txt', 'a') as f:
                f.write(str(entitylist) + '\n')

if __name__ == '__main__':
    nlp = spacy.load('en_core_web_trf')
    print('----Loaded spacy model')
    copyrightextracts = pickle.load(open('copyrightextracts.pkl', 'rb'))
    print('----Loaded copyright extracts')
    main()
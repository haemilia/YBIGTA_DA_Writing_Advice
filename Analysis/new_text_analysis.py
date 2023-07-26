import json
import re
import pandas as pd
from collections import Counter
from konlpy.tag import Kkma


def tokenize(text: str) -> dict:
    kkma = Kkma()
    tokens = kkma.morphs(text)
    pos_tokens = kkma.pos(text)
    return {'text': text, 'tokens': tokens, 'pos': pos_tokens}

def get_string_length(text: str) -> int:
    return(len(text))
def get_num_tokens(tokens: list) -> int:
    return(len(tokens))
def find_sent_id(tokens: list) -> list:
    ids = []
    for i, tok in enumerate(tokens):
        found = re.findall('[.?!]+', tok)
        if(bool(found)):
            ids.append(i)
    return ids
def split_sentence(sent_ids: list, tokens: list)-> list:  
    sentences = []
    start = 0
    for i in sent_ids:
        sentences.append(tokens[start:i+1])
        start = i+1
    return sentences
def split_pos_sentence(sent_ids: list, pos: list)-> list:  
    sentences = []
    start = 0
    for i in sent_ids:
        sent_both = pos[start:i+1] #get the sentence
        sent_tag = list(map(lambda tag: tag[1], sent_both))#get only the pos tags
        sentences.append(sent_tag)#append
        start = i+1
    return sentences
def get_num_sentences(tokens:list, pos:list):
    sent_ids = find_sent_id(tokens)
    sentences = split_sentence(sent_ids, tokens)
    pos_sentences = split_pos_sentence(sent_ids, pos)
    return len(sent_ids), sentences, pos_sentences
def get_num_token_sentences(sentences: list) -> list:
    num_tokens = []
    for sentence in sentences:
        num_tokens.append(len(sentence))
    return num_tokens

def simple_analysis(data):
    
    text = data['text']
    tokens = data['tokens']
    pos = data['pos']

    all_analysis = {}

    all_analysis['string_length'] = get_string_length(text)
    all_analysis['num_tokens'] = get_num_tokens(tokens)
    num_sentences, sentences, pos_sentences = get_num_sentences(tokens, pos)
    num_token_sentences = get_num_token_sentences(sentences)
    all_analysis['num_sentences'] = num_sentences
    all_analysis['num_token_sentences'] = num_token_sentences
    data['sentence_tokens'] = sentences
    data['sentence_pos'] = pos_sentences
    
    return data, all_analysis
def get_rel_freq(freq: dict):
    freq = pd.Series(freq, dtype = "float64")
    tot = freq.sum()
    return (freq/tot).to_dict()
def get_pos_freq(article: list[list]) -> dict:
    pos_freq = {}
    s_freq = []
    s_rel_freq = []
    article_freq = dict()

    for sentence in article:
        sentence_freq = dict(Counter(sentence))
        s_freq.append(sentence_freq)
        s_rel_freq.append(get_rel_freq(sentence_freq))
        for (key, freq) in sentence_freq.items():
            if key in article_freq.keys():
                article_freq[key] = article_freq[key] + freq
            else:
                article_freq[key] = freq

    pos_freq['s_freq'] = s_freq
    pos_freq['s_rel_freq'] = s_rel_freq
    pos_freq['a_freq'] = article_freq
    pos_freq['a_rel_freq'] = get_rel_freq(article_freq)
        
    return pos_freq 

def analysis(data):
    data, all_analysis = simple_analysis(data)
    all_analysis['pos_freq'] = get_pos_freq(data['sentence_pos'])
    return data, all_analysis



def main():
    new_input = input()
    with open(new_input) as json_file:
        new_input = json.load(json_file)
    data = new_input['text']
    category = new_input['category']

    data = tokenize(data)
    data, new_ananlysis = analysis(data)

if __name__ == "__main__":
    main()    
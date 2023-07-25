import json
import re
from collections import Counter


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
    return (len(sent_ids), sentences, pos_sentences)
def simple_analysis(data):
    data['sentence_tokens'] = []
    data['sentence_pos'] = []
    all_analysis = {'string_length':[], 'num_tokens':[], 'num_sentences':[]}
    for i in range(len(data['text'])):
        text = data['text'][i]
        tokens = data['tokens'][i]
        pos = data['pos'][i]
        all_analysis['string_length'].append(get_string_length(text))
        all_analysis['num_tokens'].append(get_num_tokens(tokens))
        num_sentences, sentences, pos_sentences = get_num_sentences(tokens, pos)
        all_analysis['num_sentences'].append(num_sentences)
        data['sentence_tokens'].append(sentences)
        data['sentence_pos'].append(pos_sentences)
    return data, all_analysis
def get_pos_freq(articles: list[list]) -> dict:
    pos_freq = {}
    pos_freq['s_freq'] = []
    pos_freq['a_freq'] = []
    for i in range(len(articles)):
        s_freq = []
        article_freq = dict()
        for sentence in articles[i]:
            sentence_freq = dict(Counter(sentence))
            s_freq.append(sentence_freq)
            for (key, freq) in sentence_freq.items():
                if key in article_freq.keys():
                    article_freq[key] = article_freq[key] + freq
                else:
                    article_freq[key] = freq
        pos_freq['s_freq'].append(s_freq)
        pos_freq['a_freq'].append(article_freq)
        
    return pos_freq       

def main():
    path = input("Please enter the path to tokenized json files")  
    with open(path) as json_file:
        data = json.load(json_file)

    data, all_analysis = simple_analysis(data)
    all_analysis['pos_freq'] = get_pos_freq(data['sentence_pos'])

    path = input("Please enter the path to save the analysis result json file")
    with open(path, "w") as outfile:
        json.dump(all_analysis, outfile)


    
    
    
if __name__ == "__main__":
    main()
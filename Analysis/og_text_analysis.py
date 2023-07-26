import json
import re
import pandas as pd
import numpy as np
from collections import Counter
from tqdm import tqdm


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
    if bool(sent_ids):
        start = 0
        for i in sent_ids:
            sentences.append(tokens[start:i+1])
            start = i+1
    else:
        sentences.append(tokens)
    return sentences
def split_pos_sentence(sent_ids: list, pos: list)-> list:  
    sentences = []
    if bool(sent_ids):
        start = 0
        for i in sent_ids:
            sent_both = pos[start:i+1] #get the sentence
            sent_tag = list(map(lambda tag: tag[1], sent_both))#get only the pos tags
            sentences.append(sent_tag)#append
            start = i+1
    else:
        sent_both = pos
        sent_tag = list(map(lambda tag: tag[1], sent_both))#get only the pos tags
        sentences.append(sent_tag)
    return sentences
def get_num_sentences(tokens:list, pos:list):
    sent_ids = find_sent_id(tokens)
    sentences = split_sentence(sent_ids, tokens)
    pos_sentences = split_pos_sentence(sent_ids, pos)
    return (len(sent_ids), sentences, pos_sentences)
def get_num_token_sentences(sentences):
    num_tokens = []
    for sentence in sentences:
        num_tokens.append(len(sentence))
    return num_tokens
def simple_analysis(data):
    data['sentence_tokens'] = []
    data['sentence_pos'] = []
    all_analysis = {'string_length':[], 'num_tokens':[], 'num_sentences':[], 'num_token_sentences':[],}
    for i in tqdm(range(len(data['text']))):
        text = data['text'][i]
        tokens = data['tokens'][i]
        pos = data['pos'][i]
        all_analysis['string_length'].append(get_string_length(text))
        all_analysis['num_tokens'].append(get_num_tokens(tokens))
        num_sentences, sentences, pos_sentences = get_num_sentences(tokens, pos)
        num_token_sentences = get_num_token_sentences(sentences)
        all_analysis['num_sentences'].append(num_sentences)
        all_analysis['num_token_sentences'].append(num_token_sentences)
        data['sentence_tokens'].append(sentences)
        data['sentence_pos'].append(pos_sentences)
    
    return data, all_analysis
def get_rel_freq(freq: dict):
    freq = pd.Series(freq, dtype = "float64")
    tot = freq.sum()
    return (freq/tot).to_dict()
def get_pos_freq(articles: list[list]) -> dict:
    pos_freq = {}
    pos_freq['s_freq'] = []
    pos_freq['a_freq'] = []
    pos_freq['s_rel_freq'] = []
    pos_freq['a_rel_freq'] = []
    for i in tqdm(range(len(articles))):
        s_freq = []
        s_rel_freq = []
        article_freq = dict()
        for sentence in articles[i]:
            sentence_freq = dict(Counter(sentence))
            s_freq.append(sentence_freq)
            s_rel_freq.append(get_rel_freq(sentence_freq))
            for (key, freq) in sentence_freq.items():
                if key in article_freq.keys():
                    article_freq[key] = article_freq[key] + freq
                else:
                    article_freq[key] = freq
        pos_freq['s_freq'].append(s_freq)
        pos_freq['s_rel_freq'].append(s_rel_freq)
        pos_freq['a_freq'].append(article_freq)
        pos_freq['a_rel_freq'].append(get_rel_freq(article_freq))
        
    return pos_freq

def calRelPosition(sentence_pos, num_token_sentences):

    for i, sentence in enumerate(sentence_pos):
        pos = np.array(sentence)
        result = {}
        for tag in set(pos):
            indices = np.where(pos == tag)
            result[tag] = (indices/num_token_sentences[i]).tolist()
           
    return result

def get_more_features(data, all_analysis):
    all_analysis['token_variety'] = []
    all_analysis['rel_position'] = []
    for i in tqdm(range(len(data['pos']))):
        num_token_sentences = np.array(all_analysis['num_token_sentences'][i])
        num_token_type = np.array(list(map(len, all_analysis['pos_freq']['s_freq'][i])))
        token_variety = (num_token_type / num_token_sentences).tolist()
        all_analysis['token_variety'].append(token_variety)
        sentence_pos = data['sentence_pos'][i]
        rel_position = calRelPosition(sentence_pos, num_token_sentences)
        all_analysis['rel_position'].append(rel_position)
    return all_analysis


def analysis(data):
    data, all_analysis = simple_analysis(data)
    all_analysis['pos_freq'] = get_pos_freq(data['sentence_pos'])
    all_analysis = get_more_features(data, all_analysis)
    return data, all_analysis
    
    
     

def main():
    ### 사용 전 해야 할 것 ###
    """
    - category 변수에 원하는 글 종류 넣기
    - data_path와 out_path 내 파일 경로 변경하기
    - 그 외에는 잘 돌아가도록 두면 됩니다
    """
    
    category = input("Please write the category name: ")
    data_path = {
        "articles":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/tokenized_data/articles_ytn_tokenized.json",
        "abstract":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/tokenized_data/abstract_tokenized.json",
        "essay":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/tokenized_data/essay_tokenized.json",
        "literature":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/tokenized_data/literature_tokenized.json",
        }

    with open(data_path[category]) as json_file:
        data = json.load(json_file)

    data, all_analysis = analysis(data)

    out_path = {
    "articles":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/article/articles_ytn_analysis.json",
    "abstract":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/abstract/abstract_analysis.json",
    "essay":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/essay/essay_analysis.json",
    "literature":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/literature/literature_analysis.json",
    }
    data_out_path = {
        "articles":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/article/articles_data.json",
        "abstract":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/abstract/abstract_data.json",
        "essay":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/essay/essay_data.json",
        "literature":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/literature/literature_data.json",
    }
    with open(out_path[category], "w") as outfile:
        json.dump(all_analysis, outfile)
    with open(data_out_path[category], "w") as outfile:
        json.dump(data, outfile)


    
    
    
if __name__ == "__main__":
    main()
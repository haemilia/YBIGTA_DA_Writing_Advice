import json
import re
import pandas as pd
import numpy as np
from collections import Counter
from konlpy.tag import Kkma
import matplotlib.pyplot as plt

re_dist_path = {
    "articles":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/article/articles_re_dist.json",
    "abstract":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/abstract/abstract_re_dist.json",
    "essay":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/essay/essay_re_dist.json",
    "literature":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/literature/literature_re_dist.json",
}
kkma_groups = {
    'N': [{'NNG', 'NNP', 'NNB', 'NNM'}, "체언"],
    'V': [{'VV', 'VA', 'VXV', 'VXA', 'VCP', 'VCN'}, '용언'],
    'VV': [{'VV'}, '동사'],
    'VA': [{'VA'},'형용사'],
    'VX': [{'VXV', 'VXA'}, '보조 용언'],
    'VC': [{'VCP', 'VCN'}, '긍정/부정 지정사'],
    'MD': [{'MDT', 'MDN'}, '관형사'],
    'MA': [{'MAG', 'MAC'}, '부사'],
    'IC': [{'IC'}, '감탄사'],
    'J': [{'JKS', 'JKC', 'JKG', 'JKO', 'JKM', 'JKI', 'JKQ', 'JX', 'JC'}, '조사'],
    'EP': [{'EPH', 'EPT', 'EPP'}, '선어말 어미'],
    'EFN': [{'EFN'}, '평서형 종결 어미'],
    'EFQ': [{'EFQ'}, '의문형 종결 어미'],
    'EFO': [{'EFO'}, '명령형 종결 어미'],
    'EFA': [{'EFA'}, '청유형 종결 어미'],
    'EFI': [{'EFI'}, '감탄형 종결 어미'],
    'EFR': [{'EFR'}, '존칭형 종결 어미'],
    'EC': [{'ECE', 'ECD', 'ECS'}, '연결 어미'],
    'ET': [{'ETN', 'ETD'}, '전성 어미'],
    'X': [{'XPN', 'XPV', 'XSN', 'XSV', 'XSA', 'XR'}, '접두/접미사, 어근'],
    'SF': [{'SF'}, '마침표, 물음표, 느낌표'],
    'SP': [{'SP'}, '쉼표, 가운뎃점, 콜론, 빗금'],
    'SS': [{'SS'}, '따옴표, 괄호표, 줄표'],
    'SE': [{'SE'}, '줄임표'],
    'SO': [{'SO'}, '붙임표'],
    'SW': [{'SW'}, '기타 기호'],
    'U': [{'UN', 'UV', 'UE'}, '분석 불능'],
    'OL': [{'OL'}, '외국어'],
    'OH': [{'OH'}, '한자'],
    'ON': [{'ON'}, '숫자'],
}
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
def calRelPosition(sentence_pos, num_token_sentences):
    for i, sentence in enumerate(sentence_pos):
        pos = np.array(sentence)
        result = {}
        for tag in set(pos):
            indices = np.where(pos == tag)[0][0]
            result[tag] = indices/num_token_sentences[i]       
    return result
def get_more_features(data, all_analysis):
    
    num_token_sentences = np.array(all_analysis['num_token_sentences'])
    num_token_type = len(all_analysis['pos_freq']['s_freq'])
    token_variety = (num_token_type / num_token_sentences)
    all_analysis['token_variety'] = token_variety
    sentence_pos = data['sentence_pos']
    rel_position = calRelPosition(sentence_pos, num_token_sentences)
    all_analysis['rel_position'] = rel_position
    return all_analysis

def analysis(data):
    data, all_analysis = simple_analysis(data)
    all_analysis['pos_freq'] = get_pos_freq(data['sentence_pos'])
    all_analysis = get_more_features(data, all_analysis)
    return data, all_analysis

def list_flatten(lst):
    result = []
    for el in lst:
        result.extend(el)
    return result
def dict_flatten(dct):
    result = {}
    for k, v in dct.items():
            if k in result.keys():
                if isinstance(result[k], list):
                    result[k].append(v)
                else:
                    result[k] = [result[k], v]
            else:
                result[k] = v
    return result
def list_of_dict(lst):
    result = {}
    for dct in lst:
        for k, v in dct.items():
            if k in result.keys():
                if isinstance(result[k], list):
                    result[k].append(v)
                else:
                    result[k] = [result[k], v]
            else:
                result[k] = v
    return result
def mean_of_dict(dct):
    for k,v in dct.items():
        dct[k] = np.mean(v)
    return dct
def check_key(key,  value, target_dct):
    if key in target_dct.keys():
        if isinstance(target_dct[key], list) and isinstance(value, list):
            target_dct[key].extend(value)
        elif isinstance(target_dct[key], list) and not isinstance(value, list):
            target_dct[key].append(value)
        else:
            target_dct = [target_dct[key], value]
    else:
        target_dct[key] = value
            
def pos_group(dct, kkma_groups):
    result = {}
    for k, v in dct.items():
        for kk, vv in kkma_groups.items():
            if k in vv[0]:
                check_key(kk, v, result)
    return result
def find_percentage(new_input: int, distribution):
    distribution = np.array(distribution)
    under = len(distribution[distribution < new_input])
    return (under / len(distribution)) * 100
def draw_graph(distribution, variable, destination_path, new_input = 0,):
    fig, ax = plt.subplots()
    fig.set_facecolor('white')
    ax.hist(distribution, bins = 100, color = '#cdb79e', density = True)
    ax.axvline(new_input, color = '#000080')
    ax.set_xlabel(variable)
    fig.savefig()


def main():
    new_input = input()
    with open(new_input) as json_file:
        new_input = json.load(json_file)
    data = new_input['text']
    category = new_input['category']

    data = tokenize(data)
    data, new_analysis = analysis(data)
    main_var = {
    "token_variety": np.mean(new_analysis['token_variety']),
    "rel_position": pos_group(np.mean(new_analysis['token_variety'])),
    "num_token_sentences": np.mean(new_analysis['num_token_sentences']),
    "s_rel_freq": pos_group(mean_of_dict(list_of_dict(new_analysis['pos_freq']['s_rel_freq']))),
    "a_rel_freq": pos_group(new_analysis['pos_freq']['a_rel_freq']),
    }
    with open(re_dist_path[category]) as json_file:
        og_dist = json.load(json_file)

    main_path = ""
    path1 = f"{main_path}/pic1.png"
    path2 = f"{main_path}/pic2.png"
    path3 = f"{main_path}/pic3.png"
    path4 = f"{main_path}/pic4.png"
    path5 = f"{main_path}/pic5.png"
    path6 = f"{main_path}/pic6.png"
    plot_vars = {
    "efr_a_rel_freq": [og_dist['a_rel_freq']['EFR'], "글 전체에서 사용한 존칭형 종결어미의 상대적 빈도", path1, main_var['a_rel_freq']['EFR']],
    "ec_s_rel_freq": [og_dist['s_rel_freq']['EC'], "문장 내 사용한 연결어미의 상대적 빈도", path2, main_var['s_rel_freq']['EC']],
    "token_variety": [og_dist['token_variety'], "문장 내 사용한 품사의 다양성", path3, main_var["token_variety"]],
    "ma_s_rel_freq": [og_dist['s_rel_freq']['MA'], "문장 내 사용한 부사의 상대적 빈도", path4, main_var['s_rel_freq']['MA']],
    "va_s_rel_freq": [og_dist['s_rel_freq']['VA'], "문장 내 사용한 형용사의 상대적 빈도", path5, main_var['s_rel_freq']['VA']],
    "efn_a_rel_freq": [og_dist['a_rel_freq']['EFN'], "글 전체에서 사용한 평서형 종결어미의 상대적 빈도", path6, main_var['a_rel_freq']['EFN']],
    }
    for k, v in plot_vars.items():
        draw_graph(v[0], v[1], v[2], v[3])
        print(f"{find_percentage(v[3], v[0]):.2f}%")

    

if __name__ == "__main__":
    main()    
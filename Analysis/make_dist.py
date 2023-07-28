import json
from tqdm import tqdm

analysis_path = {
    "articles":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/article/articles_ytn_analysis.json",
    "abstract":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/abstract/abstract_analysis.json",
    "essay":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/essay/essay_analysis.json",
    "literature":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/literature/literature_analysis.json",
    }
data_path = {
    "articles":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/article/articles_data.json",
    "abstract":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/abstract/abstract_data.json",
    "essay":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/essay/essay_data.json",
    "literature":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/literature/literature_data.json",
}
dist_path = {
    "articles":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/article/articles_dist.json",
    "abstract":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/abstract/abstract_dist.json",
    "essay":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/essay/essay_dist.json",
    "literature":"C:/Users/lhi30/Haein/2023/YBIGTA/2023-2/DA/Writing_Advice/analyzed_data/literature/literature_dist.json",
}
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


def list_extend(lst):
    result = []
    for el in tqdm(lst):
        result.extend(el)
    return result
def rel_pos_extend(dct):
    for k, v in tqdm(dct.items()):
        dct[k] = list_extend(v)
    return dct
def dict_extend(lst):
    result = {}
    for dct in tqdm(lst):
        for k, v in dct.items():
            if k in result.keys():
                result[k].extend(v)
            else: 
                result[k] = v

    return result    
def freq_extend(lst):
    result = {}
    for dct in tqdm(lst):
        for k, v in dct.items():
            if k in result.keys():
                if isinstance(result[k], list):
                    result[k].append(v)
                else:
                    result[k] = [result[k], v]
            else:
                result[k] = v
    return result

def check_key(key, value, target_dct):
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
    for k, v in tqdm(dct.items()):
        for kk, vv in kkma_groups.items():
            if k in vv[0]:
                check_key(kk, v, result)
    return result

def main():
    category = input("Please enter the text category: ")
    with open(analysis_path[category]) as json_file:
            analysis = json.load(json_file)
    with open(data_path[category]) as json_file:
            data = json.load(json_file)

    flat_token_variety = list_extend(analysis['token_variety'])
    flat_rel_position = rel_pos_extend(dict_extend(analysis['rel_position']))
    flat_num_token_sentences = list_extend(analysis['num_token_sentences'])
    flat_s_rel_freq = freq_extend(list_extend(analysis['pos_freq']['s_rel_freq']))
    flat_a_rel_freq = freq_extend(analysis['pos_freq']['a_rel_freq'])

    distributions = {
        "token_variety": flat_token_variety,
        "rel_position": flat_rel_position,
        "num_token_sentences": flat_num_token_sentences,
        "s_rel_freq": flat_s_rel_freq,
        "a_rel_freq": flat_a_rel_freq,
        }
    flat_a_regroup = pos_group(flat_a_rel_freq, kkma_groups)
    flat_s_regroup = pos_group(flat_s_rel_freq, kkma_groups)
    flat_position_regroup = pos_group(flat_rel_position, kkma_groups)
    regrouped_distributions = {
        "token_variety": flat_token_variety,
        "rel_position": flat_position_regroup,
        "num_token_sentences": flat_num_token_sentences,
        "s_rel_freq": flat_s_regroup,
        "a_rel_freq": flat_a_regroup,
        }
    with open(dist_path[category], "w") as outfile:
        json.dump(distributions, outfile)
    with open(re_dist_path[category], "w") as outfile:
        json.dump(regrouped_distributions, outfile)
    
    
if __name__ == "__main__":
    main()
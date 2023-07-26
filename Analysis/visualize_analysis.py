import json
import pandas as pd
import matplotlib.pyplot as plt

def drawGraph(tag: str, path: str, df: pd.DataFrame, figsize = (5,5)):
    data = df[tag].dropna()
    bins = len(data) // 10

    fig, ax = plt.subplots(figsize = figsize)
    ax.hist(data, bins = bins)
    ax.set_xlabel('')
    plt.savefig(path)
    pass


def main():
    all_df = pd.read_csv("C:/Users/lhi30/Desktop/Writing_Advice/Data/articles_ytn_rel_freq.csv")

    path = input("Please enter the path to analysis result json file")  
    with open(path) as json_file:
        results = json.load(json_file)
    

if __name__ == "__main__":
    main()
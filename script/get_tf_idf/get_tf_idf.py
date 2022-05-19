"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/5/10 11:49 PM
"""
import json
from re import I
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from pathlib import Path
import glob
import os
import os.path as osp


def get_tf_idf():
    directory_path = '/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/script/get_tf_idf/txt_folder'
    text_files = glob.glob(f"{directory_path}/*.txt")
    text_titles = [Path(text).stem for text in text_files]
    # create td-idf
    # Initialize TfidfVectorizer with desired parameters (default smoothing and normalization)
    tfidf_vectorizer = TfidfVectorizer(input='filename', stop_words='english')
    tfidf_vector = tfidf_vectorizer.fit_transform(text_files)
    tfidf_df = pd.DataFrame(tfidf_vector.toarray(), index=text_titles, columns=tfidf_vectorizer.get_feature_names())
    tfidf_df.loc['00_Document Frequency'] = (tfidf_df > 0).sum()
    tfidf_slice = tfidf_df[['recommend', 'smaller', 'tower', 'loves', 'little', 'quality', 'trees', 'scratching']]
    tfidf_slice.sort_index().round(decimals=2)
    tfidf_df = tfidf_df.drop('00_Document Frequency', errors='ignore')
    tfidf_df.stack().reset_index()
    tfidf_df = tfidf_df.stack().reset_index()
    tfidf_df = tfidf_df.rename(columns={0: 'tfidf', 'level_0': 'document', 'level_1': 'term', 'level_2': 'term'})
    tfidf_slice.sort_index().round(decimals=2)
    tfidf_df.sort_values(by=['document', 'tfidf'], ascending=[True, False]).groupby(['document']).head(10)
    top_tfidf = tfidf_df.sort_values(by=['document', 'tfidf'], ascending=[True, False]).groupby(['document']).head(10)
    return top_tfidf


def generate_heat_map(tfidf_df):
    import altair as alt
    import numpy as np

    # Terms in this list will get a red dot in the visualization
    term_list = ['recommend', 'smaller', 'tower', 'loves', 'little', 'quality', 'trees', 'scratching']

    # adding a little randomness to break ties in term ranking
    top_tfidf_plusRand = tfidf_df.copy()
    top_tfidf_plusRand['tfidf'] = top_tfidf_plusRand['tfidf'] + np.random.rand(tfidf_df.shape[0]) * 0.0001

    # base for all visualizations, with rank calculation
    base = alt.Chart(top_tfidf_plusRand).encode(
        x='rank:O',
        y='document:N'
    ).transform_window(
        rank="rank()",
        sort=[alt.SortField("tfidf", order="descending")],
        groupby=["document"],
    )

    # heatmap specification
    heatmap = base.mark_rect().encode(
        color='tfidf:Q'
    )

    # red circle over terms in above list
    circle = base.mark_circle(size=100).encode(
        color=alt.condition(
            alt.FieldOneOfPredicate(field='term', oneOf=term_list),
            alt.value('red'),
            alt.value('#FFFFFF00')
        )
    )

    # text labels, white for darker heatmap colors
    text = base.mark_text(baseline='middle').encode(
        text='term:N',
        color=alt.condition(alt.datum.tfidf >= 0.23, alt.value('white'), alt.value('black'))
    )
    # display the three superimposed visualizations
    chart = (heatmap + circle + text).properties(width=600)
    chart.save('/Users/huhao/Documents/GitHub/base_catree_Text_Categorization/script/get_tf_idf/altair-elections.html')



tfidf_df = get_tf_idf()
chart = generate_heat_map(tfidf_df)
print(tfidf_df)
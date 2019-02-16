# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 16:40:27 2018

@author: Eirinn
"""

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier

def add_training_data(data):
    ''' Load a dataframe of budget data. 
    Must have "Transaction Description" and "Category" columns. '''
    global df 
    df = data.copy()
    #drop rows with missing categories since we can't train with those
    df = df[~pd.isnull( df['Transaction Description'])]
    df = df[~pd.isnull( df['Category'])]
    #fix capitalisation
    df.Category = df.Category.str.title()
    #make the categories numerical
    df.Category = pd.Categorical(df['Category'])
    #extract day of the week into new column
    df['Day'] = df['Transaction Date'].str.split(expand=True)[0]

def predict(text_clf, predict_features):
    predicted_proba = text_clf.predict_proba(predict_features)
    predicted = np.argmax(predicted_proba,axis=1)
    confidence = np.max(predicted_proba, axis=1)
    return predicted, confidence
    
def build_and_predict(new_rows):
    ''' Pass rows of budget data to be predicted. 
    They will be returned with the Category column filled. '''
    # Build the model
    features = df['Transaction Description']
    targets = df.Category
#    global text_clf #declare it global so we can use it later
    text_clf = Pipeline([('vect',CountVectorizer()),
                         ('tfidf',TfidfTransformer()),
                         ('clf', SGDClassifier(loss='modified_huber', penalty='l2',
                                                alpha=1e-3, random_state=42,
                                                max_iter=5, tol=None)),
                         ])
    text_clf.fit(features, targets)
    # make predictions on new data
    predicted, confidence = predict(text_clf, new_rows['description'])
    new_rows=new_rows.copy()
    new_rows['Category'] = pd.Categorical.from_codes(predicted, df.Category.cat.categories)
    new_rows['Confidence'] = confidence
    new_rows['Assignment'] = 'A'
    mean_new_confidence = new_rows.Confidence.mean()
    print(f'Predicted categories in {len(new_rows)} new rows with average confidence of {mean_new_confidence:0.2%}')
    #compare scores on old data
    recall, recall_confidence = predict(text_clf, features)
    recall_score = recall == targets.cat.codes
    mean_recall = recall_score.mean()
    print(f'Average recall score on {len(recall)} rows of training data is {mean_recall:0.2%}.')
    return new_rows
#%% 
if __name__ == "__main__":
    data = pd.read_excel('2018 Budget.xlsx',sheet_name='London Data')
    add_training_data(data)
    new_rows = data[pd.isnull( data['Category'])]
    build_and_predict(new_rows)


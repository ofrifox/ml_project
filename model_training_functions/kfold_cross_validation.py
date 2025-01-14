from sklearn.model_selection import KFold
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, roc_auc_score

def train_model_by_kfold(df, model):
    kf = KFold(n_splits=10)
    X = df.drop(columns=['target'])
    y = df['target']
    scores = pd.DataFrame()
    for train_index, test_index in kf.split(df):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model.fit(X_train,y_train)
        training_score = roc_auc_score(y_train, model.predict_proba(X_train)[:,1])
        validation_score = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
        scores = scores.append({'Training Score': training_score, 'Validation Score': validation_score}, ignore_index=True)

    print('\n\nTraining accuracy score: %.3f +/- %.3f\n Validation accuracy score %.3f +/- %.3f' % (scores['Training Score'].mean(), scores['Training Score'].std(), scores['Validation Score'].mean(),  scores['Validation Score'].std()))
    return scores.mean()




def train_clustering_model_by_kfold(df, model):
    kf = KFold(n_splits=10)
    X = df.drop(columns=['target'])
    y = df['target']
    scores = pd.DataFrame()
    accuracy = pd.DataFrame()
    for train_index, test_index in kf.split(df):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model.fit(X_train,y_train)
        y_pred = model.predict(X_train)
        inertia = model.inertia_
        sil_score = silhouette_score(X_train, y_pred)
        boul_score = davies_bouldin_score(X_train, y_pred)

    scores = scores.append({'Inertia':inertia, 'Sillhouette Score': sil_score, 'Bouldin Score':boul_score}, ignore_index=True)
    accuracy = accuracy.append({''})

    print('\n\nTraining accuracy score: %.3f +/- %.3f\n Validation accuracy score %.3f +/- %.3f' % (scores['Training Score'].mean(), scores['Training Score'].std(), scores['Validation Score'].mean(),  scores['Validation Score'].std()))
    return scores
"""Tests de validation du pipeline; les cas synthétiques ne sont pas les métriques de soutenance."""
import numpy as np
import pandas as pd
import pytest
from train import FEATURES, ID_COLUMNS, evaluate, load_prepare, describe_predictions


def fake_sample(n=100):
    return pd.DataFrame({
        'transaction_id':[f't{i}' for i in range(n)],
        'account_id':[f'a{i%10}' for i in range(n)],
        'amount':np.linspace(5,2000,n), 'hour':np.arange(n)%24,
        'country':['MA' if i%2 else 'FR' for i in range(n)],
        'merchant_category':['SHOP' if i%3 else 'CASH' for i in range(n)],
        'transactions_last_24h':np.arange(n)%12,
        'average_amount_last_7d':np.linspace(10,300,n),
        'is_fraud':[1 if i%7==0 else 0 for i in range(n)],
    })


def test_pipeline_without_real_data(tmp_path):
    result=evaluate(fake_sample(),tmp_path)
    assert 0 <= result['fraud_precision'] <= 1
    assert (tmp_path/'metrics.json').exists()
    assert (tmp_path/'confusion_matrix.png').exists()
    assert (tmp_path/'comparaison_modeles.png').exists()
    assert len(result['cv_comparison']) == 3


def test_identifiers_and_target_excluded():
    df=fake_sample()
    X,y=load_prepare(df)
    assert X.columns.tolist()==FEATURES
    assert not set(ID_COLUMNS+['is_fraud']).intersection(X.columns)
    assert int(y.sum())>0


def test_missing_values_are_supported():
    df=fake_sample();df.loc[:6,'country']=np.nan
    df.loc[:4,'average_amount_last_7d']=np.nan
    X,_=load_prepare(df)
    assert X.country.isna().sum()==7
    assert X.average_amount_last_7d.isna().sum()==5


def test_reject_non_binary_target():
    df=fake_sample();df.loc[0,'is_fraud']=3
    with pytest.raises(ValueError,match='cible'):
        load_prepare(df)


def test_reject_duplicate_transaction_id():
    df=fake_sample();df.loc[1,'transaction_id']=df.loc[0,'transaction_id']
    with pytest.raises(ValueError,match='double'):
        load_prepare(df)


def test_confusion_matrix_known_example():
    info=describe_predictions([0,0,1,1],[0.1,0.7,0.8,0.2],0.5)
    assert info['matrice_confusion']==[[1,1],[1,1]]
    assert info['precision_fraude']==.5
    assert info['rappel_fraude']==.5

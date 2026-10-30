#!/usr/bin/env python3
"""Partie H - classification de fraude bancaire, hors microservices.

Exécution (depuis fraud/):
    python train.py --csv data/bank_transactions.csv --out results

La sélection du modèle ET du seuil utilise seulement l'entraînement.
Le test est ouvert une fois, après avoir fixé modèle et seuil.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay, accuracy_score, average_precision_score,
    confusion_matrix, f1_score, fbeta_score, precision_recall_curve,
    precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

SEED = 42
FEATURES = ['amount', 'hour', 'country', 'merchant_category',
            'transactions_last_24h', 'average_amount_last_7d']
NUMERIC = ['amount', 'hour', 'transactions_last_24h', 'average_amount_last_7d']
CATEGORICAL = ['country', 'merchant_category']
ID_COLUMNS = ['transaction_id', 'account_id']
REQUIRED = ID_COLUMNS + FEATURES + ['is_fraud']


def make_preprocessing() -> ColumnTransformer:
    num = Pipeline([
        ('imputation_mediane', SimpleImputer(strategy='median')),
        ('standardisation', StandardScaler()),
    ])
    cat = Pipeline([
        ('imputation_mode', SimpleImputer(strategy='most_frequent')),
        ('encodage_onehot', OneHotEncoder(handle_unknown='ignore')),
    ])
    return ColumnTransformer([
        ('numeriques', num, NUMERIC), ('categories', cat, CATEGORICAL)
    ], remainder='drop')


def make_pipeline() -> Pipeline:
    """Conserve l'API de la première version, utile aux tests/TP."""
    return Pipeline([
        ('preprocess', make_preprocessing()),
        ('model', LogisticRegression(max_iter=2000, class_weight='balanced', random_state=SEED)),
    ])


def candidates() -> dict[str, Pipeline]:
    return {
        'Régression logistique (pondérée)': make_pipeline(),
        'Arbre de décision (pondéré)': Pipeline([
            ('preprocess', make_preprocessing()),
            ('model', DecisionTreeClassifier(max_depth=6, min_samples_leaf=8,
                                             class_weight='balanced', random_state=SEED)),
        ]),
        'Random Forest (pondérée)': Pipeline([
            ('preprocess', make_preprocessing()),
            ('model', RandomForestClassifier(n_estimators=160, max_depth=12,
                                             min_samples_leaf=4, class_weight='balanced_subsample',
                                             random_state=SEED, n_jobs=1)),
        ]),
    }


def load_prepare(df: pd.DataFrame):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f'Colonnes obligatoires manquantes : {missing}')
    if df['is_fraud'].isna().any():
        raise ValueError('La cible is_fraud ne doit pas comporter de valeurs manquantes.')
    target_values = set(pd.to_numeric(df['is_fraud'], errors='coerce').dropna().unique())
    if target_values != {0, 1} or df['is_fraud'].isna().any():
        raise ValueError('La cible doit contenir les deux classes 0 et 1 uniquement.')
    if df['is_fraud'].value_counts().min() < 6:
        raise ValueError('6 observations par classe au minimum sont nécessaires pour une CV à 3 plis.')
    if df['transaction_id'].duplicated().any():
        raise ValueError('Identifiants de transaction en double : vérifier la qualité des données.')
    X = df[FEATURES].copy()  # AUCUN identifiant, AUCUNE cible comme variable explicative
    for col in NUMERIC:
        X[col] = pd.to_numeric(X[col], errors='coerce')
    for col in CATEGORICAL:
        # str/np.nan est compris par les imputers scikit-learn ; éviter pd.NA.
        X[col] = X[col].map(lambda v: str(v) if pd.notna(v) else np.nan).astype(object)
    y = df['is_fraud'].astype(int)
    return X, y


def describe_predictions(y_true, probas, threshold):
    predictions = (np.asarray(probas) >= threshold).astype(int)
    cm = confusion_matrix(y_true, predictions, labels=[0, 1]); tn, fp, fn, tp = cm.ravel()
    return {
        'seuil': float(threshold),
        'accuracy': float(accuracy_score(y_true, predictions)),
        'precision_fraude': float(precision_score(y_true, predictions, zero_division=0)),
        'rappel_fraude': float(recall_score(y_true, predictions, zero_division=0)),
        'f1_fraude': float(f1_score(y_true, predictions, zero_division=0)),
        'f2_fraude': float(fbeta_score(y_true, predictions, beta=2, zero_division=0)),
        'matrice_confusion': cm.tolist(),
        'vrais_negatifs': int(tn), 'faux_positifs': int(fp),
        'faux_negatifs': int(fn), 'vrais_positifs': int(tp),
        'nombre_alertes': int((predictions == 1).sum()),
    }


def make_eda_plots(df, out):
    y = df['is_fraud'].astype(int)
    fig, ax = plt.subplots(figsize=(6.6, 4.1))
    names = ['Non fraude', 'Fraude']; counts = [int((y==0).sum()), int((y==1).sum())]
    bars = ax.bar(names, counts)
    for b,n in zip(bars, counts):
        ax.text(b.get_x()+b.get_width()/2,n+25,f'{n:,}  ({n/len(df):.2%})',ha='center',fontsize=10)
    ax.set_ylim(0,max(counts)*1.16);ax.set_ylabel('Nombre de transactions')
    ax.set_title('Distribution des classes — bank_transactions.csv')
    fig.tight_layout(); fig.savefig(out/'repartition_fraudes.png',dpi=170);plt.close(fig)

    miss=df.isna().sum(); miss=miss[miss>0].sort_values(ascending=True)
    fig,ax=plt.subplots(figsize=(8.2,3.4))
    ax.barh(miss.index,miss.values)
    for i,v in enumerate(miss.values):ax.text(v+1,i,str(v),va='center')
    ax.set_xlim(0,max(miss.values)*1.2 if len(miss) else 1)
    ax.set_xlabel('Valeurs manquantes');ax.set_title('Qualité des données — colonnes incomplètes')
    fig.tight_layout();fig.savefig(out/'valeurs_manquantes.png',dpi=170);plt.close(fig)

    # Exploratoire descriptif, pas de sélection de features sur le test.
    grouped = df.groupby('merchant_category',dropna=False)['is_fraud'].agg(['count','mean'])
    grouped=grouped.loc[grouped['count']>=20].sort_values('mean')
    fig,ax=plt.subplots(figsize=(8,4.3))
    ax.barh(grouped.index.fillna('Non renseigné').astype(str), grouped['mean'].values*100)
    ax.set_xlabel('Transactions frauduleuses (%)')
    ax.set_title('Taux de fraude par catégorie commerçant (exploration)')
    fig.tight_layout();fig.savefig(out/'fraude_par_categorie.png',dpi=170);plt.close(fig)


def evaluate(df: pd.DataFrame, out: Path) -> dict:
    out = Path(out);out.mkdir(parents=True,exist_ok=True)
    X, y = load_prepare(df)
    # random_state fixe et stratification explicite (3 750 / 1 250 sur le vrai CSV).
    indices = np.arange(len(df))
    tr_idx,te_idx = train_test_split(indices,test_size=0.25,stratify=y,random_state=SEED)
    X_train, X_test = X.iloc[tr_idx], X.iloc[te_idx]
    y_train, y_test = y.iloc[tr_idx], y.iloc[te_idx]
    cv = StratifiedKFold(n_splits=3,shuffle=True,random_state=SEED)
    make_eda_plots(df,out)

    compare = []
    models = candidates()
    for name, model in models.items():
        # L'AP estime le rang des risques et reste pertinente si 5 % des cas sont positifs.
        cv_ap = cross_val_score(model,X_train,y_train,cv=cv,scoring='average_precision',n_jobs=1)
        compare.append({'modele':name, 'cv_ap_moyenne':float(cv_ap.mean()),
                        'cv_ap_ecart_type':float(cv_ap.std()),
                        'cv_plis':[float(v) for v in cv_ap]})
    # Sélection AVANT toute consultation des labels de test.
    chosen=max(compare,key=lambda item:item['cv_ap_moyenne'])['modele']
    selected = models[chosen]
    # Probabilités OOF = validation croisée de l'entraînement uniquement, jamais test.
    oof_prob = cross_val_predict(selected,X_train,y_train,cv=cv,method='predict_proba',n_jobs=1)[:,1]
    grid = np.round(np.linspace(0.05,0.95,19),2)
    grid_data=[describe_predictions(y_train,oof_prob,float(t)) for t in grid]
    # Maximisation de F1 sur les prédictions OOF, uniquement pour exploration métier.
    best_train=max(grid_data,key=lambda it:(it['f1_fraude'],-it['seuil']))
    chosen_threshold=float(best_train['seuil'])
    selected.fit(X_train,y_train)
    scores=selected.predict_proba(X_test)[:,1]

    fixed=describe_predictions(y_test,scores,0.50)
    tuned=describe_predictions(y_test,scores,chosen_threshold)
    overall_ap=float(average_precision_score(y_test,scores))
    auc=float(roc_auc_score(y_test,scores))
    baseline=DummyClassifier(strategy='most_frequent').fit(X_train,y_train)
    base=describe_predictions(y_test,baseline.predict(X_test),0.5)

    profile={
        'lignes':int(len(df)), 'colonnes':int(len(df.columns)),
        'distributions':{'non_fraude':int((y==0).sum()),'fraude':int((y==1).sum())},
        'fraude_pourcentage':round(float(y.mean())*100,4),
        'valeurs_manquantes':{k:int(v) for k,v in df.isna().sum().to_dict().items()},
        'comptes_distincts':int(df['account_id'].nunique()),
        'identifiants_transactions_doubles':int(df['transaction_id'].duplicated().sum()),
        'colonnes_exclues_de_X':ID_COLUMNS+['is_fraud'],
        'variables_utilisees':FEATURES,
        'attention_dates':'Le CSV ne contient pas de date chronologique de transaction : validation temporelle impossible avec ce fichier.'
    }
    result={
        'dataset':'bank_transactions.csv (fichier fourni)',
        'records':int(len(df)), 'train_records':int(len(X_train)),
        'test_records':int(len(X_test)),
        'train_fraud':int(y_train.sum()), 'test_fraud':int(y_test.sum()),
        'fraud_rate':float(y.mean()),
        'missing_by_column':profile['valeurs_manquantes'],
        'selected_model':chosen, 'selection_method':'Average Precision / CV stratifiée 3 plis, uniquement sur apprentissage',
        'cv_comparison':compare,
        'test_average_precision':overall_ap,
        'test_roc_auc':auc,
        'baseline_always_non_fraud':base,
        'test_threshold_fixed_0_50':fixed,
        'oof_training_selected_threshold':chosen_threshold,
        'oof_training_threshold_metric':'F1 fraude maximum sur grille 0.05 à 0.95, sur OOF apprentissage uniquement',
        'test_threshold_selected_on_training':tuned,
        'fraud_precision':fixed['precision_fraude'],
        'fraud_recall':fixed['rappel_fraude'],
        'fraud_f1':fixed['f1_fraude'],
        'average_precision':overall_ap,
        'confusion_matrix':fixed['matrice_confusion'],
        'threshold':0.5,
        'seed':SEED,'test_size':0.25,
        'limitations':[
            'Pas de timestamp dans le CSV : aucune validation temporelle réalisable.',
            'Modèle expérimental offline, pas de connexion aux microservices (conforme à l’énoncé).',
            'Des comptes peuvent apparaître dans train et test ; les ID sont exclus du modèle.',
            'Un seuil retenu sur apprentissage reste à valider selon coûts métier avant déploiement.'
        ]
    }
    (out/'dataset_profile.json').write_text(json.dumps(profile,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    pd.DataFrame(compare).drop(columns=['cv_plis']).to_csv(out/'comparaison_modeles_cv.csv',index=False)
    pd.DataFrame(grid_data)[['seuil','precision_fraude','rappel_fraude','f1_fraude',
                            'f2_fraude','faux_positifs','faux_negatifs']].to_csv(out/'analyse_seuil_sur_train.csv',index=False)
    pd.DataFrame({
        'transaction_id':df.iloc[te_idx]['transaction_id'].values,
        'vraie_classe':y_test.to_numpy(),
        'risque_fraude':scores,
        'prediction_seuil_0_50':(scores>=.5).astype(int),
        'prediction_seuil_train':(scores>=chosen_threshold).astype(int),
    }).to_csv(out/'predictions_test.csv',index=False)
    joblib.dump(selected,out/'fraud_pipeline.joblib')

    ConfusionMatrixDisplay(confusion_matrix(y_test,scores>=.5,labels=[0,1]),
                           display_labels=['Non fraude','Fraude']).plot(values_format='d',cmap='Blues')
    plt.title('Test hold-out — seuil 0,50');plt.tight_layout()
    plt.savefig(out/'confusion_matrix.png',dpi=190);plt.close()
    pp,rr,_=precision_recall_curve(y_test,scores)
    fig,ax=plt.subplots(figsize=(7.6,4.9))
    ax.plot(rr,pp,label=f'{chosen}: AP={overall_ap:.3f}')
    ax.axhline(y.mean(),linestyle='--',label=f'Prévalence={y.mean():.3f}')
    ax.set_xlabel('Rappel de la fraude');ax.set_ylabel('Précision de la fraude')
    ax.set_title('Courbe précision–rappel sur le test indépendant')
    ax.legend(loc='best');ax.grid(alpha=.2);fig.tight_layout()
    fig.savefig(out/'precision_recall.png',dpi=190);plt.close(fig)

    compdf=pd.DataFrame(compare).sort_values('cv_ap_moyenne')
    fig,ax=plt.subplots(figsize=(8,4.3))
    ax.barh(compdf['modele'],compdf['cv_ap_moyenne'],xerr=compdf['cv_ap_ecart_type'],capsize=4)
    ax.set_xlim(0,min(1.0,max(compdf['cv_ap_moyenne'])*1.25))
    ax.set_xlabel('Average precision en validation croisée (train)')
    ax.set_title('Sélection des modèles sans utiliser le test')
    fig.tight_layout();fig.savefig(out/'comparaison_modeles.png',dpi=190);plt.close(fig)

    threshold_df=pd.DataFrame(grid_data)
    fig,ax=plt.subplots(figsize=(7.6,4.4))
    for metric,lab in [('precision_fraude','Précision'),('rappel_fraude','Rappel'),('f1_fraude','F1')]:
        ax.plot(threshold_df['seuil'],threshold_df[metric],marker='o',ms=3,label=lab)
    ax.axvline(chosen_threshold,linestyle='--',label=f'Seuil apprentissage={chosen_threshold:.2f}')
    ax.set_xlabel('Seuil de décision');ax.set_ylabel('Score (validation OOF du train)')
    ax.set_title('Compromis précision/rappel — seulement sur train')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout()
    fig.savefig(out/'analyse_seuil_sur_train.png',dpi=190);plt.close(fig)

    # Permutation sur train (et non sur test) : diagnostic d'interprétation a posteriori.
    sub_idx=np.random.default_rng(SEED).choice(len(X_train),size=min(850,len(X_train)),replace=False)
    imp=permutation_importance(selected,X_train.iloc[sub_idx],y_train.iloc[sub_idx],
                               n_repeats=4,random_state=SEED,scoring='average_precision',n_jobs=1)
    impdf=pd.DataFrame({'variable':FEATURES,'importance_ap_moyenne':imp.importances_mean,
                        'ecart_type':imp.importances_std}).sort_values('importance_ap_moyenne',ascending=False)
    impdf.to_csv(out/'importance_variables.csv',index=False)
    plotimp=impdf.sort_values('importance_ap_moyenne')
    fig,ax=plt.subplots(figsize=(7.6,4.3))
    ax.barh(plotimp['variable'],plotimp['importance_ap_moyenne'],xerr=plotimp['ecart_type'])
    ax.set_xlabel('Perte moyenne d’Average Precision après permutation (train)')
    ax.set_title('Importance diagnostique des 6 variables explicatives')
    fig.tight_layout();fig.savefig(out/'importance_variables.png',dpi=190);plt.close(fig)
    return result


def main():
    parser=argparse.ArgumentParser(description='Analyse fraude Partie H — ADRIA')
    parser.add_argument('--csv',type=Path,default=Path('data/bank_transactions.csv'))
    parser.add_argument('--out',type=Path,default=Path('results'))
    args=parser.parse_args()
    if not args.csv.exists():
        print(f'CSV absent : {args.csv}',file=sys.stderr);return 2
    try:
        result=evaluate(pd.read_csv(args.csv),args.out)
    except Exception as ex:
        print(f'Erreur analyse : {ex}',file=sys.stderr);return 1
    print('ANALYSE DE FRAUDE — DONNÉES RÉELLES DU FICHIER FOURNI')
    print(f"Lignes : {result['records']}, fraudes : {result['fraud_rate']:.2%}")
    print(f"Modèle choisi uniquement sur training CV : {result['selected_model']}")
    print(f"Average precision (test) : {result['test_average_precision']:.4f}")
    f=result['test_threshold_fixed_0_50']
    print(f"Seuil 0.50 : précision {f['precision_fraude']:.4f} / rappel {f['rappel_fraude']:.4f} / F1 {f['f1_fraude']:.4f}")
    print('Matrice confusion (VN,FP / FN,VP) :',f['matrice_confusion'])
    print('Résultats et graphiques :',args.out.resolve())
    return 0

if __name__=='__main__':sys.exit(main())

#!/usr/bin/env python3
"""Frozen Threshold/Hamming baseline on NinaPro DB5 E2 validation.

Protocol:
- Sx_E2_A1.mat only, subjects 1..10
- classes 0,1,5,6
- train reps 1,3,4; validation rep 6; reps 2,5 never segmented
- 40-sample windows, 20-sample step, no class/repetition boundary crossing
- channels {1}, {1,5}, {1,3,5,7}, {1..8}
- RMS per channel
- threshold per subject/channel = mean(train-rest RMS) + 3*std(train-rest RMS)
- binarize each window channelwise
- per-class binary template: for each training repetition, bitwise majority over windows;
  then bitwise majority over the three repetition-level templates
- classify by Hamming distance; ties between classes => reject (-1)

No parameter is selected from validation outcomes.
"""
from __future__ import annotations
import argparse, io, json, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import loadmat
from sklearn.metrics import accuracy_score, f1_score

LABELS=np.array([0,1,5,6],int)
LABEL_NAMES={0:'repouso',1:'thumbs_up',5:'mao_aberta',6:'mao_fechada'}
TRAIN_REPS={1,3,4}; VAL_REPS={6}; FORBIDDEN={2,5}; ALLOWED=TRAIN_REPS|VAL_REPS
CHANNEL_SETS={1:[0],2:[0,4],4:[0,2,4,6],8:list(range(8))}
WINDOW=40; STEP=20


def _inner(outer,s):
    target=f's{s}.zip'.lower()
    names={Path(n).name.lower():n for n in outer.namelist()}
    return zipfile.ZipFile(io.BytesIO(outer.read(names[target])))

def load_e2(outer,s):
    with _inner(outer,s) as z:
        target=f'S{s}_E2_A1.mat'.lower()
        hits=[n for n in z.namelist() if Path(n).name.lower()==target]
        assert len(hits)==1
        d=loadmat(io.BytesIO(z.read(hits[0])),variable_names=['emg','restimulus','rerepetition'])
    emg=np.asarray(d['emg'],float)[:,:8]
    y=np.asarray(d['restimulus']).ravel().astype(int)
    rep=np.asarray(d['rerepetition']).ravel().astype(int)
    return emg,y,rep,hits[0]

def segment_rms(emg,y,rep):
    """Segmenta RMS com treino e validação; nunca inclui as repetições de teste."""
    starts=[]; ys=[]; rs=[]; rms=[]
    eligible=np.isin(rep,sorted(ALLOWED))
    edges=np.diff(np.r_[False,eligible,False].astype(np.int8))
    for bs,be in zip(np.flatnonzero(edges==1),np.flatnonzero(edges==-1)):
        yb=y[bs:be]; rb=rep[bs:be]
        change=np.r_[True,(yb[1:]!=yb[:-1])|(rb[1:]!=rb[:-1])]
        rstart=np.flatnonzero(change); rend=np.r_[rstart[1:],len(yb)]
        for a,b in zip(rstart,rend):
            lab=int(yb[a]); rr=int(rb[a])
            if lab not in LABELS: continue
            assert rr in ALLOWED and rr not in FORBIDDEN
            s0=bs+int(a); e0=bs+int(b)
            for st in range(s0,e0-WINDOW+1,STEP):
                en=st+WINDOW
                assert np.all(y[st:en]==lab) and np.all(rep[st:en]==rr)
                w=emg[st:en]
                starts.append(st); ys.append(lab); rs.append(rr)
                rms.append(np.sqrt(np.mean(w*w,axis=0)))
    out=(np.asarray(starts,int),np.asarray(ys,int),np.asarray(rs,int),np.asarray(rms,float))
    assert not np.any(np.isin(out[2],sorted(FORBIDDEN)))
    return out

def majority_bits(a):
    # deterministic strict majority; ties (possible only within an even number of windows) resolve to 0.
    return (np.mean(a,axis=0)>0.5).astype(np.int8)

def build_templates(bits,y,rep):
    """Maioria binária por repetição, seguida de maioria entre repetições."""
    templates={}
    rep_templates={}
    for lab in LABELS:
        one=[]
        for rr in sorted(TRAIN_REPS):
            m=(y==lab)&(rep==rr)
            if not np.any(m): raise ValueError(f'no training windows class={lab} rep={rr}')
            t=majority_bits(bits[m])
            rep_templates[(int(lab),int(rr))]=t
            one.append(t)
        # 3 repetition-level templates => strict majority has no tie
        templates[int(lab)]=majority_bits(np.vstack(one))
    return templates,rep_templates

def predict_hamming(bits,templates):
    """Empates na menor distância são rejeitados com rótulo -1."""
    T=np.vstack([templates[int(l)] for l in LABELS])
    dist=np.sum(bits[:,None,:]!=T[None,:,:],axis=2)
    minv=dist.min(axis=1)
    ismin=dist==minv[:,None]
    pred=np.full(bits.shape[0],-1,int)
    unique=ismin.sum(axis=1)==1
    pred[unique]=LABELS[np.argmax(ismin[unique],axis=1)]
    return pred,dist

def cm_with_reject(y,pred):
    cols=list(LABELS)+[-1]
    cm=np.zeros((len(LABELS),len(cols)),int)
    li={int(v):i for i,v in enumerate(LABELS)}; ci={int(v):i for i,v in enumerate(cols)}
    for t,p in zip(y,pred): cm[li[int(t)],ci[int(p)]]+=1
    return cm

def balanced_accuracy_with_reject(y_true, y_pred):
    """Recall médio entre classes reais; a rejeição (-1) conta como erro.

    Evita o aviso emitido por `balanced_accuracy_score` quando `-1`
    ocorre somente nas predições. Equivale à média dos quatro recalls.
    """
    recalls = []
    for label in LABELS:
        mask = y_true == label
        if not np.any(mask):
            raise ValueError(f"Classe verdadeira ausente: {label}")
        recalls.append(np.mean(y_pred[mask] == label))
    return float(np.mean(recalls))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--db5-zip',type=Path,required=True); ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    rows=[]; templ_rows=[]; cms={}; audit_rows=[]
    with zipfile.ZipFile(a.db5_zip) as outer:
        for s in range(1,11):
            emg,yraw,repraw,path=load_e2(outer,s)
            starts,y,rep,rms8=segment_rms(emg,yraw,repraw)
            assert set(np.unique(y))==set(LABELS)
            audit_rows.append({'subject':s,'file':path,'n_windows':len(y),'labels':','.join(map(str,np.unique(y))),
                               'reps':','.join(map(str,np.unique(rep))),'forbidden_2_5_present':bool(np.any(np.isin(rep,[2,5])))})
            tr=np.isin(rep,sorted(TRAIN_REPS)); va=np.isin(rep,sorted(VAL_REPS))
            for nch,ch in CHANNEL_SETS.items():
                X=rms8[:,ch]
                rest_tr=tr&(y==0)
                mu=X[rest_tr].mean(axis=0); sd=X[rest_tr].std(axis=0,ddof=0); thr=mu+3*sd
                bits=(X>thr).astype(np.int8)
                templates,rep_templates=build_templates(bits[tr],y[tr],rep[tr])
                # build_templates received subset arrays so rep still values 1/3/4
                pred,dist=predict_hamming(bits[va],templates)
                yv=y[va]
                f1s=f1_score(yv,pred,labels=LABELS,average=None,zero_division=0)
                cm=cm_with_reject(yv,pred)
                closed_i=np.where(LABELS==6)[0][0]; thumb_i=np.where(LABELS==1)[0][0]
                row={
                    'subject':s,'channels':nch,'pipeline':'Threshold/Hamming','n_features':nch,
                    'n_train':int(tr.sum()),'n_val':int(va.sum()),
                    'macro_f1':float(f1_score(yv,pred,labels=LABELS,average='macro',zero_division=0)),
                    'balanced_accuracy':balanced_accuracy_with_reject(yv,pred),
                    'accuracy':float(accuracy_score(yv,pred)),
                    'rejection_rate':float(np.mean(pred==-1)),
                    'closed_to_thumb_n':int(cm[closed_i,thumb_i]),'thumb_to_closed_n':int(cm[thumb_i,closed_i]),
                    'closed_to_thumb_rate':float(cm[closed_i,thumb_i]/cm[closed_i].sum()),
                    'thumb_to_closed_rate':float(cm[thumb_i,closed_i]/cm[thumb_i].sum()),
                }
                for lab,sc in zip(LABELS,f1s): row[f'f1_{LABEL_NAMES[int(lab)]}']=float(sc)
                rows.append(row)
                cms[f'S{s}_{nch}ch']=cm.tolist()
                for j,c in enumerate(ch):
                    templ_rows.append({'subject':s,'channels':nch,'channel_one_based':c+1,'rest_mu_rms':mu[j],'rest_sd_rms':sd[j],'threshold_mu_plus_3sd':thr[j],
                                      **{f'template_{lab}':int(templates[int(lab)][j]) for lab in LABELS}})
    detail=pd.DataFrame(rows).sort_values(['channels','subject'])
    detail.to_csv(a.out/'threshold_results_by_subject.csv',index=False)
    pd.DataFrame(templ_rows).to_csv(a.out/'thresholds_and_templates.csv',index=False)
    pd.DataFrame(audit_rows).to_csv(a.out/'threshold_window_audit.csv',index=False)
    metrics=['macro_f1','balanced_accuracy','accuracy','rejection_rate','f1_repouso','f1_thumbs_up','f1_mao_aberta','f1_mao_fechada','closed_to_thumb_rate','thumb_to_closed_rate']
    summ=detail.groupby('channels')[metrics].agg(['mean','std'])
    summ.columns=[f'{a}_{b}' for a,b in summ.columns]; summ=summ.reset_index(); summ.to_csv(a.out/'threshold_summary.csv',index=False)
    with open(a.out/'threshold_confusion_matrices.json','w') as f: json.dump({'rows_true':LABELS.tolist(),'cols_pred':LABELS.tolist()+[-1],'reject_label':-1,'matrices':cms},f,indent=2)
    audit={'exercise':'E2 exclusively','train_repetitions':[1,3,4],'validation_repetitions':[6],'forbidden_test_repetitions':[2,5],
           'window_samples':40,'step_samples':20,'channel_sets_one_based':{str(k):[x+1 for x in v] for k,v in CHANNEL_SETS.items()},
           'threshold_rule':'mean(train-rest RMS)+3*std(train-rest RMS), per subject/channel',
           'template_rule':'bitwise majority within each training repetition, then bitwise majority across reps 1/3/4',
           'classifier':'minimum Hamming distance; any class tie => reject (-1)',
           'tie_within_window_majority_rule':'exact 50/50 bit majority resolves to 0 deterministically',
           'no_validation_tuning':True,'forbidden_2_5_absent':bool(~pd.DataFrame(audit_rows).forbidden_2_5_present.any())}
    with open(a.out/'threshold_audit.json','w') as f: json.dump(audit,f,indent=2)
    print(summ.to_string(index=False))

if __name__=='__main__': main()

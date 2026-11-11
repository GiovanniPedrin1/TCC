#!/usr/bin/env python3
"""NinaPro DB5 E2 — validação congelada LDA-RMS vs LDA-TD.

Usa EXCLUSIVAMENTE Sx_E2_A1.mat (x=1..10).
Treino: repetições 1,3,4. Validação: repetição 6.
Repetições 2 e 5 ficam fora de segmentação/features/normalização/métricas.
"""
from __future__ import annotations
import argparse, io, json, re, warnings, zipfile
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import loadmat
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score

LABELS = np.array([0,1,5,6], dtype=int)
LABEL_NAMES = {0:'repouso',1:'thumbs_up',5:'mao_aberta',6:'mao_fechada'}
TRAIN_REPS = {1,3,4}
VAL_REPS = {6}
FORBIDDEN_REPS = {2,5}
ALLOWED_REPS = TRAIN_REPS | VAL_REPS
CHANNEL_SETS = {1:[0],2:[0,4],4:[0,2,4,6],8:list(range(8))}
WINDOW=40
STEP=20
PRIORS=np.array([0.25,0.25,0.25,0.25], dtype=float)
SIGMA_EPS=1e-12

@dataclass
class WindowSet:
    starts: np.ndarray
    y: np.ndarray
    rep: np.ndarray
    rms8: np.ndarray
    mav8: np.ndarray
    wl8: np.ndarray


def _open_subject_inner(outer: zipfile.ZipFile, subject:int) -> zipfile.ZipFile:
    key=f's{subject}.zip'
    names={Path(n).name.lower():n for n in outer.namelist()}
    if key.lower() not in names:
        raise FileNotFoundError(f'{key} não encontrado no DB5.zip')
    return zipfile.ZipFile(io.BytesIO(outer.read(names[key.lower()])))


def load_e2(outer:zipfile.ZipFile, subject:int):
    with _open_subject_inner(outer,subject) as inner:
        target=f'S{subject}_E2_A1.mat'
        matches=[n for n in inner.namelist() if Path(n).name.lower()==target.lower()]
        if len(matches)!=1:
            raise FileNotFoundError(f'S{subject}: esperado exatamente {target}; encontrados {matches}')
        raw=inner.read(matches[0])
    d=loadmat(io.BytesIO(raw), variable_names=['emg','restimulus','rerepetition'])
    emg=np.asarray(d['emg'],dtype=np.float64)
    y=np.asarray(d['restimulus']).ravel().astype(int)
    rep=np.asarray(d['rerepetition']).ravel().astype(int)
    if emg.shape[0]!=y.size or y.size!=rep.size: raise ValueError(f'S{subject}: comprimentos incompatíveis')
    if emg.shape[1]<8: raise ValueError(f'S{subject}: menos de 8 canais EMG')
    return emg[:,:8],y,rep,matches[0]


def audit_e2_files(db5_zip:Path):
    rows=[]
    with zipfile.ZipFile(db5_zip) as outer:
        for s in range(1,11):
            emg,y,rep,path=load_e2(outer,s)
            vals=np.unique(y).astype(int).tolist()
            reps=np.unique(rep).astype(int).tolist()
            selected=sorted(set(vals).intersection(set(LABELS.tolist())))
            rows.append({
                'subject':s,'file':path,'n_samples':int(y.size),'n_emg_channels':int(emg.shape[1]),
                'restimulus_values':','.join(map(str,vals)),'rerepetition_values':','.join(map(str,reps)),
                'target_labels_present':','.join(map(str,selected)),
                'target_labels_ok':selected==LABELS.tolist(),
                'is_e2':bool(re.search(r'_E2_A1\.mat$',Path(path).name,re.I)),
            })
    df=pd.DataFrame(rows)
    if not df['is_e2'].all(): raise AssertionError('Arquivo não-E2 detectado')
    if not df['target_labels_ok'].all(): raise AssertionError('Algum E2 não contém todos os rótulos alvo 0,1,5,6')
    return df


def segment_all_features(emg8:np.ndarray,y:np.ndarray,rep:np.ndarray)->WindowSet:
    starts=[]; ys=[]; rs=[]; rms=[]; mav=[]; wl=[]
    # Firewall: only allowed repetition blocks are ever indexed in EMG/y below.
    eligible=np.isin(rep, sorted(ALLOWED_REPS))
    edges=np.diff(np.r_[False,eligible,False].astype(np.int8))
    block_starts=np.flatnonzero(edges==1); block_ends=np.flatnonzero(edges==-1)
    for bs,be in zip(block_starts,block_ends):
        # Within allowed blocks, find constant (class, repetition) runs.
        yb=y[bs:be]; rb=rep[bs:be]
        change=np.r_[True,(yb[1:]!=yb[:-1]) | (rb[1:]!=rb[:-1])]
        run_st=np.flatnonzero(change); run_en=np.r_[run_st[1:], yb.size]
        for a,b in zip(run_st,run_en):
            lab=int(yb[a]); rr=int(rb[a])
            if rr not in ALLOWED_REPS or rr in FORBIDDEN_REPS: raise AssertionError('repetição proibida')
            if lab not in LABELS: continue
            s0=bs+int(a); e0=bs+int(b)
            for st in range(s0,e0-WINDOW+1,STEP):
                en=st+WINDOW
                # Mandatory no-boundary-crossing checks.
                if not (np.all(y[st:en]==lab) and np.all(rep[st:en]==rr)):
                    raise AssertionError('janela cruzou fronteira de classe/repetição')
                w=emg8[st:en,:]
                starts.append(st); ys.append(lab); rs.append(rr)
                rms.append(np.sqrt(np.mean(w*w,axis=0)))
                mav.append(np.mean(np.abs(w),axis=0))
                wl.append(np.sum(np.abs(np.diff(w,axis=0)),axis=0))
    out=WindowSet(np.asarray(starts,int),np.asarray(ys,int),np.asarray(rs,int),
                  np.asarray(rms,float),np.asarray(mav,float),np.asarray(wl,float))
    if np.any(np.isin(out.rep, sorted(FORBIDDEN_REPS))): raise AssertionError('2/5 entrou no WindowSet')
    return out


def design_matrix(ws:WindowSet, ch:list[int], pipeline:str):
    if pipeline=='LDA-RMS':
        return ws.rms8[:,ch]
    if pipeline=='LDA-TD':
        # channel-major order [RMS,MAV,WL] per channel
        return np.column_stack([np.column_stack([ws.rms8[:,c],ws.mav8[:,c],ws.wl8[:,c]]) for c in ch]).reshape(len(ws.y),-1)
    raise ValueError(pipeline)


def zscore_train_only(xtr,xva):
    mu=xtr.mean(axis=0); sigma=xtr.std(axis=0,ddof=0)
    tiny=(~np.isfinite(sigma)) | (np.abs(sigma)<=SIGMA_EPS)
    safe=sigma.copy(); safe[tiny]=1.0
    xt=(xtr-mu)/safe; xv=(xva-mu)/safe
    if not np.isfinite(xt).all() or not np.isfinite(xv).all(): raise FloatingPointError('não-finito após z-score')
    return xt,xv,mu,safe,int(tiny.sum())


def fit_lda(xtr,ytr):
    texts=[]; shrink=False
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            model=LinearDiscriminantAnalysis(priors=PRIORS)
            model.fit(xtr,ytr)
        texts=[str(w.message) for w in caught]
        bad=any(any(tok in t.lower() for tok in ['singular','ill-conditioned','divide by zero','invalid value']) for t in texts)
        if bad: raise np.linalg.LinAlgError('warning numérico persistente: '+' | '.join(texts))
    except Exception as exc:
        shrink=True; texts.append(f'fallback_trigger={type(exc).__name__}: {exc}')
        model=LinearDiscriminantAnalysis(solver='lsqr',shrinkage='auto',priors=PRIORS)
        model.fit(xtr,ytr)
    return model,shrink,texts


def evaluate(subject,nch,pipeline,ws,ch):
    X=design_matrix(ws,ch,pipeline)
    tr=np.isin(ws.rep,sorted(TRAIN_REPS)); va=np.isin(ws.rep,sorted(VAL_REPS))
    assert not np.any(np.isin(ws.rep,sorted(FORBIDDEN_REPS)))
    xtr,ytr=X[tr],ws.y[tr]; xva,yva=X[va],ws.y[va]
    if set(np.unique(ytr))!=set(LABELS) or set(np.unique(yva))!=set(LABELS):
        raise ValueError(f'S{subject} {nch}ch {pipeline}: classes ausentes')
    xtrz,xvaz,mu,sigma,guards=zscore_train_only(xtr,xva)
    model,shrink,warns=fit_lda(xtrz,ytr)
    # Exact prior audit
    if not np.allclose(model.priors_,PRIORS,atol=0,rtol=0): raise AssertionError('priors != 0.25')
    pred=model.predict(xvaz)
    cm=confusion_matrix(yva,pred,labels=LABELS)
    f1s=f1_score(yva,pred,labels=LABELS,average=None,zero_division=0)
    it=1; ic=3
    row={
        'subject':subject,'channels':nch,'pipeline':pipeline,'n_features':X.shape[1],
        'n_train':int(tr.sum()),'n_val':int(va.sum()),
        'macro_f1':float(f1_score(yva,pred,labels=LABELS,average='macro',zero_division=0)),
        'balanced_accuracy':float(balanced_accuracy_score(yva,pred)),
        'accuracy':float(accuracy_score(yva,pred)),
        'shrinkage_used':bool(shrink),'sigma_guards':guards,'warnings':' || '.join(warns),
        'closed_to_thumb_n':int(cm[ic,it]),'thumb_to_closed_n':int(cm[it,ic]),
        'closed_to_thumb_rate':float(cm[ic,it]/cm[ic].sum()),
        'thumb_to_closed_rate':float(cm[it,ic]/cm[it].sum()),
        'prior_0':float(model.priors_[0]),'prior_1':float(model.priors_[1]),'prior_5':float(model.priors_[2]),'prior_6':float(model.priors_[3]),
    }
    for lab,sc in zip(LABELS,f1s): row[f'f1_{LABEL_NAMES[int(lab)]}']=float(sc)
    return row,cm


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--db5-zip',type=Path,required=True); ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    file_audit=audit_e2_files(a.db5_zip); file_audit.to_csv(a.out/'e2_file_audit.csv',index=False)
    rows=[]; cms={}; counts=[]; window_audit=[]
    with zipfile.ZipFile(a.db5_zip) as outer:
        for s in range(1,11):
            emg,y,rep,path=load_e2(outer,s)
            ws=segment_all_features(emg,y,rep)
            # Selected windows must contain exactly target labels and only train/val reps.
            if set(np.unique(ws.y))!=set(LABELS): raise AssertionError(f'S{s}: selected labels != target')
            if not set(np.unique(ws.rep)).issubset(ALLOWED_REPS): raise AssertionError(f'S{s}: repetition leak')
            window_audit.append({'subject':s,'file':path,'n_windows':len(ws.y),'selected_labels':','.join(map(str,np.unique(ws.y))),
                                 'selected_reps':','.join(map(str,np.unique(ws.rep))), 'forbidden_2_5_present':bool(np.any(np.isin(ws.rep,[2,5])))})
            for nch,ch in CHANNEL_SETS.items():
                # Same window identities necessarily feed both pipelines; record once per channel config.
                for lab in LABELS:
                    for rr in sorted(ALLOWED_REPS):
                        counts.append({'subject':s,'channels':nch,'class':int(lab),'rep':rr,'n_windows':int(np.sum((ws.y==lab)&(ws.rep==rr)))})
                for pipe in ['LDA-RMS','LDA-TD']:
                    row,cm=evaluate(s,nch,pipe,ws,ch); rows.append(row); cms[f'S{s}_{pipe}_{nch}ch']=cm.tolist()
    detail=pd.DataFrame(rows).sort_values(['channels','pipeline','subject'])
    detail.to_csv(a.out/'results_by_subject.csv',index=False)
    pd.DataFrame(counts).to_csv(a.out/'window_counts.csv',index=False)
    pd.DataFrame(window_audit).to_csv(a.out/'window_audit.csv',index=False)
    metric_cols=['macro_f1','balanced_accuracy','accuracy','f1_repouso','f1_thumbs_up','f1_mao_aberta','f1_mao_fechada','closed_to_thumb_rate','thumb_to_closed_rate']
    summary=detail.groupby(['channels','pipeline'])[metric_cols].agg(['mean','std'])
    summary.columns=[f'{a}_{b}' for a,b in summary.columns]; summary=summary.reset_index()
    summary.to_csv(a.out/'summary.csv',index=False)
    with open(a.out/'confusion_matrices.json','w',encoding='utf-8') as f:
        json.dump({'labels':LABELS.tolist(),'label_names':LABEL_NAMES,'matrices':cms},f,ensure_ascii=False,indent=2)
    audit={
        'exercise':'E2 exclusively','file_pattern':'Sx_E2_A1.mat','raw_restimulus_values_by_subject':{str(r.subject):[int(x) for x in str(r.restimulus_values).split(',')] for _,r in file_audit.iterrows()},
        'selected_classes':LABELS.tolist(),'train_repetitions':sorted(TRAIN_REPS),'validation_repetitions':sorted(VAL_REPS),'forbidden_test_repetitions':sorted(FORBIDDEN_REPS),
        'window_samples':WINDOW,'step_samples':STEP,'channel_sets_one_based':{str(k):[x+1 for x in v] for k,v in CHANNEL_SETS.items()},
        'priors':PRIORS.tolist(),'sigma_epsilon':SIGMA_EPS,
        'assertions':{
            'all_files_e2':bool(file_audit.is_e2.all()),'all_target_labels_present_in_raw_e2':bool(file_audit.target_labels_ok.all()),
            'selected_labels_exactly_0_1_5_6':True,'repetitions_2_5_absent_from_windows_features_normalization_validation':True,
            'no_window_crosses_class_or_repetition_boundary':True,'zscore_fit_train_only':True,'equal_priors_exact':True,'same_windows_channels_for_rms_td':True,
        },
        'shrinkage_uses':int(detail.shrinkage_used.sum()),'sigma_guards_total':int(detail.sigma_guards.sum()),
        'baseline_threshold_available':False,
    }
    with open(a.out/'audit.json','w',encoding='utf-8') as f: json.dump(audit,f,ensure_ascii=False,indent=2)
    print(summary.to_string(index=False))
    print('shrinkage uses',int(detail.shrinkage_used.sum()),'sigma guards',int(detail.sigma_guards.sum()))

if __name__=='__main__': main()

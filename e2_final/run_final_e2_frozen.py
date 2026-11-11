#!/usr/bin/env python3
"""NinaPro DB5 E2 — final frozen test.

Executes exactly once on test repetitions 2 and 5 after protocol freeze.
Methods: Threshold/Hamming, LDA-RMS, LDA-TD.
Train: repetitions 1,3,4 only. Test: repetitions 2,5 only.
Repetition 6 is completely excluded from segmentation/features/training/test.
"""
from __future__ import annotations
import argparse, io, json, re, warnings, zipfile
from pathlib import Path
from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy.io import loadmat
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import f1_score, balanced_accuracy_score, accuracy_score

LABELS=np.array([0,1,5,6], dtype=int)
LABEL_NAMES={0:'repouso',1:'thumbs_up',5:'mao_aberta',6:'mao_fechada'}
TRAIN_REPS={1,3,4}; TEST_REPS={2,5}; FORBIDDEN_REPS={6}; ALLOWED_REPS=TRAIN_REPS|TEST_REPS
CHANNEL_SETS={1:[0],2:[0,4],4:[0,2,4,6],8:list(range(8))}
WINDOW=40; STEP=20; PRIORS=np.array([0.25,0.25,0.25,0.25],float); SIGMA_EPS=1e-12

@dataclass
class WindowSet:
    starts: np.ndarray
    y: np.ndarray
    rep: np.ndarray
    rms8: np.ndarray
    mav8: np.ndarray
    wl8: np.ndarray


def _open_subject_inner(outer:zipfile.ZipFile, subject:int)->zipfile.ZipFile:
    key=f's{subject}.zip'
    names={Path(n).name.lower():n for n in outer.namelist()}
    if key.lower() not in names: raise FileNotFoundError(key)
    return zipfile.ZipFile(io.BytesIO(outer.read(names[key.lower()])))


def load_e2(outer:zipfile.ZipFile, subject:int):
    with _open_subject_inner(outer,subject) as inner:
        target=f'S{subject}_E2_A1.mat'
        hits=[n for n in inner.namelist() if Path(n).name.lower()==target.lower()]
        if len(hits)!=1: raise FileNotFoundError(f'S{subject}: {hits}')
        d=loadmat(io.BytesIO(inner.read(hits[0])), variable_names=['emg','restimulus','rerepetition'])
    emg=np.asarray(d['emg'],float)
    y=np.asarray(d['restimulus']).ravel().astype(int)
    rep=np.asarray(d['rerepetition']).ravel().astype(int)
    if emg.shape[0]!=y.size or y.size!=rep.size: raise ValueError(f'S{subject}: length mismatch')
    if emg.shape[1]<8: raise ValueError(f'S{subject}: <8 EMG channels')
    return emg[:,:8],y,rep,hits[0]


def audit_raw(db5:Path)->pd.DataFrame:
    rows=[]
    with zipfile.ZipFile(db5) as outer:
        for s in range(1,11):
            emg,y,rep,path=load_e2(outer,s)
            vals=np.unique(y).astype(int).tolist(); reps=np.unique(rep).astype(int).tolist()
            rows.append({'subject':s,'file':path,'is_e2':bool(re.search(r'_E2_A1\.mat$',Path(path).name,re.I)),
                         'n_samples':len(y),'n_channels_raw_used':8,
                         'restimulus_values':','.join(map(str,vals)), 'rerepetition_values':','.join(map(str,reps)),
                         'target_classes_present':set(LABELS.tolist()).issubset(vals)})
    df=pd.DataFrame(rows)
    assert df.is_e2.all() and df.target_classes_present.all()
    return df


def segment_features(emg,y,rep)->WindowSet:
    starts=[]; ys=[]; rs=[]; rms=[]; mav=[]; wl=[]
    # hard firewall: only train/test repetitions can ever be indexed below; rep6 is not segmented
    eligible=np.isin(rep,sorted(ALLOWED_REPS))
    edges=np.diff(np.r_[False,eligible,False].astype(np.int8))
    for bs,be in zip(np.flatnonzero(edges==1),np.flatnonzero(edges==-1)):
        yb=y[bs:be]; rb=rep[bs:be]
        change=np.r_[True,(yb[1:]!=yb[:-1])|(rb[1:]!=rb[:-1])]
        run_st=np.flatnonzero(change); run_en=np.r_[run_st[1:],len(yb)]
        for a,b in zip(run_st,run_en):
            lab=int(yb[a]); rr=int(rb[a])
            if rr not in ALLOWED_REPS or rr in FORBIDDEN_REPS: raise AssertionError('forbidden repetition')
            if lab not in LABELS: continue
            s0=bs+int(a); e0=bs+int(b)
            for st in range(s0,e0-WINDOW+1,STEP):
                en=st+WINDOW
                if not (np.all(y[st:en]==lab) and np.all(rep[st:en]==rr)):
                    raise AssertionError('window crossed class/repetition boundary')
                w=emg[st:en]
                starts.append(st); ys.append(lab); rs.append(rr)
                rms.append(np.sqrt(np.mean(w*w,axis=0)))
                mav.append(np.mean(np.abs(w),axis=0))
                wl.append(np.sum(np.abs(np.diff(w,axis=0)),axis=0))
    ws=WindowSet(np.asarray(starts,int),np.asarray(ys,int),np.asarray(rs,int),
                 np.asarray(rms,float),np.asarray(mav,float),np.asarray(wl,float))
    assert not np.any(ws.rep==6)
    assert set(np.unique(ws.rep)).issubset(ALLOWED_REPS)
    assert set(np.unique(ws.y))==set(LABELS)
    return ws


def majority_bits(a):
    # frozen convention: exact 50/50 resolves to 0
    return (np.mean(a,axis=0)>0.5).astype(np.int8)


def baseline_templates(bits,y,rep):
    templates={}; rep_templates={}
    for lab in LABELS:
        one=[]
        for rr in sorted(TRAIN_REPS):
            m=(y==lab)&(rep==rr)
            if not np.any(m): raise ValueError(f'no train windows class={lab}, rep={rr}')
            t=majority_bits(bits[m]); rep_templates[(int(lab),int(rr))]=t; one.append(t)
        templates[int(lab)]=majority_bits(np.vstack(one))
    return templates,rep_templates


def hamming_predict(bits,templates):
    T=np.vstack([templates[int(l)] for l in LABELS])
    dist=np.sum(bits[:,None,:]!=T[None,:,:],axis=2)
    ismin=dist==dist.min(axis=1)[:,None]
    pred=np.full(len(bits),-1,int)
    unique=ismin.sum(axis=1)==1
    pred[unique]=LABELS[np.argmax(ismin[unique],axis=1)]
    return pred,dist


def confusion_with_reject(y,pred):
    cols=list(LABELS)+[-1]; cm=np.zeros((4,5),int)
    ri={int(v):i for i,v in enumerate(LABELS)}; ci={int(v):i for i,v in enumerate(cols)}
    for a,b in zip(y,pred): cm[ri[int(a)],ci[int(b)]]+=1
    return cm


def confusion_4(y,pred):
    cm=np.zeros((4,4),int); idx={int(v):i for i,v in enumerate(LABELS)}
    for a,b in zip(y,pred): cm[idx[int(a)],idx[int(b)]]+=1
    return cm


def design(ws,ch,method):
    if method=='LDA-RMS': return ws.rms8[:,ch]
    if method=='LDA-TD':
        parts=[]
        for c in ch: parts.extend([ws.rms8[:,c],ws.mav8[:,c],ws.wl8[:,c]])
        return np.column_stack(parts)
    raise ValueError(method)


def zscore_train_only(xtr,xte):
    mu=xtr.mean(axis=0); sd=xtr.std(axis=0,ddof=0)
    tiny=(~np.isfinite(sd))|(np.abs(sd)<=SIGMA_EPS)
    safe=sd.copy(); safe[tiny]=1.0
    a=(xtr-mu)/safe; b=(xte-mu)/safe
    if not np.isfinite(a).all() or not np.isfinite(b).all(): raise FloatingPointError('nonfinite zscore')
    return a,b,mu,safe,int(tiny.sum())


def fit_lda_strict(x,y):
    # Frozen protocol: do NOT substitute shrinkage silently. Any real numeric issue aborts.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        model=LinearDiscriminantAnalysis(priors=PRIORS)
        model.fit(x,y)
    texts=[str(w.message) for w in caught]
    bad=[t for t in texts if any(tok in t.lower() for tok in ['singular','ill-conditioned','divide by zero','invalid value'])]
    if bad: raise RuntimeError('LDA numeric instability; frozen protocol requires stop before fallback: '+' | '.join(bad))
    if not np.allclose(model.priors_,PRIORS,atol=0,rtol=0): raise AssertionError('priors not exactly 0.25')
    return model,texts


def metrics_common(y,pred,cm4=None):
    if cm4 is None: cm4=confusion_4(y,pred)
    f1s=f1_score(y,pred,labels=LABELS,average=None,zero_division=0)
    iT=1;iC=3
    row={'macro_f1':float(f1_score(y,pred,labels=LABELS,average='macro',zero_division=0)),
         'balanced_accuracy':float(balanced_accuracy_score(y,pred)),
         'accuracy':float(accuracy_score(y,pred)),
         'closed_to_thumb_n':int(cm4[iC,iT]),'thumb_to_closed_n':int(cm4[iT,iC]),
         'closed_to_thumb_rate':float(cm4[iC,iT]/cm4[iC].sum()),
         'thumb_to_closed_rate':float(cm4[iT,iC]/cm4[iT].sum())}
    for lab,sc in zip(LABELS,f1s): row[f'f1_{LABEL_NAMES[int(lab)]}']=float(sc)
    return row


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--db5-zip',type=Path,required=True); ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    raw=audit_raw(a.db5_zip); raw.to_csv(a.out/'raw_e2_audit.csv',index=False)
    rows=[]; thresholds=[]; window_rows=[]; count_rows=[]; cms={}; numeric_warnings=[]
    with zipfile.ZipFile(a.db5_zip) as outer:
      for s in range(1,11):
        emg,yraw,repraw,path=load_e2(outer,s); ws=segment_features(emg,yraw,repraw)
        tr=np.isin(ws.rep,sorted(TRAIN_REPS)); te=np.isin(ws.rep,sorted(TEST_REPS))
        assert set(np.unique(ws.rep[tr]))==TRAIN_REPS and set(np.unique(ws.rep[te]))==TEST_REPS
        assert not np.any(ws.rep==6)
        window_rows.append({'subject':s,'file':path,'n_windows_total':len(ws.y),'n_train':int(tr.sum()),'n_test':int(te.sum()),
                            'labels':','.join(map(str,np.unique(ws.y))), 'train_reps':','.join(map(str,np.unique(ws.rep[tr]))),
                            'test_reps':','.join(map(str,np.unique(ws.rep[te]))),'rep6_present':False})
        for nch,ch in CHANNEL_SETS.items():
          # exact same window identities for all three methods
          for rr in sorted(ALLOWED_REPS):
            for lab in LABELS:
              count_rows.append({'subject':s,'channels':nch,'rep':rr,'class':int(lab),'n_windows':int(np.sum((ws.rep==rr)&(ws.y==lab)))})
          # Threshold/Hamming
          X=ws.rms8[:,ch]
          rest_train=tr&(ws.y==0)
          mu=X[rest_train].mean(axis=0); sd=X[rest_train].std(axis=0,ddof=0); th=mu+3*sd
          bits=(X>th).astype(np.int8)
          templates,rep_templates=baseline_templates(bits[tr],ws.y[tr],ws.rep[tr])
          pred,dist=hamming_predict(bits[te],templates); yt=ws.y[te]
          cmr=confusion_with_reject(yt,pred)
          # 4x4 correct-pred confusion only; rejected predictions are omitted from columns but remain in denominators via y counts for directional rates handled below
          cm4=np.zeros((4,4),int)
          for i,lab in enumerate(LABELS):
            for j,plab in enumerate(LABELS): cm4[i,j]=int(np.sum((yt==lab)&(pred==plab)))
          m=metrics_common(yt,pred,cm4)
          m.update({'subject':s,'channels':nch,'method':'Threshold/Hamming','n_features':nch,
                    'n_train':int(tr.sum()),'n_test':int(te.sum()),'sigma_guards':0,'numeric_warnings':'',
                    'rejection_rate':float(np.mean(pred==-1)),'coverage':float(np.mean(pred!=-1)),
                    'selective_accuracy_nonrejected':float(accuracy_score(yt[pred!=-1],pred[pred!=-1])) if np.any(pred!=-1) else np.nan})
          # directional rates must include rejected samples in true-class denominator
          iT=1;iC=3
          m['closed_to_thumb_rate']=float(cmr[iC,iT]/cmr[iC].sum()); m['thumb_to_closed_rate']=float(cmr[iT,iC]/cmr[iT].sum())
          rows.append(m); cms[f'S{s}_{nch}ch_Threshold_Hamming']=cmr.tolist()
          for j,c in enumerate(ch):
            thresholds.append({'subject':s,'channels':nch,'channel_one_based':c+1,'rest_mu_rms':float(mu[j]),'rest_sd_rms':float(sd[j]),'threshold_mu_plus_3sd':float(th[j]),
                               **{f'template_{lab}':int(templates[int(lab)][j]) for lab in LABELS}})
          # LDAs
          for method in ['LDA-RMS','LDA-TD']:
            DX=design(ws,ch,method); xtr,xte=DX[tr],DX[te]; ytr=ws.y[tr]
            xtrz,xtez,zmu,zsd,guards=zscore_train_only(xtr,xte)
            model,warns=fit_lda_strict(xtrz,ytr); numeric_warnings.extend([{'subject':s,'channels':nch,'method':method,'warning':w} for w in warns])
            pp=model.predict(xtez); cm=confusion_4(yt,pp); mm=metrics_common(yt,pp,cm)
            mm.update({'subject':s,'channels':nch,'method':method,'n_features':DX.shape[1],
                       'n_train':int(tr.sum()),'n_test':int(te.sum()),'sigma_guards':guards,'numeric_warnings':' || '.join(warns),
                       'rejection_rate':0.0,'coverage':1.0,'selective_accuracy_nonrejected':float(accuracy_score(yt,pp)),
                       'prior_0':float(model.priors_[0]),'prior_1':float(model.priors_[1]),'prior_5':float(model.priors_[2]),'prior_6':float(model.priors_[3])})
            rows.append(mm); cms[f'S{s}_{nch}ch_{method.replace("-","_")}']=cm.tolist()
    detail=pd.DataFrame(rows).sort_values(['channels','method','subject'])
    detail.to_csv(a.out/'final_results_by_subject.csv',index=False)
    pd.DataFrame(thresholds).to_csv(a.out/'thresholds_and_templates_frozen.csv',index=False)
    pd.DataFrame(window_rows).to_csv(a.out/'window_audit.csv',index=False)
    pd.DataFrame(count_rows).to_csv(a.out/'window_counts_by_subject_rep_class.csv',index=False)
    pd.DataFrame(numeric_warnings).to_csv(a.out/'lda_warnings.csv',index=False)
    metrics=['macro_f1','balanced_accuracy','accuracy','f1_repouso','f1_thumbs_up','f1_mao_aberta','f1_mao_fechada','closed_to_thumb_rate','thumb_to_closed_rate','rejection_rate','coverage','selective_accuracy_nonrejected']
    summary=detail.groupby(['channels','method'])[metrics].agg(['mean','std'])
    summary.columns=[f'{x}_{y}' for x,y in summary.columns]; summary=summary.reset_index()
    summary.to_csv(a.out/'final_summary_mean_std.csv',index=False)
    # wide primary table + gains
    p=detail.groupby(['channels','method']).macro_f1.mean().unstack('method').reset_index()
    p['gain_TD_minus_Threshold']=p['LDA-TD']-p['Threshold/Hamming']; p['gain_TD_minus_RMS']=p['LDA-TD']-p['LDA-RMS']
    p.to_csv(a.out/'macro_f1_primary_comparison.csv',index=False)
    # evolution increments by method
    evo=[]
    for method,g in detail.groupby('method'):
        means=g.groupby('channels').macro_f1.mean().sort_index()
        vals=means.to_dict()
        evo.append({'method':method,'macro_f1_1ch':vals[1],'macro_f1_2ch':vals[2],'macro_f1_4ch':vals[4],'macro_f1_8ch':vals[8],
                    'gain_1_to_2':vals[2]-vals[1],'gain_2_to_4':vals[4]-vals[2],'gain_4_to_8':vals[8]-vals[4],'gain_1_to_8':vals[8]-vals[1]})
    pd.DataFrame(evo).to_csv(a.out/'channel_evolution.csv',index=False)
    with open(a.out/'confusion_matrices.json','w') as f:
        json.dump({'label_order':[0,1,5,6], 'baseline_columns':[0,1,5,6,-1], 'reject_label':-1, 'matrices':cms},f,indent=2)
    audit={
      'status':'PASS','execution_scope':'final frozen test','exercise':'E2 exclusively','subjects':list(range(1,11)),
      'classes':[0,1,5,6],'train_repetitions':[1,3,4],'test_repetitions':[2,5],'rep6_used':False,
      'window_samples':40,'step_samples':20,'sampling_hz':200,'channel_sets_one_based':{str(k):[c+1 for c in v] for k,v in CHANNEL_SETS.items()},
      'threshold_rule':'mean(train-rest RMS)+3*std(train-rest RMS), per subject/channel; training only',
      'baseline_template_rule':'strict majority within each training repetition; exact 50/50=>0; final strict majority across reps 1,3,4',
      'baseline_classifier':'minimum Hamming; tie for minimum=>reject (-1)',
      'lda_rms_features':['RMS'],'lda_td_features':['RMS','MAV','WL'],'zscore_fit':'training repetitions 1,3,4 only',
      'lda_priors':[0.25,0.25,0.25,0.25],'shrinkage_used':False,'subsampling_used':False,
      'sigma_guards_total':int(detail.loc[detail.method.str.startswith('LDA'),'sigma_guards'].sum()),
      'numeric_instability_detected':False,
      'assertions':{
        'all_files_e2':bool(raw.is_e2.all()),'selected_classes_only_0_1_5_6':True,'train_only_1_3_4':True,'test_only_2_5':True,'rep6_excluded':True,
        'no_window_crosses_class_or_repetition':True,'zscore_train_only':True,'thresholds_train_rest_only':True,'same_windows_and_channels_all_methods':True,
        'no_post_test_tuning':True,'lda_priors_exact_0_25_each':True,'baseline_50_50_tie_bit_zero':True
      }
    }
    with open(a.out/'FINAL_PROTOCOL_AUDIT.json','w',encoding='utf-8') as f: json.dump(audit,f,ensure_ascii=False,indent=2)
    print('\nPRIMARY MACRO-F1\n',p.to_string(index=False))
    print('\nSUMMARY\n',summary[['channels','method','macro_f1_mean','macro_f1_std','balanced_accuracy_mean','balanced_accuracy_std']].to_string(index=False))
    print('\nSigma guards:',audit['sigma_guards_total'],' Numeric instability:',audit['numeric_instability_detected'])

if __name__=='__main__': main()

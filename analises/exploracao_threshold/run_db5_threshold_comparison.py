from pathlib import Path
import numpy as np, pandas as pd
from scipy.io import loadmat
from sklearn.metrics import confusion_matrix
import json, itertools
import argparse

# Apenas adaptação das pastas de entrada/saída para computadores externos.
parser = argparse.ArgumentParser(description='Comparação exploratória auxiliar A–D, distinta do teste final congelado.')
parser.add_argument('--extracted-root', type=Path, required=True, help='Pasta com s1/S1_E2_A1.mat ... s10/S10_E2_A1.mat')
parser.add_argument('--out', type=Path, required=True, help='Pasta destinada às saídas da exploração')
args = parser.parse_args()
ROOT = args.extracted_root
OUT = args.out
OUT.mkdir(parents=True, exist_ok=True)
CLASSES=[0,1,5,6]
CLASS_NAMES={0:'repouso',1:'thumbs_up',5:'mao_aberta',6:'mao_fechada'}
TRAIN_REPS=[1,3,4]; VAL_REP=6
WIN=40; STEP=20
SUBSETS={1:[0],2:[0,4],4:[0,2,4,6],8:list(range(8))}
CONFIGS={
 'A':('MAV','mu+3sigma'),
 'B':('MAV','P95'),
 'C':('RMS','mu+3sigma'),
 'D':('RMS','P95'),
}

def contiguous_windows(emg, y, r, lab, rep):
    mask=(y==lab)&(r==rep)
    idx=np.flatnonzero(mask)
    if idx.size==0: return np.empty((0,WIN,8),dtype=np.float32)
    splits=np.where(np.diff(idx)>1)[0]+1
    runs=np.split(idx,splits)
    ws=[]
    for run in runs:
        n=len(run)
        if n<WIN: continue
        start0=run[0]
        for off in range(0,n-WIN+1,STEP):
            inds=np.arange(start0+off,start0+off+WIN)
            # safety: ensure contiguous membership
            if np.all(mask[inds]): ws.append(emg[inds,:8])
    return np.stack(ws) if ws else np.empty((0,WIN,8),dtype=np.float32)

def feat(w, kind):
    if kind=='MAV': return np.mean(np.abs(w),axis=1)
    return np.sqrt(np.mean(np.square(w,dtype=np.float64),axis=1))

def f1_stats(ytrue, ypred):
    rows=[]; f1s=[]
    for c in CLASSES:
        tp=np.sum((ytrue==c)&(ypred==c)); fp=np.sum((ytrue!=c)&(ypred==c)); fn=np.sum((ytrue==c)&(ypred!=c))
        pr=tp/(tp+fp) if tp+fp else 0.0; rc=tp/(tp+fn) if tp+fn else 0.0
        f1=2*pr*rc/(pr+rc) if pr+rc else 0.0
        f1s.append(f1); rows.append((c,pr,rc,f1,tp,fp,fn))
    return float(np.mean(f1s)),rows

def majority(bits):
    # strict simple majority; exact 50/50 tie -> inactive (0), conservative and deterministic
    return (np.mean(bits,axis=0)>0.5).astype(np.uint8)

subject_cache={}
label_audit=[]
for s in range(1,11):
    p=ROOT/f's{s}'/f'S{s}_E2_A1.mat'
    d=loadmat(p)
    emg=d['emg'].astype(np.float32)
    y=d['restimulus'].ravel().astype(int); r=d['rerepetition'].ravel().astype(int)
    freq=int(d['frequency'].ravel()[0])
    audit={'subject':s,'file':p.name,'n_samples':len(y),'freq_hz':freq,'stim_min':int(y.min()),'stim_max':int(y.max())}
    for c in CLASSES:
        for rr in TRAIN_REPS+[VAL_REP]: audit[f'n_{c}_rep{rr}']=int(np.sum((y==c)&(r==rr)))
    label_audit.append(audit)
    wins={(c,rr):contiguous_windows(emg,y,r,c,rr) for c in CLASSES for rr in TRAIN_REPS+[VAL_REP]}
    subject_cache[s]=wins

pd.DataFrame(label_audit).to_csv(OUT/'label_audit.csv',index=False)

summary_rows=[]; indiv_rows=[]; class_rows=[]; cm_rows=[]; template_rows=[]; stability_rows=[]; activation_rows=[]; pair_rows=[]; identical_rows=[]

for s,wins in subject_cache.items():
  for cfg,(fk,thr_rule) in CONFIGS.items():
    rest_train=np.concatenate([feat(wins[(0,rr)],fk) for rr in TRAIN_REPS],axis=0)
    if thr_rule=='mu+3sigma': T=rest_train.mean(axis=0)+3*rest_train.std(axis=0,ddof=0)
    else: T=np.percentile(rest_train,95,axis=0)
    # features / bits cache
    fb={}
    for c in CLASSES:
      for rr in TRAIN_REPS+[VAL_REP]:
        F=feat(wins[(c,rr)],fk); B=(F>T).astype(np.uint8); fb[(c,rr)]=(F,B)
        for ch in range(8):
          activation_rows.append({'subject':s,'config':cfg,'feature':fk,'threshold_rule':thr_rule,'class':c,'class_name':CLASS_NAMES[c],'repetition':rr,'split':'train' if rr in TRAIN_REPS else 'validation','channel':ch+1,'activation_rate':float(B[:,ch].mean()) if len(B) else np.nan,'n_windows':len(B),'threshold':float(T[ch])})
    for nch,chs in SUBSETS.items():
      reps_templates={}
      finals={}
      for c in CLASSES:
        rt=[]
        for rr in TRAIN_REPS:
          b=fb[(c,rr)][1][:,chs]
          t=majority(b); rt.append(t); reps_templates[(c,rr)]=t
        final=majority(np.stack(rt))
        finals[c]=final
        template_rows.append({'subject':s,'config':cfg,'channels_n':nch,'class':c,'class_name':CLASS_NAMES[c],'template_bits':' '.join(map(str,final.tolist()))})
        for rr,t in zip(TRAIN_REPS,rt):
          stability_rows.append({'subject':s,'config':cfg,'channels_n':nch,'class':c,'class_name':CLASS_NAMES[c],'repetition':rr,'hamming_to_final':int(np.sum(t!=final))})
      # identical pairs
      for c1,c2 in itertools.combinations(CLASSES,2):
        dist=int(np.sum(finals[c1]!=finals[c2]))
        identical_rows.append({'subject':s,'config':cfg,'channels_n':nch,'class1':c1,'class2':c2,'class1_name':CLASS_NAMES[c1],'class2_name':CLASS_NAMES[c2],'hamming_between_templates':dist,'identical':int(dist==0)})
      # validation concat class windows
      yt=[]; yp=[]
      for c in CLASSES:
        b=fb[(c,VAL_REP)][1][:,chs]
        templates=np.stack([finals[k] for k in CLASSES])
        dists=np.sum(b[:,None,:]!=templates[None,:,:],axis=2)
        mins=dists.min(axis=1); tie=np.sum(dists==mins[:,None],axis=1)>1
        pred=np.array([CLASSES[i] for i in dists.argmin(axis=1)],dtype=int)
        pred[tie]=-1
        yt.append(np.full(len(pred),c,dtype=int)); yp.append(pred)
      yt=np.concatenate(yt); yp=np.concatenate(yp)
      acc=float(np.mean(yt==yp)); rej=float(np.mean(yp==-1)); cov=1-rej
      accepted=yp!=-1; acc_acc=float(np.mean(yt[accepted]==yp[accepted])) if accepted.any() else np.nan
      macro, stats=f1_stats(yt,yp)
      indiv_rows.append({'subject':s,'config':cfg,'feature':fk,'threshold_rule':thr_rule,'channels_n':nch,'accuracy_global':acc,'macro_f1':macro,'rejection_rate':rej,'coverage':cov,'accuracy_accepted':acc_acc,'n_validation_windows':len(yt)})
      for c,pr,rc,f1,tp,fp,fn in stats:
        class_rows.append({'subject':s,'config':cfg,'channels_n':nch,'class':c,'class_name':CLASS_NAMES[c],'precision':pr,'recall':rc,'f1':f1,'tp':tp,'fp':fp,'fn':fn})
      cm=confusion_matrix(yt,yp,labels=CLASSES+[-1])
      for i,truec in enumerate(CLASSES):
        for j,predc in enumerate(CLASSES+[-1]):
          cm_rows.append({'subject':s,'config':cfg,'channels_n':nch,'true_class':truec,'true_name':CLASS_NAMES[truec],'pred_class':predc,'pred_name':'rejeicao' if predc==-1 else CLASS_NAMES[predc],'count':int(cm[i,j])})
      for truec,predc,direction in [(6,1,'fechada->thumbs_up'),(1,6,'thumbs_up->fechada')]:
        den=np.sum(yt==truec); num=np.sum((yt==truec)&(yp==predc))
        pair_rows.append({'subject':s,'config':cfg,'channels_n':nch,'direction':direction,'rate':float(num/den) if den else np.nan,'count':int(num),'denominator':int(den)})

indiv=pd.DataFrame(indiv_rows)
# aggregate subject-level metrics (unweighted mean/std, as protocol asks across participants)
agg=indiv.groupby(['config','feature','threshold_rule','channels_n']).agg(
 accuracy_mean=('accuracy_global','mean'),accuracy_std=('accuracy_global','std'),
 macro_f1_mean=('macro_f1','mean'),macro_f1_std=('macro_f1','std'),
 rejection_mean=('rejection_rate','mean'),rejection_std=('rejection_rate','std'),
 coverage_mean=('coverage','mean'),coverage_std=('coverage','std'),
 accepted_accuracy_mean=('accuracy_accepted','mean'),accepted_accuracy_std=('accuracy_accepted','std')
).reset_index()
agg.to_csv(OUT/'summary_AD_channels.csv',index=False)
indiv.to_csv(OUT/'individual_metrics.csv',index=False)
pd.DataFrame(class_rows).to_csv(OUT/'class_f1.csv',index=False)
pd.DataFrame(cm_rows).to_csv(OUT/'confusion_matrices_long.csv',index=False)
pd.DataFrame(template_rows).to_csv(OUT/'templates.csv',index=False)
pd.DataFrame(stability_rows).to_csv(OUT/'template_stability.csv',index=False)
pd.DataFrame(activation_rows).to_csv(OUT/'activation_rates.csv',index=False)
pd.DataFrame(pair_rows).to_csv(OUT/'close_vs_thumb_confusion.csv',index=False)
pd.DataFrame(identical_rows).to_csv(OUT/'template_pair_distances.csv',index=False)

# Aggregated confusion matrices across subjects
cm_df=pd.DataFrame(cm_rows)
cm_agg=cm_df.groupby(['config','channels_n','true_class','true_name','pred_class','pred_name'],as_index=False)['count'].sum()
cm_agg.to_csv(OUT/'confusion_matrices_aggregated.csv',index=False)

# compact findings json
pair_df=pd.DataFrame(pair_rows)
idf=pd.DataFrame(identical_rows)
stab=pd.DataFrame(stability_rows)
find={}
find['best_by_macro_f1_per_channels']=agg.sort_values(['channels_n','macro_f1_mean'],ascending=[True,False]).groupby('channels_n').head(1).to_dict('records')
find['pair_confusion_means']=pair_df.groupby(['config','channels_n','direction'])['rate'].mean().reset_index().to_dict('records')
find['identical_counts']=idf.groupby(['config','channels_n'])['identical'].sum().reset_index().to_dict('records')
find['close_thumb_identical_counts']=idf[((idf.class1==1)&(idf.class2==6))|((idf.class1==6)&(idf.class2==1))].groupby(['config','channels_n'])['identical'].sum().reset_index().to_dict('records')
find['stability_mean_hamming']=stab.groupby(['config','channels_n'])['hamming_to_final'].mean().reset_index().to_dict('records')
with open(OUT/'findings.json','w') as f: json.dump(find,f,indent=2)
print(agg.to_string(index=False))

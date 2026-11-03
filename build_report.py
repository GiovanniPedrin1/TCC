from pathlib import Path
import pandas as pd, numpy as np, json
import matplotlib.pyplot as plt

base=Path('/mnt/data/e2_final/results')
out=Path('/mnt/data/e2_final')
d=pd.read_csv(base/'final_results_by_subject.csv')
s=pd.read_csv(base/'final_summary_mean_std.csv')
p=pd.read_csv(base/'macro_f1_primary_comparison.csv')
e=pd.read_csv(base/'channel_evolution.csv')
methods=['Threshold/Hamming','LDA-RMS','LDA-TD']
chs=[1,2,4,8]

# Plot: one chart, default matplotlib colors/styles only.
fig,ax=plt.subplots(figsize=(8,5))
for method in methods:
    g=s[s.method==method].set_index('channels').loc[chs]
    ax.errorbar(chs,g['macro_f1_mean'],yerr=g['macro_f1_std'],marker='o',capsize=4,label=method)
ax.set_xlabel('Número de canais')
ax.set_ylabel('Macro-F1 (média ± DP entre participantes)')
ax.set_xticks(chs)
ax.set_ylim(0,1)
ax.grid(True,alpha=0.25)
ax.legend()
fig.tight_layout()
fig.savefig(out/'macro_f1_vs_channels.png',dpi=200)
plt.close(fig)

# Aggregate confusion matrices and normalized forms for descriptive visualization/reporting.
with open(base/'confusion_matrices.json') as f: cmj=json.load(f)
rows=[0,1,5,6]
for ch in chs:
  for method in methods:
    keym=method.replace('-','_') if method!='Threshold/Hamming' else 'Threshold_Hamming'
    arr=[]
    for sub in range(1,11):
      key=f'S{sub}_{ch}ch_{keym}'
      arr.append(np.array(cmj['matrices'][key],dtype=int))
    cm=sum(arr)
    if method=='Threshold/Hamming':
      cols=[0,1,5,6,-1]
    else:
      cols=[0,1,5,6]
    pd.DataFrame(cm,index=rows,columns=cols).to_csv(out/f'cm_{ch}ch_{keym}_counts.csv')
    denom=cm.sum(axis=1,keepdims=True)
    norm=np.divide(cm,denom,out=np.zeros_like(cm,dtype=float),where=denom!=0)
    pd.DataFrame(norm,index=rows,columns=cols).to_csv(out/f'cm_{ch}ch_{keym}_row_normalized.csv')

# helper
fmt=lambda x: f'{x:.4f}'.replace('.',',')
pm=lambda m,sd: f'{m:.4f} ± {sd:.4f}'.replace('.',',')

# tables
prim=[]
for ch in chs:
    r={'Canais':ch}
    for method in methods:
        q=s[(s.channels==ch)&(s.method==method)].iloc[0]
        r[method]=pm(q.macro_f1_mean,q.macro_f1_std)
    pr=p[p.channels==ch].iloc[0]
    r['Δ TD−Threshold']=fmt(pr.gain_TD_minus_Threshold)
    r['Δ TD−RMS']=fmt(pr.gain_TD_minus_RMS)
    prim.append(r)
prim=pd.DataFrame(prim)

ba=[]
for ch in chs:
    for method in methods:
        q=s[(s.channels==ch)&(s.method==method)].iloc[0]
        ba.append({'Canais':ch,'Método':method,'Balanced accuracy':pm(q.balanced_accuracy_mean,q.balanced_accuracy_std),'Acurácia':pm(q.accuracy_mean,q.accuracy_std)})
ba=pd.DataFrame(ba)

f1=[]
for ch in chs:
    for method in methods:
      q=s[(s.channels==ch)&(s.method==method)].iloc[0]
      f1.append({'Canais':ch,'Método':method,'Repouso':pm(q.f1_repouso_mean,q.f1_repouso_std),'Thumbs up':pm(q.f1_thumbs_up_mean,q.f1_thumbs_up_std),'Mão aberta':pm(q.f1_mao_aberta_mean,q.f1_mao_aberta_std),'Mão fechada':pm(q.f1_mao_fechada_mean,q.f1_mao_fechada_std)})
f1=pd.DataFrame(f1)

conf=[]
for ch in chs:
  for method in methods:
    q=s[(s.channels==ch)&(s.method==method)].iloc[0]
    conf.append({'Canais':ch,'Método':method,'Fechada→Thumbs':pm(q.closed_to_thumb_rate_mean,q.closed_to_thumb_rate_std),'Thumbs→Fechada':pm(q.thumb_to_closed_rate_mean,q.thumb_to_closed_rate_std)})
conf=pd.DataFrame(conf)

rej=[]
for ch in chs:
 q=s[(s.channels==ch)&(s.method=='Threshold/Hamming')].iloc[0]
 rej.append({'Canais':ch,'Rejeição':pm(q.rejection_rate_mean,q.rejection_rate_std),'Cobertura':pm(q.coverage_mean,q.coverage_std),'Acurácia não rejeitadas':pm(q.selective_accuracy_nonrejected_mean,q.selective_accuracy_nonrejected_std)})
rej=pd.DataFrame(rej)

# participant macro F1 pivot
pv=d.pivot_table(index='subject',columns=['channels','method'],values='macro_f1')
# flatten logical order
ordered=[]
for ch in chs:
  for m in methods: ordered.append((ch,m))
pv=pv[ordered]
pv.columns=[f'{ch}ch {m}' for ch,m in pv.columns]
pv=pv.reset_index().rename(columns={'subject':'Participante'})

# aggregate 8ch confusion normalized table text for key focus
cms8={}
for method in methods:
 keym=method.replace('-','_') if method!='Threshold/Hamming' else 'Threshold_Hamming'
 cms8[method]=pd.read_csv(out/f'cm_8ch_{keym}_row_normalized.csv',index_col=0)

# method evolution
em={r.method:r for _,r in e.iterrows()}

md=[]
md.append('# Teste final congelado — NinaPro DB5 E2')
md.append('')
md.append('## Escopo e integridade do protocolo')
md.append('')
md.append('O teste final foi executado com o protocolo previamente congelado, usando exclusivamente `Sx_E2_A1.mat` dos 10 participantes. O treino utilizou somente as repetições 1, 3 e 4 e o teste final somente as repetições 2 e 5. A repetição 6 foi excluída da segmentação, extração de features, normalização, treinamento e teste. Nenhum parâmetro, canal, feature, threshold ou modelo foi alterado após observar o teste.')
md.append('')
md.append('Verificações: E2 exclusivo; classes {0,1,5,6}; janela 40 amostras, passo 20; nenhuma janela atravessa classe/repetição; thresholds calculados somente com repouso do treino; z-score ajustado somente no treino; priors LDA exatamente 0,25 por classe; mesmos canais e identidades de janela entre os três métodos. Não houve shrinkage, subamostragem, salvaguarda de desvio-padrão nem instabilidade numérica.')
md.append('')
md.append('## 1. Resultados medidos')
md.append('')
md.append('### Macro-F1 — métrica principal')
md.append('')
md.append(prim.to_markdown(index=False))
md.append('')
md.append('O LDA-TD apresentou o maior macro-F1 médio nas quatro configurações. A vantagem sobre LDA-RMS foi +0,0393, +0,0278, +0,0068 e +0,0121 para 1, 2, 4 e 8 canais, respectivamente. O ganho do LDA-TD sobre Threshold/Hamming foi substancialmente maior: +0,3402, +0,3423, +0,2649 e +0,1584.')
md.append('')
md.append('### Balanced accuracy e acurácia global')
md.append('')
md.append(ba.to_markdown(index=False))
md.append('')
md.append('A acurácia global é apresentada apenas como auxiliar devido à forte predominância do repouso. A balanced accuracy acompanha melhor o comportamento das quatro classes.')
md.append('')
md.append('### F1 por classe')
md.append('')
md.append(f1.to_markdown(index=False))
md.append('')
md.append('Em 8 canais, o LDA-TD atingiu F1 médio de '+', '.join([f"{name}={fmt(s[(s.channels==8)&(s.method=='LDA-TD')].iloc[0][col+'_mean'])}" for name,col in [('repouso','f1_repouso'),('thumbs up','f1_thumbs_up'),('mão aberta','f1_mao_aberta'),('mão fechada','f1_mao_fechada')]])+'.')
md.append('')
md.append('### Confusão mão fechada ↔ thumbs up')
md.append('')
md.append(conf.to_markdown(index=False))
md.append('')
md.append('A confusão permaneceu assimétrica: em geral, mão fechada → thumbs up foi mais frequente que thumbs up → mão fechada. Em 8 canais, as médias foram 16,05% vs 2,38% no LDA-TD; 16,83% vs 3,68% no LDA-RMS; e 13,21% vs 3,26% no Threshold/Hamming. No baseline, taxas baixas de confusão direta devem ser interpretadas junto com as rejeições, pois uma amostra rejeitada continua sendo erro para macro-F1.')
md.append('')
md.append('### Rejeição do Threshold/Hamming')
md.append('')
md.append(rej.to_markdown(index=False))
md.append('')
md.append('A rejeição é particularmente alta em 1 e 2 canais. A acurácia nas amostras não rejeitadas é secundária e não substitui macro-F1, pois ignora justamente os casos em que o baseline ficou indeterminado.')
md.append('')
md.append('### Evolução com o número de canais')
md.append('')
for method in methods:
 r=em[method]
 md.append(f"- **{method}:** 1→2 {fmt(r.gain_1_to_2)}, 2→4 {fmt(r.gain_2_to_4)}, 4→8 {fmt(r.gain_4_to_8)}; ganho total 1→8 = {fmt(r.gain_1_to_8)}.")
md.append('')
md.append('O ganho de desempenho com mais canais é claro nos três métodos. A diferença entre os LDAs diminui bastante em 4 e 8 canais, enquanto a distância entre os LDAs e o baseline também se reduz com mais canais, mas permanece relevante em 8 canais.')
md.append('')
md.append('### Resultados individuais — macro-F1')
md.append('')
md.append(pv.to_markdown(index=False,floatfmt='.4f'))
md.append('')
md.append('A tabela completa por participante, incluindo balanced accuracy, acurácia, F1 por classe, confusões direcionais e métricas de rejeição/cobertura, está em `results/final_results_by_subject.csv`.')
md.append('')
md.append('### Matrizes de confusão')
md.append('')
md.append('Foram exportadas matrizes por participante e método, além de matrizes agregadas em contagens e normalizadas por linha para 1/2/4/8 canais. As matrizes agregadas servem apenas como descrição do padrão de erros; as métricas principais continuam sendo calculadas por participante e depois resumidas por média ± desvio-padrão.')
md.append('')
for method in methods:
 m=cms8[method].copy()
 m.index=['Repouso','Thumbs up','Mão aberta','Mão fechada']
 m.columns=['Repouso','Thumbs up','Mão aberta','Mão fechada'] + (['Rejeição'] if method=='Threshold/Hamming' else [])
 md.append(f'**8 canais — {method}, proporções por classe real**')
 md.append('')
 md.append(m.to_markdown(floatfmt='.4f'))
 md.append('')
md.append('## 2. Interpretação')
md.append('')
md.append('O resultado do teste final confirma o padrão observado na validação sem exigir qualquer alteração do protocolo. O ganho mais importante é a passagem do Threshold/Hamming para um classificador LDA supervisionado; a inclusão de MAV e WL sobre o RMS acrescenta um ganho adicional menor, mas positivo em média nas quatro configurações. Em 4 canais, LDA-RMS e LDA-TD permanecem muito próximos. Em 8 canais, o LDA-TD mantém vantagem modesta no macro-F1 e melhora, em média, os F1 de thumbs up, mão aberta e mão fechada.')
md.append('')
md.append('O baseline melhora substancialmente à medida que o número de canais aumenta e sua taxa de rejeição cai para cerca de 2,8% em 8 canais. Ainda assim, seu macro-F1 médio em 8 canais fica abaixo dos dois LDAs. A alta acurácia condicional entre amostras não rejeitadas mostra que a rejeição funciona como mecanismo conservador, mas essa métrica não deve ser confundida com desempenho global.')
md.append('')
md.append('## 3. Conclusão / recomendação')
md.append('')
md.append('Com o protocolo congelado, **LDA-TD permanece o pipeline ML principal**. No teste final ele alcançou macro-F1 médio de 0,8404 ± 0,0423 em 8 canais, contra 0,8282 ± 0,0481 do LDA-RMS e 0,6820 ± 0,1707 do Threshold/Hamming. A vantagem do LDA-TD sobre LDA-RMS é consistente em média, porém modesta — especialmente em 4 e 8 canais — e deve ser descrita dessa forma no TCC. O LDA-RMS continua útil como ablação por demonstrar quanto do ganho vem do classificador supervisionado usando somente RMS; o ganho adicional de TD quantifica o efeito de enriquecer a representação com MAV e WL.')
md.append('')
md.append('Nenhuma nova otimização deve ser realizada com base neste teste final.')
md.append('')
md.append('## Arquivos de auditoria e reprodutibilidade')
md.append('')
md.append('- `run_final_e2_frozen.py`: execução reproduzível do teste final congelado.')
md.append('- `results/FINAL_PROTOCOL_AUDIT.json`: auditoria formal das regras congeladas.')
md.append('- `results/raw_e2_audit.csv`: confirmação dos arquivos E2 e rótulos brutos.')
md.append('- `results/window_audit.csv`: treino/teste e exclusão da repetição 6.')
md.append('- `results/window_counts_by_subject_rep_class.csv`: contagens de janelas.')
md.append('- `results/thresholds_and_templates_frozen.csv`: thresholds e templates do baseline.')
md.append('- `results/final_results_by_subject.csv`: tabela individual completa.')
md.append('- `results/final_summary_mean_std.csv`: média ± DP entre participantes.')
md.append('- `results/confusion_matrices.json`: matrizes por participante/método.')
md.append('- `macro_f1_vs_channels.png`: gráfico principal.')

(out/'FINAL_REPORT.md').write_text('\n'.join(md),encoding='utf-8')
print('report written',out/'FINAL_REPORT.md')

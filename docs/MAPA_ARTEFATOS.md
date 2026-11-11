# Mapa de artefatos para o leitor do TCC

| Uso no TCC | Caminho a partir da raiz do repositório | Conteúdo |
| --- | --- | --- |
| Execução final | `e2_final/run_final_e2_frozen.py` | Script do protocolo congelado |
| Geração do relatório | `e2_final/build_report.py` | Pós-processamento e relatório; entradas/saídas parametrizadas na Etapa 4 |
| Auditoria final | `e2_final/results/FINAL_PROTOCOL_AUDIT.json` | Verificações do teste final |
| Janelas treino/teste | `e2_final/results/window_audit.csv` | Conferência da separação por repetição |
| Contagens por classe | `e2_final/results/window_counts_by_subject_rep_class.csv` | Contagens por participante/repetição/classe |
| Resultados individuais | `e2_final/results/final_results_by_subject.csv` | Valores individuais por método e canais |
| Resumo final | `e2_final/results/final_summary_mean_std.csv` | Médias/desvios-padrão entre participantes |
| Matrizes de confusão | `e2_final/results/confusion_matrices.json` | Matrizes do teste final |
| Limiar e templates | `e2_final/results/thresholds_and_templates_frozen.csv` | Parâmetros congelados do baseline |
| Validação LDA | `e2_validation/results/summary.csv` | Resumo LDA-RMS/LDA-TD da validação |
| Validação individual | `e2_validation/results/results_by_subject.csv` | Dados individuais da validação LDA |
| Auditoria de validação | `e2_validation/results/audit.json` | Parâmetros/auditorias da validação LDA |
| Diagnóstico LDA | `e2_validation/results/pipeline_comparison.csv` | Comparação dos pipelines na validação |
| Validação conjunta | `comparison/comparison_summary.csv` | Resumo Threshold/Hamming/LDA na validação |
| Identidade de janelas | `comparison/same_window_counts_audit.csv` | Contagens de janelas dos métodos na validação |
| Validação Threshold | `threshold_results/threshold_results_by_subject.csv` | Resultados de referência do baseline na validação |
| Bootstrap exploratório | `analises/bootstrap/Analise_Exploratoria_Etapa2_Bootstrap.csv` | Intervalos exploratórios, calculados posteriormente |
| Manifesto | `docs/MANIFESTO_SHA256.csv` | Hash de cada arquivo versionado, exceto o próprio manifesto |

**A Tabela C2 do TCC usa caminhos relativos a `e2_final/`**, enquanto a presente tabela usa caminhos relativos à raiz do repositório. Isso explica a diferença aparente nos prefixos.

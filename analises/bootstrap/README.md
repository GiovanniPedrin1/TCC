# Análise bootstrap exploratória (posterior ao teste final)

O CSV aqui incluído contém os resultados exploratórios já calculados. O script foi adaptado para consumir o CSV de métricas individuais do repositório:

```bash
python analises/bootstrap/recalcular_bootstrap_etapa2.py --csv e2_final/results/final_results_by_subject.csv --out reproducoes/bootstrap.csv
```

Não use o resultado como teste confirmatório. São 50.000 reamostragens pareadas de 10 participantes com semente fixa, sem reexecução da classificação. O argumento histórico `--zip` continua aceito para os pacotes anteriores.

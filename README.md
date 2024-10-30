# Desafio Técnico - Cientista de Dados Júnior

Respostas para as perguntas contidos nos arquivos `perguntas_sql.md` e `perguntas_api.md`.

Respostas se encontram em `respostas/Python` e `respostas/SQL`.

Dashboard Looker Studio para as questoes de visualização de dados se encontra [aqui](https://lookerstudio.google.com/s/glSx5IH2Qu0).

# 📄 Explicação de minhas soluções 

O link para a explicação de cada resposta encontrasse [aqui](https://doc-desafio-rio.vercel.app/). 

# 🛠️ Ferramentas Utilizadas

- **Python**:
- **Basedosdados**
- **BigQuery**
- **Jupyter**
- **Docusaurus**

# 🚀 Como Rodar

## Requisitos

- Python 3.6 ou superior
- Jupyter Notebook

### 1. Instalação das Bibliotecas 

```bash
!pip install basedosdados
```

### 2. Configurando basedosdados

*Importante*: billing_project_id deve corresponder ao ID do seu projeto na GCP, NÃO ao nome do projeto. No caso da imagem abaixo, seria "primeiro-projeto-350017"

Rode o comando abaixo para configurar o basedosdados:

```python
query = "SELECT * FROM `datario.educacao_basica.aluno` LIMIT 10"
df = bd.read_sql(query, billing_project_id="<id-do-seu-projeto>")
df.head()
```

Pedira para você fazer a autenticação pelo Google. Uma vez autenticado conseguira rodar as queries normalmente.

# 📚 Referências
- [Documentação do datario](https://docs.dados.rio/tutoriais/como-acessar-dados/)
- [Documentação do basedosdados](https://basedosdados.github.io/mais/)


# IS_AGRO — Repositório de Desenvolvimento de Código e Engenharia de Dados

> **Módulo Digital de Indicadores Agro-Socioambientais**
> Fruto da colaboração institucional entre o **Ministério de Agricultura, Pecuária e Abastecimento (MAPA)**, a **Embrapa** e o **Serviço Geológico do Brasil (SGB/CPRM)**.

---

## 📌 Sobre o Projeto IS_AGRO

O **IS_AGRO** é uma plataforma digital voltada para a criação, estimativa, visualização e difusão de indicadores agro-socioambientais. O projeto tem como finalidade fornecer inteligência estratégica para fortalecer a sustentabilidade da agropecuária nacional, integrando variáveis ambientais, agronômicas e socioeconômicas para subsidiar a formulação de políticas públicas, a tomada de decisão estratégica e o planejamento do uso do solo no Brasil.

### Funcionalidades e Objetivos Principais
* **Estimativa de Indicadores:** Automação no cálculo de métricas de sustentabilidade em diversas escalas territoriais.
* **Plataforma WebGIS:** Ambientes interativos para consulta, análise e espacialização de dados geográficos.
* **Suporte à Decisão:** Apoio a gestores públicos, pesquisadores e setor produtivo.
* **Interoperabilidade:** Integração contínua de bases sobre recursos hídricos, solos, aptidão agrícola e vulnerabilidade social.

---

## 💻 Propósito Deste Repositório

Este repositório é dedicado ao **desenvolvimento de código e engenharia de dados (ETL/ELT)** do projeto IS_AGRO. 

Aqui são desenvolvidos e mantidos os pipelines que realizam a extração de dados públicos (SIDRA/IBGE, MapBiomas, Lapig, bases meteorológicas e de recursos hídricos), limpeza, enriquecimento, cálculo dos indicadores metodológicos e consolidação das bases de dados que servirão para o desenvolvimento da rotina autômata no __Apache Airflow__ que irá alimentar periodicamente a camada analítica e os painéis/WebSIG da plataforma IS_AGRO.

---

## 🏛️ Arquitetura de Dados (Medallion Architecture)

O fluxo de processamento de dados nas pipelines segue o padrão de arquitetura Medallion:

* 🟤 **Bronze:** Dados brutos (*raw*) armazenados no formato original provenientes das distintas fontes públicas.
* ⚪ **Prata:** Dados tratados, padronizados, validados e salvos no formato colunar de alto desempenho `.parquet`.
* 🟡 **Ouro:** Dados calculados, enriquecidos e consolidados de acordo com as metodologias do projeto, salvos em formato `.csv` para consumo nos dashboards e WebSIG.

---

## 📂 Estrutura de Diretórios

```plaintext
IS_Agro/
├── databases/                      # Armazenamento das bases de dados nas camadas Bronze, Prata e Ouro
├── scripts/                        # Notebooks de engenharia de dados (ETL) e cálculo de indicadores
│   ├── Outros/                     # Códigos experimentais, estudos de caso e scripts temporários
│   └── *.ipynb                     # Pipelines de processamento de indicadores e fontes de dados
├── FDS_colhida_versao1/            # Pipeline de ETL em R para cálculo de produção de safras nacionais
│   ├── input/                      # Dados brutos adquiridos (SIDRA/IBGE)
│   └── output/                     # Dados calculados
├── indicador_CF_FDS_colhida/       # Pipeline de ETL em R para área agrícola (OCDE) e frequência de plantio (CF)
│   ├── input/                      # Dados brutos adquiridos (SIDRA/IBGE)
│   └── output/                     # Dados gerados
├── agents.md                       # Diretrizes de desenvolvimento, arquitetura e padrões para agentes
├── esboco_leiame.md                # Descritivo institucional e conceitual do projeto
├── readme.md                       # Documentação principal deste repositório
└── LEIAME.md                       # Documentação espelho em português
```

---

## 📝 Padrões de Nomenclatura e Desenvolvimento

### 1. Nomenclatura de Scripts e Notebooks (`scripts/`)
Os notebooks Jupyter (`.ipynb`) seguem padrões bem definidos de nomenclatura de acordo com sua função na pipeline:
* `Indicador`: Processo analítico completo (contemplando as etapas bronze, prata e ouro).
* `Indicador_Dado`: Processo focado em uma variável ou dado específico necessário para compor um indicador global.
* `Fonte_Dado`: Processo de extração/padronização de uma fonte externa que serve de insumo para outros cálculos.
* `Dado`: Pipeline base que gera insumos e tabelas derivadas.

### 2. Padrões de Código
* **Linguagens:** Python 3.7+ (Jupyter Notebooks para engenharia de dados) e R (scripts analíticos legados e complementares).
* **Nomenclatura no Código:**
  * `snake_case` para variáveis, funções e nomes de arquivos.
  * `UPPER_SNAKE_CASE` para constantes globais.
* **Documentação interna:** Código comentado e documentado para garantir a rastreabilidade metodológica dos cálculos e transformações.
* **Testes e Qualidade:** Uso de `pytest` para testes automatizados e validação de consistência dos dados gerados.

---

## 🔬 Descrição dos Scripts de Engenharia de Dados (`scripts/`)

Abaixo estão descritos os notebooks Jupyter desenvolvidos para os processos de extração, transformação e modelagem dos indicadores agro-socioambientais:

### Indicadores e Séries Internacionais (OCDE)
* **`OCDE_amonia.ipynb`**: Extrai e padroniza as séries históricas de emissões de amônia ($NH_3$) da agricultura a partir de dados da OCDE, gerando a base `ouro_amonia_OCDE.csv`.
* **`OCDE_area_agricola.ipynb`**: Processa e converte os dados da OCDE referentes à área agrícola total (culturas e pastagens em milhares de hectares) para a camada ouro (`ouro_area_agricola_OCDE.csv`).
* **`OCDE_gee.ipynb`**: Realiza o tratamento e a harmonização das séries de emissões de gases de efeito estufa (GEE) do setor agropecuário oriundas da OCDE, consolidando o arquivo `ouro_gee_OCDE.csv`.

### Georreferenciamento e Cadastros Base
* **`geocodigo_internacional.ipynb`**: Coleta via web scraping a tabela de códigos de países ISO 3166 (numérico, Alpha-2 e Alpha-3) e traduz as denominações para o português.
* **`ibge_geocodigo.ipynb`**: Consome a API de Localidades do IBGE para gerar a base cadastral de referência de municípios, microrregiões, mesorregiões e UFs utilizada em todos os cruzamentos espaciais.

### Uso da Terra, Cobertura Vegetal e Manejo
* **`area_agropecuaria_pastagem.ipynb`**: Cruza dados de pastagens do LAPIG com estatísticas de uso da terra da Embrapa/MapBiomas para consolidar as áreas agropecuárias municipais.
* **`ilpf_spd.ipynb`**: Trata dados tabulares sobre a adoção de Integração Lavoura-Pecuária-Floresta (ILPF) e Sistema Plantio Direto (SPD), salvando as camadas em formato `.parquet`.
* **`lapig_pastagem.ipynb`**: Coleta e processa dados do Atlas das Pastagens (LAPIG/UFG) sobre áreas e níveis de degradação de pastagens por município e estado.
* **`mapbiomas_uso_terra.ipynb`**: Baixa e estrutura as séries temporais de cobertura e uso do solo do MapBiomas, gerando tabelas agregadas por município, UF e tabela de legendas.

### Culturas Agrícolas e Safras (PAM / SIDRA / IBGE)
* **`cultivo_duplasafra_específicas.ipynb`**: Extrai da API SIDRA/IBGE dados municipais de 1ª e 2ª safras de milho, amendoim, batata e feijão (tabelas 839, 1000, 1001 e 1002).
* **`cultivo_lavouras_permanentes.ipynb`**: Ingestão e padronização de dados municipais de área destinada, colhida e produção de lavouras permanentes (IBGE tabela 1613).
* **`cultivo_lavouras_temporarias.ipynb`**: Processa dados de área colhida e produção de lavouras temporárias (IBGE tabela 1612), segregando os volumes por ciclos de safra.

### Emissões de Amônia e Gases de Efeito Estufa (Nacional)
* **`amonia_agro.ipynb`**: Trata as estimativas de emissões de amônia ($NH_3$) volatilizada da agropecuária nacional e associa aos geocódigos do IBGE (`ouro_amonia_agro.csv`).
* **`gee_agropecuaria.ipynb`**: Faz o download e a padronização das estimativas oficiais de emissões de GEE da agropecuária (MCTI/Comunicações Nacionais) por gás, subsetor e UF.

### Balanço de Nutrientes no Solo (NPK)
* **`npk_agricultura.ipynb`**: Calcula o volume de Nitrogênio, Fósforo e Potássio exportados pelas colheitas agrícolas aplicando teores nutricionais sobre a produção municipal da PAM/IBGE.
* **`npk_balanco.ipynb`**: Integra todas as entradas e saídas de NPK (fertilizantes, dejetos, fixação biológica e deposição vs. colheitas e abate), gerando o indicador final `ouro_npk-balanco.csv`.
* **`npk_carcaca_bovina.ipynb`**: Estima a exportação de nutrientes NPK do solo por meio do peso de carcaças bovinas abatidas a partir da pesquisa de abate do IBGE (tabela 1092).
* **`npk_dejetos.ipynb`**: Calcula a quantidade de NPK incorporada ao solo via dejetos animais a partir dos efetivos de rebanhos da PPM/IBGE (tabela 3939).
* **`npk_deposicao_atmosferica.ipynb`**: Estima o aporte de Nitrogênio incorporado ao solo por deposição atmosférica sobre as áreas agropecuárias mapeadas pelo MapBiomas.
* **`npk_fertilizantes_organicos.ipynb`**: Calcula a entrada de N, P e K no solo decorrente da aplicação de vinhaça oriunda da produção sucroalcooleira.
* **`npk_fertilizantes_sinteticos.ipynb`**: Trata dados de entrega de fertilizantes sintéticos (NPK) ao mercado nacional para quantificar os aportes minerais no solo.
* **`npk_fix_bio_N.ipynb`**: Estima a quantidade de Nitrogênio incorporada ao solo por Fixação Biológica de Nitrogênio (FBN) em culturas leguminosas como a soja.
* **`npk_sementes.ipynb`**: Calcula a quantidade de nutrientes (NPK) introduzida no solo pelo plantio de sementes a partir das taxas de semeadura e áreas plantadas do IBGE.

### Risco de Erosão Hídrica do Solo
* **`risco_erosao.ipynb`**: Consolida os cálculos de risco de erosão hídrica do solo de pastagens, lavouras permanentes e temporárias no indicador final unificado `ouro_risco_erosao.csv`.
* **`risco_erosao_lav_permanentes.ipynb`**: Calcula o risco de erosão em lavouras permanentes utilizando áreas destinadas à colheita (IBGE tabela 1613) e fatores de manejo.
* **`risco_erosao_lav_temporarias.ipynb`**: Estima o risco de erosão em lavouras temporárias integrando áreas colhidas (IBGE tabela 1612), safras e taxas de adoção de Plantio Direto (SPD).
* **`risco_erosao_pastagem.ipynb`**: Avalia o risco de erosão em pastagens cruzando dados de degradação do LAPIG, área de pastagem e áreas sob ILPF.

### Produtividade e Eficiência
* **`ptf.ipynb`**: Coleta via web scraping e processa as séries históricas da Produtividade Total dos Fatores (PTF) da agricultura brasileira, gerando `ouro_ptf.csv`.

---

## 🔗 Referências Oficiais

* [Página do Projeto na Embrapa (Código 220069)](https://www.embrapa.br/busca-de-projetos/-/projeto/220069/modulo-is_agro---solucoes-digitais-para-criacao-estimativa-e-divulgacao-de-indicadores-agro-socioambientais---inteligencia-estrategica-para-a-sustentabilidade-da-agropecuaria-nacional)
* [Plataforma Interativa IS_AGRO (SGB)](https://isagro.sgb.gov.br/)
* [Publicação Técnica nos Anais (Embrapa ALICE, 2024)](https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1171457/1/IS-AGRO-modulo-digital-2024.pdf)

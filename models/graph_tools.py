import numpy
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# from helpers import resume_numero

import pandas as pd

class Graph():
  
  """
    Classe Atalho para Geração de Gráficos usando o Plotly.
    
    [ATENÇÃO] Essa classe não tem o intuíto de clonar as funções do Plotly e sim
    tornar a geração de alguns gráficos mais práticas. Dessa forma, para personalizações 
    avançadas e detalhamentos mais apurados, crie o gráfico diretamente pelo Potly!

    ~~~ Parâmetros Padrões ~~~  
      
      1. Gráficos de Linha
        * __line_mode: `String` com o Tipo de Linha do Gráfico, ex: `lines`, `lines+markers`, `markers`.
        * __line_fill: `String` com o Tipo de preenchimento do gráfico, ex: `None`, `tonexty`, `tozeroy`.
        
      2. Gráfico de Barras
        * __bar_mode: `String` com o Modo que devem ser agrupadas as colunas, `group`(agrupamento) e `stack`(empilhamento).
      
      3. Cores
        * __pastel_colors: `List` com paleta de 8 cores pasteis, em RGB.
        * __semipastel_colors: `List` com paleta de 8 cores semi pasteis, em RGB.
        * __brilhant_colors: `List` com paleta de 26 cores brilhantes, em HEX.
        
      4. Subplots
        * __figure_coluns: `Int` com quantidade de colunas que deve haver no subplot.
        * __figure_is_subplot: `Bool` identificador do tipo de gráfico, comum ou subplot.

    ~~~ Métodos ~~~
    
      * update_layout: Inicializa o layout modelo e pode ser evocado para atualizar o layout.
      * __subplot_validate: Validador se o gráfico é um subplot e os parâmetros (rows, row_width) foram passados corretamente.
      * __line_parameters_validade: Validador dos parâmetros passados em Line.
      * line: Gera gráfico de linhas;
      * bar: Gera gráfico de barras;
      * pizza: Gera Gráfico de pizza;
      * show: Retorna a figura completa do gráfico;
      
    ~~~ Instanciação do Objeto ~~~  
    
      1. Parâmetros de Inicialização:
      
        * df: Dataset do tipo `DataFrame`;
        * title: `String` com o título do Gráfico, por padrão inicializa vazio;
        * tit_is_bold: `Bool` que define se o título será negrito, por padrão inicializa com `True`;
        * is_subplot: `Bool` identificador do tipo de gráfico, comum ou subplot, por padrão inicializa com `False`.
        * rows: Quantidade de Linhas que o subplot deve ter, por padrão inicializa com 2; [APENAS P/ SUBPLOTS]
        * row_width: Proporcionamento das linhas no subplot, por padrão inicializa com 30% e 70%; [APENAS P/ SUBPLOTS]
        
      2. Exemplos de evocação da função:
      
        0. Dataset de Exemplo:
        
          json={'data_relatorio': {0: '2020-03-31', 1: '2020-03-30', 2: '2020-03-28', 3: '2020-03-27', 4: '2020-03-26', 5: '2020-03-25', 6: '2020-03-24', 7: '2020-03-23'},
               'msg': {0: 309, 1: 141, 2: 31, 3: 346, 4: 223, 5: 148, 6: 213, 7: 443},
               'canais': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2},
               'env_canal': {0: 192, 1: 99, 2: 14, 3: 209, 4: 134, 5: 97, 6: 122, 7: 259},
               'env_contato': {0: 117, 1: 42, 2: 17, 3: 137, 4: 89, 5: 51, 6: 91, 7: 184},
               'read': {0: 113.0, 1: 68.0, 2: 11.0, 3: 135.0, 4: 87.0, 5: 75.0, 6: 114.0, 7: 186.0},
               'failed': {0: 3.0, 1: 9.0, 2: None, 3: 3.0, 4: 7.0, 5: 14.0, 6: 4.0, 7: None}}

          df=pd.DataFrame(json)

        1. GRÁFICO DE LINHA:
          #Linha Comum
          Graph(df, title='MENSAGENS').line(x_col='data_relatorio', y_cols=['env_contato' , 'env_canal']).show()

          #Configurações Avançadas
          # >>> Preenchimento
          # Graph(df, 'MENSAGENS').line('data_relatorio', ['env_contato' , 'env_canal'], fills=['tonexty', 'tozeroy']).show()

          # >>> Modos
          # Graph(df, 'MENSAGENS').line('data_relatorio', ['env_contato' , 'env_canal'], modes=['lines+markers', 'markers']).show()

          # >>> Subplots
          Graph(df, 'MENSAGENS',is_subplot=True).line('data_relatorio', ['env_contato' , 'env_canal'], row = 1
          ).line('data_relatorio', ['read' , 'failed'], cols_colors=['gray', 'green'], row = 2).show()

        2. GRÁFICO DE BARRA 
          #Barra Comum
          Graph(df, title='MENSAGENS').bar('data_relatorio', ['env_canal', 'env_contato']).show()

          #Configurações Avançadas
          # >>> Modos
          Graph(df, title='MENSAGENS').bar('data_relatorio', ['env_canal', 'env_contato'], barmode="stack").show()
          Graph(df, title='MENSAGENS').bar('data_relatorio', ['env_canal', 'env_contato'], barmode="group").show()

          # >>> Cores
          Graph(df, title='MENSAGENS').bar('data_relatorio', ['env_canal', 'env_contato'], marker_colors=['green', 'red']).show()

          # >>> Subplots
          Graph(df, title='MENSAGENS', is_subplot=True).bar('data_relatorio', ['env_canal', 'env_contato'], row=1
                                                         ).bar('data_relatorio', ['env_canal', 'env_contato'], row=2).show()

        4. GRÁFICO DE PIZZA:
          #Pizza Comum
          Graph(df, title='MENSAGENS').pizza(['env_canal', 'env_contato'], ['Canal', 'Contato']).show()
          
          #Rosca e Settamento de Cores
          Graph(df, title='MENSAGENS').pizza(['env_canal', 'env_contato'], ['Canal', 'Contato'], is_danut=True, marker_colors=['red', 'green']).show()
          
        3. SUBPLOTS MESCLADOS
          Graph(df, title='MENSAGENS', is_subplot=True, rows=3, row_width=[0.33, 0.33, .33]).bar('data_relatorio', ['env_canal', 'env_contato'], row=1
                                                           ).line(x_col='data_relatorio', y_cols=['env_contato' , 'env_canal'], row=1
                                                           ).line(x_col='data_relatorio', y_cols=['env_contato' , 'env_canal'], row=2
                                                           ).bar('data_relatorio', ['env_canal', 'env_contato'], row=3).show()
  """
  
  #DEFAULT PARAMETERS
  #Lines 
  __line_mode = 'lines'
  __line_fill=None
  
  #Bar
  __bar_mode = 'group'
  
  #General - Colors
  __pastel_colors = px.colors.qualitative.Pastel2
  __semipastel_colors = px.colors.qualitative.Set2 
  __brilhant_colors = px.colors.qualitative.Alphabet
  __plotly_colors = px.colors.qualitative.Plotly
  __continue_hot = ['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921']
  __continue_blu = ['#012A4A', '#013A63', '#01497C', '#014F86', '#2A6F97', '#2C7DA0', '#468FAF', '#61A5C2', '#89C2D9', '#A9D6E5']

  @property
  def contact_color(self): return 'mediumseagreen'
  @property
  def operator_color(self): return 'darkslateblue'
  @property
  def bot_color(self): return 'royalblue'
  @property
  def management_color(self): return 'gray'
  @property
  def msg_color(self): return 'cornflowerblue'
  
  @property
  def brilhant_colors(self): return self.__brilhant_colors
  
  @property
  def hot(self): return self.__continue_hot
  
  @property
  def blu(self): return self.__continue_blu
  
  @property
  def cor(self): return self.__plotly_colors

  @property
  def pastel_colors(self): return self.__pastel_colors
  
  #General - Subplots
  __figure_is_subplot = False
  
  def  __init__(self, df: pd.DataFrame, title:str = '', tit_is_bold=True, is_subplot=False, rows=2, row_width=[0.30, 0.70], cols=1, cols_width=[1]):
    """
    Parâmetros de Inicialização:
      * df: Dataset do tipo `DataFrame`;
      * title: `String` com o título do Gráfico, por padrão inicializa vazio;
      * tit_is_bold: `Bool` que define se o título será negrito, por padrão inicializa com `True`;
      * is_subplot: `Bool` identificador do tipo de gráfico, comum ou subplot, por padrão inicializa com `False`.
      * rows: Quantidade de Linhas que o subplot deve ter, por padrão inicializa com 2; [APENAS P/ SUBPLOTS]
      * cols: Quantidade de Colunas que o subplot deve ter, por padrão inicializa com 1; [APENAS P/ SUBPLOTS]
      * cols_width: Proporcionamento das Colunas no subplot, por padrão inicializa com 100%; [APENAS P/ SUBPLOTS]
    """
    if is_subplot in [True, False]: self.__figure_is_subplot = is_subplot
    else: raise Exception('O Parâmetro `is_subplot` deve receber um valor do tipo boleno.')
    
    self.__fig = make_subplots(rows=rows, cols=cols, row_width=row_width, column_widths=cols_width, horizontal_spacing = 0, vertical_spacing=.02) if is_subplot else go.Figure()

    self.df = df
    self.title = f'<b>{title}' if tit_is_bold else title
    
    self.update_layout()
  
  def update_layout(self):
    """Inicializa o layout modelo e pode ser evocado para atualizar o layout."""

    self.__fig.update_xaxes(showgrid=False)
    self.__fig.update_yaxes(showgrid=False)
    if self.__figure_is_subplot: self.__fig.update_layout(xaxis_showticklabels=False)
    self.__fig.update_layout(
      title=self.title, 
      title_y=1, 
      title_x=0,
      legend_font_family="Courier", 
      autosize=True,
      plot_bgcolor='rgba(0,0,0,0)', 
      paper_bgcolor='rgba(0,0,0,0)', 
      margin=dict(l=0, r=0, b=25, t=20), 
      legend=dict(orientation="h", y=-0.13, xanchor="right", x=1)
    )
    
  #Tratamento Subplot
  def __subplot_validate(self, func:str, row:int = None):
    """Validador se o gráfico é um subplot e os parâmetros (rows, row_width) foram passados corretamente."""
    if (func == 'pizza') & (self.__figure_is_subplot == True): 
      raise Exception('Tipo de Gráfico Não suportado para subplots.\nEssa classe ainda não suporta a criação de subplots com gráficos de pizza.')
      
    if (row is not None) & (self.__figure_is_subplot == False): 
      raise Exception('Este Gráfico não é um subplot.\n Para torná-lo um subplot e setar suas rows, na instanciação do objeto defina: `Graph(is_subplot=True)`.')
    else: 
      if (row is None) & (self.__figure_is_subplot == True): 
        raise Exception(f'Este Gráfico é um subplot.\nVocê precisa informar a linha que o gráfico será gerado em: `{func}(row=1)`.')
     
  #Valida parâmetros recebidos em `line`
  def __line_parameters_validade(self, y_col_names:list, modes:list, fills:list):
    """Validador dos parâmetros passados em Line."""
    #Tratamento de Tipagem de Dados
    if type(y_col_names) not in [list]: 
      raise Exception(f'Tipo de dados Inválido para `y_col_names`!\nEsperava-se: `list`, Recebido: `{type(y_col_names)}`.')
      
    if type(modes) not in [list]: raise Exception(f'Tipo de dados Inválido para `modes`!\nEsperava-se: `list`, Recebido: `{type(modes)}`.')
      
    if type(fills) not in [list]: raise Exception(f'Tipo de dados Inválido para `fill`!\nEsperava-se: `list`, Recebido: `{type(fills)}`.')

  #Insere anotação a figura
  def annotations(self, text:str='', x:float=.01, y:float=1, xref= 'paper', yref='paper', bgcolor="white", opacity=0.9, showarrow=False, arrowhead=1, align='left', font_size=11, font_color='black', anottations:list=None):
    """Insere anotação a figura.
      Ex.:
      * Passando uma lista de anotações (list[dict]):
        annot_header = {
            'xref': 'paper', 'yref': 'paper', 'x': .01, 'y': 1, 'bgcolor':"white", 'opacity':0.9, 'showarrow': False, 'arrowhead': 1, 'align':'left','font': {'size': 11, 'color': 'black'},
            'text': f'Minha anotação',
        }
        fig.annotations([annot_header])
    * Passando apenas o texto:
        fig.annotations(text='Minha anotação')
    """
    if anottations is None: 
      annot_header = {
        'xref': xref, 
        'yref': yref, 
        'x': x, 
        'y': y, 
        'bgcolor': bgcolor, 
        'opacity':opacity, 
        'showarrow': showarrow, 
        'arrowhead': arrowhead, 
        'align': align,
        'font': {'size': font_size, 'color': font_color},
        'text': text
      }
      anottations = [annot_header]
      self.__fig.update_layout({'annotations': [annot_header]})
    else:
      if type(anottations) in [list]: 
        for i in anottations:
          if type(i) not in [dict]: raise Exception(f'Tipo de dados Inválido para `anottations`!\nEsperava-se: `list[dict]`, Recebido: `{type(i)}`.')
      else: raise Exception(f'Tipo de dados Inválido para `anottations`!\nEsperava-se: `list`, Recebido: `{type(anottations)}`.')
    
      self.__fig.update_layout({'annotations': anottations})
    
  #Gera Gráfico de Linha 
  def line(self, x_col:str, y_cols:list, y_col_names:list = [], cols_colors:list = [], modes:list = [], fills:list =[], row=None, fill_colors:list = [], column=1, marker_color=None, marker_colorscale= 'teal', hovertemplate:str='%{y:,.0f}<br>%{x}'):
    """Gera gráfico de linhas, recebendo como parâmetros:
        1. x_col: coluna do eixo x.
        2. y_cols: lista coluna(s) do eixo y.
        3. y_col_names: lista de nome(s) das coluna(s) para legenda. [OPCIONAL]
        4. cols_colors: lista de cores para as coluna(s). [OPCIONAL]
        5. modes: lista de Tipos de Linhas. [OPCIONAL]
        6. fills: lista de Tipos de preenchimento de Linhas. [OPCIONAL]
        7. row: numero da linha do gráfico. [APENAS SUBPLOT]
        8. column: numero da coluna do gráfico. [APENAS SUBPLOT]
        9. marker_color: cor OU coluna para marcadores. [OPCIONAL]
        10. marker_colorscale: string com escala de cores plotly. [OPCIONAL]
          10.1 Melhores escalas: 'darkmint', 'emrld', 'magenta', 'mint', 'purp', 'teal', 'tempo', 'blues', 'darkmint' e 'emrld'
        11. hovertemplate: Formatação dos eixos. Por padrão o valor é formatado com '%{y:,.0f}<br>%{x}' [OPCIONAL]"""

    #Tratamento Subplot
    self.__subplot_validate(row=row, func='line')
    
    #Tratamento de Tipagem de Dados
    self.__line_parameters_validade(y_col_names, modes, fills)
    
    #Criação de Linha por Coluna
    for col in y_cols:
      if col not in list(self.df.columns): raise Exception(f'Coluna `{col}` não encontrada!\nColunas válidas:\n{list(self.df.columns)}')
      if self.df[col].dtypes not in [int, float]: raise Exception(f'Tipo de dados recebido na coluna `{col}` não é um int ou float.')
      
      #Nome do índice
      col_name = col.replace('_', ' ').title()
      try: col_name = y_col_names[y_cols.index(col)]
      except: pass
      
      #Modos
      mode = self.__line_mode
      try: mode = modes[y_cols.index(col)]
      except: pass
      
      #Preenchimento
      fill = self.__line_fill
      try: fill = fills[y_cols.index(col)]
      except: pass
      fillcolor = None
      try: fillcolor = fill_colors[y_cols.index(col)]
      except: pass
      
      #Coloração
      cor = self.__brilhant_colors[y_cols.index(col)]
      try: cor = cols_colors[y_cols.index(col)]
      except: pass
      
      #Criação da Linha
      # best_marker_colorscale=['darkmint', 'emrld', 'magenta', 'mint', 'purp', 'teal', 'tempo', 'blues', 'darkmint', 'emrld']
      markers_is_colored = True if (marker_color == None) & (mode not in ['lines', 'lines+markers']) & (cols_colors == [])else False
      line = go.Scatter(name=col_name, x=self.df[x_col], y=self.df[col], mode=mode, fill=fill, fillcolor=fillcolor, line_color=cor, marker_colorscale=marker_colorscale, marker_color=self.df[col] if markers_is_colored else marker_color, hovertemplate=hovertemplate)
      if self.__figure_is_subplot: self.__fig.add_trace(line, row=row, col=column)
      else: self.__fig.add_trace(line)
      
    return self
  
  #Gera Gráfico de barras
  def bar(self, x_col:str, y_cols:list, y_col_names:list = [], barmode:str='', marker_colors:list = [], row=None):
    """Gera gráfico de barras, recebendo como parâmetros:
        * x_col: coluna do eixo x.
        * y_cols: lista coluna(s) do eixo y.
        * y_col_names: lista de nome(s) das coluna(s) para legenda. [OPCIONAL]
        * barmode: tipo de barra (`group`/`stack`). [OPCIONAL]
        * marker_colors: lista de cores para as coluna(s). [OPCIONAL]
        * row: numero da linha do gráfico. [APENAS SUBPLOT]"""

    #Tratamento Subplot
    self.__subplot_validate(row=row, func='bar')
    
    for col in y_cols:
      if self.df[col].dtypes not in [int, float]: raise Exception(f'Tipo de dados recebido na coluna `{col}` não é um int ou float.')
      if type(y_col_names) not in [list]: raise Exception(f'Tipo de dados Inválido!\nEsperava-se: `list`, Recebido: `{type(y_col_names)}`.')
      
      col_name = col.replace('_', ' ').title()
      
      try: col_name = y_col_names[y_cols.index(col)]
      except: pass
      
      cor= self.__semipastel_colors[y_cols.index(col)] if marker_colors == [] else marker_colors[y_cols.index(col)]
      
      #Criação da barra
      bar = go.Bar(name=col_name, x=self.df[x_col], y=self.df[col], marker={'color':cor})
      
      if self.__figure_is_subplot: self.__fig.add_trace(bar, row=row, col=1)
      else: self.__fig.add_trace(bar)
    
    #Settamento de Barmode para defalt caso não seja passado como parâmetro
    barmode=self.__bar_mode if barmode == '' else barmode
    self.__fig.update_layout(barmode=barmode)
      
    return self
  
  #Gera Gráfico de pizza/rosca
  def pizza(self, cols:list, cols_names:list = [], is_danut:bool = True, showlegend:bool=False, marker_colors:list = [], textinfo:str='label+percent'):
    """Gera Gráfico de pizza, recebendo como parâmetros:
        * cols: lista coluna(s).
        * cols_names: lista de nome(s) das coluna(s) para legenda. [OPCIONAL]
        * is_danut: classificador do tipo de gráfico (pizza ou rosca). [OPCIONAL]
        * marker_colors: lista de cores para as coluna(s). [OPCIONAL]
        * showlegend: exibe legenda. [OPCIONAL]
        * textinfo: texto que será exibido no gráfico (label, label+percent, value, none). [OPCIONAL]
        """

    #Tratamento Subplot
    self.__subplot_validate('pizza')
    
    #Configurações de variáveis
    labels = cols_names if cols_names != [] else [col.replace("_",'').title() for col in cols]
    values = [self.df[col].sum() for col in cols]
    colors = marker_colors if marker_colors != [] else self.__brilhant_colors
    hole = .4 if is_danut else .0
            
    #Criação da pizza/rosca
    pizza = go.Pie(labels=labels, values=values, hole=hole)
    self.__fig.add_trace(pizza)
    self.__fig.update_traces(hoverinfo='label+value', textinfo=textinfo, marker=dict(colors=colors))
    self.__fig.update_layout(margin = dict(t=20, l=0, r=0, b=25), showlegend=showlegend)
    
    return self
    
  #Retorna o gráfico completo
  def show(self): 
    """Retorna a figura completa do gráfico"""
    fig = self.__fig
    return fig

def graph_periods(df:pd.DataFrame, cols_period: list, title: str, is_percent=False, col_total:str=None) -> Graph:
    """
    ## graph_periods
    Retorna um Gráfico de Barras com os valores por período \n
    Parâmetros:
    1. df: Conjunto de Dados [Obrigatório]
    2. cols_period: Nomes das colunas dos totalizadores dos periodos, em ordem (mad, man, tar e noite) [Obrigatório]
    3. title: Título do Gráfico [Obrigatório]
    4. is_percent: Se True, os valores são convertidos para porcentagem
    5. col_total: Nome da coluna que contém o totalizador [Obrigatório caso is_percent=True]

    ### Exemplo de uso: 
    #### Criação de um Dataset randomico
    import numpy as np\n
    js={
      'madrugada': list(np.random.randint(low = 1, high=30, size=30)), 
      'manha': list(np.random.randint(low = 1, high=30, size=30)), 
      'tarde': list(np.random.randint(low = 1, high=30, size=30)), 
      'noite': list(np.random.randint(low = 1, high=30, size=30)),
      'data_relatorio': [f'2022-01-{day}' for day in range(1,31)], 
      'mes': ['01']*30 \n
    }\n
    js['total'] = [js['madrugada'][i] + js['manha'][i] + js['tarde'][i] + js['noite'][i] for i in range(30)]
    #### Evocação da Função
    graph_periods(
      df = pd.DataFrame(js),\n
      cols_period = ['madrugada', 'manha', 'tarde', 'noite'], \n
      title='ENCAMINHAMENTOS POR PERÍODO (Exemplo)', \n
      is_percent=False, \n
      col_total='encaminhados'\n
    )

    """

    if len(cols_period) != 4: raise ValueError('Número de colunas deve ser igual a 4')

    fig=Graph(df, title)

    if is_percent:
        if col_total is None: raise ValueError('col_total deve ser informado quando is_percent=True')
        df[cols_period] = df[cols_period].apply(lambda total_period: round(total_period/df[col_total],2))
        fig.show().update_layout(yaxis= {'tickformat': ',.0%', 'title':f'Porcentagem'})

    fig.bar('data_relatorio', cols_period, ['Madrugada', 'Manhã', 'Tarde', 'Noite'], marker_colors= ['indianred', 'lightcoral', 'darkorange', 'saddlebrown'])
    
    return fig.show()

def graph_tempos(df:pd.DataFrame, title:str, col_tempo:str='', col_tmp_name:str=None, line_color:str = 'steelblue', box_color:str = 'cornflowerblue', is_pizza:bool=False, tipo:str='leitura', prefix: str = '', col_total:str='', center_title:str='') -> Graph:
    """
    ## graph_tempos
    Retorna um Subplot com um um gráfico de linhas representando os fluxos
     de ocorrencias e um gráfico de caixa correspondente à distribuição dos dados. \n

    ### Parâmetros:
    * `df`: Conjunto de Dados [Obrigatório]
    * `title`: Título do Gráfico [Obrigatório]
    * `col_tempo`: Nome da coluna que contém o tempo [Obrigatório]
    * `col_tmp_name`: Nome da legenda do tempo [Opcional]
    * `line_color`: Cor da linha. Por padrão já vem `steelblue` [Opcional]
    * `box_color`: Cor da caixa. Por padrão já vem `cornflowerblue` [Opcional]
    * `is_pizza`: Se True, o gráfico é uma pizza. Por padrão retorna um Subplot com Linha e Caixa [Opcional]
    * `tipo`: Tipo do tempo: leitura, espera, atendimento, etc. Por padrão o valor é `leitura`[Opcional]
    * `prefix`: Prefixo do nome da coluna. Ex: `status.mensagens.tempo_leitura` [Opcional]
        1. Se `prefix` for informado, `tipo` é ignorado
        2. Exemplos de prefixos: `status.mensagens.tempo_leitura`, `grupo.mensagens.tempo_espera`, `transmissao.mensagens.tempo_atendimento`
    * `col_total`: Nome da coluna que contém o totalizador [Obrigatório caso is_pizza=True]
    * `center_title`: Título do centro da pizza [Opcional]
    """

    if is_pizza & (col_total == ''): raise ValueError('col_total deve ser informado quando is_pizza=True')
    if (is_pizza==False) & (col_tempo == ''): raise ValueError('col_tempo deve ser informado quando is_pizza=False')

    if is_pizza:
      values={
        'value_interv_1' : df[f"{f'tempo_{tipo}' if prefix == '' else prefix}.interval_h.0-1 hs"].sum(),
        'value_interv_2' : df[f"{f'tempo_{tipo}' if prefix == '' else prefix}.interval_h.1-4 hs"].sum(),
        'value_interv_3' : df[f"{f'tempo_{tipo}' if prefix == '' else prefix}.interval_h.4-8 hs"].sum(),
        'value_interv_4' : df[f"{f'tempo_{tipo}' if prefix == '' else prefix}.interval_h.8-12 hs"].sum(),
        'value_interv_5' : df[f"{f'tempo_{tipo}' if prefix == '' else prefix}.interval_h.12-16 hs"].sum(),
        'value_interv_6' : df[f"{f'tempo_{tipo}' if prefix == '' else prefix}.interval_h.16-20 hs"].sum(),
        'value_interv_7' : df[f"{f'tempo_{tipo}' if prefix == '' else prefix}.interval_h.20+ hs"].sum()
      }
      values['total'] = sum(values.values())
      
      labels={
        'interv_1':f'0-1h<br>{(values["value_interv_1"]*100/df[col_total].sum()) if df[col_total].sum() > 0 else 0:.1f}%',
        'interv_2':f'1-4h<br>{(values["value_interv_2"]*100/df[col_total].sum()) if df[col_total].sum() > 0 else 0:.1f}%',
        'interv_3':f'4-8h<br>{(values["value_interv_3"]*100/df[col_total].sum()) if df[col_total].sum() > 0 else 0:.1f}%',
        'interv_4':f'8-12h<br> {(values["value_interv_4"]*100/df[col_total].sum()) if df[col_total].sum() > 0 else 0:.1f}%',
        'interv_5':f'12-16h<br>{(values["value_interv_5"]*100/df[col_total].sum()) if df[col_total].sum() > 0 else 0:.1f}%',
        'interv_6':f'16-20h<br>{(values["value_interv_6"]*100/df[col_total].sum()) if df[col_total].sum() > 0 else 0:.1f}%',
        'interv_7':f'+20h<br>{(values["value_interv_7"]*100/df[col_total].sum()) if df[col_total].sum() > 0 else 0:.1f}%',
        'title_total':f'<b>{center_title}</b><br> {resume_numero(values["total"])}',
      }

      fig=Graph(df, title)
      fig.show().add_trace(go.Sunburst(
          labels= list(labels.values()),
          parents=[labels["title_total"]]*(len(labels)-1) + [''],
          values= list(values.values()) ,
          branchvalues='total'
      )) 
      return fig.show()
    else:

      df = df[df[col_tempo] < 2880] #48hrs

      fig=Graph(df, title, is_subplot=True, cols=2, cols_width=[.15,.85], rows=1, row_width=[1])
      fig.line('data_relatorio', [col_tempo], [col_tmp_name] if col_tmp_name is not None else [], cols_colors=[line_color], modes=['lines+markers'], row=1, column=2).show().update_layout(yaxis=dict(title_text='Minutos'))
      
      fig.show().add_trace(go.Box(y=df[col_tempo], boxpoints='outliers', name='Variação', marker_color=box_color, jitter=1, pointpos=0, boxmean=True), row=1, col=1)
      fig.show().update_layout(yaxis_showticklabels=True, yaxis2_showticklabels=False)
      return fig.show()

def totalizers(title, value, is_number=True, is_total=True, is_median=True, is_sub=False, padding_bottom=20):
  import streamlit as st
  from functions import human_format
  
  """ funcao para graficar totais
  input: 
      - (array) config = [data_init, data_fin]
      - (function_query) query_df 
      - (text markdown) title
      - col_name = nome da coluna a calcular
  """
  value = value if is_number is False else value if value >= 0 else 0 
  st.markdown(f"<h5 style='text-align: center; padding-top: 5%; line-height: 0px;color: grey;'><b>{title}</b></h5>", unsafe_allow_html=True)
  st.markdown(f"<h6 style='text-align: center; line-height: 0px;color: silver;'><b>{'Total' if is_total else ('Mediana' if is_median else 'Média') if is_number else ''}</b></h6>", unsafe_allow_html=True)
  st.markdown(f"<h{3 if is_sub else 1} style='text-align: center; line-height: 0px; padding-bottom: {padding_bottom}%; color: grey;'>{human_format(value) if is_number else value}</h{3 if is_sub else 1}>", unsafe_allow_html=True)

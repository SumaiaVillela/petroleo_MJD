# Gota a Gota - prospectando petróleo em produtos
<sup>***Uma ferramenta educativa com uso de IA para conscientização da onipresença do petróleo em nossas vidas***<sup>

Esse é um projeto que surgiu a partir de um desejo: **ampliar a discussão sobre a necessidade de se reduzir o uso do petróleo para além dos combustíveis.** A ideia era construir uma ferramenta de impacto educativo para que as pessoas pudessem refletir sobre produtos que as cercam.

Um protótipo de buscador de substâncias de petróleo em produtos foi criado com três tipos de inputs:
- A análise de imagens de rótulos e etiquetas de roupas;
- A análise de textos (listas de ingredientes, por exemplo);
- E a disponibilização da lista de substâncias, para consulta, que usamos como parte da análise dos dois outros inputs.

A aplicação foi criada como trabalho final da primeira metade o Marter em Jornalismo de Dados, Automação e Data Storytelling do Insper.

Usei `Python`, `Flask`, `HTML`, `CSS`, `Google Sheets` e o `ChatGPT` (para imagem e texto) para desenvolver o projeto.

> [!IMPORTANT]
> Apesar de ter contado com a ajuda de um PhD em química para acompanhar a precisão das informações fornecidas pela ferramenta nesta primeira fase de desenvolvimento, como detalho mais abaixo, 
ela não deve ser usada com objetivos científicos.

Cabe ressaltar, no entanto, que há potencial para o desenvolvimento de uma aplicação que utilize informação cientificamente embasada para análise dos inputs extraídos com a ajuda de Inteligência Artificial. Explicamos mais à frente como iniciamos esse processo e qual a forma que usamos para monitorar as respostas dadas via IA.

***Se quiser apoiar esse projeto, entre em contato: dadosparasumaia@gmail.com***

## Os recursos

Para construir a ferramenta, era preciso:
- Ferramenta de extração de texto de imagem (image to text);
- Uma maneira de analisar possíveis derivados de petróleo e responder ao usuário;
- Plataforma de usabilidade (o site foi o escolhido) e envio de inputs;
- Conteúdo complementar, informativo, para apresentar o tema e ajudar a causar impacto em usuários;
- Controle do que estava sendo respondido pela Inteligência Artificial.

### Image to text

Para a **extração de texto das imagens**, o modelo escolhido foi o ChatGPT, acessado via API. A escolha foi feita após pesquisa de modelos de machine learning gratuitos em Hugging Face, que não resultou na combinação de simplicidade de uso da API + qualidade da extração de texto.

É bom ressaltar que há custos nesta escolha, embora, na escala de testes, não seja significativo (a limitação de tokens foi usada tanto para formatar os retornos de forma mais padronizada como para controlar o gasto da ferramenta).


```python
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
  prompt = "Existe uma lista de ingredientes nesta imagem. O trecho normalmente começa com 'composição', 'ingredientes', 'ingredients', 'ingr' ou uma palavra sinônima. Extraia essa lista de ingredientes."
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ROBO_GPT_TOKEN}"
  }
```


Após envio de diferentes qualidade de imagem (nitidez, enquadramento, iluminação) e de diferentes fontes (de rótulos a símbolos do tipo de plástico em embalagens), foram fornecidas instruções ao usuário, no site, para que a foto/print resulte em maior chance de retorno, e foi delimitado o escopo de rótulos e etiquetas de roupa.

Há também a possibilidade de envio de texto direto na ferramenta, cujos procedimentos de análise são os mesmos do conteúdo que foi extraído da imagem.

### Análise dos inputs 

A função que envia o input do site para a API do ChatGPT e retorna o texto é combinada, na sequência, com a análise fundamental: **há ou não possíveis derivados de petróleo no item?**

O uso exclusivo de IA para fornecer as repostas sobre possíveis derivados de petróleo presentes nos inputs não era o ideal, seja pela possibilidade de erros, pela falta de padronização na resposta ou pela ausência de referência científica. Meu protótipo começou a implementar uma metodologia para minimizar essas questões - e que deve ficar mais robusta caso o projeto tenha continuidade.

A princípio, a escolha foi por **construir uma lista de substâncias derivadas do petróleo para comparação primária com os inputs**, e somente na ausência de reconhecimento, a automatização pede ao ChatGPT a resposta. Foram adicionados termos em português e inglês e siglas, de acordo com o que aparece usualmente em rótulos. O código normaliza as palavras (retira acento, por ex), as coloca em caixa baixa e ambas as colunas são percorridas, garantindo que não sejam adicionados termos repetidos ao resultado. Veja parte da lógica abaixo: 


```python
    for i, termo in enumerate(termos_coluna1):
        termo_sem_acentos = unicodedata.normalize('NFKD', termo).encode('ASCII', 'ignore').decode('utf-8')
        if termo_sem_acentos.lower() in texto_sem_acentos.lower():
            termo_encontrado = termo
            tem_derivado = termos_coluna3[i]
            explicacao = termos_coluna4[i]
            if termo_encontrado:
                termos_presentes.append({
                    'termo_encontrado': termo_encontrado,
                    'tem_derivado': tem_derivado,
                    'explicacao': explicacao
                })
```


> [!NOTE]
> A ideia inicial era usar raspagem de dados para isso, mas as listas de produtos químicos, aditivos alimentares e outros conjuntos de dados mais ou menos estruturados não costumavam explicitar a origem no petróleo, e tampouco traziam linguagem acessível ao público leigo para definição de uso. Por isso, até que exista tempo e recursos para a busca de bases de dados que possam ser raspadas, a opção desta primeira fase foi construir a lista manualmente, com sistematização e síntese do ChatGPT e revisão de especialista.

Foram testados diferentes formatos de prompt para garantir que respostas absolutas fossem evitadas e a objetividade fosse encorajada. Optei por passar o número de tokens também no prompt, porque o que ocorria é a resposta chegar cortada, não concluída, sem isso.


```python
if termos_presentes:
    resposta = termos_presentes

  elif not termos_presentes:
    prompt = "Analise se o termo ou a lista de termos enviada tem derivados de petróleo. Caso exista alguma substância geralmente derivada de petróleo, indique, de forma objetiva, qual é ou quais são e em que produtos normalmente é usada ou são usadas. Caso não tenha, informe que não foi possível encontrar dentro do limite dos seus conhecimentos (e não acrescente nada mais sobre que produtos ou substâncias podem ser derivadas do petróleo). O retorno deste prompt precisa ter no máximo 300 tokens."
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ROBO_GPT_TOKEN}"
    }
```


Essas etapas foram colocadas em funções diferentes, tanto para construir um fluxo em módulos que pudesse reaproveitar partes repetidas de código, como para organizar alguns recursos do `Flask`, usado para estruturar o site - rotas, inputs e outputs, conexão com o HTML e com o servidor. E o banco de dados escolhido para armazenar a lista inicial de substâncias foi a planilha eletrônica do Google, pela facilidade em enviar o conteúdo para validação do professor de química da UFF que auxiliou no projeto.

### Construção do site
O objetivo foi que o site apresentasse não só a ferramenta, mas a problemática (a onipresença do petróleo). Ele foi pensado como um protótipo do conteúdo que pode ser construído em torno da funcionalidade.

Ele foi construído em `Flask`, `HTML` e `CSS`.

A identidade visual tem o preto da substância e o laranja do macacão dos petroleiros a Petrobras, presente também, em diferentes tons, nos equipamentos de segurança e até mesmo nas plataformas de extração de petróleo.

Um texto traz a apresentação do problema - a dimensão da presença do petróleo nas coisas que usamos cotidianamente -, do porquê devemos nos preocupar com isso e da apresentação da ferramenta. Há também um infográfico para concretizar essa variedade de itens para o usuário.

### Monitoramento
Como já citado, o projeto contou com a observação voluntária do professor do Departamento de Química Inorgânica da Universidade Federal Fluminense (UFF), [Thiago de Melo Lima](http://buscatextual.cnpq.br/buscatextual/visualizacv.do;jsessionid=D33923E61978548D3A75BDE03999A811.buscatextual_0). A escolha se deu pela pesquisa que desenvolve: [desenvolve fontes de energia alternativas ao petróleo](https://www.uff.br/?q=noticias/06-06-2023/pesquisa-da-uff-desenvolve-fontes-de-energia-alternativas-ao-petroleo), utilizando plantas que são um "problema" em grandes centros urbanos.

Primeiro, discutimos quais os parâmetros mais seguros para o prompt do ChaGPT, dada a necessidade de não usar respostas absolutas (muitas substâncias, por exemplo, possuem versão orgânica e sintética) e tornar a resposta de IA mais precisa.

Depois, outra planilha eletrônica foi adicionada ao processo. Desta vez, para armazenar as respostas dadas pelo GPT após o envio de input de texto (oriundo de imagem ou não) para o modelo. Assim, era possível verificar como a IA estava reagindo a diferentes prompts. Ambos reviamos esse conteúdo para aperfeiçoamento da ferramenta.

O professor também revisou a lista de substâncias adotadas como verificador primário. E iniciamos uma discussão sobre métodos automatizados de adição de novas substâncias, mas esta etapa foi deixada para uma nova entrega, em função do tempo.

## Potenciais

Quando o projeto foi pensado, o primeiro passou que pensei em dar foi raspar os nomes de substâncias derivadas do petróleo e suas descrições de sites ou bases de dados abertas. Essa se mostrou a maior dificuldade. Ao que parece não há uma sistematização dessas substâncias com o recorte desejado, somente das "famílias" das substâncias, como naftas, que não são os termos encontrados em rótulos. Essa limitação, que não permitiu a robustez que foi inicialmente planejada, também expos uma oportunidade, que é criar esse banco de dados por meio e ao longo de uma segunda etapa do projeto.

É possível atuar em conjunto com especialistas da área para a construção de uma lista cientificamente referenciada, com links para comprovação das informações, que possa vir a ser uma referência de pesquisa. Outra possível funcionalidade é criar um grande banco de dados com nomes de produtos ou até mesmo itens genéricos (bola de futebol, lente de contato), que possa expor concretamente se geralmente possui derivado de petróleo. O trabalho braçal pode ser feito inclusive com a ajuda do ChatGPT, deixando o trabalho humano para a revisão e aperfeiçoamento dos dados.

Outra possibilidade é evoluir o projeto para uma reportagem especial, com mais fontes, dados e publicação em um veículo jornalístico.

## Limitações e transparência

Como já explicitado ao longo do arquivo, o projeto não pode ser encarado como uma busca científica ou fornecedor de respostas absolutas. Ainda há razoável espaço para imprecisões.

O principal limitador do projeto, atualmente, é a falta de coleta automatizada e estruturada das substâncias. Esse fator será melhor estudado para um novo ciclo de melhorias, mas um pool de especialistas e o financiamento do projeto para a reestruturação da ferramenta com bases científicas sólidas e referenciadas são caminhos viáveis para tornar a ferramenta mais robusta.

Os custos para deixar o projeto no ar como está agora também devem ser mensurados, pois a API do ChatGPT é paga. Além disso, o servidor gratuito que coloca o site online não roda a ferramenta com a velocidade necessária. A manutenção de uma consultoria especializada também demandar ou pagamento direto ou o convênio com um instituto de pesquisa universitário.

É importante citar também que o ChatGPT foi usado como "assistente" para a identificação de erros em alguns processos e especialmente na construção de `CSS`, embora muitas das vezes a desenvolvedora é que corrigisse a Inteligência Artificial.


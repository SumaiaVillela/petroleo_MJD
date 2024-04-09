# Gota a Gota - prospectando petróleo em produtos
<sup>***Uma ferramenta educativa com uso de IA para conscientização da onipresença do petróleo em nossas vidas***<sup>

Esse é um projeto que surgiu a partir de um desejo: **ampliar a discussão sobre a necessidade de se reduzir o uso do petróleo para além dos combustíveis.** A ideia era construir uma ferramenta de impacto educativo para que as pessoas pudessem refletir sobre produtos que as cercam.

Um protótipo de buscador de substâncias de petróleo em produtos foi criado com três tipos de inputs: a análise de imagens de rótulos e etiquetas de roupas; a de textos (listas de ingredientes, por exemplo) e a disponibilização da lista que usamos como parte da análise dos dois outros inputs.

A aplicação foi criada como trabalho final da primeira metade o Marter em Jornalismo de Dados, Automação e Data Storytelling do Insper.

Usei `Python`, `Flask`, `HTML`, `CSS`, `Google Sheets` e o `ChatGPT` (para imagem e texto) para desenvolver o projeto.

> [!IMPORTANT]
> Apesar de ter contado com a ajuda de um PhD em química para acompanhar a precisão das informações fornecidas pela ferramenta nesta primeira fase de desenvolvimento, como detalho mais abaixo, 
ela não deve ser usada com objetivos científicos.

Cabe ressaltar, no entanto, que há potencial para o desenvolvimento de uma aplicação que utilize informação cientificamente embasada para análise dos inputs extraídos com a ajuda de Inteligência Artificial. Explicamos mais à frente como iniciamos esse processo e qual a forma que usamos para monitorar as respostas dadas via IA.

***Se quiser financiar esse projeto, entre em contato: dadosparasumaia@gmail.com***

## Os recursos

Para construir a ferramenta, era preciso:
- Ferramenta de extração de texto de imagem (image to text);
- Uma maneira de analisar possíveis derivados de petróleo e responder ao usuário;
- Plataforma de usabilidade (o site foi o escolhido) e envio de inputs;
- Conteúdo complementar, informativo, para apresentar o tema e ajudar a causar impacto em usuários.

### Image to text

Para a **extração de texto das imagens**, o modelo escolhido foi o ChatGPT, acessado via API. A escolha foi feita após pesquisa de modelos de machine learning gratuitos em Hugging Face, que não resultou na combinação de simplicidade de uso da API + qualidade da extração de texto.

É bom ressaltar que há custos nesta escolha, embora, na escala de testes, não seja significativo (a limitação de tokens foi usada tanto para formatar os retornos de forma mais padronizada como para controlar o gasto da ferramenta).

Após envio de diferentes qualidade de imagem (nitidez, enquadramento, iluminação) e de diferentes fontes (de rótulos a símbolos do tipo de plástico em embalagens), foram fornecidas instruções no site para que a foto/print resulte em maior chance de retorno, e foi delimitado o escopo de rótulos e etiquetas de roupa.

Há também a possibilidade de envio de texto direto na ferramenta, cujos procedimentos de análise são os mesmos do conteúdo que foi extraído da imagem.

### Análise dos inputs 

A função que envia o input do site para a API do ChatGPT e retorna o texto é combinada, na sequência, com a análise fundamental: **há ou não possíveis derivados de petróleo no item?**

O uso exclusivo de IA para fornecer as repostas sobre possíveis derivados de petróleo presentes nos inputs não era o ideal, seja pela possibilidade de erros, pela falta de padronização na resposta ou pela ausência de referência científica. Meu protótipo começou a implementar uma metodologia para minimizar essas questões - e que deve ficar mais robusta caso o projeto tenha continuidade.

A princípio, a escolha foi por **construir uma lista de substâncias derivadas do petróleo para comparação primária com os inputs**, e somente na ausência de reconhecimento, a automatização pede ao ChatGPT a resposta.

> [!NOTE]
> A ideia inicial era usar raspagem de dados para isso, mas as listas de produtos químicos, aditivos alimentares e outros conjuntos de dados mais ou menos estruturados não costumavam explicitar a origem no petróleo, e tampouco traziam linguagem acessível ao público leigo para definição de uso. Por isso, até que exista tempo e recursos para a busca de bases de dados que possam ser raspadas, a opção desta primeira fase foi construir a lista manualmente, com sistematização e síntese do ChatGPT e revisão de especialista.

Essas etapas foram colocadas em funções diferentes, tanto para construir um fluxo em módulos que pudesse reaproveitar partes repetidas de código, como para organizar alguns recursos do `Flask`, usado para estruturar o site - rotas, inputs e outputs, conexão com o HTML e com o servidor. E o banco de dados escolhido para armazenar a lista inicial de substâncias foi a planilha eletrônica do Google, pela facilidade em enviar o conteúdo para validação do professor de química da UFF que auxiliou no projeto.

### Construção do site

### Conteúdo complementar

## Monitoramento
Como já citado, o projeto contou com a observação voluntária do professor do Departamento de Química Inorgânica da Universidade Federal Fluminense (UFF), [Thiago de Melo Lima](http://buscatextual.cnpq.br/buscatextual/visualizacv.do;jsessionid=D33923E61978548D3A75BDE03999A811.buscatextual_0). A escolha se deu pela pesquisa que desenvolve: [desenvolve fontes de energia alternativas ao petróleo](https://www.uff.br/?q=noticias/06-06-2023/pesquisa-da-uff-desenvolve-fontes-de-energia-alternativas-ao-petroleo), utilizando plantas que são um "problema" em grandes centros urbanos.

Primeiro, discutimos quais os parâmetros mais seguros para o prompt do ChaGPT, dada a necessidade de não usar respostas absolutas (muitas substâncias, por exemplo, possuem versão orgânica e sintética) e tornar a resposta de IA mais precisa.

Depois, outra planilha eletrônica foi adicionada ao processo. Desta vez, para armazenar as respostas dadas pelo GPT após o envio de input de texto (oriundo de imagem ou não) para o modelo. Assim, era possível verificar como a IA estava reagindo a diferentes prompts. Ambos reviamos esse conteúdo para aperfeiçoamento da ferramenta.

O professor também revisou a lista de substâncias adotadas como verificador primário. E iniciamos uma discussão sobre métodos automatizados de adição de novas substâncias, mas esta etapa foi deixada para uma nova entrega, em função do tempo.


## Potenciais


## Limitações e transparência

Como já explicitado ao longo do arquivo, o projeto não pode ser encarado como uma busca científica ou fornecedor de respostas absolutas. Ainda há razoável espaço para imprecisões.

O principal limitador do projeto, atualmente, é a falta de coleta automatizada e estruturada das substâncias. Esse fator será melhor estudado para um novo ciclo de melhorias, mas um pool de especialistas e o financiamento do projeto para a reestruturação da ferramenta com bases científicas sólidas e referenciadas (por exemplo, raspando artigos científicos a partir dos nomes das substâncias e adicionando à resposta ao usuário) são caminhos viáveis para tornar a ferramenta mais robusta.

É importante citar também que o ChatGPT foi usado como "assistente" para a construção de códigos e identificação de erros em alguns processos, embora muitas das vezes a desenvolvedora é que corrigisse a Inteligência Artificial. Entendo que essa é uma ferramenta válida de aprendizado e agilização de tarefas, especialmente para jornalistas de dados iniciantes, embora só seja plenamente útil se soubermos o que estamos fazendo.


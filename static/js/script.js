document.addEventListener('DOMContentLoaded', function() {
  // Imagem do cabeçalho fixada parcialmente
  const header = document.getElementById('header');
  headerHeight = 556;
  const headerImage = document.querySelector('.cabeçalho-embaixo img');

  // Define a altura do cabeçalho só quando a imagem é carregada
  headerImage.addEventListener('load', function() {
    const headerHeight = headerImage.offsetHeight;
    const fixedPoint = headerHeight / 1.5;

    // Define um ponto em que a imagem será fixada a partir da rolagem da tela
    window.addEventListener('scroll', function() {
      if (window.scrollY >= fixedPoint) {
        header.classList.add('fixed-partial');
        header.style.top = `-${fixedPoint}px`;

        // Criação da nova div apenas após o scroll atingir o fixedPoint
        if (!document.getElementById('new-div')) {
          const newDiv = document.createElement('div');
          newDiv.id = 'new-div';
          newDiv.style.marginTop = `${headerHeight}px`; // Ajustado para usar headerHeight

          // Seleção do ponto onde a nova div será inserida
          const insertionPoint = document.getElementById('insertion-point');
          insertionPoint.parentNode.insertBefore(newDiv, insertionPoint.nextSibling);
        }
      } else {
        header.classList.remove('fixed-partial');
        header.style.top = '0';

        // Remove a nova div se o scroll for menor que o fixedPoint
        const newDiv = document.getElementById('new-div');
        if (newDiv) {
          newDiv.parentNode.removeChild(newDiv);
        }
      }
    });
  });

  // Menu toggle
  const iconeMenuToggle = document.querySelector('.menu-toggle');
  const conteudoToggle = document.querySelector('.conteudo-toggle');
  const menuPrincipal = document.querySelector('.menu-principal');

  // Função para trocar os menus conforme tamanho da tela
  function handleResize() {
    if (window.innerWidth > 700) {
      iconeMenuToggle.style.display = 'none';
      conteudoToggle.classList.remove('mostrar');
      menuPrincipal.style.display = 'flex';
    } else {
      iconeMenuToggle.style.display = 'block';
      menuPrincipal.style.display = 'none';
    }
  }

  // Mostra as opções do menu quando o ícone é clicado
  iconeMenuToggle.addEventListener('click', function() {
    conteudoToggle.classList.toggle('mostrar');
  });

  // Verificação inicial ao carregar a página
  handleResize();

  // Observa o redimensionamento da janela
  window.addEventListener('resize', handleResize);

  // Joguinho narrativo do começo do material

  // Criação das sentenças e opções para cada lacuna
  const story = [
    {
      text: "Um barulho invade o sonho. A pessoa alcança o/os _______ na mesa de cabeceira e desliga o alarme.",
      options: ["óculos", "celular", "rádio-relógio"]
    },
    {
      text: "Levanta da cama e arruma os/as _______ sobre um colchão fino.",
      options: ["lençóis", "roupas", "travesseiros"]
    },
    {
      text: "Abre a janela e rasteja até o banheiro. Pega o/a _______ e encara o rosto sonolento no espelho.",
      options: ["pasta de dente", "barbeador", "escova de dente"]
    },
    {
      text: "No banho, nota que o _______ está no fim e ainda é dia 15.",
      options: ["shampoo", "sabonete", "condicionador"]
    },
    {
      text: "Veste um/uma _______ para trabalhar",
      options: ["casaco de nylon", "gravata", "meia-calça"]
    },
    {
      text: "Pega a caneta e anota o que precisa comprar: detergente, margarina e _______.",
      options: ["pimentão", "chocolate", "tomate"]
    },
    {
      text: "Passa _______ apressadamente e sai, alcançando a bolsa e torcendo a chave na porta com rapidez.",
      options: ["perfume", "desodorante", "batom"]
    },
    {
      text: "No caminho para o ponto de ônibus, pula um/uma _______ na calçada estreita e xinga mentalmente.",
      options: ["saco de lixo", "mancha de óleo automotivo", "cano quebrado de esgoto"]
    },
    {
      text: "Um/uma _______ aparece virando a esquina, chacoalhando no asfalto esburacado de um bairro do subúrbio.",
      options: ["ônibus", "bicicleta", "carro elétrico"]
    },
    {
      text: "Finalmente a linha chega e desvia o olhar daquele balanço desritmado. Usa o cartão do vale transporte e segue em pé, com o/a _______ balançando na mochila.",
      options: ["marmita", "guarda-chuva", "notebook"]
    },
    {
      text: "Vê pela janela um restaurante japonês baratinho e deseja salmão, mas precisa do dinheiro para a/o _______.",
      options: ["ração do gato", "pintar o cabelo", "lente de contato nova"]
    }
  ];

  const storyContainer = document.getElementById("story-container");
  const optionsContainer = document.getElementById("options-container");

  let currentStep = 0;

  //Mostra cada sentença com as opções progressivamente, a cada escolha
  function showSentence() {
    if (currentStep < story.length) {
      const sentence = story[currentStep].text;
      const sentenceElement = document.createElement("p");
      sentenceElement.id = `sentence-${currentStep}`;
      sentenceElement.innerHTML = sentence.replace("_______", "<span class='lacuna'></span>");
      storyContainer.appendChild(sentenceElement);

      optionsContainer.innerHTML = "";
      story[currentStep].options.forEach(option => {
        const button = document.createElement("button");
        button.textContent = option;
        button.onclick = () => chooseOption(option, sentenceElement);
        optionsContainer.appendChild(button);
      });

      autoScroll(); // Adiciona rolagem automática ao mostrar uma nova sentença

      // Verifica se é a sexta sentença para fixar parcialmente o cabeçalho
      if (currentStep === 5) {
        const fixedPoint = headerHeight / 1.5;

        window.addEventListener('scroll', function checkHeaderPosition() {
          if (window.scrollY >= fixedPoint) {
            header.classList.add('fixed-partial');
            header.style.top = `-${fixedPoint}px`;

            // Criação da nova div apenas após o scroll atingir o fixedPoint
            if (!document.getElementById('new-div')) {
              const newDiv = document.createElement('div');
              newDiv.id = 'new-div';
              newDiv.style.marginTop = `${headerHeight}px`; // Ajustado para usar headerHeight

              // Seleção do ponto onde a nova div será inserida
              const insertionPoint = document.getElementById('insertion-point');
              insertionPoint.parentNode.insertBefore(newDiv, insertionPoint.nextSibling);
            }
          } else {
            header.classList.remove('fixed-partial');
            header.style.top = '0';

            // Remove a nova div se o scroll for menor que o fixedPoint
            const newDiv = document.getElementById('new-div');
            if (newDiv) {
              newDiv.parentNode.removeChild(newDiv);
            }
          }
        });
      }

    } else {
      optionsContainer.innerHTML = "";
      document.getElementById("message").classList.remove("hidden");
      enableScrollToShowContent();
      autoScroll(); // Adicionar a rolagem automática ao finalizar o jogo
    }
  }

  // Escolhe a opção e avança para a próxima sentença
  function chooseOption(option, sentenceElement) {
    sentenceElement.querySelector('.lacuna').textContent = option;
    currentStep++;
    showSentence();
  }

  // Rola automaticamente até o final da página
  function autoScroll() {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  }

  // Ativa a rolagem para mostrar o conteúdo conforme o scroll
  function enableScrollToShowContent() {
    window.addEventListener('scroll', handleScroll);
  }

  // Verifica o scroll para revelar todo o conteúdo oculto
  function handleScroll() {
    // Adicionar um pequeno buffer antes de revelar o conteúdo
    if (window.scrollY + window.innerHeight >= document.body.scrollHeight - 100) {
      revealAllHiddenContent();
      window.removeEventListener('scroll', handleScroll);
    }
  }

  // Revela todo o conteúdo oculto de forma animada, com atraso
  function revealAllHiddenContent() {
    const hiddenElements = document.querySelectorAll('.hidden-content');
    hiddenElements.forEach(element => {
      element.style.display = 'block';
      // Pequeno atraso antes de adicionar a classe `show`
      setTimeout(() => {
        requestAnimationFrame(() => {
          element.classList.add('show');
        });
      }, 100);
    });
  }

  // Iniciar o jogo narrativo quando o DOM estiver carregado
  showSentence();

  // ícone de rolagem pro topo
  window.addEventListener('scroll', function() {
    var voltarAoTopo = document.querySelector('.volta-topo');
    if (window.scrollY > window.innerHeight / 2) {
      voltarAoTopo.style.display = 'block';
    } else {
      voltarAoTopo.style.display = 'none';
    }
  });

  // Retorna ao topo ao clicar no ícone
  document.querySelector('.volta-topo').addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

});

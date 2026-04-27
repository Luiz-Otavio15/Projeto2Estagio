function scrollCarrossel(botao, direcao) {
    const contanier = botao.closest(".carrossel-container");
    const carrossel = contanier.querySelector(".carrossel");

    const larguraScroll = 220; // largura do card + gap

    carrossel.scrollBy({
        left: direcao * larguraScroll,
        behavior: 'smooth'
    });
}
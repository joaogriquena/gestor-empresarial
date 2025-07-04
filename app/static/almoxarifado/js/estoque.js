document.addEventListener('DOMContentLoaded', function () {
    const btnTabela = document.getElementById('btn-tabela');
    const btnCards = document.getElementById('btn-cards');
    const tabela = document.querySelector('.tabela-container');
    const cards = document.getElementById('cards-container');

    if (btnTabela && btnCards && tabela && cards) {
        btnTabela.addEventListener('click', () => {
            tabela.classList.remove('hidden');
            cards.classList.add('hidden');
            btnTabela.classList.add('active');
            btnCards.classList.remove('active');
        });

        btnCards.addEventListener('click', () => {
            cards.classList.remove('hidden');
            tabela.classList.add('hidden');
            btnCards.classList.add('active');
            btnTabela.classList.remove('active');
        });
    }
});

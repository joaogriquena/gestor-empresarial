document.addEventListener('DOMContentLoaded', () => {
    const btnTema = document.getElementById('btn-tema');
    const corpo = document.body;

    btnTema.addEventListener('click', () => {
        corpo.classList.toggle('modo-escuro');
        corpo.classList.toggle('modo-claro');
    });
});

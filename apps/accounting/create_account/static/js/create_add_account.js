document.addEventListener('DOMContentLoaded', function() {
    const choiceBtns = document.querySelectorAll('.choice-btn');
    const forms = document.querySelectorAll('.form-card');
    const backBtns = document.querySelectorAll('.btn-back');
    const createForm = document.getElementById('createForm');
    const joinForm = document.getElementById('joinForm');

    choiceBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.dataset.action;

            // Скрываем все формы
            forms.forEach(form => form.classList.remove('active'));

            // Показываем нужную форму
            if (action === 'create') {
                createForm.classList.add('active');
            } else if (action === 'join') {
                joinForm.classList.add('active');
            }

            // Прокрутка к форме
            document.querySelector('.form-card.active').scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    backBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            forms.forEach(form => form.classList.remove('active'));
        });
    });
});
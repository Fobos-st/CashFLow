document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('transactionsBody');

    // Пример структуры данных, которую должен генерировать backend
    const mockData = Array.from({ length: 20 }).map((_, i) => ({
        id: i,
        date: '20.10.2023',
        status: i % 2 === 0 ? 'business' : 'personal',
        statusName: i % 2 === 0 ? 'Бизнес' : 'Личное',
        type: i % 3 === 0 ? 'income' : 'expense',
        typeName: i % 3 === 0 ? 'Приход' : 'Расход',
        category: 'Маркетинг',
        subcategory: 'Реклама FB',
        amount: (Math.random() * 10000).toFixed(2)
    }));

    // Логика фильтрации (клиентская часть для удобства)
    const filters = document.querySelectorAll('.filter-select, .filter-input');
    filters.forEach(filter => {
        filter.addEventListener('change', () => {
            console.log('Отправка запроса на бэкенд с параметрами фильтрации...');
            // В твоем случае здесь может быть либо переход по URL с query string,
            // либо просто отправка формы.
        });
    });

    // Обработка формы
    const form = document.getElementById('addTransactionForm');
    form.addEventListener('submit', (e) => {
        // Твоему бэкенду нужно просто принять POST запрос отсюда
        console.log('Форма готова к отправке на сервер');
    });
});

function renderTable(data) {
    tableBody.innerHTML = data.map(item => `
        <tr>
            <td data-label="Дата">${item.date}</td>
            <td data-label="Статус"><span class="status-tag status-${item.status}">${item.statusName}</span></td>
            <td data-label="Тип" class="${item.type === 'income' ? 'type-income' : 'type-expense'}">${item.typeName}</td>
            <td data-label="Категория">${item.category}</td>
            <td data-label="Подкатегория">${item.subcategory}</td>
            <td data-label="Сумма" class="text-right"><strong>${item.amount} ₽</strong></td>
        </tr>
    `).join('');
}

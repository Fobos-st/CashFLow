document.addEventListener('DOMContentLoaded', function() {
    const filterType = document.getElementById('filterType');
    const filterCategory = document.getElementById('filterCategory');
    const filterSubCategory = document.getElementById('filterAnotherCategory');

    // Сохраняем все опции категорий и подкатегорий в массивы для фильтрации
    const allCategories = Array.from(filterCategory.querySelectorAll('option')).filter(opt => opt.value !== "");
    const allSubCategories = Array.from(filterSubCategory.querySelectorAll('option')).filter(opt => opt.value !== "");

    // Функция для сброса и блокировки селекта
    function resetAndDisable(selectElement) {
        selectElement.innerHTML = '<option value="">Выберите вариант</option>';
        selectElement.disabled = true;
        selectElement.dispatchEvent(new Event('change')); // Уведомляем дочерние элементы
    }

    // Логика для категорий (зависит от filterType)
    filterType.addEventListener('change', function() {
        const selectedTypeId = this.value;

        if (!selectedTypeId) {
            resetAndDisable(filterCategory);
            return;
        }

        // Фильтруем
        const filtered = allCategories.filter(opt => opt.getAttribute('data-type-id') === selectedTypeId);

        filterCategory.innerHTML = '<option value="">Выберите категорию</option>';
        filtered.forEach(opt => filterCategory.appendChild(opt.cloneNode(true)));
        filterCategory.disabled = false;

        // Сбрасываем подкатегории при смене типа
        resetAndDisable(filterSubCategory);
    });

    // Логика для подкатегорий (зависит от filterCategory)
    filterCategory.addEventListener('change', function() {
        const selectedCategoryId = this.value;

        if (!selectedCategoryId) {
            resetAndDisable(filterSubCategory);
            return;
        }

        // Фильтруем подкатегории по data-category-id
        const filtered = allSubCategories.filter(opt => opt.getAttribute('data-category-id') === selectedCategoryId);

        filterSubCategory.innerHTML = '<option value="">Выберите подкатегорию</option>';
        filtered.forEach(opt => filterSubCategory.appendChild(opt.cloneNode(true)));
        filterSubCategory.disabled = false;
    });

    // Инициализация (на случай если страница загружена с уже выбранными значениями)
    if (!filterType.value) filterCategory.disabled = true;
    if (!filterCategory.value) filterSubCategory.disabled = true;
});

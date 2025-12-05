console.log("Скрипт загружен!");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM загружен");
    
    const searchForm = document.getElementById('searchForm');
    const moodInput = document.getElementById('moodInput');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsCount = document.getElementById('resultsCount');
    
    // Инициализация карты 
    let map = L.map('map', {
        attributionControl: false
    }).setView([55.7558, 37.6173], 12);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    
    let markerLayer = L.layerGroup().addTo(map);

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const searchText = moodInput.value.trim();
        console.log("Форма отправлена, запрос:", searchText);
        
        if (!searchText) {
            alert("Введите запрос для поиска");
            return;
        }

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mood: searchText })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Ответ от сервера:", data);
            if (data.success) {
                displayResults(data.results);
                updateMap(data.results);
            } else {
                alert("Ошибка: " + data.error);
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
            alert("Ошибка соединения");
        });
    });
    
    function displayResults(restaurants) {
        console.log("Отображение результатов:", restaurants.length);
        
        if (restaurants.length === 0) {
            resultsContainer.innerHTML = '<div class="alert alert-info">Ничего не найдено</div>';
        } else {
            resultsContainer.innerHTML = restaurants.map((restaurant, index) => `
                <div class="card restaurant-card" data-index="${index}">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="card-title mb-0">${restaurant.name}</h6>
                            <div>
                                <span class="badge bg-secondary me-2">
                                    ${restaurant.price_range === 'бюджетный' ? '₽' : 
                                      restaurant.price_range === 'средний' ? '₽₽' : '₽₽₽'}
                                </span>
                                <span class="text-warning">★ ${restaurant.rating}</span>
                            </div>
                        </div>
                        <div class="mb-2">
                            <span class="badge bg-primary">${restaurant.cuisine}</span>
                            <span class="badge bg-info">${restaurant.atmosphere}</span>
                        </div>
                        <p class="card-text small">${restaurant.description}</p>
                        <div class="mb-2">
                            <small class="text-muted">📍 ${restaurant.address}</small>
                        </div>
                        <div>
                            ${restaurant.tags.map(tag => `<span class="badge bg-light text-dark me-1">${tag}</span>`).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        resultsCount.textContent = restaurants.length;
        resultsSection.style.display = 'block';
    }
    
    function updateMap(restaurants) {
        // Очищаем старые маркеры
        markerLayer.clearLayers();
        
        if (restaurants.length === 0) return;
        
        const bounds = [];
        
        restaurants.forEach((restaurant, index) => {
            // ИСПОЛЬЗУЕМ РЕАЛЬНЫЕ КООРДИНАТЫ ИЗ БАЗЫ ДАННЫХ

	const lat = restaurant.latitude || 55.7558;
            const lng = restaurant.longitude || 37.6173;
            
            const marker = L.marker([lat, lng])
                .addTo(markerLayer)
                .bindPopup(`
                    <div>
                        <strong>${restaurant.name}</strong><br>
                        <small>${restaurant.cuisine}</small><br>
                        <em>${restaurant.address}</em><br>
                        <span class="text-warning">★ ${restaurant.rating}</span>
                    </div>
                `);
            
            bounds.push([lat, lng]);
            
            // Добавляем обработчик клика на карточку
            setTimeout(() => {
                const card = document.querySelector(`[data-index="${index}"]`);
                if (card) {
                    card.addEventListener('click', () => {
                        // Подсвечиваем выбранную карточку
                        document.querySelectorAll('.restaurant-card').forEach(c => {
                            c.classList.remove('active');
                        });
                        card.classList.add('active');
                        
                        // Открываем попап на карте и приближаем
                        marker.openPopup();
                        map.setView([lat, lng], 15);
                    });
                }
            }, 100);
        });
        
        // Подстраиваем карту под все маркеры
        if (bounds.length > 0) {
            map.fitBounds(bounds, { padding: [20, 20] });
        }
    }
    
    // Быстрые кнопки
    document.querySelectorAll('.quick-mood').forEach(button => {
        button.addEventListener('click', function(e) {
            moodInput.value = e.target.dataset.mood;
            searchForm.dispatchEvent(new Event('submit'));
        });
    });
});
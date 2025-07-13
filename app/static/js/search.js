const input = document.getElementById('search');
const resultsBox = document.getElementById('results');

let timeout = null;

function performSearch(query) {
    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            resultsBox.innerHTML = '';
            if (data.length > 0) {
                data.forEach(book => {
                    const item = document.createElement('a');
                    item.href = `/book/${book.id}`;
                    item.className = 'list-group-item list-group-item-action';
                    item.textContent = book.title;
                    resultsBox.appendChild(item);
                });
                resultsBox.style.display = 'block';
            } else {
                resultsBox.style.display = 'none';
            }
        });
}

input.addEventListener('input', () => {
    clearTimeout(timeout);
    const query = input.value.trim();

    if (query.length < 2) {
        resultsBox.innerHTML = '';
        resultsBox.style.display = 'none';
        return;
    }

    timeout = setTimeout(() => performSearch(query), 300);
});

input.addEventListener('focus', () => {
    const query = input.value.trim();
    if (query.length >= 2) {
        performSearch(query);
    }
});

document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !resultsBox.contains(e.target)) {
        resultsBox.innerHTML = '';
        resultsBox.style.display = 'none';
    }
});


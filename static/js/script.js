let debounceTimer;
let currentFocus = -1;
const selectedFeatures = [];
function showSuggestions(suggestions) {
    const input = document.getElementById('song_name');
    const suggestionBox = document.getElementById('suggestions');
    suggestionBox.innerHTML = ''; 

    if (suggestions.length > 0) {
        suggestionBox.style.display = 'block';  

        suggestions.forEach(fullText => {
            const div = document.createElement('div');
            div.className = 'suggestion-item';

            const [song, artist] = fullText.includes(' by ') 
                ? fullText.split(' by ') 
                : [fullText, 'Unknown Artist'];

            div.innerHTML = `
                <div class="song-title">${song}</div>
                <div class="artist-name">${artist}</div>
            `;

            div.onclick = () => {
                input.value = song;
                suggestionBox.style.display = 'none';  
            };

            suggestionBox.appendChild(div);
        });
    } else {
        suggestionBox.style.display = 'none';  
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.getElementById('song_name');

    if (inputField) {
        inputField.addEventListener('input', function (e) {
            const songName = e.target.value.trim();
            clearTimeout(debounceTimer);

            debounceTimer = setTimeout(() => {
                if (songName.length > 1) {
                    $.ajax({
                        url: '/get_suggestions',
                        method: 'GET',
                        data: { song_name: songName },
                        success: (response) => showSuggestions(response.suggestions),
                        error: (xhr) => console.error('Error:', xhr.statusText)
                    });
                } else {
                    document.getElementById('suggestions').style.display = 'none';
                }
            }, 300);
        });

        inputField.addEventListener('keydown', function (e) {
            const items = document.getElementById('suggestions').children;

            if (['ArrowDown', 'ArrowUp', 'Enter'].includes(e.key)) {
                e.preventDefault();

                if (e.key === 'ArrowDown') {
                    currentFocus = Math.min(currentFocus + 1, items.length - 1);
                } else if (e.key === 'ArrowUp') {
                    currentFocus = Math.max(currentFocus - 1, -1);
                } else if (e.key === 'Enter' && currentFocus > -1) {
                    items[currentFocus].click();
                    return;
                }

                Array.from(items).forEach((item, index) => {
                    item.classList.toggle('highlighted', index === currentFocus);
                });
            }
        });
    }

    document.querySelector("form").addEventListener("submit", function () {
        const hiddenInput = document.getElementById("selected_features_input");
        hiddenInput.value = JSON.stringify(selectedFeatures);
    });

    document.querySelectorAll(".feature-button").forEach(button => {
        button.addEventListener("click", () => {
            button.classList.toggle('selected');
            const feature = button.dataset.feature;
            const index = selectedFeatures.indexOf(feature);

            if (index > -1) {
                selectedFeatures.splice(index, 1);
            } else {
                selectedFeatures.push(feature);
            }
        });
    });
});
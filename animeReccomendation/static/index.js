
addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchBtn');
    const resultsSection = document.getElementById('results');
    const searchText = document.getElementById("search-text");

    searchBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        console.log("Search button clicked");
        const MovieTitle = searchText.value;
        if (!MovieTitle) {
            alert('Please enter a search term.');
            return;
        }

        const response = await fetch("/recommend", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: MovieTitle })
        });

        if (response.ok) {
            const data = await response.json();
            for (let i = 0; i < data.length; i++) {
            const textElement = document.createElement('p');
            textElement.textContent = data[i];
            resultsSection.appendChild(textElement);
            }
        } else {
            resultsSection.innerHTML = '<p>Error fetching recommendations.</p>';
        }
    });




});

addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.getElementById("searchBtn");
    const resultsSection = document.getElementById("results");
    const searchText = document.getElementById("search-text");

    searchBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        
        // Clear previous results
        resultsSection.innerHTML = "";

        console.log("Search button clicked");
        const MovieTitle = searchText.value;
        console.log("Searching for:", MovieTitle);
        if (!MovieTitle) {
            alert("Please enter a search term.");
            return;
        }

        const response = await fetch("/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title: MovieTitle })
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Received data:", data);
            //data format is a list of objects with title, image, description, url , genres,  studio, producers

            data.forEach(item => {
                console.log(item.title, item.image);

                const itemContainer = document.createElement("div");
                itemContainer.classList.add("history-item", "mb-4", "d-flex", "bg-light"); 
                itemContainer.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.1)";
                itemContainer.style.padding = "15px";
                itemContainer.style.borderRadius = "8px";

                const image = document.createElement("img");
                image.src = item[1];
                image.style.max_width = "200px";
                image.style.borderRadius = "8px";
                image.alt = item.title;

                const textContainer = document.createElement("div");
                textContainer.classList.add("history-text-container", "mb-2");
                textContainer.style.marginLeft = "20px";
                textContainer.style.marginRight = "20px";

                const title = document.createElement("h3");
                title.textContent = item[0];
                const description = document.createElement("p");
                description.textContent = item[2];
                const studio = document.createElement("p");
                studio.textContent = "Studio: " + item[5];
                const genres = document.createElement("p");
                genres.textContent = "Genres: " + item[4];
                const producers = document.createElement("p");
                producers.textContent = "Producers: " + item[6];
                const link = document.createElement("a");
                link.href = item[3];
                link.textContent = "More Info";

                textContainer.appendChild(title);
                textContainer.appendChild(description);
                textContainer.appendChild(studio);
                textContainer.appendChild(producers);
                textContainer.appendChild(link);
            
                itemContainer.appendChild(image);
                itemContainer.appendChild(textContainer);

                resultsSection.appendChild(itemContainer);
            });
        } else {
            resultsSection.innerHTML = "<p>Error fetching recommendations.</p>";
        }
    });




});
const links = document.querySelectorAll('.sidebar a');
const contentDiv = document.querySelector('.content');

links.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default anchor click behavior
        const criteria = e.target.getAttribute('data-criteria'); // Get the criteria from the data attribute
        loadContent(criteria); // Function to load the corresponding content
    });
});

function loadContent(criteria) {
    // Fetch content based on criteria or show static content
    fetch(`/${criteria}`) // This assumes you have Flask routes set up
        .then(response => response.text())
        .then(html => {
            contentDiv.innerHTML = html; // Load new content
        })
        .catch(error => {
            console.error('Error loading content:', error);
        });
}
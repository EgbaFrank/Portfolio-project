document.addEventListener('DOMContentLoaded', () => {
	const buttons = document.querySelectorAll('.add-to-list');
	buttons.forEach((button) => {
		button.addEventListener('click', () => {
			const productId = button.dataset.id;
			const testListId = "3de5f04b-06f1-4aac-8647-5aeba3dc29b0"
			console.log(`Button clicked for product ID: ${productId}`);
			url = `http://127.0.0.1:5000/api/v1/shop_lists/${testListId}/products/${productId}`
			fetch(url, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({})
			})
			.then(response => {
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
			})
			.catch(error => console.error(error));
		});
	});

	const searchInput = document.getElementById('search-input');
	const searchButton = document.getElementById('search-button');

	searchButton.addEventListener('click', () => {
		const searchQuery = searchInput.value.trim();
		if (searchQuery !== '') {
			const formattedQuery = encodeURIComponent(searchQuery);
			window.location.href = `/product_search?name=${formattedQuery}`;
		}
	});
});

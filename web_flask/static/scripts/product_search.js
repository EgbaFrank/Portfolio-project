document.addEventListener('DOMContentLoaded', () => {
	const buttons = document.querySelectorAll('.add-to-list');
	buttons.forEach((button) => {
		button.addEventListener('click', () => {
			const productId = button.dataset.id;
			const testListId = "3de5f04b-06f1-4aac-8647-5aeba3dc29b0"
			console.log(`Button clicked for product ID: ${productId}`);
			const url = `http://127.0.0.1:5000/api/v1/shop_lists/${testListId}/products/${productId}`
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
			const url = 'http://127.0.0.1:5000/api/v1/products/search'
			fetch(url, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					name: formattedQuery
				})
			})
			.then(response => response.json())
			.then(data => {
				const container = document.getElementById('dynamic-content');
				container.innerHTML = '';
				data.shops.forEach(shop => {
					const shopHtml = `
					<section class="shop-section">
					<h2>${shop.shop_name}</h2>
					<div class="product-grid">
					${shop.products.map(product => `
					 	<div class="product-card">
						<div class="image-placeholder"></div>
						<p>${product.name}</p>
						<p>${product.brand}</p>
						<p class="price">$${product.price}</p>
						<button class="add-to-list" data-id="${product.id}">Add to List</button>
						<button class="see-details-button">See details</button>
						</div>
					`).join('')}
					</div>
					</section>
					`;
				container.insertAdjacentHTML('beforeend', shopHtml);
				});
			})
			.catch(error => console.error(error));
		}
	});
});

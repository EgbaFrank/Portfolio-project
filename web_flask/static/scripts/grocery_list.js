function updateTotalCost() {
	  const totalPriceElements = document.querySelectorAll('.total-price');
	  let totalCost = 0;

	  totalPriceElements.forEach((element) => {
		      const price = parseInt(element.innerText.replace('$', ''));
		      totalCost += price;
		    });

	  document.querySelector('.total-cost span').innerText = `$${totalCost}`;
}

document.addEventListener('DOMContentLoaded', () => {
	document.querySelectorAll('.quantity-input').forEach(input => {
		input.addEventListener('blur', () => {
			const productId = (input.dataset.id);
			const qty = parseInt(input.value);
			const testListId = "3de5f04b-06f1-4aac-8647-5aeba3dc29b0"
			const url = `http://127.0.0.1:5000/api/v1/shop_lists/${testListId}/products/${productId}`

			// Basic validation
			if (isNaN(qty) || qty < 1) {
				console.error('Invalid quantity');
				return;
			}

			fetch(url, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ quantity: qty })
			})
			.then(response => {
				if (response.ok) {
					console.log('Quantity updated successfully');
					const totalPriceElement = document.querySelector(`.total-price[data-id="${productId}"]`);
					const priceElement = document.querySelector(`.total-price[data-id="${productId}"]`);
					const price = parseInt(priceElement.dataset.price);

					const total = price * qty;
					totalPriceElement.innerText = `$${total}`;
					updateTotalCost();
				} else {
					console.error('Error:', response.status);
				}
			})
			.catch(error => console.error('Error:', error));
		});
	});

	document.querySelectorAll('.remove-btn').forEach(btn => {
		btn.addEventListener('click', () => {
			const productId = btn.dataset.id;
			const testListId = "3de5f04b-06f1-4aac-8647-5aeba3dc29b0"
			const url = `http://127.0.0.1:5000/api/v1/shop_lists/${testListId}/products/${productId}`

			fetch(url, {
				method: 'DELETE',
			})
			.then(response => {
				if (response.ok) {
					console.log('Resource deleted successfully');
					btn.closest('.product-item').remove();
					updateTotalCost();
				} else {
					console.error('Error:', response.status);
				}
			})
			.catch(error => console.error('Error:', error));
		});
	});

	const checkout = document.querySelector('.checkout-btn')
	checkout.addEventListener('click', () => {
		const testListId = "3de5f04b-06f1-4aac-8647-5aeba3dc29b0"
		url = `http://127.0.0.1:5000/api/v1/shop_lists/${testListId}/orders`

		fetch(url, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
		})
		.then(response => {
			if (response.ok) {
				window.location.href = `/orders`;
			} else {
				console.error('Error', response.status);
			}
		})
		.catch(error => console.error('Error', error));
	});
});

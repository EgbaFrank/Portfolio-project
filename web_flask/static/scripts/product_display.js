document.addEventListener('DOMContentLoaded', () => {
	const buttons = document.querySelectorAll('.add-to-list');
	buttons.forEach((button) => {
		button.addEventListener('click', () => {
			const productId = button.dataset.id;
			console.log(`Button clicked for product ID: ${productId}`);
		});
	});
});

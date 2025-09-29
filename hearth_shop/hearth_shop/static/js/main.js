// Disable right-click to deter downloads
document.addEventListener('contextmenu', e => e.preventDefault());

// Handle thumbnail clicks to open modal
document.querySelectorAll('.thumbnail a').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    const imageUrl = this.dataset.image;
    const productId = this.dataset.id;
    openModal(imageUrl, productId);
  });
});

// Modal logic
function openModal(imageUrl, productId) {
  const modal = document.getElementById('image-modal');
  modal.querySelector('img').src = imageUrl;
  modal.querySelector('button').dataset.id = productId;
  modal.style.display = 'block';
}

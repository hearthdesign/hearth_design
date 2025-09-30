// Disable right-click to deter downloads
document.addEventListener('contextmenu', e => e.preventDefault());

// Handle thumbnail clicks to open modal
// document.querySelectorAll('.thumbnail a').forEach(link => {
//   link.addEventListener('click', function(e) {
//     e.preventDefault();
//     const imageUrl = this.dataset.image;
//     const productId = this.dataset.id;
//     openModal(imageUrl, productId);
//   });
// });
document.querySelectorAll('.thumbnail a').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    const imageUrl = this.dataset.image;
    const productId = this.dataset.id;
    const title = this.dataset.title;
    openModal(imageUrl, productId, title);
  });
});


// Modal logic
// function openModal(imageUrl, productId) {
//   const modal = document.getElementById('image-modal');
//   modal.querySelector('img').src = imageUrl;
//   modal.querySelector('button').dataset.id = productId;
//   modal.style.display = 'block';
// }
function openModal(imageUrl, productId, title) {
  const modal = document.getElementById('image-modal');
  modal.querySelector('#modal-image').src = imageUrl;
  modal.querySelector('#modal-title').textContent = title;
  modal.querySelector('#modal-product-id').value = productId;
  modal.style.display = 'block';
}

// Close modal
document.querySelector('.close').addEventListener('click', () => {
  document.getElementById('image-modal').style.display = 'none';
});
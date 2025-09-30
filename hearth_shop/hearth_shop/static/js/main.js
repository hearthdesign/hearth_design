// Disable right-click to deter image downloads
document.addEventListener('contextmenu', e => e.preventDefault());

// Attach click listeners to all thumbnail links
document.querySelectorAll('.thumbnail a').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault(); // Prevent default link behavior

    // Extract image URL, product ID, and title from data attributes
    const imageUrl = this.dataset.image; 
    const productId = this.dataset.id; 
    const title = this.dataset.title;
    // Open modal with the extracted data attributes 
    openModal(imageUrl, productId, title);  
  });
});

// Function to populate and show the modal
function openModal(imageUrl, productId, title) {
  const modal = document.getElementById('image-modal');
  // Set image source and title
  modal.querySelector('#modal-image').src = imageUrl;
  modal.querySelector('#modal-title').textContent = title;
  // Set hidden input value for product ID and default quantity
  modal.querySelector('#modal-product-id').value = productId;
  modal.querySelector('#modal-quantity').value = 1;
  modal.style.display = 'block';  // show the modal
}

// Close modal when the close button is clicked
document.querySelector('.close').addEventListener('click', () => {
  document.getElementById('image-modal').style.display = 'none';
});
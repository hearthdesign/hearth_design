// ===============================
// NAVBAR: Hamburger Menu
// ===============================
const hamburger = document.getElementById("hamburger-btn");
const navLinks = document.getElementById("nav-links");

if (hamburger && navLinks) {
  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navLinks.classList.toggle("show");
  });
}

// ===============================
// NAVBAR: Language Switcher
// ===============================
const switchBtn = document.getElementById("switch-btn");
const languageForm = document.getElementById("language-form");
const languageSelect = document.getElementById("language-select");

if (switchBtn && languageForm) {
  switchBtn.addEventListener("click", () => {
    languageForm.style.display =
      languageForm.style.display === "none" ? "inline-block" : "none";
  });
}

if (languageSelect && languageForm) {
  languageSelect.addEventListener("change", () => {
    languageForm.submit();
  });
}

document.addEventListener('DOMContentLoaded', () => {

// Disable right-click to deter image downloads
document.addEventListener('contextmenu', e => e.preventDefault());

const galleryLinks = Array.from(document.querySelectorAll('.thumbnail a'));
let currentIndex = 0;

// Attach click listeners to all thumbnail links
galleryLinks.forEach((link, index) => {
  link.addEventListener('click', function(e) {
    e.preventDefault(); // Prevent default link behavior

    // Extract image URL, product ID, and title from data attributes
    currentIndex = index; // stores the currentIndex for navigation 
    const imageUrl = this.dataset.image;
    const productId = this.dataset.id;
    const title = this.dataset.title;
    // Open modal with the extracted data attributes 
    openModal(imageUrl, productId, title);  
  });
});
// Preload Images for Smoother Navigation
const preloadImages = () => {
  galleryLinks.forEach(link => {
    const img = new Image();
    img.src = link.dataset.image;
  });
};

preloadImages();

// Function to populate and show the modal
function openModal(imageUrl, productId, title) {
  const modal = document.getElementById('image-modal');
  // Set image source and title
  modal.querySelector('#modal-image').src = imageUrl;
  modal.querySelector('#modal-title').textContent = title;
  modal.classList.add('show');
  // Set hidden input value for product ID and default quantity
  const productInput = modal.querySelector('#modal-product-id');
  const quantityInput = modal.querySelector('#modal-quantity');

  if (productInput && quantityInput) {
    productInput.value = productId;
    quantityInput.value = 1;
  }

  modal.classList.add('show');
  modal.style.display = 'block';  // show the modal
}

function closeModal() {
  const modal = document.getElementById('image-modal');
  modal.classList.remove('show');
  setTimeout(() => {
    modal.style.display = 'none';
  }, 300); // match transition duration
}

// Close modal when clicking outside the modal content
const modal = document.getElementById('image-modal');
modal.addEventListener('click', function(e) {
  // Only close if the click is directly on the modal background
  if (e.target === modal) {
    closeModal();
  }
});


// Close modal when the close button is clicked
document.querySelector('.close').addEventListener('click', closeModal); 
document.getElementById('close-btn').addEventListener('click', closeModal);


// Function to navigate to the next image
function showNextImage() {
  currentIndex = (currentIndex + 1) % galleryLinks.length;
  const next = galleryLinks[currentIndex];
  openModal(next.dataset.image, next.dataset.id, next.dataset.title);
}
// Function to navigate to the previous image
function showPreviousImage() {
  currentIndex = (currentIndex - 1 + galleryLinks.length) % galleryLinks.length;
  const prev = galleryLinks[currentIndex];
  openModal(prev.dataset.image, prev.dataset.id, prev.dataset.title);
}

document.getElementById('prev-btn').addEventListener('click', showPreviousImage);
document.getElementById('next-btn').addEventListener('click', showNextImage);

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  const modal = document.getElementById('image-modal');
  if (modal.style.display === 'block') {
    if (e.key === 'ArrowRight') {
      showNextImage();
    } else if (e.key === 'ArrowLeft') {
      showPreviousImage();
    } else if (e.key === 'Escape') {
      modal.style.display = 'none';
    }
  }
});

});
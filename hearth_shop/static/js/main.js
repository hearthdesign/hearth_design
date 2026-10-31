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
// LOADS AFTER DOM CONTENT TO 
// ENSURE ELEMENTS ARE AVAILABLE
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  // ===============================
// NAVBAR: Theme Switcher
// ===============================

const themeBtn = document.getElementById("theme-btn");
const themeForm = document.getElementById("theme-form");
const themeSelect = document.getElementById("theme-select");

if (themeBtn && themeForm) {
    themeBtn.addEventListener("click", () => {
        themeForm.style.display =
            themeForm.style.display === "none"
                ? "inline-block"
                : "none";
    });
}

if (themeSelect && themeForm) {
    themeSelect.addEventListener("change", () => {

        if (themeSelect.value === "") {
            window.location.href = "/";
            return;
        }

        themeForm.submit();
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

  // ===============================
  // Disable right-click
  // to deter image downloads
  // ===============================
  document.addEventListener('contextmenu', e => e.preventDefault());
  
  // ===============================
  // GALLERY + MODAL LOGIC
  // ===============================
  const galleryLinks = Array.from(document.querySelectorAll('.thumbnail a'));
  let currentIndex = 0;
  
  // =============================================
  // Attach click listeners to all thumbnail links
  // to open the modal with the correct image
  // =============================================
  galleryLinks.forEach((link, index) => {
    link.addEventListener('click', function(e) {
      e.preventDefault(); // Prevent default link behavior
    
      // Extract image URL, product ID, and title from data attributes
      currentIndex = index; // stores the currentIndex for navigation 
      // Open modal with the data attributes 
      openModal(this.dataset.image, this.dataset.id, this.dataset.title,
    this.dataset.price);
  
    });
  });
  // =======================================
  // Preload Images for Smoother Navigation
  // ======================================
  const preloadImages = () => {
    galleryLinks.forEach(link => {
      const img = new Image();
      img.src = link.dataset.image;
    });
  };
  preloadImages();
  
  // ========================================
  // Function to populate and show the modal
  // ========================================
function openModal(imageUrl, productId, title, price) {
    const modal = document.getElementById("image-modal");

    if (!modal) {
        return;
    }

    modal.querySelector("#modal-image").src = imageUrl;
    modal.querySelector("#modal-title").textContent = title;

    const priceElement = modal.querySelector("#modal-price");

    if (priceElement) {
        priceElement.textContent = price || "";
    }

    const productInput = modal.querySelector("#modal-product-id");
    const quantityInput = modal.querySelector("#modal-quantity");

    if (productInput && quantityInput) {
        productInput.value = productId;
        quantityInput.value = 1;
    }

    modal.classList.add("show");
    modal.style.display = "block";
}
  
function closeModal() {
    const modal = document.getElementById("image-modal");

    if (!modal) {
        return;
    }

    modal.classList.remove("show");

    setTimeout(() => {
        modal.style.display = "none";
    }, 300); // match transition duration
  }
  
  
// Close modal when clicking outside the modal content
const modal = document.getElementById("image-modal");

if (modal) {
  modal.addEventListener("click", function (e) {
    if (e.target === modal) {
      closeModal();
    }
  });
}

// Close modal when the close button is clicked
const closeIcon = document.querySelector(".close");

if (closeIcon) {
  closeIcon.addEventListener("click", closeModal);
}

const closeBtn = document.getElementById("close-btn");

if (closeBtn) {
  closeBtn.addEventListener("click", closeModal);
}

const prevBtn = document.getElementById("prev-btn");

if (prevBtn) {
  prevBtn.addEventListener("click", showPreviousImage);
}

const nextBtn = document.getElementById("next-btn");

if (nextBtn) {
  nextBtn.addEventListener("click", showNextImage);
}

  // Function to navigate to the next image
  function showNextImage() {
    if (galleryLinks.length === 0) {
        return;
    }

    currentIndex = (currentIndex + 1) % galleryLinks.length;

    const next = galleryLinks[currentIndex];

    openModal(
        next.dataset.image,
        next.dataset.id,
        next.dataset.title,
        next.dataset.price
    );
}
  // Function to navigate to the previous image
  function showPreviousImage() {
    if (galleryLinks.length === 0) {
        return;
    }

    currentIndex =
        (currentIndex - 1 + galleryLinks.length) %
        galleryLinks.length;

    const prev = galleryLinks[currentIndex];

    openModal(
        prev.dataset.image,
        prev.dataset.id,
        prev.dataset.title,
        prev.dataset.price
    );
}
  
  // ====================
  // Keyboard navigation
  // ====================
  document.addEventListener('keydown', (e) => {
  const modal = document.getElementById('image-modal');

  if (!modal || modal.style.display !== 'block') {
    return;
  }

  if (e.key === 'ArrowRight') {
    showNextImage();
  } else if (e.key === 'ArrowLeft') {
    showPreviousImage();
  } else if (e.key === 'Escape') {
    closeModal();
  }
});
}
)


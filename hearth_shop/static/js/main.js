// jshint esversion: 11 

// ===============================
// MAIN JAVASCRIP
// Runs after the DOM has fully loaded
// ENSURE ELEMENTS ARE AVAILABLE
// ===============================
document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // NAVBAR: THEME SWITCHER
    // Automatically submits the form when a theme is selected
    // =====================================================
    const galleryCards = document.querySelectorAll(".gallery-card"); // Ensure this matches your CSS/HTML class
    let currentIndex = 0;
    const imagesData = [];

    // Collect data from all visible cards
    galleryCards.forEach((card, index) => {
        card.setAttribute("data-index", index);
        const img = card.querySelector("img");
        const title = card.querySelector(".print-title") ? card.querySelector(".print-title").textContent : "";
        const price = card.querySelector(".print-price") ? card.querySelector(".print-price").textContent : "";
        
        imagesData.push({
            src: img ? img.src : "",
            title: title,
            price: price
        });

        // Open modal on click
        card.addEventListener("click", () => {
            currentIndex = index;
            openModal(imagesData[currentIndex]);
        });
    });

    const modal = document.getElementById("imageModal"); // Adjust to your modal ID
    const modalImg = modal ? modal.querySelector(".modal-image") : null;
    const modalTitle = modal ? modal.querySelector(".modal-title") : null;
    const modalPrice = modal ? modal.querySelector(".modal-price") : null;

    function openModal(data) {
        if (!modal) return;
        if (modalImg) modalImg.src = data.src;
        if (modalTitle) modalTitle.textContent = data.title;
        if (modalPrice) modalPrice.textContent = data.price;
        modal.style.display = "block"; // or your active modal class toggle
    }

    // Fix the Next / Previous buttons
    const prevBtn = document.querySelector(".gallery-prev");
    const nextBtn = document.querySelector(".gallery-next");

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            currentIndex = (currentIndex - 1 + imagesData.length) % imagesData.length;
            openModal(imagesData[currentIndex]);
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            currentIndex = (currentIndex + 1) % imagesData.length;
            openModal(imagesData[currentIndex]);
        });
    }
});
// ===============================
// NAVBAR: Theme Switcher
// Automatically submit the form
// when a new theme is selected
// ===============================

const themeForm =
    document.getElementById("theme-form");

const themeSelect =
    document.getElementById("theme-select");

if (themeSelect && themeForm) {
    themeSelect.addEventListener("change", () => {
        console.log("Theme changed:", themeSelect.value);
        console.log("Submitting to:", themeForm.action);

        // Optional reset logic if needed in future:
        // if (themeSelect.value === "") {
        //     window.location.href =
        //         themeForm.action.replace("theme-filter/", "");
        //     return;
        // }

        themeForm.submit();
    });
}

  // ===============================
  // NAVBAR: Language Switcher
  // ===============================
  const languageForm = document.getElementById("language-form");
  const languageSelect = document.getElementById("language-select");

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

/* ===============================================
    COLLAPSIBLE INFO SECTION (prints formats)
=============================================== */
document.querySelectorAll(".gallery-info-trigger").forEach((btn) => {
  const panelId = btn.getAttribute("aria-controls");
  const panel = panelId ? document.getElementById(panelId) : null;
  if (!panel) return;

  btn.addEventListener("click", () => {
    const isExpanded = btn.getAttribute("aria-expanded") === "true";
    const nextState = !isExpanded;
    btn.setAttribute("aria-expanded", String(nextState));
    btn.classList.toggle("is-open", nextState);
    panel.hidden = !nextState;
  });
});

  // =============================================
// Attach click listeners to all gallery items
// Open modal using data attributes when available
// Fall back to visible card text if necessary
// =============================================

galleryLinks.forEach((link, index) => {

  link.addEventListener("click", function (e) {

    e.preventDefault();

    if (!this.dataset.image) {
      return;
    }

    currentIndex = index;

    // Find the surrounding gallery card
    const card = this.closest(".gallery-card");

    // Prefer data attributes.
    // If they are missing, use the visible text.
    const title =
      this.dataset.title ||
      card?.querySelector(".print-title")
        ?.textContent
        ?.trim() ||
      "";

    const price =
      this.dataset.price ||
      card?.querySelector(".print-price")
        ?.textContent
        ?.trim() ||
      "";

    openModal(
      this.dataset.image,
      this.dataset.id,
      title,
      price
    );
  });

});

  // =======================================
  // Preload Images for Smoother Navigation
  // ======================================
  const preloadImages = () => {
    galleryLinks.forEach(link => {
      if (!link.dataset.image) {
        return;
      }

      const img = new Image();
      img.src = link.dataset.image;
    });
  };
  preloadImages();

  // ========================================
  // Function to populate and show the modal
  // Safely exits if modal elements are not present
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
  // ========================================
  // Close modal safely
  // Prevent errors on pages without a gallery modal
  // ========================================
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
  // ========================================
  // Modal Controls
  // Add listeners only when modal elements exist
  // Prevent JavaScript errors on non-gallery pages
  // ========================================
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
  // Retains image, title, product ID and price
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
  // Retains image, title, product ID and price
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

  // ====================================
  // Keyboard navigation
  // Runs only while the modal is open
  // ====================================
  document.addEventListener('keydown', (e) => {
    const modal = document.getElementById('image-modal');
    // Exit gracefully when the modal is not available
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


// ====================================
// Back to top button
// ====================================
document.addEventListener('DOMContentLoaded', () => {
    const backToTopBtn = document.getElementById('back-to-top');
    if (!backToTopBtn) return;

    window.addEventListener('scroll', () => {
        // Total scrollable height minus the viewport height
        const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
        const currentScroll = window.scrollY;

        // Show button when the user is within 100px of the bottom of the page
        if (currentScroll >= scrollableHeight - 100) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });

    // Smooth scroll back to top when clicked
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

function initAboutHearthToggle() {
  const toggleBtn = document.getElementById("about-hearth-toggle");
  const panel = document.getElementById("about-hearth-panel");

  if (!toggleBtn || !panel) return;

  toggleBtn.addEventListener("click", () => {
    const isExpanded = toggleBtn.getAttribute("aria-expanded") === "true";
    const nextExpanded = !isExpanded;

    toggleBtn.setAttribute("aria-expanded", String(nextExpanded));
    toggleBtn.classList.toggle("is-open", nextExpanded);
    panel.hidden = !nextExpanded;
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initAboutHearthToggle);
} else {
  initAboutHearthToggle();
}
document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggle = document.getElementById("sidebarToggle");
  if (toggle && sidebar) toggle.addEventListener("click", () => sidebar.classList.toggle("open"));

  const path = window.location.pathname;
  document.querySelectorAll(".side-link").forEach(link => {
    if (link.getAttribute("href") && path === new URL(link.href).pathname) link.classList.add("active");
  });

  document.querySelectorAll(".flash").forEach(el => {
    setTimeout(() => { if (el.isConnected) el.remove(); }, 5000);
  });

  const file = document.querySelector('input[type="file"][name="image"]');
  if (file) {
    file.addEventListener("change", () => {
      const old = document.querySelector(".image-preview");
      if (old) old.remove();
      const selected = file.files && file.files[0];
      if (!selected) return;
      const img = document.createElement("img");
      img.className = "image-preview";
      img.alt = "Selected complaint image preview";
      img.src = URL.createObjectURL(selected);
      file.closest(".field")?.appendChild(img);
    });
  }
});
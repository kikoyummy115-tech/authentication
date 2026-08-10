function dismissToast(toastElement) {
  if (!toastElement) return;

  // 1. Trigger Tailwind transition animations smoothly out of view
  toastElement.classList.add("opacity-0", "-translate-y-4", "scale-95");

  // 2. Wait exactly for the 300ms transition duration to finish before scrubbing the HTML node element entirely
  setTimeout(() => {
    toastElement.remove();

    const container = document.getElementById("toast-container");
    if (container && container.children.length === 0) {
      container.remove();
    }
  }, 300);
}

// Automatically pick up all toasts present on view initialization execution
document.addEventListener("DOMContentLoaded", () => {
  const toasts = document.querySelectorAll(".toast-card");

  toasts.forEach((toast, index) => {
    // Stagger sequential item dismissals if multiple alerts trigger consecutively
    setTimeout(
      () => {
        dismissToast(toast);
      },
      4000 + index * 500,
    ); // Default alert view duration 4 seconds
  });
});

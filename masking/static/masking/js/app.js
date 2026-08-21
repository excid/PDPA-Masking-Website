function maskApp() {
  return {
    charCount: 0,
    selectedCount: 0,

    syncRuleCount() {
      this.selectedCount = document.querySelectorAll('input[name="rules"]:checked').length;
    },

    toggleAllRules() {
      const rules = [...document.querySelectorAll('input[name="rules"]')];
      const shouldEnable = this.selectedCount !== rules.length;
      rules.forEach((rule) => {
        rule.checked = shouldEnable;
      });
      this.syncRuleCount();
    },
  };
}

document.addEventListener("alpine:init", () => {
  window.maskApp = maskApp;
});

function setProcessingState(isProcessing) {
  document.querySelector(".app-shell")?.classList.toggle("is-processing", isProcessing);
  const submitButton = document.querySelector(".button-primary[type='submit']");
  if (submitButton) {
    submitButton.disabled = isProcessing;
    submitButton.setAttribute("aria-disabled", String(isProcessing));
  }
}

document.body?.addEventListener("htmx:beforeRequest", (event) => {
  if (event.detail.elt.closest(".mask-form")) {
    setProcessingState(true);
  }
});

document.body?.addEventListener("htmx:afterRequest", () => {
  setProcessingState(false);
});

document.body?.addEventListener("htmx:afterSwap", (event) => {
  if (event.detail.target.id === "input-area") {
    event.detail.target.querySelector("textarea")?.dispatchEvent(new Event("input", { bubbles: true }));
  }

  if (event.detail.target.id === "result" && window.innerWidth <= 760) {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    event.detail.target.closest(".output-panel")?.scrollIntoView({
      behavior: reduceMotion ? "auto" : "smooth",
      block: "start",
    });
  }
});

document.body?.addEventListener("htmx:responseError", () => {
  setProcessingState(false);
});

/* COMPSCI 301 — Week 1 exercises page behaviour.
 *
 * Two features only, both progressive enhancements:
 *   1. Language tabs. Clicking a language anywhere on the page selects that
 *      language for EVERY problem (and remembers it in localStorage), so
 *      students pick their language once.
 *   2. A "Copy" button per code group that copies the currently visible panel.
 *
 * Without JavaScript the page still works: <noscript> CSS reveals every
 * panel, so all reference answers are readable.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "cs301-week1-lang";
  var DEFAULT_LANG = "java";

  var groups = Array.prototype.slice.call(document.querySelectorAll(".tabs[data-tabs]"));
  if (groups.length === 0) {
    return;
  }

  function buttonsOf(group) {
    return Array.prototype.slice.call(group.querySelectorAll(".tab-btn[data-lang]"));
  }

  function panelsOf(group) {
    return Array.prototype.slice.call(group.querySelectorAll(".tab-panel[data-lang]"));
  }

  function setGroupLang(group, lang) {
    var buttons = buttonsOf(group);
    var panels = panelsOf(group);
    var hasLang = buttons.some(function (b) {
      return b.getAttribute("data-lang") === lang;
    });
    if (!hasLang) {
      return;
    }
    buttons.forEach(function (button) {
      var selected = button.getAttribute("data-lang") === lang;
      button.setAttribute("aria-selected", selected ? "true" : "false");
      button.tabIndex = selected ? 0 : -1;
    });
    panels.forEach(function (panel) {
      var selected = panel.getAttribute("data-lang") === lang;
      panel.hidden = !selected;
      panel.setAttribute("aria-hidden", selected ? "false" : "true");
    });
  }

  function selectLang(lang) {
    groups.forEach(function (group) {
      setGroupLang(group, lang);
    });
    try {
      window.localStorage.setItem(STORAGE_KEY, lang);
    } catch (err) {
      /* localStorage may be unavailable (file://, private mode); ignore. */
    }
    // If the student changed language from inside a group, keep that group's
    // active tab focused so the tablist stays keyboard-navigable.
    var focused = document.activeElement;
    if (focused && focused.classList.contains("tab-btn")) {
      var group = focused.closest(".tabs");
      if (group) {
        var match = group.querySelector('.tab-btn[data-lang="' + lang + '"]');
        if (match && match !== focused) {
          match.focus();
        }
      }
    }
  }

  function storedLang() {
    var value = null;
    try {
      value = window.localStorage.getItem(STORAGE_KEY);
    } catch (err) {
      value = null;
    }
    var known = buttonsOf(groups[0]).map(function (b) {
      return b.getAttribute("data-lang");
    });
    return value && known.indexOf(value) !== -1 ? value : DEFAULT_LANG;
  }

  // --- tabs -----------------------------------------------------------------
  groups.forEach(function (group) {
    group.addEventListener("click", function (event) {
      var button = event.target.closest(".tab-btn[data-lang]");
      if (!button || !group.contains(button)) {
        return;
      }
      selectLang(button.getAttribute("data-lang"));
    });

    group.addEventListener("keydown", function (event) {
      var button = event.target.closest(".tab-btn[data-lang]");
      if (!button) {
        return;
      }
      var buttons = buttonsOf(group);
      var index = buttons.indexOf(button);
      var next = null;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") {
        next = buttons[(index + 1) % buttons.length];
      } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
        next = buttons[(index - 1 + buttons.length) % buttons.length];
      } else if (event.key === "Home") {
        next = buttons[0];
      } else if (event.key === "End") {
        next = buttons[buttons.length - 1];
      }
      if (!next) {
        return;
      }
      event.preventDefault();
      next.focus();
      selectLang(next.getAttribute("data-lang"));
    });
  });

  var initialLang = storedLang();
  groups.forEach(function (group) {
    setGroupLang(group, initialLang);
  });

  // --- copy button ----------------------------------------------------------
  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      try {
        var ok = document.execCommand("copy");
        document.body.removeChild(area);
        ok ? resolve() : reject(new Error("copy failed"));
      } catch (err) {
        document.body.removeChild(area);
        reject(err);
      }
    });
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest(".copy-btn");
    if (!button) {
      return;
    }
    var group = button.closest(".tabs");
    if (!group) {
      return;
    }
    var panel = group.querySelector(".tab-panel:not([hidden])");
    if (!panel) {
      return;
    }
    var code = panel.querySelector("pre, code") || panel;
    var text = code.innerText.replace(/\s+$/, "");
    var original = button.textContent;
    copyText(text)
      .then(function () {
        button.textContent = "Copied!";
        button.classList.add("copied");
      })
      .catch(function () {
        button.textContent = "Press Ctrl+C";
      })
      .finally(function () {
        window.setTimeout(function () {
          button.textContent = original;
          button.classList.remove("copied");
        }, 1400);
      });
  });
})();

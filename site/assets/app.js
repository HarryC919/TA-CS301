/* Progressive enhancements for static code: highlighting, temporary starter
 * editors, synchronized language tabs, copy and reset. Only the language choice
 * is persisted; edited code lives in textarea elements and resets on page load.
 */
(function () {
  "use strict";

  document.querySelectorAll(".recitation-menu").forEach(function (menu) {
    document.addEventListener("click", function (event) {
      if (!menu.contains(event.target)) menu.open = false;
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && menu.open) {
        menu.open = false;
        menu.querySelector("summary").focus();
      }
    });
  });

  // Theme switch: follow system → light → dark. Only "light"/"dark" are stored.
  var themeToggle = document.querySelector(".theme-toggle");
  if (themeToggle) {
    var THEME_KEY = "cs301-theme";
    var themeModes = ["auto", "light", "dark"];
    var themeLabels = { auto: "Theme: follow system", light: "Theme: light", dark: "Theme: dark" };
    var currentTheme = function () {
      var value = document.documentElement.getAttribute("data-theme");
      return value === "light" || value === "dark" ? value : "auto";
    };
    var showTheme = function (mode) {
      themeToggle.setAttribute("data-mode", mode);
      themeToggle.setAttribute("aria-label", themeLabels[mode] + " (click to change)");
      themeToggle.title = themeLabels[mode];
    };
    themeToggle.addEventListener("click", function () {
      var mode = themeModes[(themeModes.indexOf(currentTheme()) + 1) % themeModes.length];
      if (mode === "auto") {
        document.documentElement.removeAttribute("data-theme");
      } else {
        document.documentElement.setAttribute("data-theme", mode);
      }
      try {
        if (mode === "auto") window.localStorage.removeItem(THEME_KEY);
        else window.localStorage.setItem(THEME_KEY, mode);
      } catch (err) {
        /* Storage may be unavailable; the choice then lasts for this page only. */
      }
      showTheme(mode);
    });
    showTheme(currentTheme());
    themeToggle.hidden = false;
  }

  // Sticky section bar: sit below the header and mark the section in view.
  var jump = document.querySelector(".page-jump");
  if (jump) {
    var siteHeader = document.querySelector(".site-header");
    var jumpLinks = Array.prototype.slice.call(jump.querySelectorAll("a[href^='#']"));
    var jumpTargets = jumpLinks.map(function (link) {
      return document.getElementById(link.getAttribute("href").slice(1));
    });
    var measureJump = function () {
      var headerHeight = siteHeader ? siteHeader.getBoundingClientRect().height : 0;
      document.documentElement.style.setProperty("--header-h", headerHeight + "px");
      document.documentElement.style.scrollPaddingTop = (headerHeight + jump.offsetHeight + 12) + "px";
      document.documentElement.classList.add("has-jump");
    };
    var markJump = function () {
      var line = jump.getBoundingClientRect().bottom + 24;
      var current = -1;
      jumpTargets.forEach(function (target, index) {
        if (target && target.getBoundingClientRect().top <= line) current = index;
      });
      // At the very bottom, a short last section can never reach the line.
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
        current = jumpLinks.length - 1;
      }
      jumpLinks.forEach(function (link, index) {
        if (index === current) {
          if (link.getAttribute("aria-current") !== "location") {
            link.setAttribute("aria-current", "location");
            var inner = link.parentElement;
            inner.scrollLeft = link.offsetLeft - (inner.clientWidth - link.offsetWidth) / 2;
          }
        } else {
          link.removeAttribute("aria-current");
        }
      });
    };
    var jumpQueued = false;
    window.addEventListener("scroll", function () {
      if (jumpQueued) return;
      jumpQueued = true;
      window.requestAnimationFrame(function () { jumpQueued = false; markJump(); });
    }, { passive: true });
    window.addEventListener("resize", function () { measureJump(); markJump(); });
    measureJump();
    markJump();
  }

  var STORAGE_KEY = "cs301-week1-lang";
  var DEFAULT_LANG = "java";

  function escapeHTML(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Lexical highlighting only: source is escaped before any markup is added.
  function highlight(text, lang) {
    var keywords = ("if else elif for while do break continue return class public private protected " +
      "static final const let var void int long double float char bool boolean string String " +
      "new null true false using namespace import from def pass None True False and or not " +
      "in is with as try catch except finally throw throws function module exports include " +
      "struct typedef unsigned signed sizeof auto switch case default this super extends " +
      "implements interface async await yield lambda nonlocal global assert to swap append " +
      "length floor both non empty end").split(/\s+/);
    var isShell = ["bash", "zsh", "powershell"].indexOf(lang) !== -1;
    var isHashComment = lang === "py" || lang === "pseudo" || isShell;
    var comments = isHashComment ? "#[^\\n]*" : "\\/\\*[\\s\\S]*?(?:\\*\\/|$)|\\/\\/[^\\n]*|#[ \\t]*(?:include|define|ifdef|ifndef|endif|else|pragma)";
    var strings = '\"\"\"[\\s\\S]*?(?:\"\"\"|$)|\'\'\'[\\s\\S]*?(?:\'\'\'|$)|"(?:\\\\.|[^"\\\\\\n])*"?|\'(?:\\\\.|[^\'\\\\\\n])*\'?|`(?:\\\\.|[^`\\\\])*`?';
    var pattern = new RegExp(comments + "|" + strings + "|\\b(?:0[xX][0-9a-fA-F]+|[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)[a-zA-Z]*\\b|[A-Za-z_$][\\w$]*", "g");
    var result = "";
    var last = 0;
    var match;
    while ((match = pattern.exec(text)) !== null) {
      result += escapeHTML(text.slice(last, match.index));
      var token = match[0];
      var type = "";
      if ((isHashComment && token[0] === "#") || token.slice(0, 2) === "//" || token.slice(0, 2) === "/*") {
        type = "comment";
      } else if (/^[\"'`]/.test(token)) {
        type = "string";
      } else if (/^[0-9]/.test(token)) {
        type = "number";
      } else if (isShell && ["uv", "mise", "curl", "sh", "powershell", "winget", "mkdir", "cd", "python", "java", "javac", "irm", "iex", "setopt"].indexOf(token) !== -1) {
        type = "function";
      } else if (keywords.indexOf(token) !== -1 || token[0] === "#") {
        type = "keyword";
      } else if (/^\s*\(/.test(text.slice(pattern.lastIndex))) {
        type = "function";
      }
      result += type ? '<span class="syntax-' + type + '">' + escapeHTML(token) + '</span>' : escapeHTML(token);
      last = pattern.lastIndex;
    }
    return result + escapeHTML(text.slice(last));
  }

  document.querySelectorAll("pre code").forEach(function (code) {
    var panel = code.closest(".tab-panel");
    var block = code.closest("[data-language]");
    code.innerHTML = highlight(code.textContent, panel ? panel.getAttribute("data-lang") : block ? block.getAttribute("data-language") : "pseudo");
  });

  document.querySelectorAll(".code-block[data-language] .copy-btn").forEach(function (button) {
    button.hidden = false;
  });

  document.addEventListener("click", function (event) {
    var button = event.target.closest(".copy-btn");
    if (!button) {
      return;
    }
    var group = button.closest(".tabs");
    var panel = group ? group.querySelector(".tab-panel:not([hidden])") : button.closest(".code-block[data-language]");
    if (!panel) {
      return;
    }
    var input = panel.querySelector("textarea");
    var code = panel.querySelector("pre code") || panel;
    var text = (input ? input.value : code.textContent).replace(/\s+$/, "");
    var original = button.dataset.tooltip;
    copyText(text)
      .then(function () {
        button.dataset.tooltip = "Copied!";
        button.setAttribute("aria-label", "Copied!");
        button.classList.add("copied");
      })
      .catch(function () {
        button.dataset.tooltip = "Press Ctrl+C";
        button.setAttribute("aria-label", "Press Ctrl+C");
      })
      .finally(function () {
        window.setTimeout(function () {
          button.dataset.tooltip = original;
          button.setAttribute("aria-label", original);
          button.classList.remove("copied");
        }, 1400);
      });
  });
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

  // Signature tables list every language without JavaScript; show only the chosen one.
  function showSignatures(lang) {
    document.querySelectorAll(".sig-table tr[data-sig-lang]").forEach(function (row) {
      row.hidden = row.getAttribute("data-sig-lang") !== lang;
    });
  }

  function selectLang(lang) {
    groups.forEach(function (group) {
      setGroupLang(group, lang);
    });
    showSignatures(lang);
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

  var editors = [];
  groups.filter(function (group) { return group.hasAttribute("data-editable"); }).forEach(function (group) {
    var reset = document.createElement("button");
    reset.type = "button";
    reset.className = "reset-btn icon-btn";
    reset.setAttribute("aria-label", "Reset code");
    reset.dataset.tooltip = "Reset code";
    var resetIcon = document.createElement("img");
    resetIcon.src = "assets/icons/reset-right-fill.svg";
    resetIcon.alt = "";
    reset.appendChild(resetIcon);
    group.querySelector(".code-actions").appendChild(reset);
    panelsOf(group).forEach(function (panel) {
      var original = panel.querySelector("pre");
      var initial = original.textContent;
      var lang = panel.getAttribute("data-lang");
      var editor = document.createElement("div");
      editor.className = "code-editor";
      var preview = document.createElement("pre");
      preview.className = "code-preview";
      preview.setAttribute("aria-hidden", "true");
      var code = document.createElement("code");
      preview.appendChild(code);
      var input = document.createElement("textarea");
      input.className = "code-input";
      input.value = initial;
      input.defaultValue = initial;
      input.spellcheck = false;
      input.wrap = "off";
      input.autocomplete = "off";
      input.setAttribute("autocapitalize", "off");
      input.setAttribute("autocorrect", "off");
      input.setAttribute("aria-label", panel.id.replace(/-/g, " ") + " temporary code editor");
      input.setAttribute("aria-describedby", "editor-help");
      function syncScroll() {
        preview.scrollTop = input.scrollTop;
        preview.scrollLeft = input.scrollLeft;
      }
      function render() {
        // One trailing space keeps the final empty line visible in the preview.
        code.innerHTML = highlight(input.value + " ", lang);
        syncScroll();
      }
      input.addEventListener("input", render);
      input.addEventListener("scroll", syncScroll);
      var releaseTab = false;
      input.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
          releaseTab = true;
          return;
        }
        if (event.key !== "Tab") {
          releaseTab = false;
          return;
        }
        if (releaseTab || event.ctrlKey || event.metaKey || event.altKey) {
          releaseTab = false;
          return;
        }
        event.preventDefault();
        var start = input.selectionStart;
        var end = input.selectionEnd;
        if (event.shiftKey) {
          var lineStart = input.value.lastIndexOf("\n", start - 1) + 1;
          var leading = input.value.slice(lineStart).match(/^(?: {1,4}|\t)/);
          if (leading) {
            input.setRangeText("", lineStart, lineStart + leading[0].length, "preserve");
          }
        } else {
          input.setRangeText("    ", start, end, "end");
        }
        render();
      });
      function restore() {
        input.value = initial;
        input.scrollTop = 0;
        input.scrollLeft = 0;
        render();
      }
      editors.push(restore);
      panel.restoreCode = restore;
      original.hidden = true;
      editor.style.height = Math.min(460, Math.max(220, (initial.split("\n").length + 1) * 22 + 30)) + "px";
      editor.appendChild(preview);
      editor.appendChild(input);
      panel.appendChild(editor);
      render();
    });
    reset.addEventListener("click", function () {
      var panel = group.querySelector(".tab-panel:not([hidden])");
      panel.restoreCode();
      panel.querySelector("textarea").focus();
    });
  });
  // Override browser form restoration as well as normal reload state.
  window.addEventListener("pageshow", function () {
    editors.forEach(function (restore) { restore(); });
  });

  var initialLang = storedLang();
  groups.forEach(function (group) {
    setGroupLang(group, initialLang);
  });
  showSignatures(initialLang);

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


})();

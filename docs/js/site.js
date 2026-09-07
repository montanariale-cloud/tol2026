// TALES OF LAMU — menu overlay + lightbox condivisi

// impedisce il trascinamento delle immagini sulla scrivania (CSS user-drag
// non e' supportato ovunque, quindi si blocca anche via JS, delegato cosi'
// da coprire pure le immagini create dopo, come quella della lightbox)
document.addEventListener("dragstart", (e) => {
  if (e.target.tagName === "IMG") e.preventDefault();
});
document.addEventListener("contextmenu", (e) => {
  if (e.target.tagName === "IMG") e.preventDefault();
});

// Gate — password d'ingresso. Cortesia, non protezione vera: la repo e'
// pubblica e le immagini restano raggiungibili per URL diretto (vedi BRIEF.md).
// La password non e' salvata in chiaro nel sorgente, solo il suo hash SHA-256.
const GATE_HASH = "e71d1dc9f6b1f8b88d7c81bd6ef4125536d3030c7c49b7fc6ad0ab30096dee27";

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

function initGate() {
  const gate = document.getElementById("gate");
  if (!gate) return;
  const form = document.getElementById("gate-form");
  const input = document.getElementById("gate-input");
  const error = document.getElementById("gate-error");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const hash = await sha256Hex(input.value.trim().toLowerCase());
    if (hash === GATE_HASH) {
      localStorage.setItem("tol_unlocked", "1");
      gate.classList.add("unlocked");
      error.classList.remove("show");
    } else {
      error.classList.add("show");
      input.value = "";
      input.focus();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initGate();
  const menuBtn = document.querySelector("[data-menu-open]");
  const menuClose = document.querySelector("[data-menu-close]");
  const overlay = document.querySelector(".nav-overlay");
  if (menuBtn && overlay) {
    menuBtn.addEventListener("click", () => overlay.classList.add("open"));
    menuClose.addEventListener("click", () => overlay.classList.remove("open"));
    overlay.addEventListener("click", (e) => { if (e.target === overlay) overlay.classList.remove("open"); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") overlay.classList.remove("open"); });
  }

  initLightbox();
  initToTop();
});

function initToTop() {
  const footer = document.querySelector(".site-footer");
  const btn = document.createElement("button");
  btn.className = "to-top";
  btn.setAttribute("aria-label", "Torna all'inizio");
  btn.innerHTML = "&#8593;";
  document.body.appendChild(btn);

  btn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  let ticking = false;
  window.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const pastThreshold = window.scrollY > window.innerHeight * 0.8;
      const footerVisible = footer && footer.getBoundingClientRect().top < window.innerHeight;
      btn.classList.toggle("show", pastThreshold && !footerVisible);
      ticking = false;
    });
  });
}

function initLightbox() {
  const figures = Array.from(document.querySelectorAll("figure[data-full]"));
  if (!figures.length) return;

  const noDownload = document.body.dataset.noDownload === "1";

  const lb = document.createElement("div");
  lb.className = "lightbox";
  lb.innerHTML = `
    <button class="lb-prev" aria-label="Precedente">&#8249;</button>
    <img alt="">
    <button class="lb-next" aria-label="Successiva">&#8250;</button>
    ${noDownload ? "" : '<a class="lb-dl" download><span>Scarica</span> &#8595;</a>'}
    <button class="lb-close" aria-label="Chiudi">&times;</button>
    <div class="lb-counter"></div>
  `;
  document.body.appendChild(lb);

  const img = lb.querySelector("img");
  const counter = lb.querySelector(".lb-counter");
  const dl = lb.querySelector(".lb-dl");
  let idx = 0;

  function show(i) {
    idx = (i + figures.length) % figures.length;
    const f = figures[idx];
    img.src = f.dataset.full;
    img.alt = f.dataset.alt || "";
    if (dl) {
      dl.href = f.dataset.full;
      dl.setAttribute("download", f.dataset.full.split("/").pop());
    }
    counter.textContent = `${idx + 1} / ${figures.length}`;
    // preload neighbours
    new Image().src = figures[(idx + 1) % figures.length].dataset.full;
    new Image().src = figures[(idx - 1 + figures.length) % figures.length].dataset.full;
  }

  function open(i) {
    show(i);
    lb.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function close() {
    lb.classList.remove("open");
    document.body.style.overflow = "";
  }

  figures.forEach((f, i) => f.addEventListener("click", () => open(i)));
  lb.querySelector(".lb-close").addEventListener("click", close);
  lb.querySelector(".lb-prev").addEventListener("click", () => show(idx - 1));
  lb.querySelector(".lb-next").addEventListener("click", () => show(idx + 1));
  lb.addEventListener("click", (e) => { if (e.target === lb) close(); });

  document.addEventListener("keydown", (e) => {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") show(idx + 1);
    if (e.key === "ArrowLeft") show(idx - 1);
  });

  // touch swipe
  let touchX = null;
  lb.addEventListener("touchstart", (e) => { touchX = e.touches[0].clientX; });
  lb.addEventListener("touchend", (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
    touchX = null;
  });
}

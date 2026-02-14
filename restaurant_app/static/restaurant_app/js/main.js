// =======================
// CSRF (Django)
// =======================
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

// =======================
// Toast (Savatchaga qo‘shildi)
// =======================
function showToast(title, text) {
  let wrap = document.querySelector(".mx-toast-wrap");
  if (!wrap) {
    wrap = document.createElement("div");
    wrap.className = "mx-toast-wrap";
    document.body.appendChild(wrap);
  }

  const t = document.createElement("div");
  t.className = "mx-toast";
  t.innerHTML = `
    <div class="mx-toast__icon">✓</div>
    <div class="mx-toast__body">
      <div class="mx-toast__title">${title}</div>
      <div class="mx-toast__text">${text}</div>
    </div>
    <button class="mx-toast__x" aria-label="Close">×</button>
  `;
  wrap.appendChild(t);

  const kill = () => {
    t.classList.add("out");
    setTimeout(() => t.remove(), 180);
  };
  t.querySelector(".mx-toast__x").addEventListener("click", kill);
  setTimeout(kill, 1800);
}

// =======================
// Floating cart badge update
// =======================
function updateFloatingCart(totalQty) {
  const badge = document.querySelector(".mx-floating-cart__count");
  const floating = document.querySelector(".mx-floating-cart");
  if (!badge) return;

  badge.textContent = totalQty;

  // xohlasangiz 0 bo'lsa yashirish:
  if (floating) {
    floating.style.display = totalQty > 0 ? "flex" : "none";
  }
}

// =======================
// POST qty helper (x-www-form-urlencoded)
// =======================
async function postQty(url, qty) {
  const body = new URLSearchParams();
  body.append("qty", String(qty));

  const res = await fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrftoken,
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    },
    body: body.toString()
  });

  const data = await res.json();
  if (!res.ok || !data.ok) throw new Error(data.message || "Server error");
  return data;
}

// =======================
// CLICK HANDLER (Add / Inc / Dec)
// =======================
document.addEventListener("click", async (e) => {
  const addBtn = e.target.closest(".mx-cartctl__add");
  const qtyBtn = e.target.closest(".mx-qty-btn");

  // 1) ADD
  if (addBtn) {
    const ctl = addBtn.closest(".mx-cartctl");
    const addUrl = ctl.dataset.addUrl;
    const name = ctl.dataset.name || "Mahsulot";

    addBtn.disabled = true;

    try {
      const res = await fetch(addUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken
        }
      });

      const data = await res.json();
      if (!res.ok || !data.ok) throw new Error(data.message || "Qo‘shib bo‘lmadi");

      // UI update
      ctl.classList.add("is-added");
      ctl.dataset.qty = String(data.qty || 1);
      ctl.querySelector(".mx-qty-num").textContent = String(data.qty || 1);

      updateFloatingCart(data.cart_total_qty || 0);
      showToast(name, "savatchaga qo‘shildi!");

    } catch (err) {
      showToast("Xatolik", err.message || "Muammo yuz berdi");
    } finally {
      addBtn.disabled = false;
    }
    return;
  }

  // 2) INC / DEC
  if (qtyBtn) {
    const ctl = qtyBtn.closest(".mx-cartctl");
    const setUrl = ctl.dataset.setUrl;
    const act = qtyBtn.dataset.act;

    let qty = parseInt(ctl.dataset.qty || "0", 10);
    if (Number.isNaN(qty)) qty = 0;

    qty = act === "inc" ? qty + 1 : qty - 1;
    if (qty < 0) qty = 0;

    qtyBtn.disabled = true;

    try {
      const data = await postQty(setUrl, qty);

      ctl.dataset.qty = String(data.qty || 0);

      if ((data.qty || 0) <= 0) {
        // back to add button
        ctl.classList.remove("is-added");
        ctl.querySelector(".mx-qty-num").textContent = "1";
      } else {
        ctl.classList.add("is-added");
        ctl.querySelector(".mx-qty-num").textContent = String(data.qty);
      }

      updateFloatingCart(data.cart_total_qty || 0);

    } catch (err) {
      showToast("Xatolik", err.message || "Muammo yuz berdi");
    } finally {
      qtyBtn.disabled = false;
    }
  }
});


// ===== INIT: page loadda default holat (qty=0 bo'lsa faqat "Savatga qo'shish") =====
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".mx-cartctl").forEach((ctl) => {
    let qty = parseInt(ctl.dataset.qty || "0", 10);
    if (Number.isNaN(qty)) qty = 0;

    if (qty > 0) {
      ctl.classList.add("is-added");
      const num = ctl.querySelector(".mx-qty-num");
      if (num) num.textContent = String(qty);
    } else {
      ctl.classList.remove("is-added");
      const num = ctl.querySelector(".mx-qty-num");
      if (num) num.textContent = "1"; // default ko'rsatish
    }
  });
});




// Smooth scroll for internal anchors (#blog, #about, #contact, #products)
document.addEventListener("click", (e) => {
  const a = e.target.closest('a[href*="#"]');
  if (!a) return;

  const href = a.getAttribute("href");
  if (!href) return;

  const hashIndex = href.indexOf("#");
  if (hashIndex === -1) return;

  const id = href.slice(hashIndex + 1);
  if (!id) return;

  const target = document.getElementById(id);
  if (!target) return;

  // faqat shu sahifadagi anchorlar uchun
  e.preventDefault();

  const header = document.querySelector(".mx-topbar");
  const offset = header ? header.offsetHeight + 14 : 90;

  const top = target.getBoundingClientRect().top + window.scrollY - offset;
  window.scrollTo({ top, behavior: "smooth" });
});



document.querySelector("#feedbackForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const form = e.target;
    const data = new FormData(form);

    const res = await fetch("/send-feedback/", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: data
    });

    const json = await res.json();

    if(json.ok){
        alert("Rahmat! Xabaringiz yuborildi 👍");
        form.reset();
    }
});






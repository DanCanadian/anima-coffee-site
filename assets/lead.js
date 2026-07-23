/* Anima Volitiva — lead capture.
 * Works today with zero backend: composes a pre-filled email to the sales inbox.
 * If a Formspree endpoint is set on the form (data-endpoint="https://formspree.io/f/XXXX"),
 * it POSTs the lead directly instead (hands-off CRM delivery). That endpoint id is the
 * single missing secret for automatic delivery — until set, the mailto path is used.
 */
(function () {
  var INBOX = "hello@animacoffee.com.ua";
  var uk = (document.documentElement.lang || "en").toLowerCase().indexOf("uk") === 0;
  var T = uk
    ? { opening: "Відкриваємо ваш поштовий застосунок…", sent: "Дякуємо! Ми звʼяжемося з вами протягом одного робочого дня.", err: "Не вдалося надіслати. Напишіть нам: " + INBOX, subject: "Запит на B2B-аудит кави" }
    : { opening: "Opening your email app…", sent: "Thank you. We'll reply within one business day.", err: "Could not send. Email us: " + INBOX, subject: "B2B coffee assessment request" };

  function setStatus(el, msg, cls) { el.textContent = msg; el.className = "lf-status" + (cls ? " " + cls : ""); }

  function handle(form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var status = form.querySelector(".lf-status");
      var data = {};
      Array.prototype.forEach.call(form.querySelectorAll("input,textarea"), function (f) {
        if (f.name) data[f.name] = (f.value || "").trim();
      });
      var endpoint = (form.getAttribute("data-endpoint") || "").trim();

      if (endpoint) {
        setStatus(status, T.opening, "");
        fetch(endpoint, {
          method: "POST",
          headers: { "Accept": "application/json", "Content-Type": "application/json" },
          body: JSON.stringify(data)
        }).then(function (r) {
          if (r.ok) { form.reset(); setStatus(status, T.sent, "ok"); }
          else { setStatus(status, T.err, "err"); }
        }).catch(function () { setStatus(status, T.err, "err"); });
        return;
      }

      // Zero-secret fallback: compose a qualified email via the user's mail client.
      var lines = [
        (uk ? "Імʼя: " : "Name: ") + (data.name || ""),
        (uk ? "Компанія: " : "Business: ") + (data.business || ""),
        (uk ? "Місто: " : "City: ") + (data.city || ""),
        (uk ? "Кількість машин: " : "Machines needed: ") + (data.machines || ""),
        (uk ? "Контакт: " : "Contact: ") + (data.contact || ""),
        "",
        (uk ? "Деталі: " : "Details: ") + (data.message || "")
      ];
      var href = "mailto:" + INBOX +
        "?subject=" + encodeURIComponent(T.subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      setStatus(status, T.opening, "ok");
      window.location.href = href;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll("form.lead-form"), handle);
  });
})();

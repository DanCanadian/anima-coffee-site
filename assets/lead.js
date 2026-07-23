/* Anima Volitiva — lead capture -> AmoCRM.
 * Works today with zero backend: composes a pre-filled email to the sales inbox.
 * If an incoming-webhook endpoint is set on the form
 *   (data-endpoint="https://<subdomain>.amocrm.ru/...")  <-- the ONE secret (AmoCRM incoming webhook URL)
 * it POSTs the lead as JSON {name,business,city,machines,contact,details,source_page}
 * directly to AmoCRM instead. Until data-endpoint is filled, the mailto path is used.
 * On a successful submit it fires the generate_lead conversion via window.animaTrackLead().
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
      var raw = {};
      Array.prototype.forEach.call(form.querySelectorAll("input,textarea"), function (f) {
        if (f.name) raw[f.name] = (f.value || "").trim();
      });
      // Canonical AmoCRM payload — stable schema regardless of the field named "message" or "details".
      var data = {
        name: raw.name || "",
        business: raw.business || "",
        city: raw.city || "",
        machines: raw.machines || "",
        contact: raw.contact || "",
        details: raw.details || raw.message || "",
        source_page: location.pathname
      };
      function fireLead() { try { if (window.animaTrackLead) window.animaTrackLead(data.source_page); } catch (e) {} }
      var endpoint = (form.getAttribute("data-endpoint") || "").trim();

      if (endpoint) {
        setStatus(status, T.opening, "");
        fetch(endpoint, {
          method: "POST",
          headers: { "Accept": "application/json", "Content-Type": "application/json" },
          body: JSON.stringify(data)
        }).then(function (r) {
          if (r.ok) { fireLead(); form.reset(); setStatus(status, T.sent, "ok"); }
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
        (uk ? "Сторінка: " : "Source page: ") + (data.source_page || ""),
        "",
        (uk ? "Деталі: " : "Details: ") + (data.details || "")
      ];
      var href = "mailto:" + INBOX +
        "?subject=" + encodeURIComponent(T.subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      fireLead();
      setStatus(status, T.opening, "ok");
      window.location.href = href;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll("form.lead-form"), handle);
  });
})();

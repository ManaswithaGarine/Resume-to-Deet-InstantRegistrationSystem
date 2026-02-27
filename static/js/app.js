/* ══════════════════════════════════════════════════════
   DEET Registration — Client-side logic
   Handles: upload, preview editing, dashboard updates
══════════════════════════════════════════════════════ */

// ── Upload Page ──────────────────────────────────────────────────────────────
(function initUpload() {
  const dropZone = document.getElementById("dropZone");
  const fInput   = document.getElementById("fInput");
  const chipArea = document.getElementById("chipArea");
  const msgArea  = document.getElementById("msgArea");
  const spinner  = document.getElementById("spinner");
  const procMsg  = document.getElementById("processingMsg");
  if (!dropZone) return;   // not on upload page

  dropZone.addEventListener("click", () => fInput.click());
  fInput.addEventListener("change", () => {
    if (fInput.files[0]) handleUpload(fInput.files[0]);
  });
  dropZone.addEventListener("dragover", e => {
    e.preventDefault(); dropZone.classList.add("drag-over");
  });
  dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
  dropZone.addEventListener("drop", e => {
    e.preventDefault(); dropZone.classList.remove("drag-over");
    if (e.dataTransfer.files[0]) handleUpload(e.dataTransfer.files[0]);
  });

  function handleUpload(file) {
    chipArea.innerHTML = ""; msgArea.innerHTML = "";

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      showMsg("err", "Only PDF files are supported."); return;
    }
    if (file.size > 10 * 1024 * 1024) {
      showMsg("err", "File exceeds the 10 MB limit."); return;
    }

    // Show chip
    chipArea.innerHTML = `
      <div class="file-chip">
        <div class="chip-ico">📎</div>
        <div>
          <div class="chip-name">${esc(file.name)}</div>
          <div class="chip-size">${fmtSize(file.size)}</div>
        </div>
        <span class="chip-rm" id="chipRm" title="Remove">✕</span>
      </div>`;
    document.getElementById("chipRm").addEventListener("click", () => {
      chipArea.innerHTML = ""; msgArea.innerHTML = ""; fInput.value = "";
      if (spinner) spinner.style.display = "none";
      if (procMsg) procMsg.style.display = "none";
    });

    showMsg("ok", "Uploading and extracting details…");
    if (spinner) spinner.style.display = "block";
    if (procMsg) procMsg.style.display = "block";

    // POST to Flask API
    const fd = new FormData();
    fd.append("resume", file);

    fetch("/api/upload", { method: "POST", body: fd })
      .then(r => r.json())
      .then(data => {
        if (data.error) {
          showMsg("err", data.error);
          if (spinner) spinner.style.display = "none";
          if (procMsg) procMsg.style.display = "none";
        } else {
          showMsg("ok", "✓ Extraction complete — loading preview…");
          setTimeout(() => { window.location.href = "/preview"; }, 800);
        }
      })
      .catch(() => {
        showMsg("err", "Upload failed. Please try again.");
        if (spinner) spinner.style.display = "none";
        if (procMsg) procMsg.style.display = "none";
      });
  }

  function showMsg(type, text) {
    msgArea.innerHTML = `<div class="msg ${type}"><span class="msg-dot"></span>${esc(text)}</div>`;
  }
})();


// ── Preview Page ─────────────────────────────────────────────────────────────
(function initPreview() {
  if (!document.getElementById("previewForm")) return;

  // Skill tag management
  window.removeSkill = function(btn) {
    btn.closest(".stag").remove(); recalc();
  };
  window.addSkill = function() {
    const inp = document.getElementById("skillInput");
    const val = inp.value.trim();
    if (!val) return;
    const wrap = document.getElementById("skillsWrap");
    const tag  = document.createElement("span");
    tag.className = "stag";
    tag.innerHTML = `${esc(val)} <span class="stag-rm" onclick="removeSkill(this)">✕</span>`;
    wrap.appendChild(tag);
    inp.value = "";
    recalc();
  };
  document.getElementById("skillInput")
    ?.addEventListener("keydown", e => { if (e.key === "Enter") { e.preventDefault(); addSkill(); } });

  // Entry row management
  window.delRow = function(btn) { btn.closest(".erow").remove(); recalc(); };
  window.addEdu = function() {
    const row = document.createElement("div"); row.className = "erow";
    row.innerHTML = `<input type="text" placeholder="Degree / Title"><input type="text" placeholder="Institution"><span class="erow-rm" onclick="delRow(this)">✕</span>`;
    document.getElementById("eduList").appendChild(row);
  };
  window.addExp = function() {
    const row = document.createElement("div"); row.className = "erow";
    row.innerHTML = `<input type="text" placeholder="Role"><input type="text" placeholder="Company / Event"><input type="text" placeholder="Year"><span class="erow-rm" onclick="delRow(this)">✕</span>`;
    document.getElementById("expList").appendChild(row);
  };

  // Live completeness
  function recalc() {
    const name  = document.getElementById("fName")?.value.trim() || "";
    const email = document.getElementById("fEmail")?.value.trim() || "";
    const phone = document.getElementById("fPhone")?.value.trim() || "";
    const edu   = document.getElementById("eduList")?.children.length || 0;
    const exp   = document.getElementById("expList")?.children.length || 0;
    const skCount = document.getElementById("skillsWrap")?.children.length || 0;
    let s = 0;
    if (name)   s += 22; if (email)  s += 20; if (phone)  s += 15;
    if (edu>0)  s += 20; if (exp>0)  s += 10; if (skCount>0) s += 13;
    s = Math.min(s, 100);
    const fill = document.getElementById("bFill");
    const lbl  = document.getElementById("pctLbl");
    if (fill) fill.style.width = s + "%";
    if (lbl)  lbl.textContent  = s + "%";
    // update overview banner
    if (document.getElementById("ob-name"))  document.getElementById("ob-name").textContent  = name  || "—";
    if (document.getElementById("ob-email")) document.getElementById("ob-email").textContent = email || "—";
    if (document.getElementById("ob-skills"))document.getElementById("ob-skills").textContent = skCount;
    if (document.getElementById("ob-edu"))   document.getElementById("ob-edu").textContent   = edu;
    if (document.getElementById("ob-exp"))   document.getElementById("ob-exp").textContent   = exp;
  }
  window.recalc = recalc;

  // Expose for inline oninput
  document.querySelectorAll("#previewForm input, #previewForm textarea")
    .forEach(el => el.addEventListener("input", recalc));

  // Submit
  document.getElementById("btnSubmit")?.addEventListener("click", submitProfile);
  function submitProfile() {
    const skills = [...document.querySelectorAll("#skillsWrap .stag")]
      .map(t => t.childNodes[0].textContent.trim());

    const education = [...document.querySelectorAll("#eduList .erow")].map(r => {
      const inputs = r.querySelectorAll("input");
      return { title: inputs[0]?.value || "", institution: inputs[1]?.value || "" };
    });
    const experience = [...document.querySelectorAll("#expList .erow")].map(r => {
      const inputs = r.querySelectorAll("input");
      return { role: inputs[0]?.value || "", company: inputs[1]?.value || "", year: inputs[2]?.value || "" };
    });

    const payload = {
      name:       document.getElementById("fName")?.value.trim()  || "",
      email:      document.getElementById("fEmail")?.value.trim() || "",
      phone:      document.getElementById("fPhone")?.value.trim() || "",
      skills, education, experience,
    };

    fetch("/api/submit-profile", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) window.location.href = "/dashboard";
      else alert("Submission error: " + JSON.stringify(data.error));
    })
    .catch(() => alert("Network error. Please try again."));
  }

  recalc();
})();


// ── Dashboard Page ───────────────────────────────────────────────────────────
(function initDashboard() {
  const roleSelect = document.getElementById("roleSelect");
  if (!roleSelect) return;

  // Animate gauge on load
  const gArc = document.getElementById("gArc");
  if (gArc) {
    const pct = parseInt(document.getElementById("gVal")?.textContent) || 0;
    setTimeout(() => {
      gArc.style.strokeDashoffset = 173 - (pct / 100) * 173;
    }, 300);
  }

  roleSelect.addEventListener("change", updateRoleAnalysis);

  function updateRoleAnalysis() {
    const role = roleSelect.value;
    const skills = [...document.querySelectorAll(".hpill")]
      .map(p => p.textContent.replace("✓","").trim());

    fetch("/api/role-analysis", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ role, skills }),
    })
    .then(r => r.json())
    .then(data => renderRoleData(role, data))
    .catch(err => console.error("Role analysis error:", err));
  }

  function renderRoleData(role, data) {
    const gap = data.gap || {};

    // Gap pills
    const gapPills = document.getElementById("gapPills");
    if (gapPills) {
      gapPills.innerHTML = (gap.missing || [])
        .map(s => `<span class="gpill">${esc(s)}</span>`).join("");
    }
    document.getElementById("gapRole") && (document.getElementById("gapRole").textContent = role);
    document.getElementById("courseBadge") && (document.getElementById("courseBadge").textContent = "For " + role);

    // Severity
    const sev = gap.severity || "moderate";
    const sevLbl = sev === "high" ? "High" : sev === "low" ? "Low" : "Moderate";
    const sevCls = sev === "high" ? "h" : sev === "low" ? "l" : "m";
    const badgeCls = sev === "high" ? "r" : sev === "low" ? "g" : "y";
    const sevDot = document.getElementById("sevDot");
    if (sevDot) sevDot.className = "sev-dot " + sevCls;
    const sevText = document.getElementById("sevText");
    if (sevText) sevText.textContent = sevLbl;
    const sevBadge = document.getElementById("sevBadge");
    if (sevBadge) { sevBadge.textContent = sevLbl; sevBadge.className = "badge " + badgeCls; }

    // Match bars
    const barsWrap = document.getElementById("matchBars");
    if (barsWrap) {
      barsWrap.innerHTML = (data.breakdown || []).map(b => {
        const col = b.pct >= 70 ? "#1a9e8f" : b.pct >= 40 ? "#f59e0b" : "#ef4444";
        return `<div class="mrow">
          <span class="nm">${esc(b.name)}</span>
          <div class="mtrack"><div class="mfill" style="width:${b.pct}%;background:${col}"></div></div>
          <span class="pc">${b.pct}%</span>
        </div>`;
      }).join("");
    }

    // Courses
    const courseList = document.getElementById("courseList");
    if (courseList) {
      courseList.innerHTML = (gap.courses || []).map(c => `
        <div class="citem">
          <div class="citem-ico">${c.icon}</div>
          <div>
            <div class="citem-name">${esc(c.name)}</div>
            <div class="citem-tag">${esc(c.provider)} · ${esc(c.duration)}</div>
          </div>
        </div>`).join("");
    }
  }
})();


// ── Utilities ────────────────────────────────────────────────────────────────
function fmtSize(b) {
  return b < 1048576 ? (b / 1024).toFixed(1) + " KB" : (b / 1048576).toFixed(1) + " MB";
}
function esc(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

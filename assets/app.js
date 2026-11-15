/* Test EMR (training site). FICTIONAL PATIENTS ONLY.
   This is a static practice site for testing software (e.g. a bot that reads prior-authorization decisions and
   adds comments). The sign-in is a practice step, not security: anyone can read this page's source.
   Comments are kept only in this browser (localStorage). */
const TEST_USER = "authorization";
const TEST_PASSWORD = "hello";
const SESSION_KEY = "testemr_user";

function signedIn() {
  try { return sessionStorage.getItem(SESSION_KEY); } catch (e) { return null; }
}

function requireSignIn() {
  if (!signedIn()) {
    const next = encodeURIComponent(location.pathname.split("/").pop() + location.search);
    location.replace("index.html?next=" + next);
    return false;
  }
  return true;
}

function signOut() {
  try { sessionStorage.removeItem(SESSION_KEY); } catch (e) {}
  location.href = "index.html";
}

function topbar(active) {
  const user = signedIn();
  return `<div class="topbar"><span class="brand">Test EMR</span><span class="ribbon">TRAINING SITE · FAKE PATIENTS</span>
    <span class="sp"></span>${user ? `<span>Signed in as <b>${esc(user)}</b></span>
    <a href="patients.html" id="nav-patients"${active === "patients" ? ' aria-current="page"' : ""}>Patient list</a>
    <button class="link" id="signout" onclick="signOut()">Sign out</button>` : ""}</div>
    <div class="fakebar"><b>Not a real medical record system.</b> Every patient, date and number on this site is fictional,
    made up for software testing.</div>`;
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
}

async function loadPatients() {
  const r = await fetch("data/patients.json", {cache: "no-store"});
  return (await r.json()).patients;
}

/* ---------- comments (this browser only) ---------- */
function commentKey(mrn) { return "testemr_comments_" + mrn; }
function getComments(mrn) {
  try { return JSON.parse(localStorage.getItem(commentKey(mrn)) || "[]"); } catch (e) { return []; }
}
function saveComments(mrn, list) {
  try { localStorage.setItem(commentKey(mrn), JSON.stringify(list)); return true; } catch (e) { return false; }
}
function nowStamp() {
  const d = new Date(), p = n => String(n).padStart(2, "0");
  return `${p(d.getMonth() + 1)}/${p(d.getDate())}/${d.getFullYear()} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

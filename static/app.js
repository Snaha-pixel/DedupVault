const state = {
  files: [],
  activity: [],
  filter: "all",
};

const elements = {
  activityCount: document.querySelector("#all-count"),
  connection: document.querySelector("#connection-label"),
  dropZone: document.querySelector("#drop-zone"),
  duplicatesCount: document.querySelector("#duplicates-count"),
  error: document.querySelector("#error-banner"),
  fileInput: document.querySelector("#file-input"),
  fileList: document.querySelector("#file-list"),
  inventoryTitle: document.querySelector("#inventory-title"),
  progress: document.querySelector("#upload-progress"),
  progressLabel: document.querySelector("#upload-status"),
  results: document.querySelector("#results-label"),
  search: document.querySelector("#search-input"),
  tableHead: document.querySelector("#table-head"),
  toastRegion: document.querySelector("#toast-region"),
};

const formatBytes = (bytes) => {
  if (!bytes) return "0 B";
  const units = ["B", "KB", "MB", "GB", "TB"];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const value = bytes / 1024 ** index;
  return `${value.toFixed(index === 0 || value >= 10 ? 0 : 1)} ${units[index]}`;
};

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric" }).format(date);
}

function showError(message) {
  elements.error.textContent = message;
  elements.error.hidden = false;
}

function hideError() {
  elements.error.hidden = true;
  elements.error.textContent = "";
}

function showToast(title, message, kind) {
  const toast = document.createElement("div");
  toast.className = `toast ${kind}`;
  const heading = document.createElement("strong");
  const detail = document.createElement("span");
  heading.textContent = title;
  detail.textContent = message;
  toast.append(heading, detail);
  elements.toastRegion.append(toast);
  window.setTimeout(() => toast.remove(), 4800);
}

function setStat(id, value) {
  document.querySelector(`#${id}`).textContent = value;
}

async function loadDashboard() {
  try {
    const response = await fetch("/api/dashboard");
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not load the dashboard.");
    hideError();
    state.files = data.files;
    state.activity = data.activity;
    setStat("stat-files", Number(data.stats.unique_files).toLocaleString());
    setStat("stat-storage", formatBytes(data.stats.stored_bytes));
    setStat("stat-duplicates", Number(data.stats.duplicate_uploads).toLocaleString());
    setStat("stat-prevented", formatBytes(data.stats.bytes_prevented));
    elements.activityCount.textContent = Number(data.stats.unique_files).toLocaleString();
    elements.duplicatesCount.textContent = Number(data.stats.duplicate_uploads).toLocaleString();
    elements.connection.textContent = "Vault connected";
    elements.connection.parentElement.dataset.connection = "connected";
    renderFiles();
  } catch (error) {
    elements.connection.textContent = "Vault connection issue";
    elements.connection.parentElement.dataset.connection = "error";
    showError(error.message);
    elements.fileList.innerHTML = '<tr><td colspan="4" class="empty-state">Connect to the configured MySQL database to view your vault.</td></tr>';
    elements.results.textContent = "Unavailable";
  }
}

function makeFileIcon() {
  const wrapper = document.createElement("span");
  wrapper.className = "file-type-icon";
  wrapper.innerHTML = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M7 3.8h7l4 4V20H7a2 2 0 0 1-2-2V5.8a2 2 0 0 1 2-2Z" stroke="currentColor" stroke-width="1.6"/><path d="M14 4v4h4M8 13h8m-8 3h6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>';
  return wrapper;
}

function makeCell(className, text) {
  const cell = document.createElement("td");
  if (className) cell.className = className;
  cell.textContent = text;
  return cell;
}

function renderFiles() {
  const search = elements.search.value.trim().toLocaleLowerCase();
  const isActivity = state.filter === "recent";
  let rows = isActivity ? state.activity : state.files;
  if (state.filter === "duplicates") {
    rows = state.files.filter((file) => Number(file.upload_count) > 1);
  }
  rows = rows.filter((item) => {
    const name = isActivity ? item.uploaded_name : item.original_name;
    return name.toLocaleLowerCase().includes(search) || item.file_hash.toLocaleLowerCase().includes(search);
  });

  elements.inventoryTitle.textContent = isActivity
    ? "Recent uploads"
    : state.filter === "duplicates" ? "Files with duplicate uploads" : "Stored files";
  elements.tableHead.innerHTML = isActivity
    ? "<th scope=\"col\">FILE</th><th scope=\"col\">SIZE</th><th scope=\"col\">RESULT</th><th scope=\"col\">RECORD</th>"
    : "<th scope=\"col\">FILE</th><th scope=\"col\">SIZE</th><th scope=\"col\">UPLOADS</th><th scope=\"col\">ADDED</th>";
  elements.fileList.replaceChildren();

  if (!rows.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 4;
    cell.className = "empty-state";
    const heading = document.createElement("strong");
    heading.textContent = search ? "No matching files" : state.filter === "duplicates" ? "No duplicate uploads yet" : "Your vault is ready";
    const detail = document.createElement("span");
    detail.textContent = search ? "Try a different file name or SHA-256 hash." : "Upload a file to start building your library.";
    cell.append(heading, detail);
    row.append(cell);
    elements.fileList.append(row);
  } else {
    for (const item of rows) {
      const row = document.createElement("tr");
      const name = isActivity ? item.uploaded_name : item.original_name;
      const fileCell = document.createElement("td");
      const fileWrap = document.createElement("div");
      fileWrap.className = "file-cell";
      const details = document.createElement("div");
      details.style.minWidth = "0";
      const fileName = document.createElement("div");
      fileName.className = "file-name";
      fileName.title = name;
      fileName.textContent = name;
      if (!isActivity && Number(item.upload_count) > 1) {
        const badge = document.createElement("span");
        badge.className = "copy-badge";
        badge.textContent = `${Number(item.upload_count) - 1} duplicate${Number(item.upload_count) === 2 ? "" : "s"} caught`;
        fileName.append(badge);
      }
      const hash = document.createElement("div");
      hash.className = "file-hash";
      hash.textContent = item.file_hash;
      details.append(fileName, hash);
      fileWrap.append(makeFileIcon(), details);
      fileCell.append(fileWrap);
      row.append(fileCell, makeCell("size-cell", formatBytes(item.file_size)));

      if (isActivity) {
        const result = document.createElement("td");
        const badge = document.createElement("span");
        badge.className = Number(item.duplicate) ? "upload-count duplicate" : "upload-count";
        const dot = document.createElement("span");
        dot.className = "count-dot";
        badge.append(dot, document.createTextNode(Number(item.duplicate) ? "Duplicate caught" : "New file"));
        result.append(badge);
        row.append(result, makeCell("date-cell", `#${item.record_id}`));
      } else {
        const count = document.createElement("td");
        const countBadge = document.createElement("span");
        countBadge.className = Number(item.upload_count) > 1 ? "upload-count duplicate" : "upload-count";
        const dot = document.createElement("span");
        dot.className = "count-dot";
        countBadge.append(dot, document.createTextNode(`${Number(item.upload_count)} upload${Number(item.upload_count) === 1 ? "" : "s"}`));
        count.append(countBadge);
        row.append(count, makeCell("date-cell", formatDate(item.created_at)));
      }
      elements.fileList.append(row);
    }
  }
  elements.results.textContent = `${rows.length} ${rows.length === 1 ? "result" : "results"}`;
}

async function uploadFiles(fileList) {
  const files = Array.from(fileList);
  if (!files.length) return;
  hideError();
  elements.progress.hidden = false;
  document.querySelector("#browse-trigger").disabled = true;
  document.querySelector("#upload-trigger").disabled = true;
  let succeeded = 0;

  for (let index = 0; index < files.length; index += 1) {
    const file = files[index];
    elements.progressLabel.textContent = `Checking ${index + 1} of ${files.length}: ${file.name}`;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await fetch("/api/upload", { method: "POST", body: formData });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || `Could not upload ${file.name}.`);
      succeeded += 1;
      if (result.duplicate) {
        showToast("Duplicate upload caught", `${result.filename} matches ${result.original_name}. The file wasn't stored again.`, "duplicate");
      } else {
        showToast("File added to your vault", `${result.filename} · ${formatBytes(result.file_size)}`, "success");
      }
    } catch (error) {
      showToast("Upload failed", error.message, "error");
    }
  }

  elements.progress.hidden = true;
  document.querySelector("#browse-trigger").disabled = false;
  document.querySelector("#upload-trigger").disabled = false;
  elements.fileInput.value = "";
  if (succeeded) await loadDashboard();
}

document.querySelector("#upload-trigger").addEventListener("click", () => elements.fileInput.click());
document.querySelector("#browse-trigger").addEventListener("click", () => elements.fileInput.click());
elements.fileInput.addEventListener("change", (event) => uploadFiles(event.target.files));
elements.search.addEventListener("input", renderFiles);

document.querySelectorAll(".filter-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    state.filter = tab.dataset.filter;
    document.querySelectorAll(".filter-tab").forEach((item) => {
      const selected = item === tab;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-selected", String(selected));
    });
    document.querySelectorAll(".nav-item").forEach((item) => {
      item.classList.toggle("active", item.dataset.view === state.filter);
    });
    renderFiles();
  });
});

document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", () => {
    state.filter = item.dataset.view;
    document.querySelectorAll(".nav-item").forEach((link) => link.classList.toggle("active", link === item));
    document.querySelectorAll(".filter-tab").forEach((tab) => {
      const selected = tab.dataset.filter === state.filter;
      tab.classList.toggle("active", selected);
      tab.setAttribute("aria-selected", String(selected));
    });
    renderFiles();
  });
});

for (const eventName of ["dragenter", "dragover"]) {
  elements.dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropZone.classList.add("drag-active");
  });
}
for (const eventName of ["dragleave", "drop"]) {
  elements.dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropZone.classList.remove("drag-active");
  });
}
elements.dropZone.addEventListener("drop", (event) => uploadFiles(event.dataTransfer.files));

loadDashboard();

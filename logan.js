const fileInput = document.getElementById("fileInput");
const searchBox = document.getElementById("searchBox");

const logsDiv = document.getElementById("logs");

const totalLogs = document.getElementById("totalLogs");
const infoCount = document.getElementById("infoCount");
const warningCount = document.getElementById("warningCount");
const errorCount = document.getElementById("errorCount");

const showAll = document.getElementById("showAll");
const showInfo = document.getElementById("showInfo");
const showWarnings = document.getElementById("showWarnings");
const showErrors = document.getElementById("showErrors");

let allLogs = [];
let currentFilter = "ALL";

function getLogType(line) {
    const upper = line.toUpperCase();

    if (upper.includes("ERROR")) return "ERROR";
    if (upper.includes("WARNING")) return "WARNING";
    if (upper.includes("INFO")) return "INFO";

    return "OTHER";
}

function displayLogs(lines) {
    logsDiv.innerHTML = "";

    if (!lines.length) {
        logsDiv.innerHTML = `
            <div class="empty-state">
                No matching log entries found.
            </div>
        `;
        return;
    }

    lines.forEach((line, index) => {
        const div = document.createElement("div");

        div.classList.add("log-entry");

        const type = getLogType(line);

        if (type === "ERROR") div.classList.add("error");
        if (type === "WARNING") div.classList.add("warning");
        if (type === "INFO") div.classList.add("info");

        div.innerHTML = `
            <span class="line-number">#${index + 1}</span>
            <span class="log-text">${escapeHtml(line)}</span>
        `;

        div.title = "Click to copy";

        div.addEventListener("click", () => {
            navigator.clipboard.writeText(line);

            div.classList.add("copied");

            setTimeout(() => {
                div.classList.remove("copied");
            }, 500);
        });

        logsDiv.appendChild(div);
    });
}

function updateStats(lines) {
    let info = 0;
    let warning = 0;
    let error = 0;

    const duplicates = new Set();
    const seen = new Set();

    lines.forEach(line => {
        const type = getLogType(line);

        if (type === "INFO") info++;
        if (type === "WARNING") warning++;
        if (type === "ERROR") error++;

        if (seen.has(line)) {
            duplicates.add(line);
        }

        seen.add(line);
    });

    totalLogs.textContent = lines.length;
    infoCount.textContent = info;
    warningCount.textContent = warning;
    errorCount.textContent = error;

    const duplicateCounter = document.getElementById("duplicateCount");

    if (duplicateCounter) {
        duplicateCounter.textContent = duplicates.size;
    }
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function applyFilters() {
    const search = searchBox.value.toLowerCase();

    let filtered = [...allLogs];

    if (currentFilter !== "ALL") {
        filtered = filtered.filter(line =>
            getLogType(line) === currentFilter
        );
    }

    if (search) {
        filtered = filtered.filter(line =>
            line.toLowerCase().includes(search)
        );
    }

    displayLogs(filtered);
    updateStats(filtered);
}

fileInput.addEventListener("change", function () {
    const file = this.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = e => {
        allLogs = e.target.result
            .split(/\r?\n/)
            .filter(line => line.trim());

        applyFilters();
    };

    reader.readAsText(file);
});

searchBox.addEventListener("input", applyFilters);

showAll.addEventListener("click", () => {
    currentFilter = "ALL";
    applyFilters();
});

showInfo.addEventListener("click", () => {
    currentFilter = "INFO";
    applyFilters();
});

showWarnings.addEventListener("click", () => {
    currentFilter = "WARNING";
    applyFilters();
});

showErrors.addEventListener("click", () => {
    currentFilter = "ERROR";
    applyFilters();
});

document.getElementById("exportLogs")?.addEventListener("click", () => {
    const text = Array.from(
        document.querySelectorAll(".log-text")
    )
        .map(el => el.textContent)
        .join("\n");

    const blob = new Blob([text], { type: "text/plain" });

    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "filtered_logs.txt";
    a.click();
});
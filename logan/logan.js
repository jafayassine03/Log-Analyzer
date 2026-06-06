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

function displayLogs(lines) {
    logsDiv.innerHTML = "";

    if (lines.length === 0) {
        logsDiv.textContent = "No matching log entries found.";
        return;
    }

    lines.forEach(line => {
        const div = document.createElement("div");

        div.textContent = line;

        const upper = line.toUpperCase();

        if (upper.includes("ERROR")) {
            div.classList.add("error");
        } else if (upper.includes("WARNING")) {
            div.classList.add("warning");
        } else if (upper.includes("INFO")) {
            div.classList.add("info");
        }

        logsDiv.appendChild(div);
    });
}

function updateStats(lines) {
    let info = 0;
    let warning = 0;
    let error = 0;

    lines.forEach(line => {
        const upper = line.toUpperCase();

        if (upper.includes("ERROR")) {
            error++;
        } else if (upper.includes("WARNING")) {
            warning++;
        } else if (upper.includes("INFO")) {
            info++;
        }
    });

    totalLogs.textContent = lines.length;
    infoCount.textContent = info;
    warningCount.textContent = warning;
    errorCount.textContent = error;
}

fileInput.addEventListener("change", function () {
    const file = this.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (e) {
        const content = e.target.result;

        allLogs = content
            .split("\n")
            .filter(line => line.trim() !== "");

        updateStats(allLogs);
        displayLogs(allLogs);
    };

    reader.readAsText(file);
});

searchBox.addEventListener("input", () => {
    const term = searchBox.value.toLowerCase();

    const filtered = allLogs.filter(line =>
        line.toLowerCase().includes(term)
    );

    displayLogs(filtered);
});

showAll.addEventListener("click", () => {
    displayLogs(allLogs);
});

showInfo.addEventListener("click", () => {
    const filtered = allLogs.filter(line =>
        line.toUpperCase().includes("INFO")
    );

    displayLogs(filtered);
});

showWarnings.addEventListener("click", () => {
    const filtered = allLogs.filter(line =>
        line.toUpperCase().includes("WARNING")
    );

    displayLogs(filtered);
});

showErrors.addEventListener("click", () => {
    const filtered = allLogs.filter(line =>
        line.toUpperCase().includes("ERROR")
    );

    displayLogs(filtered);
});
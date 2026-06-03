# Log Analyzer

A simple web-based Log Analyzer built with HTML, CSS, and JavaScript.

This application allows users to upload log files, analyze log entries, and view statistics such as the number of INFO, WARNING, and ERROR messages. The tool provides a clean interface with color-coded log entries for easier troubleshooting and monitoring.

---

## Features

* Upload and analyze `.log` and `.txt` files
* Count total log entries
* Detect and count INFO messages
* Detect and count WARNING messages
* Detect and count ERROR messages
* Color-coded log display
* Scrollable log viewer
* Fast client-side processing
* No external libraries required
* Responsive design

---

## Technologies Used

* HTML5
* CSS3
* JavaScript (Vanilla JS)

---

## Installation

### Option 1: Download

Download the project files and place them in a folder:

```text
log-analyzer/
│
├── index.html
└── README.md
```

Open `index.html` in your web browser.

---

### Option 2: Local Web Server

Navigate to the project folder:

```bash
cd log-analyzer
```

Start a local server using Python:

```bash
python -m http.server 8000
```

Open:

```text
http://localhost:8000
```

in your browser.

---

## Usage

1. Launch the application.
2. Click the file upload button.
3. Select a `.log` or `.txt` file.
4. The analyzer will automatically:

   * Read the file
   * Count log entries
   * Detect INFO messages
   * Detect WARNING messages
   * Detect ERROR messages
   * Display the results

---

## Example Log File

```text
INFO Application started
INFO Database connected
WARNING Disk usage is high
ERROR Failed to connect to API
INFO User logged in
ERROR Authentication failed
```

Example output:

```text
Total Lines: 6
INFO: 3
WARNING: 1
ERROR: 2
```

---

## Project Structure

```text
log-analyzer/
│
├── index.html
└── README.md
```

---

## Future Improvements

* Search and filter logs
* Export analysis reports
* Support for JSON logs
* Log severity charts
* Timestamp analysis
* Dark and light themes
* Real-time log monitoring
* Drag-and-drop file upload
* Downloadable reports
* Multiple file analysis

---

## Browser Support

* Google Chrome
* Microsoft Edge
* Mozilla Firefox
* Safari
* Opera

---

## License

This project is open source and free to use for educational, personal, and commercial purposes.

---

## Author

Created as a beginner-friendly web project for learning file handling, DOM manipulation, and JavaScript-based data analysis.

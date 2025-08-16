document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("gradeForm");
    const resultsTableBody = document.querySelector("#resultsTable tbody");
    const downloadBtn = document.getElementById("downloadReport");
    let lastResults = [];

    // Change this when switching local ↔ deployed
    const API_BASE_URL = "http://127.0.0.1:5000";
    // const API_BASE_URL = "https://checkwise-backend.onrender.com";

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        resultsTableBody.innerHTML = "";
        downloadBtn.style.display = "none";
        lastResults = [];

        const questionText = document.getElementById("questionText").value.trim();
        const zipFile = document.getElementById("answersZip").files[0];

        if (!questionText) return alert("Please enter a question.");
        if (!zipFile) return alert("Please upload a zip file.");

        const formData = new FormData();
        formData.append("question", questionText);
        formData.append("zipfile", zipFile);  // ✅ consistent

        const loadingRow = document.createElement("tr");
        loadingRow.innerHTML = `<td colspan="3">Grading answers... Please wait.</td>`;
        resultsTableBody.appendChild(loadingRow);

        try {
            const response = await fetch(`${API_BASE_URL}/grade_ai`, {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error(`Server error: ${response.status}`);
            const data = await response.json();
            resultsTableBody.innerHTML = "";

            if (data.error) {
                resultsTableBody.innerHTML = `<tr><td colspan="3">Error: ${data.error}</td></tr>`;
                return;
            }

            lastResults = data;
            if (data.length > 0) {
                downloadBtn.style.display = "inline-block";
            }

            data.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `<td>${row.answer_file}</td><td>${row.marks}</td><td>${row.suggestions}</td>`;
                resultsTableBody.appendChild(tr);
            });

        } catch (err) {
            resultsTableBody.innerHTML = `<tr><td colspan="3">Error: ${err.message}</td></tr>`;
        }
    });

    downloadBtn.addEventListener("click", () => {
        if (!lastResults.length) return;
        const headers = ["Answer File", "Marks", "Suggestions"];
        const rows = lastResults.map(row =>
            [row.answer_file, row.marks, `"${row.suggestions.replace(/"/g, '""')}"`]
        );
        let csvContent = headers.join(",") + "\n" + rows.map(r => r.join(",")).join("\n");

        const blob = new Blob([csvContent], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "grading_report.csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});

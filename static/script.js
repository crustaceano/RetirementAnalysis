document.getElementById("upload-form").onsubmit = async function(event) {
    event.preventDefault();
    const status = document.getElementById("status");
    const progressBar = document.getElementById("progress-bar");

    status.textContent = "Uploading files...";
    status.classList.remove("success", "error");
    progressBar.style.display = "block";
    progressBar.value = 0;

    const formData = new FormData(this);

    try {
        const response = await fetch("/predict/", {
            method: "POST",
            body: formData,
            headers: { "Accept": "application/json" },
        });

        if (response.ok) {
            const blob = await response.blob();
            downloadFile(blob, "result.csv");
            status.textContent = "File downloaded successfully!";
            status.classList.add("success");
        } else {
            handleError(response);
        }
    } catch (error) {
        handleError(error);
    } finally {
        progressBar.style.display = "none";
    }
};

document.getElementById("interpret-form").onsubmit = async function(event) {
    event.preventDefault();
    console.log("Form submission initiated");

    const interpretStatus = document.getElementById("interpret-status");
    const sampleIndex = document.getElementById("sample-index").value;

    interpretStatus.textContent = "Interpreting...";
    interpretStatus.classList.remove("success", "error");

    // Подготовка данных для отправки как формы
    const formData = new FormData();
    formData.append("sample_index", sampleIndex);

    try {
        const response = await fetch("/interpret/", {
            method: "POST",
            body: formData // Отправка данных формы
        });

        if (response.ok) {
            const result = await response.json();
            interpretStatus.textContent = "Interpretation successful";
            interpretStatus.classList.add("success");

            // Отображение изображения
            const img = document.createElement("img");
            img.src = result.image_url;
            img.alt = `LIME Interpretation for Sample ${sampleIndex}`;
            document.getElementById("interpretation-result").innerHTML = ""; // Очистить предыдущие результаты
            document.getElementById("interpretation-result").appendChild(img); // Добавить новое изображение
        } else {
            const errorDetail = await response.json();
            interpretStatus.textContent = `Interpretation failed: ${errorDetail.detail}`;
            interpretStatus.classList.add("error");
        }
    } catch (error) {
        interpretStatus.textContent = "Error occurred: " + error.message;
        interpretStatus.classList.add("error");
        console.error("Error details:", error);
    }
};



// Функция для загрузки файла
function downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}

// Функция для обработки ошибок
function handleError(error) {
    const status = document.getElementById("status");
    status.textContent = "Prediction failed. Please try again.";
    status.classList.add("error");
    console.error(error);
}

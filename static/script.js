document.getElementById("upload-form").onsubmit = async function(event) {
    event.preventDefault();
    const status = document.getElementById("status");
    const progressBar = document.getElementById("progress-bar");

    // Сбрасываем статус и отображаем прогресс-бар
    status.textContent = "Uploading files...";
    status.classList.remove("success", "error");
    progressBar.style.display = "block";
    progressBar.value = 0;

    const formData = new FormData();
    formData.append("file1", document.querySelector('input[name="file1"]').files[0]);
    formData.append("file2", document.querySelector('input[name="file2"]').files[0]);

    try {
        const response = await fetch("/predict/", {
            method: "POST",
            body: formData,
            headers: { "Accept": "application/json" },
        });

        if (response.ok) {
            status.textContent = "Prediction complete. Downloading result...";
            status.classList.add("success");

            // Плавное заполнение прогресс-бара до 100%
            let progress = 0;
            const interval = setInterval(() => {
                if (progress < 100) {
                    progress += 10;
                    progressBar.value = progress;
                } else {
                    clearInterval(interval);
                }
            }, 100);

            // Создаем ссылку для скачивания
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "result.csv";
            document.body.appendChild(a);
            a.click();
            a.remove();

            // Очищаем после загрузки
            progressBar.style.display = "none";
            status.textContent = "File downloaded successfully!";
        } else {
            status.textContent = "Prediction failed. Please try again.";
            status.classList.add("error");
            progressBar.style.display = "none";
        }
    } catch (error) {
        status.textContent = "Error occurred: " + error.message;
        status.classList.add("error");
        progressBar.style.display = "none";
    }
};

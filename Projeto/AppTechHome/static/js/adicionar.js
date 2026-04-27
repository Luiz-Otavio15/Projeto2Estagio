const fileInput = document.getElementById("fileInput");
    const fileText = document.getElementById("fileText");

    fileInput.addEventListener("change", function() {
        if (this.files.length > 0) {
            fileText.textContent = this.files[0].name;
            document.querySelector(".file-upload").classList.add("active");
        }
    });
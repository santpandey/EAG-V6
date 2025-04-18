document.addEventListener("DOMContentLoaded", function () {
  const usernameBox = document.getElementById("usernameBox");
  const saveNameBtn = document.getElementById("saveNameBtn");
  const nameStatus = document.getElementById("nameStatus");
  const uploadBtn = document.getElementById("uploadBtn");
  const imageInput = document.getElementById("imageInput");
  const uploadStatus = document.getElementById("uploadStatus");
  const questionBox = document.getElementById("questionBox");
  const submitBtn = document.getElementById("submitBtn");
  const responseContainer = document.getElementById("responseContainer");
  const downloadSummaryCheckbox = document.getElementById('downloadSummaryCheckbox');
  const sendEmailCheckbox = document.getElementById('sendEmailCheckbox');
  const emailInput = document.getElementById('emailInput');

  let imageUploaded = false;
  let username = "";
  let lastResponseText = "";

  // Show/hide email input based on checkbox
  sendEmailCheckbox.addEventListener('change', function() {
    emailInput.style.display = this.checked ? '' : 'none';
  });

  // Restore username if saved
  if (localStorage.getItem("blood_report_username")) {
    username = localStorage.getItem("blood_report_username");
    usernameBox.value = username;
    enableMainUI();
    nameStatus.textContent = `Welcome, ${username}!`;
  }

  saveNameBtn.addEventListener("click", function () {
    const name = usernameBox.value.trim();
    if (!name) {
      nameStatus.textContent = "Please enter your name.";
      disableMainUI();
      return;
    }
    username = name;
    localStorage.setItem("blood_report_username", username);
    nameStatus.textContent = `Welcome, ${username}!`;
    enableMainUI();
  });

  function enableMainUI() {
    uploadBtn.disabled = false;
    questionBox.disabled = false;
    submitBtn.disabled = false;
  }
  function disableMainUI() {
    uploadBtn.disabled = true;
    questionBox.disabled = true;
    submitBtn.disabled = true;
  }

  uploadBtn.addEventListener("click", function () {
    imageInput.click();
  });

  imageInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (!file) return;
    if (!username) {
      uploadStatus.textContent = "Please enter your name first.";
      return;
    }
    uploadStatus.textContent = "Uploading...";
    const formData = new FormData();
    formData.append("image", file);
    formData.append("username", username);

    // No longer upload image here. Just store the file for later submission.
    uploadStatus.textContent = "Image selected: " + file.name;
    imageUploaded = true;
    window.selectedImageFile = file; // Store globally for submit
  });

  submitBtn.addEventListener("click", function () {
    const question = questionBox.value.trim();
    if (!imageUploaded) {
      responseContainer.textContent =
        "Please upload your blood report image first.";
      return;
    }
    if (!question) {
      responseContainer.textContent = "Please enter a question.";
      return;
    }
    if (!username) {
      responseContainer.textContent = "Please enter your name first.";
      return;
    }
    responseContainer.textContent = "Fetching answer...";
    const formData = new FormData();
    formData.append("username", username);
    formData.append("image", window.selectedImageFile || "");
    formData.append("download_summary", downloadSummaryCheckbox.checked);
    formData.append("send_email", sendEmailCheckbox.checked);
    if (sendEmailCheckbox.checked) {
      formData.append("email", emailInput.value.trim());
    } else {
      formData.append("email", "");
    }
    fetch(
      `http://127.0.0.1:8000/get_llm_response/${encodeURIComponent(question)}`,
      {
        method: "POST",
        body: formData,
      }
    )
      .then(async (response) => {
        if (!response.ok) throw new Error("Failed to get response");
        const data = await response.json();
        responseContainer.innerHTML = renderPydanticObject(data);
        lastResponseText = JSON.stringify(data, null, 2);
      })
      .catch((err) => {
        responseContainer.textContent = "Failed to get response from server.";
      });
  });

  function renderPydanticObject(obj) {
    if (typeof obj !== "object" || obj === null) return "<span>No data</span>";
    let html = '<ul style="list-style:none;padding-left:0;">';
    for (const [key, value] of Object.entries(obj)) {
      html += `<li><strong>${key}:</strong> ${
        typeof value === "object" ? JSON.stringify(value, null, 2) : value
      }</li>`;
    }
    html += "</ul>";
    return html;
  }
});

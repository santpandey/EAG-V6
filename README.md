# EAG-V6: Blood Report Analyzer

## Overview
EAG-V6 is an AI-powered application that helps users analyze blood report images, extract relevant health information, and answer questions about their blood report. The system consists of a FastAPI backend and a Chrome extension frontend for seamless user interaction.

Key features:
- Upload blood report images and extract information using an LLM (Gemini)
- Ask questions about your report and receive structured, accurate answers
- Download a summary of your report
- Send the summary to an email address

---

## Project Structure

- `app/` - FastAPI backend and AI orchestration logic
- `chrome-plugin/` - Chrome extension frontend
- `app/system_prompt.txt` - System prompt for the LLM
- `README.md` - This documentation

---

## Setup Instructions

1. **Clone the repository**
2. **Create and activate a Python virtual environment**
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Create a `.env` file in the root of the project:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
5. **Run the FastAPI server**
   ```sh
   fastapi dev app/agent.py
   ```
6. **Load the Chrome extension**
   - Go to chrome://extensions, enable Developer Mode, and load the `chrome-plugin/` directory as an unpacked extension.

---

## API Documentation

### `POST /get_llm_response/{message}`
Analyze a blood report image and/or answer a question.

**Path Parameter:**
- `message` (str): The user's question or prompt.

**Form Data:**
- `username` (str, required): Name of the user.
- `image` (file, optional): Blood report image file (PNG/JPG).
- `download_summary` (bool, optional): If true, generates and returns a summary of the report (default: false).
- `send_email` (bool, optional): If true, sends the summary to the provided email address (default: false).
- `email` (str, optional): Email address to send the summary to (required if `send_email` is true).

**Returns:**
- `crafted_prompt` (str): The LLM's answer to the user's question.
- `download_summary` (str, optional): The generated summary (if requested).
- `summary_file` (str, optional): Absolute path to the saved summary file (if requested).
- `email_sent_to` (str, optional): The email address the summary was sent to (if requested).
- `image_filename` (str, optional): The uploaded image's filename.

**Example cURL:**
```sh
curl -X POST "http://127.0.0.1:8000/get_llm_response/What%20are%20my%20haemoglobin%20levels" \
  -F "username=John Doe" \
  -F "image=@/path/to/report.png" \
  -F "download_summary=true" \
  -F "send_email=true" \
  -F "email=john@example.com"
```

---

## Chrome Plugin Usage
1. Enter your name and save it.
2. Upload your blood report image.
3. (Optional) Check "Download Summary" to generate and save a summary.
4. (Optional) Check "Send Email" and enter your email address to receive the summary by email.
5. Enter your question and click "Submit".
6. View the AI's response, download the summary, or check your email as needed.

---

## Notes
- The summary file (`summary.txt`) is saved on the server. To allow users to download it from the browser, implement a download endpoint and trigger it from the frontend.
- Make sure your Gemini API key is valid and has sufficient quota.
- For production, consider securing the API endpoints and validating email addresses.

---

## License
MIT License
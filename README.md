# 🛡️ Hybrid Vishing Detection System (English & Tanglish)

A dual-layer defense system against **Voice Phishing (Vishing)** attacks. This project combines **Computer Vision (OCR)** for technical defense and **Natural Language Processing (NLP)** for content analysis, with a unique focus on **Tanglish (Tamil-English Code-Mixed)** detection.

---

## 📖 Project Overview
Traditional vishing detection systems often focus only on call metadata or pure English text. This project introduces a **Hybrid Architecture** that protects users at two distinct stages:

1.  **Layer 1 (The Guard - VENTINEL):** Detects technical attacks like **Display Overlays** and **Contact Duplication** before the user even answers the call.
2.  **Layer 2 (The Brain - NLP Classifier):** Analyzes the conversation transcript using Machine Learning (Random Forest) to detect scam intent in **English, Hinglish, and Tanglish**.

**Key Innovation:**
Unlike standard models trained only on English, this system is specifically fine-tuned on **Code-Mixed Dravidian languages (Tanglish)** to suit real-world Indian scam scenarios.

---

## 🏗️ System Architecture



### **Layer 1: Visual & Behavioral Security (VENTINEL Simulation)**
* **Goal:** Detect if the phone's UI is lying to the user.
* **Method:** Uses **Tesseract OCR** to read the phone screen during an incoming call.
* **Attacks Detected:**
    * **Display Overlay Attacks:** When a scam app plasters a fake "Bank Customer Care" screen over a real call from an unknown number.
    * **Duplicated Contact Attacks:** When a scammer saves their number as "Mom" or "Bank" to trick the user.

### **Layer 2: Content Analysis (NLP Model)**
* **Goal:** Detect scam intent in the conversation.
* **Method:** A **Random Forest Classifier** trained on a custom dataset.
* **Data Augmentation:** Uses **Back-Translation** logic to expand small datasets.
* **Languages Supported:** English, Tanglish (Tamil-English), Hinglish.

---

## 📂 Dataset

We utilize a custom-built **High-Quality Grammar Dataset** containing **1,500 labeled samples**:

| Language | Count | Description |
| :--- | :--- | :--- |
| **English** | 500 | Standard international scam scripts (IRS, Amazon, etc.) |
| **Tanglish** | 500 | *New Addition:* Tamil-English code-mixed scams (e.g., "Sir, unga account block aagidum") |
| **Hinglish** | 500 | Hindi-English mixed scams (e.g., "Aapka lottery lag gaya hai") |

* **Labels:** `0` (Safe/Neutral) vs `1` (Scam/Suspicious)
* **Balance:** The final training set is perfectly balanced (50/50 split) to prevent bias.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8+
* **Tesseract OCR Engine** (Required for Layer 1)
    * *Mac (Homebrew):* `brew install tesseract`
    * *Windows:* [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)

### Step 1: Clone the Repository
```bash
git clone [https://github.com/kishore2k05/Hybrid-Vishing-Detection-System.git](https://github.com/kishore2k05/Hybrid-Vishing-Detection-System.git)
cd Hybrid-Vishing-Detection-System
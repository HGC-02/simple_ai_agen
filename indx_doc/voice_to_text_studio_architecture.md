# Voice-to-Text Studio: Architecture & How It Works

**Voice-to-Text Studio** is a 100% client-side, browser-native speech recognition and offline dictation workspace. Designed with zero backend infrastructure or external cloud roundtrips for processing, it runs entirely inside the user's browser using modern Web APIs.

---

## 1. Core Technical Stack

* **Frontend Framework:** Single-file HTML5 application structure.
* **Styling & UI:** Tailwind CSS v3 (via CDN) paired with FontAwesome v6 icons and Inter typography.
* **Speech Recognition:** Native browser `window.SpeechRecognition` / `window.webkitSpeechRecognition` API.
* **Speech Synthesis:** Native `window.speechSynthesis` API for text-to-speech feedback.
* **State Management:** Pure Vanilla JavaScript variables tracking transcription history, real-time buffers, and UI modes.

---

## 2. Architecture & Workflow Overview

```
 [ Microphone Input ] 
         │
         ▼
 ┌──────────────────────────────────────────────┐
 │          Browser Speech API Engine           │
 │ (webkitSpeechRecognition / SpeechRecognition)│
 └──────────────────────┬───────────────────────┘
                        │
                        ▼ (onresult event stream)
 ┌──────────────────────────────────────────────┐
 │        Client-Side JavaScript Buffer         │
 │  • Merges final & interim transcript segments│
 │  • Tracks word count & character length      │
 └──────────────────────┬───────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
 ┌──────────────────────┐      ┌──────────────────────┐
 │   Interactive UI     │      │   Export / Actions   │
 │ • Textarea Document  │      │ • Copy to Clipboard  │
 │ • Live Audio Pulse   │      │ • TXT File Download  │
 │ • Language Switcher  │      │ • Speech Synthesis   │
 └──────────────────────┘      └──────────────────────┘
```

---

## 3. Key Feature Implementations

### A. Browser-Native Speech Recognition
The app initializes the Web Speech API interface upon DOM load:
```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
recognition = new SpeechRecognition();
```
* **Multilingual Support:** Configured dynamically via `language-select` supporting Cantonese (`yue-Hant-HK`), Mandarin (`zh-CN`), English (`en-US`), and Russian (`ru-RU`).
* **Continuous Dictation:** Handles both interim results (real-time typing previews) and final results (committed text segments) to prevent stream loss.

### B. Fallback Offline Dictation Simulator
To ensure the application remains fully testable even in sandboxed browser frames or restricted network environments, an **Offline Dictation Simulator** is built in:
* Generates localized sample text streams matching the selected language at regular intervals.
* Triggered automatically if microphone permission is denied or native speech APIs are unavailable.

### C. Document Management & Client-Side Persistence
* **State Variables:** Transcripts and session histories are maintained in local memory arrays (`savedTranscriptsHistory`, `finalTranscript`).
* **Export Utilities:** Instant browser-side generation of downloadable `.txt` blobs using `URL.createObjectURL()` without hitting any external servers.
```javascript
const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
const url = URL.createObjectURL(blob);
```

---

## 4. Privacy & Security Model
Because Voice-to-Text Studio operates entirely on the client side:
1. **Zero Data Transmission:** Audio data and text transcripts never leave the user's local browser environment.
2. **No API Keys Required:** Relies solely on built-in browser engine capabilities, eliminating third-party API dependencies or subscription overhead.

###### made by ai not conform
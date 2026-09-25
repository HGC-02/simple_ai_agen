# Voice-to-Text Studio - 函數詳細解釋 (Functions Explanation)

呢個檔案詳細記錄咗 `index.html` 入面所有 JavaScript 函數嘅作用、運作原理同埋定義嘅行數，全部以繁體中文解說。

---

## 1. 核心控制與初始化函數

### `DOMContentLoaded` 事件監聽器
* **行數**：Line 170
* **用途**：網頁載入完成（DOM 準備就緒）時自動執行。負責檢測瀏覽器係咪支援原生語音識別 (`SpeechRecognition`)、綁定各個事件監聽器（如 `textarea` 輸入、語言切換），以及設定語音識別回調函數 (`onstart`, `onresult`, `onerror`, `onend`)。

### `updateRecognitionSettings()`
* **行數**：Line 253
* **用途**：更新語音識別實例 (`recognition`) 嘅設定。
* **運作原理**：將 `languageSelect.value` 設定落去 `recognition.lang`，並根據 `continuousToggle.checked` 設定連續聆聽狀態，同時開啟中途結果回調 (`interimResults = true`)。

### `toggleOfflineSimulator()`
* **行數**：Line 260
* **用途**：切換「離線模擬器模式 (`useSimulator`)」。
* **運作原理**：反轉 `useSimulator` 嘅布林值，為模擬器按鈕加上或移除高亮樣式，並顯示對應嘅狀態提示橫幅。如果當時正喺度錄音，會順便觸發停止/重啟流程。

---

## 2. 錄音與模擬器控制函數

### `toggleRecording()`
* **行數**：Line 273
* **用途**：控制錄音嘅開始與停止（對應主畫面嘅大按鈕）。
* **運作原理**：
  * 如果 `isRecording` 係 `true`，會停止識別（或停止模擬器），將當前文字內容存入 `savedTranscriptsHistory` 陣列，並呼叫 `stopRecordingState()`。
  * 如果 `isRecording` 係 `false`，會重設或保留現有文字，啟動錄音介面狀態，並根據 `useSimulator` 決定啟動網頁原生 `recognition.start()` 定係 `startSimulator()`。

### `startSimulator()`
* **行數**：Line 328
* **用途**：啟動離線語音模擬器。
* **運作原理**：利用 `setInterval` 每隔 3 秒自動從 `simulatedPhrasesMap` 抽取對應語言嘅預設句子，模擬真人講嘢咁逐句加入到 `finalTranscript` 同 `transcriptBox` 入面。

### `stopSimulator()`
* **行數**：Line 342
* **用途**：停止離線語音模擬器。
* **運作原理**：清除 `simulatorInterval` 計時器，停止自動文字生成。

---

## 3. 介面狀態更新函數

### `setRecordingUIState(active)`
* **行數**：Line 350
* **用途**：設定錄音進行中嘅 UI 樣式。
* **參數**：`active` (Boolean)
* **運作原理**：將主錄音按鈕改為紅色呼吸燈效果 (`bg-rose-600`, `animate-pulse`)，將圖示改為停止符號 (`fa-stop`)，並顯示錄音中嘅閃爍提示 (`recordingIndicator`)。

### `stopRecordingState()`
* **行數**：Line 368
* **用途**：將介面恢復為未錄音（靜止）嘅狀態。
* **運作原理**：重設 `isRecording` 為 `false`，清空模擬器計時器，還原主按鈕顏色同文字 (`Start Recording`)，隱藏錄音中嘅指示器。

### `updateStats()`
* **行數**：Line 382
* **用途**：計算並更新即時字數同字元數統計。
* **運作原理**：讀取 `transcriptBox.value`，用正則表達式計算單詞/字數 (`word-count`) 同總字元長度 (`char-count`) 並更新到 DOM。

### `showBanner(message, type)`
* **行數**：Line 427
* **用途**：在頂部顯示彈出式通知橫幅。
* **參數**：`message` (String - 訊息內容), `type` (String - 類型，如 `'success'`, `'error'`, `'info'`)
* **運作原理**：根據不同類型配搭對應嘅背景顏色同邊框，顯示訊息後透過 `setTimeout` 在 4.5 秒後自動隱藏。

---

## 4. 文件操作與輔助函數

### `clearText()`
* **行數**：Line 391
* **用途**：清空整個轉錄文件。
* **運作原理**：如果當時正在錄音會先叫 `toggleRecording()` 停低，然後清空 `transcriptBox.value`、`finalTranscript` 同 `window.latestRecognitionResult`，重設統計數據並彈出提示。

### `copyToClipboard()`
* **行數**：Line 403
* **用途**：一鍵複製轉錄內容到剪貼簿。
* **運作原理**：建立暫時嘅 `<textarea>` 元素執行 `document.execCommand('copy')`，將文字複製低並顯示成功通知。

### `downloadText()`
* **行數**：Line 420
* **用途**：將文字匯出下載為 `.txt` 檔案。
* **運作原理**：利用 `Blob` 包裝文字內容，透過 `URL.createObjectURL` 建立臨時下載連結，自動觸發瀏覽器下載，最後清除記憶體。

### `speakText()`
* **行數**：Line 451
* **用途**：文字轉語音朗讀功能 (Text-to-Speech)。
* **運作原理**：檢查瀏覽器係咪支援 `speechSynthesis`，建立 `SpeechSynthesisUtterance` 物件並設定好對應語言 (`languageSelect.value`)，然後將文字朗讀出嚟。
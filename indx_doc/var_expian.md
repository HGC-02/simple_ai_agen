# Voice-to-Text Studio - 變數與狀態設定對照表

呢個檔案詳細記錄咗 `index.html` 內 JavaScript 部分所使用嘅全域變數、DOM 元素參照以及狀態變數，並標明咗佢哋被設定嘅行數。

## 1. 核心狀態與控制變數

| 變數名稱 | 行數 | 類型 | 說明 |
| :--- | :---: | :---: | :--- |
| `recognition` | Line 144 | Object / null | 儲存瀏覽器原生嘅 `SpeechRecognition` 語音識別實例。 |
| `isRecording` | Line 145 | Boolean | 追蹤目前錄音狀態 (`true` 代表錄音中，`false` 代表停止)。 |
| `finalTranscript` | Line 148 | String | 累積並儲存已經確認（Final）嘅語音辨識文字。 |
| `interimTranscript` | Line 149 | String | 儲存辨識過程中暫時性（Interim）嘅即時文字。 |
| `savedTranscriptsHistory` | Line 150 | Array | 陣列變數，用來儲存每一次停止錄音後封存嘅歷史紀錄。 |
| `useSimulator` | Line 152 | Boolean | 標記係咪啟用「離線模擬器模式」（當瀏覽器不支援原生 API 時自動啟用或手動切換）。 |
| `simulatorInterval` | Line 153 | Number / null | 儲存模擬器計時器（`setInterval`）嘅 ID，方便之後清除。 |

---

## 2. DOM 元素快取變數 (UI References)

呢啲變數喺網頁載入時透過 `document.getElementById` 綁定，方便隨時操作介面元素：

| 變數名稱 | 行數 |對應 HTML ID | 說明 |
| :--- | :---: | :--- | :--- |
| `micBtn` | Line 155 | `mic-btn` | 主錄音按鈕元素。 |
| `micIcon` | Line 156 | `mic-icon` | 錄音按鈕入面嘅圖示（咪高峰 / 停止符號）。 |
| `micBtnText` | Line 157 | `mic-btn-text` | 錄音按鈕上面嘅文字（"Start Recording" / "Stop Recording"）。 |
| `transcriptBox` | Line 158 | `transcript-box` | 主文字輸入框（Textarea），顯示所有轉錄內容。 |
| `recordingIndicator` | Line 159 | `recording-indicator` | 錄音中嘅閃爍提示標籤。 |
| `indicatorText` | Line 160 | `indicator-text` | 提示標籤入面嘅文字說明。 |
| `wordCountEl` | Line 161 | `word-count` | 顯示總字數統計嘅數字元素。 |
| `charCountEl` | Line 162 | `char-count` | 顯示總字元數統計嘅數字元素。 |
| `languageSelect` | Line 163 | `language-select` | 語言選擇下拉選單。 |
| `continuousToggle` | Line 164 | `continuous-toggle` | 持續聆聽（Continuous Listening）嘅勾選框。 |
| `supportStatus` | Line 165 | `support-status` | 顯示瀏覽器支援狀態嘅徽章。 |
| `statusBanner` | Line 166 | `status-banner` | 頂部嘅通知橫幅容器。 |
| `statusMsg` | Line 167 | `status-msg` | 通知橫幅入面嘅文字訊息。 |
| `simModeBtn` | Line 168 | `sim-mode-btn` | 切換離線模擬器模式嘅按鈕。 |

---

## 3. 模擬器專用變數

| 變數名稱 | 行數 | 類型 | 說明 |
| :--- | :---: | :---: | :--- |
| `simulatedPhrasesMap` | Line 321 | Object | 儲存唔同語言（粵語、普通話、英文、俄文）嘅預設模擬對話字串對應表。 |
| `simIndex` | Line 326 | Number | 追蹤模擬器目前輸出緊邊一句預設對話嘅索引值。 |
# Hướng Dẫn Sử Dụng Web Application (Streamlit)

## 🚀 Khởi Động Ứng Dụng

### Bước 1: Mở Terminal

```bash
cd /home/imdakk/Documents/AdaptiveBitrate/AdaptiveBitrate
```

### Bước 2: Kích Hoạt Virtual Environment

```bash
source ../venv/bin/activate
```

### Bước 3: Chạy Ứng Dụng

```bash
streamlit run adaptive_bitrate_demo.py
```

### Bước 4: Mở Trình Duyệt

```
http://localhost:8502
```

Hoặc copy URL từ terminal output

---

## 📱 Giao Diện Chính

Ứng dụng có **6 tabs chính** ở phía trên:

```
┌─────────────────────────────────────────────────────────┐
│ 📊 Audio Features │ 🌐 Network Analysis │ 🎯 Adaptive   │
│ 📈 Metrics        │ 💾 Summary          │ 🎵 Playback   │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Bước Sử Dụng Chi Tiết

### **Bước 1: Tải/Ghi Âm Thanh**

**Cách A: Tải file audio**
1. Bên trái sidebar, tìm mục **"📁 Upload Audio File"**
2. Click **"Browse Files"**
3. Chọn file WAV (khuyến nghị < 2 MB)
4. Ứng dụng tự động xử lý

**Cách B: Ghi âm từ microphone**
1. Tìm mục **"🎤 Record Audio"**
2. Click **"Start recording"**
3. Nói/chơi nhạc trong ~10 giây
4. Click **"Stop recording"**

### **Bước 2: Điều Chỉnh Tham Số** (Sidebar)

```
┌─────────────────────────────┐
│        THAM SỐ              │
├─────────────────────────────┤
│ 📊 Chunk Duration (ms)      │ 500-2000 ms
│ 🌐 Network Pattern          │ 7 patterns
│ 🔨 Aggressive Compression   │ On/Off
│ 📈 Visualization Settings   │ Chart options
└─────────────────────────────┘
```

**Các tham số quan trọng:**

- **Chunk Duration**: Khoảng thời gian phân tích
  - Nhỏ (500ms): Chi tiết cao, xử lý chậm
  - Lớn (2000ms): Xử lý nhanh, chi tiết thấp
  - **Khuyến nghị**: 1000 ms

- **Network Pattern**: Mô phỏng điều kiện mạng
  - Stable: Mạng tốt
  - Decreasing: Mạng suy giảm
  - Sinusoidal: Mạng dao động
  - Recovery: Mạng sụt rồi phục hồi
  - Weak: Mạng yếu
  - Very Weak: Mạng rất yếu (5-16 kbps)
  - Random: Mạng không ổn định

- **Aggressive Compression**: Tiết kiệm bandwidth
  - Tắt: Chất lượng ưu tiên
  - Bật: Bandwidth ưu tiên

---

## 📊 Tab 1: Audio Features (Đặc Trưng Âm Thanh)

### Hiển Thị Gì?

**5 biểu đồ riêng lẻ:**

```
1. RMS Energy Over Time
   ├─ Trục Y: Năng lượng (0.0 - 1.0)
   ├─ Trục X: Thời gian (ms)
   └─ Ý nghĩa: Âm thanh to hay nhỏ?

2. Zero Crossing Rate Over Time
   ├─ Trục Y: ZCR (0.0 - 1.0)
   └─ Ý nghĩa: Tần số thay đổi nhanh chậm?
           Cao = Voice, Thấp = Music

3. Spectral Centroid Over Time
   ├─ Trục Y: Hz
   └─ Ý nghĩa: Tần số trọng tâm?
           Cao = Tiếng cao, Thấp = Tiếng bổm

4. Spectral Bandwidth Over Time
   ├─ Trục Y: Hz
   └─ Ý nghĩa: Phổ tần rộng hay hẹp?
           Rộng = Chi tiết, Hẹp = Đơn giản

5. Spectral Flatness Over Time
   ├─ Trục Y: 0.0 - 1.0
   └─ Ý nghĩa: Phổ bằng phẳng?
           = 1.0: Noise, < 1.0: Signal
```

### Cách Sử Dụng

1. Tải file hoặc ghi audio
2. Tự động hiển thị 5 biểu đồ
3. Di chuột lên chart để xem chi tiết
4. Tìm vùng "đỉnh" để hiểu khi nào cần bitrate cao

**Ví dụ đọc:**
```
RMS cao + ZCR cao → Nói chuyện to
RMS vừa + ZCR thấp → Nhạc bình thường
RMS thấp → Yên tĩnh hoặc silence
```

---

## 🌐 Tab 2: Network Analysis (Phân Tích Mạng)

### Hiển Thị Gì?

```
┌─────────────────────────────────┐
│ Network Bandwidth Over Time     │
├─────────────────────────────────┤
│ Biểu đồ 1:                      │
│ - Trục Y: Bandwidth (kbps)      │
│ - Trục X: Thời gian             │
│ - Màu xanh: Mô phỏng bandwidth  │
│                                 │
│ Biểu đồ 2:                      │
│ - Thống kê: Min, Max, Avg       │
│ - Standard Deviation            │
│ - Số chunk được xử lý           │
└─────────────────────────────────┘
```

### Network Patterns (Giải Thích)

| Pattern | Bandwidth | Mô Tả | Khi Nào Dùng |
|---------|-----------|-------|------------|
| 🟢 **Stable** | 256 kbps | Không đổi | WiFi tốt |
| 📉 **Decreasing** | 256→10 | Giảm dần | Đi chuyển |
| 〰️ **Sinusoidal** | 24-104 | Dao động | Nhiễu EM |
| ⬇️⬆️ **Recovery** | 64→10→64 | Sụt phục hồi | Mất kết nối |
| 📊 **Weak** | ~48 | Yếu ổn định | 4G yếu |
| 💔 **Very Weak** | 5-16 | Rất yếu | 2G/edge |
| 🎲 **Random** | 64±spikes | Ngẫu nhiên | Không ổn định |

### Cách Sử Dụng

1. Vào Tab "🌐 Network Analysis"
2. Chọn Network Pattern từ sidebar
3. Quan sát biểu đồ bandwidth
4. Nhận xét:
   - Bandwidth nhiều → Bitrate cao
   - Bandwidth ít → Bitrate thấp

---

## 🎯 Tab 3: Adaptive Bitrate (Chọn Bitrate)

### Hiển Thị Gì?

```
┌──────────────────────────────────────────┐
│ Bitrate Selection Decision               │
├──────────────────────────────────────────┤
│ 1. Content Type Detected                 │
│    └─ Speech / Music / Mixed / Silence   │
│                                          │
│ 2. Complexity Level                      │
│    └─ Low / Medium / High                │
│                                          │
│ 3. Selected Bitrates Over Time           │
│    └─ Biểu đồ: Bitrate vs Thời gian    │
│                                          │
│ 4. Selection Reasons Table               │
│    └─ Mỗi chunk: Lý do tại sao chọn    │
│       bitrate này                        │
└──────────────────────────────────────────┘
```

### Cách Sử Dụng

1. Vào Tab "🎯 Adaptive Bitrate"
2. Quan sát:
   - Content Type: Phát hiện loại nội dung đúng?
   - Complexity: Độ phức tạp hợp lý?
   - Bitrate Selection Chart: Bitrate thích ứng với network?
   - Reasons Table: Lý do tại sao chọn bitrate?

**Ví dụ:**
```
Content Type: SPEECH
Complexity: MEDIUM (0.45)
Available Bandwidth: 64 kbps
→ Selected Bitrate: 16 kbps
→ Reason: Adaptive selection based on speech + medium complexity
```

---

## 📈 Tab 4: Metrics (Chỉ Số Chất Lượng)

### Hiển Thị Gì?

```
┌──────────────────────────────────────────┐
│ Quality Metrics & Statistics             │
├──────────────────────────────────────────┤
│ 1. Audio Features Statistics             │
│    ├─ RMS: Min, Max, Mean                │
│    ├─ ZCR: Min, Max, Mean                │
│    ├─ Spectral Centroid, Bandwidth       │
│    └─ Complexity Score                   │
│                                          │
│ 2. Bitrate Statistics                    │
│    ├─ Selected Bitrate: Min, Max, Mean   │
│    ├─ Bitrate Changes                    │
│    └─ Stability Ratio                    │
│                                          │
│ 3. Network Statistics                    │
│    ├─ Bandwidth: Min, Max, Mean          │
│    ├─ Bandwidth Variability              │
│    └─ Pattern Type                       │
│                                          │
│ 4. Efficiency Metrics                    │
│    ├─ Average Utilization (Bitrate/BW)  │
│    ├─ Quality Score                      │
│    └─ Adaptation Aggressiveness          │
└──────────────────────────────────────────┘
```

### Cách Sử Dụng

1. Vào Tab "📈 Metrics"
2. Kiểm tra:
   - **RMS Mean**: Âm thanh to hay nhỏ?
   - **Complexity Score**: Nội dung phức tạp?
   - **Bitrate Mean**: Bitrate trung bình?
   - **Bandwidth Mean**: Mạng chất lượng nào?
   - **Utilization**: Tận dụng mạng hiệu quả?

---

## 💾 Tab 5: Summary (Tóm Tắt)

### Hiển Thị Gì?

```
📊 AUDIO SUMMARY
├─ Duration: X seconds
├─ Content Type: Speech / Music / ...
├─ Average Complexity: 0.XX (Low/Med/High)
└─ Loudness: X dB

🌐 NETWORK SUMMARY
├─ Pattern: [Selected pattern]
├─ Average Bandwidth: X kbps
├─ Min/Max Bandwidth: X - Y kbps
└─ Variability: X%

🎯 ADAPTIVE BITRATE SUMMARY
├─ Average Bitrate: X kbps
├─ Bitrate Range: X - Y kbps
├─ Number of Changes: N
└─ Adaptation Quality: X/10

💡 RECOMMENDATIONS
├─ Bitrate Tier: Use XX kbps for stable playback
├─ Best Pattern: Network [pattern] works best
├─ Improvement: [Suggestion]
└─ Further Action: [Next step]
```

### Cách Sử Dụng

Xem tóm tắt nhanh gọn của toàn bộ phân tích

---

## 🎵 Tab 6: Audio Playback (Phát Âm Thanh)

### 3 Chế Độ Phát

#### 1️⃣ **Mode: Original Audio**
```
Phát âm thanh gốc 100% (không nén)
└─ Tần số: 22050 Hz (full spectrum)
```

#### 2️⃣ **Mode: Simulated Quality**
```
Phát âm thanh theo bitrate đã chọn
├─ Slider: Chọn bitrate (5-256 kbps)
├─ Tần số Cutoff: Tự động điều chỉnh
└─ Ví dụ: 64 kbps → 8000 Hz
```

#### 3️⃣ **Mode: Compare Audio**
```
So sánh nhiều bitrate cùng lúc
├─ Chọn tối đa 4 bitrate
├─ Phát tuần tự từng cái
└─ Nghe rõ sự khác biệt
```

### Cách Sử Dụng

**Step 1: Chọn chế độ phát**
```
Radio button: Original / Simulated / Compare
```

**Step 2: Chọn bitrate** (nếu Simulated hoặc Compare)
```
Slider hoặc Multiselect: Chọn 1-4 bitrate
```

**Step 3: Phát**
```
Click nút ▶️ "Play Audio"
```

**Step 4: Nghe và so sánh**
```
Chú ý sự khác biệt:
- Treble (cao) bị mất đi?
- Voice còn rõ ràng?
- Nhạc nền bị mây mờ?
```

### Ví Dụ So Sánh

```
Original (256 kbps)
└─ Âm thanh sạch, chi tiết đầy đủ

Simulated 64 kbps
└─ Treble mất, nhưng voice vẫn tốt

Simulated 16 kbps
└─ Chỉ còn voice cơ bản, nhạc không rõ

Simulated 5 kbps
└─ Rất lọc, chỉ phù hợp comfort noise
```

---

## ⚙️ Sidebar Configuration (Cấu Hình)

### 📊 Chunk Duration (ms)
- **Mặc định**: 1000 ms
- **Phạm vi**: 500 - 2000 ms
- **Ảnh hưởng**: 
  - Nhỏ = Chi tiết cao nhưng chậm
  - Lớn = Nhanh nhưng ít chi tiết

### 🌐 Network Pattern
- **Mặc định**: Stable
- **Tùy chọn**: 7 patterns (xem trên)
- **Tác dụng**: Mô phỏng điều kiện mạng khác nhau

### 🔨 Aggressive Compression
- **Tắt (mặc định)**: Chất lượng ưu tiên
- **Bật**: Tiết kiệm bandwidth ưu tiên
- **Ảnh hưởng**: 
  - Tắt: Bitrate cao hơn, chất lượng tốt
  - Bật: Bitrate thấp hơn, tiết kiệm (khá hơn)

---

## 🎓 Mẹo & Thủ Thuật

### 1. **Chạy Test Đầu Tiên**
```
1. Để Network Pattern = Stable
2. Tải file audio nói chuyện 10 giây
3. Xem Tab 1 & 3: Hệ thống hoạt động?
```

### 2. **Kiểm Tra Thích Ứng**
```
1. Đặt Network Pattern = Decreasing
2. Xem Tab 3: Bitrate giảm khi bandwidth giảm?
3. Xem Tab 2: Bandwidth thực tế giảm?
```

### 3. **So Sánh Chất Lượng**
```
1. Tab 6 → Compare Mode
2. Chọn [64 kbps, 32 kbps, 16 kbps, 8 kbps]
3. Nghe lần lượt → Nhận biết sự khác biệt
```

### 4. **Ultra-Low Bandwidth Test**
```
1. Network = Very Weak (10 kbps)
2. Upload music file
3. Tab 3: Xem bitrate bị giới hạn?
4. Tab 6 → Simulated @ 5 kbps: Nghe gì?
```

### 5. **Xem Logs Chi Tiết**
```
Terminal sẽ in:
- Chunk được xử lý
- Bitrate được chọn
- Lý do chọn
```

---

## 🐛 Xử Lý Lỗi

### ❌ **"No audio file uploaded"**
- **Giải pháp**: Upload file WAV hoặc ghi audio

### ❌ **"Bandwidth pattern error"**
- **Giải pháp**: Refresh browser (Ctrl+R)

### ❌ **"Audio playback not working"**
- **Kiểm tra**: 
  - Volume máy tính có bật?
  - Browser hỗ trợ HTML5 audio?
  - File có valid?

### ❌ **"App chạy chậm"**
- **Giải pháp**:
  - Tăng Chunk Duration lên 1500-2000 ms
  - Dùng file audio nhỏ hơn
  - Tắt các tab khác

### ❌ **"Memory error"**
- **Giải pháp**: Restart app
  ```bash
  Ctrl+C → streamlit run adaptive_bitrate_demo.py
  ```

---

## 📱 Mobile Access

Truy cập từ điện thoại cùng mạng:

```
1. Xem URL trong terminal: http://XXX.XXX.XXX.XXX:8502
2. Mở trên điện thoại
3. Sử dụng như bình thường
```

---

## 🎯 Workflow Đề Xuất

```
┌─────────────────┐
│ 1. Tải Audio    │
└────────┬────────┘
         │
┌────────┴───────────────────┐
│ 2. Xem Tab 1 (Features)    │
│    Hiểu đặc trưng audio    │
└────────┬───────────────────┘
         │
┌────────┴───────────────────┐
│ 3. Thay Network Pattern    │
│    Xem Tab 2 (Network)     │
└────────┬───────────────────┘
         │
┌────────┴───────────────────┐
│ 4. Quan sát Tab 3 (Bitrate)│
│    Thích ứng ra sao?       │
└────────┬───────────────────┘
         │
┌────────┴───────────────────┐
│ 5. Xem Tab 4 & 5 (Metrics) │
│    Đánh giá performance    │
└────────┬───────────────────┘
         │
┌────────┴───────────────────┐
│ 6. Tab 6 (Playback)        │
│    Nghe chất lượng thực tế  │
└─────────────────────────────┘
```

---

**Xem ALGORITHM_EXPLANATION.md để hiểu cách thuật toán hoạt động!**
**Xem WEB_CONTENT_EXPLANATION.md để chi tiết từng tab!**

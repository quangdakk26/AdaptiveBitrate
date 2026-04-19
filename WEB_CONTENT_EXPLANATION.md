# Giải Thích Nội Dung Hiển Thị Trên Web

## 📌 Tổng Quan Ứng Dụng

Ứng dụng gồm **6 tabs** + **1 sidebar** để cấu hình

```
┌──────────────────────────────────────────────────────────────┐
│  SIDEBAR (Bên Trái)    │  MAIN CONTENT (6 Tabs - Giữa)      │
├────────────────────────┼──────────────────────────────────────┤
│ 📁 Upload Audio        │  Tab 1: 📊 Audio Features           │
│ 🎤 Record Audio        │  Tab 2: 🌐 Network Analysis        │
│ 📊 Chunk Duration      │  Tab 3: 🎯 Adaptive Bitrate        │
│ 🌐 Network Pattern     │  Tab 4: 📈 Metrics                 │
│ 🔨 Compression Mode    │  Tab 5: 💾 Summary                 │
│                        │  Tab 6: 🎵 Audio Playback          │
└────────────────────────┴──────────────────────────────────────┘
```

---

## 🎛️ SIDEBAR: Điều Khiển Chính

### 📁 Upload Audio File

```
┌─────────────────────────────┐
│ 📁 Upload Audio File        │
├─────────────────────────────┤
│ Button: "Browse files"      │
│ Formats: .wav (chính)       │
│ Size: ≤ 5 MB (khuyến nghị)  │
│ Sample rate: 16000 - 48000  │
│ Channels: Mono / Stereo     │
└─────────────────────────────┘
```

**Chức năng:**
- Tải file audio từ máy tính
- Ứng dụng tự động đọc và xử lý
- Nếu không có file → không thể phân tích

**Lưu ý:**
- Dùng file .wav (không .mp3)
- Audio tối thiểu 2 giây
- File lớn (> 5MB) xử lý chậm

---

### 🎤 Record Audio

```
┌─────────────────────────────┐
│ 🎤 Record Audio             │
├─────────────────────────────┤
│ Button: "Start recording"   │
│ Duration: ~10-30 seconds    │
│ Sample rate: 16000 Hz       │
│ Channels: Mono              │
│ Button: "Stop recording"    │
└─────────────────────────────┘
```

**Chức năng:**
- Ghi âm từ microphone của máy tính
- Yêu cầu quyền truy cập microphone
- Lưu tạm thời để phân tích

**Cách sử dụng:**
1. Click "Start recording"
2. Nói hoặc phát nhạc
3. Click "Stop recording"
4. Ứng dụng tự động xử lý

**Ví dụ ghi âm:**
- Voice: "Hello, this is a test recording"
- Music: Phát nhạc từ speaker
- Mixed: Nói + nhạc nền

---

### 📊 Chunk Duration (ms)

```
┌─────────────────────────────┐
│ Chunk Duration (ms)         │
├─────────────────────────────┤
│ Slider: 500 ←───●─→ 2000   │
│ Mặc định: 1000              │
│ Unit: Milliseconds          │
└─────────────────────────────┘
```

**Ý nghĩa:**
Khoảng thời gian để phân tích 1 "khúc" audio

**Chi tiết:**
- **500 ms**: Phân tích rất chi tiết (chậm)
  ```
  Ưu: Bitrate thay đổi từng 0.5 giây
  Nhược: Chậm, dùng nhiều CPU
  ```

- **1000 ms** (khuyến nghị): Cân bằng
  ```
  Ưu: Đủ chi tiết + nhanh hợp lý
  Nhược: Không quá nhanh, không quá chậm
  ```

- **2000 ms**: Phân tích ít chi tiết (nhanh)
  ```
  Ưu: Xử lý nhanh, dùng ít CPU
  Nhược: Bitrate thay đổi từng 2 giây
  ```

**Ảnh hưởng:**
```
Chunk Duration nhỏ
├─ Bitrate thay đổi thường xuyên
├─ Chi tiết cao
├─ Xử lý chậm
└─ Dễ thấy sự "gâyvô"

Chunk Duration lớn
├─ Bitrate thay đổi ít
├─ Chi tiết thấp
├─ Xử lý nhanh
└─ Chất lượng ổn định
```

---

### 🌐 Network Pattern

```
┌──────────────────────────────┐
│ Network Pattern              │
├──────────────────────────────┤
│ ☐ Stable (256 kbps)          │
│ ☐ Decreasing (256→10 kbps)   │
│ ☐ Sinusoidal (24-104 kbps)   │
│ ☐ Recovery (64→10→64 kbps)   │
│ ☐ Weak (48 kbps)             │
│ ☐ Very Weak (5-16 kbps)      │
│ ☐ Random Spikes              │
│ (Select one)                 │
└──────────────────────────────┘
```

**Chọn 1 trong 7 pattern:**

| Pattern | Mô Tả | Bandwidth | Khi Nào? |
|---------|-------|-----------|---------|
| 🟢 **Stable** | Ổn định | 256 kbps | WiFi tốt, LTE tốt |
| 📉 **Decreasing** | Suy giảm | 256→10 | Đi chuyển, mất sóng |
| 〰️ **Sinusoidal** | Dao động | 24-104 | Nhiễu EM, tín hiệu dao động |
| ⬇️⬆️ **Recovery** | Sụt + phục hồi | 64→10→64 | Mất kết nối tạm, khôi phục |
| 📊 **Weak** | Yếu ổn định | ~48 | 4G yếu, 3G ổn định |
| 💔 **Very Weak** | Rất yếu | 5-16 | 2G, vùng sóng kém |
| 🎲 **Random** | Ngẫu nhiên | 64±spikes | Mạng bất ổn định |

**Ảnh hưởng trực tiếp:**
```
Pattern ← Bandwidth
     ↓
Bitrate Selection (Tab 3)
     ↓
Audio Quality (Tab 6)
```

---

### 🔨 Aggressive Compression

```
┌──────────────────────────────┐
│ Aggressive Compression       │
├──────────────────────────────┤
│ ☐ Off (Mặc định)            │
│ ☑ On (Tiết kiệm)            │
└──────────────────────────────┘
```

**On / Off:**

- **Off** (Mặc định):
  ```
  Ưu tiên: Chất lượng
  Bitrate: Cao hơn 20%
  Tối ưu: Mạng tốt
  Khi dùng: Khi có bandwidth dư
  ```

- **On** (Aggressive):
  ```
  Ưu tiên: Tiết kiệm bandwidth
  Bitrate: Thấp hơn 20%
  Tối ưu: Mạng yếu
  Khi dùng: Mạng rất kém, cần tiết kiệm
  ```

---

## 📊 TAB 1: Audio Features (Đặc Trưng Âm Thanh)

### Cấu Trúc

```
┌────────────────────────────────────────────────────┐
│ 📊 AUDIO FEATURES                                  │
├────────────────────────────────────────────────────┤
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ RMS Energy Over Time                         │  │
│ │ (5 phút trở lại)                             │  │
│ │ Trục Y: Năng lượng (0.0 - 1.0)               │  │
│ │ Trục X: Thời gian (Chunk ID)                 │  │
│ │ Biểu đồ: Line chart (xanh)                   │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Zero Crossing Rate Over Time                 │  │
│ │ Trục Y: ZCR (0.0 - 1.0)                      │  │
│ │ Trục X: Thời gian (Chunk ID)                 │  │
│ │ Biểu đồ: Line chart (cam)                    │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Spectral Centroid Over Time                  │  │
│ │ Trục Y: Hz (0 - 8000)                        │  │
│ │ Trục X: Thời gian (Chunk ID)                 │  │
│ │ Biểu đồ: Line chart (tím)                    │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Spectral Bandwidth Over Time                 │  │
│ │ Trục Y: Hz (0 - 4000)                        │  │
│ │ Trục X: Thời gian (Chunk ID)                 │  │
│ │ Biểu đồ: Line chart (đỏ)                     │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Spectral Flatness Over Time                  │  │
│ │ Trục Y: Flatness (0.0 - 1.0)                 │  │
│ │ Trục X: Thời gian (Chunk ID)                 │  │
│ │ Biểu đồ: Line chart (hồng)                   │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 5 Biểu Đồ Chi Tiết

#### 1️⃣ **RMS Energy Over Time**

```
Định nghĩa: Root Mean Square (Năng lượng)
Công thức: √(Σ(sample²) / N)
Giá trị: 0.0 (Im lặng) ← → 1.0 (Rất to)

Ý nghĩa:
- Cao (> 0.5): Âm thanh to, có năng lượng
- Vừa (0.2-0.5): Âm thanh bình thường
- Thấp (< 0.2): Âm thanh nhỏ, gần yên tĩnh

Ví dụ:
- Nói bình thường: 0.3 - 0.6
- Thì thầm: 0.1 - 0.2
- Nhạc mạnh: 0.7 - 0.9
```

**Cách đọc:**
- Đỉnh cao → Vùng âm thanh mạnh
- Đáy thấp → Vùng yên tĩnh
- Đều ổn định → Âm thanh steady

---

#### 2️⃣ **Zero Crossing Rate Over Time**

```
Định nghĩa: Số lần tín hiệu qua 0 trên giây
Công thức: ZCR = Σ(|sgn(x[n]) - sgn(x[n-1])|) / (2*N)
Giá trị: 0.0 (Thấp) ← → 1.0 (Cao)

Ý nghĩa:
- Cao ZCR (> 0.4): Tần số thay đổi nhanh = VOICE
- Thấp ZCR (< 0.2): Tần số thay đổi chậm = MUSIC/BASS

Ví dụ:
- Nói chuyện: 0.4 - 0.7 (ZCR cao)
- Âm trầm: 0.1 - 0.2 (ZCR thấp)
- Tiếng cao: 0.5 - 0.9 (ZCR rất cao)
```

**Cách đọc:**
- ZCR cao & RMS cao → Voice rõ ràng
- ZCR thấp & RMS cao → Bass/Music mạnh
- ZCR vừa phải → Mixed content

---

#### 3️⃣ **Spectral Centroid Over Time**

```
Định nghĩa: Tần số trọng tâm (weighted average frequency)
Công thức: Centroid = Σ(f × magnitude[f]) / Σ(magnitude[f])
Giá trị: 0 - 22050 Hz (phụ thuộc sample rate)

Ý nghĩa:
- Cao centroid (> 4000 Hz): Âm thanh cao, sắc
- Trung bình (2000-4000 Hz): Bình thường
- Thấp (< 1000 Hz): Âm thanh bổm, bass

Ví dụ:
- Voice nữ: 3000 - 5000 Hz
- Voice nam: 2000 - 3500 Hz
- Piano: 2000 - 8000 Hz (full range)
- Bass: 50 - 500 Hz
```

**Cách đọc:**
- Đỉnh cao → Vùng âm sắc, tiếng cao
- Thấp → Vùng bass, tiếng bổm

---

#### 4️⃣ **Spectral Bandwidth Over Time**

```
Định nghĩa: Độ rộng phổ tần (band of frequencies)
Công thức: BW = √(Σ((f - centroid)² × magnitude[f]) / Σ(magnitude[f]))
Giá trị: 0 - 11025 Hz (nửa Nyquist)

Ý nghĩa:
- Rộng (> 3000 Hz): Nhiều tần số, chi tiết cao
- Vừa (1000-3000 Hz): Bình thường
- Hẹp (< 500 Hz): Ít tần số, đơn giản

Ví dụ:
- Nói chuyện: 500 - 2000 Hz
- Nhạc orkêstra: 5000 - 8000 Hz
- Tiếng bổm (drum bass): 50 - 300 Hz
```

**Cách đọc:**
- Bandwidth rộng → Audio có chi tiết
- Bandwidth hẹp → Audio đơn giản/focus

---

#### 5️⃣ **Spectral Flatness Over Time**

```
Định nghĩa: Độ bằng phẳng phổ (Wiener entropy)
Công thức: Flatness = exp(mean(log(mag))) / mean(mag)
Giá trị: 0.0 - 1.0

Ý nghĩa:
- Gần 1.0: Phổ bằng phẳng = NOISE (Nhiễu)
- Gần 0.0: Phổ gập khúc = SIGNAL (Tín hiệu)

Ví dụ:
- Tiếng trắng (white noise): 0.8 - 0.95
- Voice: 0.1 - 0.3
- Music: 0.2 - 0.4
- Yên tĩnh: 0.5 - 0.7
```

**Cách đọc:**
- Cao (> 0.7) → Nhiều noise, ít tín hiệu
- Thấp (< 0.3) → Ít noise, tín hiệu rõ

---

### Cách Sử Dụng Tab 1

**Bước 1: Tải audio**
- Upload file hoặc ghi âm

**Bước 2: Chờ biểu đồ hiển thị**
- 5 chart sẽ xuất hiện

**Bước 3: Phân tích**
```
Ví dụ: Âm thanh nói chuyện
┌─────────────────────────────────────┐
│ RMS: ~0.4 (to bình thường)          │
│ ZCR: ~0.5 (cao - phù hợp voice)    │
│ Centroid: ~3000 Hz (voice voice)    │
│ Bandwidth: ~1500 Hz (voice)         │
│ Flatness: ~0.25 (tín hiệu rõ)      │
│ ↓                                   │
│ KẾT LUẬN: Speech, chất lượng tốt   │
└─────────────────────────────────────┘
```

**Bước 4: So sánh các vùng**
- Đầu / Giữa / Cuối khác nhau?
- Có đỉnh (spike) đột ngột?
- Có yên tĩnh (silence)?

---

## 🌐 TAB 2: Network Analysis (Phân Tích Mạng)

### Cấu Trúc

```
┌────────────────────────────────────────────────────┐
│ 🌐 NETWORK ANALYSIS                                │
├────────────────────────────────────────────────────┤
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Network Bandwidth Over Time (Selected Pattern)│ │
│ │ Pattern: [Network Pattern từ Sidebar]        │  │
│ │                                               │  │
│ │ Trục X: Chunk ID (0, 1, 2, ...)             │  │
│ │ Trục Y: Bandwidth (kbps)                     │  │
│ │ Đường: Mạn xanh (dự báo/mô phỏng)           │  │
│ │ Dạng: Line chart (hoặc area chart)          │  │
│ │                                               │  │
│ │ Di chuột: Hiển thị giá trị exact             │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Network Statistics                           │  │
│ │ ┌────────────────────────────────────────┐  │  │
│ │ │ Pattern Type: [Selected Pattern]       │  │  │
│ │ │ Average Bandwidth: X.X kbps            │  │  │
│ │ │ Min Bandwidth: X.X kbps                │  │  │
│ │ │ Max Bandwidth: X.X kbps                │  │  │
│ │ │ Std Deviation: X.X kbps                │  │  │
│ │ │ Chunks Processed: N                    │  │  │
│ │ └────────────────────────────────────────┘  │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Network Statistics Chi Tiết

```
📊 STATISTICS

Pattern Type
├─ 7 options: Stable, Decreasing, Sinusoidal, ...
└─ Hiển thị pattern được chọn ở sidebar

Average Bandwidth
├─ Trung bình bandwidth của toàn bộ audio
├─ Công thức: Σ(bandwidth[i]) / N
├─ Ý nghĩa: Bandwidth chủ yếu
└─ Ví dụ: Avg 64 kbps = mạng trung bình

Min Bandwidth
├─ Bandwidth thấp nhất gặp phải
├─ Ý nghĩa: Trường hợp tệ nhất
└─ Ví dụ: Min 10 kbps = mạng có thể xuống 10

Max Bandwidth
├─ Bandwidth cao nhất có
├─ Ý nghĩa: Trường hợp tốt nhất
└─ Ví dụ: Max 256 kbps = mạng có thể lên 256

Std Deviation (Độ Lệch Chuẩn)
├─ Biểu thị tính ổn định của mạng
├─ Công thức: √(Σ(x - mean)² / N)
├─ Thấp: Mạng ổn định
│  Ví dụ: StdDev 5 kbps = rất ổn định
├─ Cao: Mạng dao động
│  Ví dụ: StdDev 50 kbps = rất dao động
└─ Ý nghĩa:
  - StdDev < 10: Ổn định (Stable)
  - StdDev 10-30: Bình thường
  - StdDev > 50: Không ổn định

Chunks Processed
├─ Số "khúc" audio được xử lý
├─ Công thức: Duration / Chunk Duration
├─ Ví dụ: 30s audio / 1s chunk = 30 chunks
└─ Ý nghĩa: Độ phân giải phân tích
```

### Cách Đọc Biểu Đồ Bandwidth

```
Stable Pattern
├─ Đường thẳng ngang ở 256
└─ StdDev ≈ 0 (hoàn toàn ổn định)

Decreasing Pattern
├─ Đường giảm dần từ 256 → 10
└─ StdDev thấp (giảm đều)

Sinusoidal Pattern
├─ Đường dao động giữa 24 - 104
└─ StdDev vừa phải (dao động có nhịp)

Recovery Pattern
├─ Giảm mạnh 64→10, rồi phục hồi 10→64
└─ StdDev cao (có biến đổi lớn)

Random Pattern
├─ Đường lên xuống ngẫu nhiên quanh 64
└─ StdDev cao (bất quy tắc)
```

---

## 🎯 TAB 3: Adaptive Bitrate (Chọn Bitrate)

### Cấu Trúc

```
┌────────────────────────────────────────────────────┐
│ 🎯 ADAPTIVE BITRATE                                │
├────────────────────────────────────────────────────┤
│                                                    │
│ [Content Type & Complexity Info]                   │
│ ┌──────────────────────────────────────────────┐  │
│ │ Content Type: SPEECH / MUSIC / MIXED / ...   │  │
│ │ Avg Complexity: 0.XX (Low / Medium / High)   │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Bitrate Selection Over Time                  │  │
│ │                                               │  │
│ │ Trục X: Chunk ID                             │  │
│ │ Trục Y: Bitrate (kbps)                       │  │
│ │ Đường: Bitrate được chọn (đỏ hoặc xanh)     │  │
│ │ Giải thích: Thích ứng với network/content   │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Selection Reasons Table (Top 20 rows)        │  │
│ │                                               │  │
│ │ Chunk ID │ Bandwidth │ Content │ Complexity │  │
│ ├──────────┼───────────┼─────────┼────────────┤  │
│ │ 0        │ 256       │ SPEECH  │ 0.45 (M)   │  │
│ │ 1        │ 245       │ SPEECH  │ 0.42 (M)   │  │
│ │ 2        │ 220       │ MUSIC   │ 0.58 (M)   │  │
│ │ ...      │ ...       │ ...     │ ...        │  │
│ │                                               │  │
│ │ Bitrate │ Reason                              │  │
│ ├─────────┼──────────────────────────────────┤  │
│ │ 16 kbps │ Speech + medium = 16 kbps       │  │
│ │ 16 kbps │ Bandwidth 245 allows <= 220     │  │
│ │ 64 kbps │ Music detected, up to 64        │  │
│ │ 64 kbps │ Buffer good, maintain           │  │
│ │ 32 kbps │ Bandwidth tight, down to 32     │  │
│ │ ...     │ ...                              │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Content Type Detection

```
Cách hệ thống phân loại:

Input: Audio Features (RMS, ZCR, Spectral, etc.)
       ↓
Quy tắc:
├─ RMS < 0.01 → SILENCE (Yên tĩnh)
├─ ZCR cao (> 0.4) + RMS trung bình → SPEECH (Nói)
├─ ZCR thấp (< 0.2) + RMS cao → MUSIC (Nhạc)
└─ Khác → MIXED (Hỗn hợp)

Output: Content Type
         ↓
Kết quả: Hiển thị ở đầu tab
Ví dụ: "Content Type: SPEECH"
       "Avg Complexity: 0.45 (Medium)"
```

### Complexity Classification

```
Tính toán:
Complexity = (RMS × 0.3) + (ZCR × 0.2) 
           + (Spectral_Flatness × 0.2) 
           + (Bandwidth_ratio × 0.3)

Phân loại:
├─ 0.0 - 0.33: LOW (Đơn giản)
│  └─ Ví dụ: Tiếng bổm, silence, voice đơn
├─ 0.33 - 0.67: MEDIUM (Trung bình)
│  └─ Ví dụ: Voice bình thường, nhạc bình thường
└─ 0.67 - 1.0: HIGH (Phức tạp)
   └─ Ví dụ: Voice với nhiều biến đổi, nhạc orkêstra

Hiển thị: "Avg Complexity: 0.XX (Low/Medium/High)"
```

### Bitrate Selection Process

```
Quy trình chi tiết:

1. Xác định Content Type
   └─ SPEECH / MUSIC / MIXED / SILENCE

2. Tính Complexity Level
   └─ LOW / MEDIUM / HIGH

3. Tra bảng Bitrate Requirements
   ├─ SPEECH + LOW → 8 kbps
   ├─ SPEECH + MEDIUM → 16 kbps
   ├─ SPEECH + HIGH → 32 kbps
   ├─ MUSIC + LOW → 32 kbps
   ├─ MUSIC + MEDIUM → 96 kbps
   ├─ MUSIC + HIGH → 192 kbps
   ├─ MIXED + LOW → 16 kbps
   ├─ MIXED + MEDIUM → 64 kbps
   ├─ MIXED + HIGH → 128 kbps
   └─ SILENCE → 8 kbps

4. Điều chỉnh Buffer
   ├─ Buffer < 500 ms → ×0.7 (giảm)
   ├─ Buffer 500-5000 → ×1.0 (giữ)
   └─ Buffer > 5000 → ×1.2 (tăng)

5. Áp Aggressive Compression (nếu bật)
   └─ Bitrate ×0.8 (giảm 20%)

6. Giới hạn Bandwidth
   └─ Bitrate = min(bitrate, available_bandwidth × 0.9)

7. Làm mượt (Smoothing)
   └─ Final = 0.7×previous + 0.3×new

8. Snap to Available Levels
   └─ [5, 8, 16, 32, 64, 96, 128, 192, 256]

Output: Bitrate cuối cùng
```

### Selection Reasons Table

```
Cột: Chunk ID
├─ 0, 1, 2, 3, ... (STT khúc)
└─ Dùng để track thay đổi

Cột: Bandwidth
├─ Available bandwidth cho chunk này (kbps)
└─ Từ Network Pattern

Cột: Content
├─ SPEECH / MUSIC / MIXED / SILENCE
└─ Phát hiện từ audio features

Cột: Complexity
├─ Giá trị 0.0 - 1.0 + nhãn (Low/Med/High)
└─ Tính từ features

Cột: Bitrate
├─ Bitrate được chọn cho chunk (kbps)
└─ Kết quả quyết định

Cột: Reason
├─ Giải thích tại sao chọn bitrate này
├─ Ví dụ:
│  "Speech + medium = 16 kbps"
│  "Bandwidth 64 allows max 58 → 64 (cap)"
│  "Buffer low, reduce to 12 kbps"
│  "Smoothing: prev 32 + new 24 → 30 kbps"
└─ Giúp hiểu quyết định
```

---

## 📈 TAB 4: Metrics (Chỉ Số Chất Lượng)

### Cấu Trúc

```
┌────────────────────────────────────────────────────┐
│ 📈 METRICS                                         │
├────────────────────────────────────────────────────┤
│                                                    │
│ [Metrics Table - Statistics tổng hợp]             │
│ ┌──────────────────────────────────────────────┐  │
│ │ AUDIO FEATURES STATISTICS                    │  │
│ │ ├─ RMS: Min, Max, Mean, Std                  │  │
│ │ ├─ ZCR: Min, Max, Mean, Std                  │  │
│ │ ├─ Spectral Centroid: Min, Max, Mean, Std   │  │
│ │ ├─ Spectral Bandwidth: Min, Max, Mean, Std  │  │
│ │ ├─ Spectral Flatness: Min, Max, Mean, Std   │  │
│ │ └─ Complexity Score: Min, Max, Mean, Std    │  │
│ │                                               │  │
│ │ BITRATE STATISTICS                           │  │
│ │ ├─ Selected Bitrate: Min, Max, Mean, Std    │  │
│ │ ├─ Bitrate Changes: N (số lần thay đổi)     │  │
│ │ ├─ Max Change: ±X kbps (thay đổi lớn nhất)  │  │
│ │ └─ Stability Ratio: X% (ổn định)            │  │
│ │                                               │  │
│ │ NETWORK STATISTICS                           │  │
│ │ ├─ Bandwidth: Min, Max, Mean, Std           │  │
│ │ ├─ Bandwidth Variability: X%                 │  │
│ │ └─ Pattern: [Pattern name]                   │  │
│ │                                               │  │
│ │ EFFICIENCY METRICS                           │  │
│ │ ├─ Avg Utilization: X% (bitrate/bandwidth)   │  │
│ │ ├─ Quality Score: X/10 (tương đối)           │  │
│ │ ├─ Adaptation Aggressiveness: X (0-1)        │  │
│ │ └─ Wasted Bandwidth: X% (dự phòng)           │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Detailed Metrics Explanation

#### **AUDIO FEATURES STATISTICS**

```
RMS Statistics
├─ Min: RMS thấp nhất (quiet parts)
├─ Max: RMS cao nhất (loudest parts)
├─ Mean: RMS trung bình
├─ Std: Độ lệch chuẩn (variability)
└─ Ý nghĩa: Tính biến đổi của volume

ZCR Statistics
├─ Min: ZCR thấp nhất (bass parts)
├─ Max: ZCR cao nhất (voice parts)
├─ Mean: ZCR trung bình
├─ Std: Độ lệch chuẩn
└─ Ý nghĩa: Tính đa dạng tần số

Spectral Centroid Statistics
├─ Min: Tần số trọng tâm thấp nhất
├─ Max: Tần số trọng tâm cao nhất
├─ Mean: Trung bình
├─ Std: Độ lệch chuẩn
└─ Ý nghĩa: Phạm vi tần số

Spectral Bandwidth / Flatness: Tương tự

Complexity Score Statistics
├─ Min: Độ phức tạp thấp nhất
├─ Max: Độ phức tạp cao nhất
├─ Mean: Độ phức tạp trung bình
├─ Std: Biến đổi độ phức tạp
└─ Ý nghĩa: Nội dung tổng thể phức tạp?
```

#### **BITRATE STATISTICS**

```
Selected Bitrate
├─ Min: Bitrate thấp nhất được chọn
│  Ví dụ: 8 kbps (quá yếu hoặc silence)
├─ Max: Bitrate cao nhất được chọn
│  Ví dụ: 256 kbps (khi có bandwidth)
├─ Mean: Bitrate trung bình sử dụng
│  Ý nghĩa: Bitrate "điển hình"
└─ Std: Biến đổi bitrate
   Thấp = Ổn định
   Cao = Thay đổi thường xuyên

Bitrate Changes
├─ Số lần bitrate thay đổi
├─ Ví dụ: 5 changes = thay đổi 5 lần
└─ Ý nghĩa: 
  Ít change = Ổn định (tốt)
  Nhiều change = Linh hoạt (nhưng gâyvô)

Max Change
├─ Thay đổi bitrate lớn nhất
├─ Ví dụ: ±40 kbps = từ 32 nhảy 72 hoặc vice versa
└─ Ý nghĩa: Độ cộng hưởng của thuật toán

Stability Ratio
├─ % thời gian bitrate không thay đổi
├─ Công thức: (chunks unchanged / total chunks) × 100%
├─ Ví dụ: 80% = 80% thời gian bitrate ổn định
└─ Ý nghĩa:
  Cao (> 80%) = Rất ổn định (tốt)
  Thấp (< 50%) = Thường xuyên thay (có vấn đề)
```

#### **NETWORK STATISTICS**

```
Bandwidth Statistics
├─ Min: Bandwidth thấp nhất
├─ Max: Bandwidth cao nhất
├─ Mean: Bandwidth trung bình
├─ Std: Biến đổi
└─ Ý nghĩa: Chất lượng mạng

Bandwidth Variability
├─ Công thức: (Max - Min) / Mean × 100%
├─ Ví dụ: 100% = Max = 2 × Min
└─ Ý nghĩa:
  Thấp (< 20%) = Mạng ổn định
  Cao (> 80%) = Mạng biến đổi nhiều

Pattern: Tên pattern đã chọn
```

#### **EFFICIENCY METRICS**

```
Avg Utilization
├─ Công thức: (Avg Bitrate / Avg Bandwidth) × 100%
├─ Ví dụ: 75% = sử dụng 75% bandwidth hiện có
└─ Ý nghĩa:
  50-70% = Tối ưu (dự phòng hợp lý)
  > 90% = Rủi ro (sẽ quá tải nếu mạng tệ)
  < 50% = Lãng phí (không tận dụng)

Quality Score
├─ Công thức: (Avg Bitrate / Max Bitrate) × 10
├─ Ví dụ: 64/256 × 10 = 2.5/10
└─ Ý nghĩa: Mức độ cảm nhận chất lượng
  8-10: Tuyệt vời
  5-7: Tốt
  3-5: Chấp nhận được
  1-3: Kém

Adaptation Aggressiveness
├─ Công thức: (Bitrate Changes / Total Chunks)
├─ Ví dụ: 5 changes / 50 chunks = 0.1
└─ Ý nghĩa: Mức độ "hung hăng" của thuật toán
  0.0-0.1: Ổn định (ít thay đổi)
  0.1-0.3: Bình thường (thích ứng hợp lý)
  > 0.3: Hung hăng (thay đổi quá thường)

Wasted Bandwidth
├─ Công thức: 100% - Avg Utilization
├─ Ví dụ: 100% - 75% = 25% (dành dự phòng)
└─ Ý nghĩa: 
  10-30% = Tốt (dự phòng hợp lý)
  > 50% = Lãng phí (quá bảo thủ)
```

---

## 💾 TAB 5: Summary (Tóm Tắt)

### Cấu Trúc

```
┌────────────────────────────────────────────────────┐
│ 💾 SUMMARY                                         │
├────────────────────────────────────────────────────┤
│                                                    │
│ 📊 AUDIO SUMMARY                                   │
│ ├─ Duration: X seconds                            │
│ ├─ Sample Rate: X Hz                              │
│ ├─ Channels: Mono / Stereo                        │
│ ├─ Content Type: SPEECH / MUSIC / MIXED           │
│ ├─ Avg Complexity: X.XX (Low/Med/High)            │
│ ├─ Loudness: X dB                                 │
│ └─ Quality Assessment: Good / Fair / Poor         │
│                                                    │
│ 🌐 NETWORK SUMMARY                                 │
│ ├─ Pattern: [Selected]                            │
│ ├─ Avg Bandwidth: X kbps                          │
│ ├─ Min/Max Bandwidth: X - Y kbps                  │
│ ├─ Variability: X%                                │
│ ├─ Stability: Good / Fair / Poor                  │
│ └─ Network Type: Excellent / Good / Fair / Poor   │
│                                                    │
│ 🎯 ADAPTIVE BITRATE SUMMARY                        │
│ ├─ Avg Bitrate Selected: X kbps                   │
│ ├─ Bitrate Range: X - Y kbps                      │
│ ├─ Number of Bitrate Changes: N                   │
│ ├─ Stability Ratio: X%                            │
│ ├─ Adaptation Quality: X/10                       │
│ └─ Algorithm Performance: Excellent / Good / Fair │
│                                                    │
│ 💡 RECOMMENDATIONS                                 │
│ ├─ Optimal Bitrate: Use X kbps for stable play   │
│ ├─ Network Type Suited: [Description]             │
│ ├─ Best For: [Use case]                           │
│ ├─ Improvement Areas: [Suggestion]                │
│ └─ Next Steps:                                     │
│    - Try [Pattern] for [Reason]                  │
│    - Adjust [Parameter] to [Value]               │
│    - Test with [Content Type]                    │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Summary Chi Tiết

**AUDIO SUMMARY**
- **Duration**: Tổng thời gian audio (giây)
- **Sample Rate**: 16000, 44100, 48000 Hz (tần số lấy mẫu)
- **Channels**: Mono (1 kênh) hoặc Stereo (2 kênh)
- **Content Type**: Phát hiện nội dung
- **Avg Complexity**: Độ phức tạp trung bình
- **Loudness**: Âm lượng theo chuẩn LUFS
- **Quality Assessment**: Đánh giá tổng thể

**NETWORK SUMMARY**
- **Pattern**: Network pattern được chọn
- **Avg Bandwidth**: Bandwidth trung bình
- **Min/Max**: Phạm vi bandwidth
- **Variability**: % biến đổi
- **Stability**: Ổn định đến mức nào
- **Network Type**: Phân loại chung

**ADAPTIVE BITRATE SUMMARY**
- **Avg Bitrate**: Bitrate trung bình sử dụng
- **Bitrate Range**: Từ thấp nhất đến cao nhất
- **Bitrate Changes**: Bao nhiêu lần thay đổi
- **Stability Ratio**: % ổn định
- **Adaptation Quality**: Điểm đánh giá (0-10)
- **Algorithm Performance**: Đánh giá chung

**RECOMMENDATIONS**
- **Optimal Bitrate**: Gợi ý bitrate tối ưu
- **Network Type Suited**: Loại mạng phù hợp
- **Best For**: Trường hợp sử dụng tốt nhất
- **Improvement Areas**: Có thể cải thiện gì
- **Next Steps**: Bước tiếp theo để test thêm

---

## 🎵 TAB 6: Audio Playback (Phát Âm Thanh)

### Cấu Trúc

```
┌────────────────────────────────────────────────────┐
│ 🎵 AUDIO PLAYBACK                                  │
├────────────────────────────────────────────────────┤
│                                                    │
│ [Playback Mode Selection]                          │
│ ┌──────────────────────────────────────────────┐  │
│ │ Select Playback Mode:                        │  │
│ │ ◯ Original Audio                              │  │
│ │ ◯ Simulated Quality                           │  │
│ │ ◯ Compare Audio (Multiple Bitrates)           │  │
│ │                                               │  │
│ │ (Radio buttons - chọn 1)                     │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ────────────────────────────────────────────────── │
│ [Mode-Specific Controls]                           │
│                                                    │
│ ≡ Simulated Quality Mode:                          │
│ ├─ Slider: Select Bitrate                         │
│ │  5 ←─────●───────→ 256 kbps                    │
│ │  (hoặc multiselect)                             │
│ └─ Cutoff Frequency: X Hz (auto calculated)       │
│                                                    │
│ ≡ Compare Mode:                                    │
│ ├─ Multiselect: Choose 1-4 Bitrates               │
│ │  ☐ 5 kbps   ☐ 32 kbps   ☐ 128 kbps             │
│ │  ☐ 8 kbps   ☐ 64 kbps   ☐ 192 kbps             │
│ │  ☐ 16 kbps  ☐ 96 kbps   ☐ 256 kbps             │
│ └─ (Select up to 4)                              │
│                                                    │
│ ────────────────────────────────────────────────── │
│ [Audio Playback Control]                           │
│ ├─ ▶️ Play Audio (Button)                         │
│ ├─ Status: Ready / Processing / Playing           │
│ └─ HTML5 Audio Widget (nếu cần)                   │
│                                                    │
│ ────────────────────────────────────────────────── │
│ [Listening Notes / Observations]                   │
│ ├─ Info box giải thích mỗi mode                  │
│ ├─ Tips: Nghe cái gì? Focus mấy cái?             │
│ └─ Ví dụ: "Notice the loss of high frequencies" │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 3 Playback Modes Chi Tiết

#### 1️⃣ **Original Audio (Gốc - 256 kbps)**

```
Chức năng: Phát âm thanh gốc 100% không nén
Bitrate: 256 kbps (lossless)
Cutoff Frequency: 22050 Hz (full spectrum)

Cách sử dụng:
1. Chọn radio button: "Original Audio"
2. Click: ▶️ "Play Audio"
3. Nghe: Âm thanh sạch, đầy đủ chi tiết

Ý nghĩa:
- Baseline để so sánh
- Tham chiếu chất lượng tốt nhất
- Nghe khác biệt so với simulated

Ví dụ nghe:
├─ Voice: Rõ ràng, không méo
├─ Nhạc: Chi tiết đầy đủ, treble rõ
└─ Background: Tất cả âm thanh có mặt
```

#### 2️⃣ **Simulated Quality (Mô Phỏng)**

```
Chức năng: Phát audio ở bitrate cụ thể
Bitrate: Có thể chọn 5-256 kbps
Cutoff Frequency: Tự động điều chỉnh

Bảng Bitrate → Cutoff:
├─ 5 kbps → 800 Hz
├─ 8 kbps → 2000 Hz
├─ 16 kbps → 3500 Hz
├─ 32 kbps → 5500 Hz
├─ 64 kbps → 8000 Hz
├─ 96 kbps → 11000 Hz
├─ 128 kbps → 14000 Hz
├─ 192 kbps → 18000 Hz
└─ 256 kbps → 22050 Hz (full)

Cách sử dụng:
1. Chọn: "Simulated Quality"
2. Điều chỉnh slider / input: Bitrate
3. Xem: Cutoff frequency auto update
4. Click: ▶️ "Play Audio"
5. Nghe: Audio ở bitrate đó

Thử từng bitrate:
├─ 5 kbps: Gần như comfort noise
├─ 16 kbps: Voice nghe được, nhạc mất
├─ 64 kbps: Cân bằng tốt
├─ 128 kbps: Rất tốt
└─ 256 kbps: Lossless

Ý nghĩa:
- Nghe ảnh hưởng thực tế của bitrate
- Nhận ra giới hạn của ultra-low bandwidth
- Đánh giá trade-off chất lượng ↔ bandwidth
```

#### 3️⃣ **Compare Audio (So Sánh)**

```
Chức năng: Phát nhiều bitrate lần lượt để so sánh
Bitrates: Chọn 1-4 cùng lúc
Phát: Tuần tự (từng cái một)

Cách sử dụng:
1. Chọn: "Compare Audio (Multiple Bitrates)"
2. Tick vào: 4 bitrates muốn so sánh
   Ví dụ: [✓ 16 kbps] [✓ 32 kbps] [✓ 64 kbps] [✓ 128 kbps]
3. Click: ▶️ "Play Audio"
4. Ứng dụng phát tuần tự:
   Phát 16 kbps (5 giây)
   → Dừng 1 giây
   → Phát 32 kbps (5 giây)
   → Dừng 1 giây
   → Phát 64 kbps (5 giây)
   → Dừng 1 giây
   → Phát 128 kbps (5 giây)
5. Nghe và so sánh sự khác biệt

Ý nghĩa:
- Trực tiếp nghe sự khác biệt
- Nhận thức rõ về chất lượng tại từng bitrate
- Hiểu sweet spot (bitrate tốt nhất)

Gợi ý so sánh:
- Ghé tai: Detect sự mất của treble
- Focus: Đầu tiên thay đổi gì?
- Threshold: Bitrate thấp nhất có chấp nhận được?

Ví dụ so sánh:
16 kbps: Voice rõ, nhạc... không
32 kbps: Voice rõ, nhạc bắt đầu nghe
64 kbps: Tất cả nghe được tốt
128 kbps: Rất tốt, gần original
256 kbps: Identical to original
```

### Listening Tips (Mẹo Nghe)

```
🎧 Chuẩn Bị:
├─ Dùng tai nghe/loa chất lượng tốt
├─ Âm thanh yên tĩnh xung quanh
├─ Volume vừa phải (không quá to/nhỏ)
└─ Tai tươi (nghe lần đầu khi tỉnh)

👂 Khi Nghe Original:
├─ Để ý đặc điểm cơ bản:
│  ├─ Tần số cao (sắc)
│  ├─ Tần số thấp (bass)
│  ├─ Voice clarity
│  └─ Background details
└─ Tạo baseline tâm lý

🎯 Khi Nghe Simulated:
├─ So với Original:
│  ├─ Mất chi tiết gì?
│  ├─ Voice vẫn rõ không?
│  ├─ Bass bị giảm?
│  └─ Có méo (artifact)?
└─ Xác định "chấp nhận được"

⚖️ Khi Compare:
├─ Nghe từng cái một
├─ Focus: Cái khác nhất là gì?
├─ Hỏi: Bitrate này đủ để...?
│  ├─ Voice call? (thường 16-32 kbps)
│  ├─ Music streaming? (64-128 kbps)
│  └─ Podcast/audiobook? (32-64 kbps)
└─ Ghi nhớ threshold cá nhân

💡 Insight Bạn Sẽ Có:
- Trực giác về bitrate impact
- Hiểu tại sao adaptive bitrate cần thiết
- Đánh giá mạng: "mạng này phù hợp gì?"
- Quyết định: "project của tôi cần bitrate nào?"
```

---

## 📊 Tóm Tắt Tab

| Tab | Hiển Thị | Mục Đích |
|-----|---------|---------|
| **1: Audio Features** | 5 biểu đồ đặc trưng | Hiểu audio properties |
| **2: Network Analysis** | Bandwidth pattern | Kiểm tra mạng |
| **3: Adaptive Bitrate** | Bitrate decision & reason | Thấy thuật toán hoạt động |
| **4: Metrics** | Statistics tổng hợp | Đánh giá performance |
| **5: Summary** | Tóm tắt + Recommendations | Tìm insight nhanh |
| **6: Audio Playback** | Phát âm thanh 3 mode | Nghe chất lượng thực tế |

---

**Xem WEB_USAGE_GUIDE.md để hướng dẫn sử dụng chi tiết!**

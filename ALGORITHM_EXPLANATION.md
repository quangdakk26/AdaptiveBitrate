# Thuật Toán Adaptive Bitrate (Giải Thích Chi Tiết)

## 📌 Tổng Quan

Hệ thống **Adaptive Bitrate** tự động điều chỉnh chất lượng âm thanh dựa trên:
1. **Đặc trưng nội dung âm thanh** (audio features)
2. **Điều kiện mạng hiện tại** (network bandwidth)
3. **Loại nội dung** (speech, music, mixed)
4. **Độ phức tạp** (complexity)

---

## 🎯 Quy Trình Chọn Bitrate

### Bước 1: Phân Tích Đặc Trưng Âm Thanh

Hệ thống trích xuất các đặc trưng từ audio:

| Đặc trưng | Ý nghĩa | Giá trị |
|-----------|---------|--------|
| **RMS** | Năng lượng trung bình | 0.0 - 1.0 |
| **ZCR** | Tần số qua không | 0.0 - 1.0 |
| **Spectral Centroid** | Tần số trọng tâm | Hz |
| **Spectral Bandwidth** | Độ rộng phổ | Hz |
| **Spectral Flatness** | Độ bằng phẳng phổ | 0.0 - 1.0 |
| **Complexity** | Độ phức tạp tổng hợp | 0.0 - 1.0 |

### Bước 2: Phân Loại Nội Dung

Dựa trên các đặc trưng, hệ thống phân loại:

```
┌─────────────────────────────────────┐
│ Đặc trưng Âm Thanh                  │
├─────────────────────────────────────┤
│ RMS thấp → SILENCE (Yên tĩnh)      │
│ ZCR cao → SPEECH (Nói chuyện)       │
│ Phổ rộng + RMS cao → MUSIC (Nhạc) │
│ Khác → MIXED (Hỗn hợp)             │
└─────────────────────────────────────┘
```

### Bước 3: Xác Định Độ Phức Tạp

**Công thức tính Complexity:**
```
Complexity = (RMS × 0.3) + (ZCR × 0.2) + (Spectral_Flatness × 0.2) 
           + (Bandwidth_ratio × 0.3)
```

**Phân loại:**
- **Thấp (< 0.33)**: Âm thanh đơn giản, yêu cầu bitrate thấp
- **Trung bình (0.33 - 0.67)**: Âm thanh bình thường
- **Cao (> 0.67)**: Âm thanh phức tạp, cần bitrate cao

### Bước 4: Xác Định Bitrate Cơ Sở

Theo **loại nội dung** và **độ phức tạp**:

```
Content Type: SPEECH
├── Complexity: Thấp → 8 kbps
├── Complexity: Trung bình → 16 kbps
└── Complexity: Cao → 32 kbps

Content Type: MUSIC
├── Complexity: Thấp → 32 kbps
├── Complexity: Trung bình → 96 kbps
└── Complexity: Cao → 192 kbps

Content Type: MIXED
├── Complexity: Thấp → 16 kbps
├── Complexity: Trung bình → 64 kbps
└── Complexity: Cao → 128 kbps
```

### Bước 5: Điều Chỉnh Theo Buffer Level

**Buffer quá thấp (< 500ms)** → Giảm bitrate 30%
```
adjusted_bitrate = base_bitrate × 0.7
```

**Buffer bình thường (500-5000ms)** → Giữ nguyên

**Buffer quá cao (> 5000ms)** → Tăng bitrate 20%
```
adjusted_bitrate = base_bitrate × 1.2
```

### Bước 6: Áp Dụng Giới Hạn Bandwidth

Bitrate không được vượt quá 90% bandwidth hiện tại:
```
final_bitrate = min(adjusted_bitrate, available_bandwidth × 0.9)
```

### Bước 7: Làm Mượt (Smoothing)

Tránh thay đổi đột ngột, sử dụng trung bình động:
```
smoothed_bitrate = 0.7 × previous_bitrate + 0.3 × new_bitrate
```

### Bước 8: Snap to Available Levels

Làm tròn đến các mức bitrate có sẵn: 5, 8, 16, 32, 64, 96, 128, 192, 256 kbps

---

## 🌐 Các Network Pattern (Mô Phỏng Mạng)

### 1. **Stable (256 kbps)** - Mạng lý tưởng
```
Bandwidth: Không đổi 256 kbps
Trường hợp: Mạng WiFi chất lượng cao
```

### 2. **Decreasing (256→10 kbps)** - Mạng suy giảm
```
Bandwidth: Giảm dần từ 256 đến 10 kbps
Trường hợp: Đi chuyển ra khỏi vùng sóng tốt
Kiểm tra: Thuật toán có thích ứng nhanh không?
```

### 3. **Sinusoidal (24-104 kbps)** - Mạng dao động
```
Bandwidth: Dao động quanh 64 kbps ± 40
Trường hợp: Môi trường có nhiễu điện từ
Kiểm tra: Thuật toán có ổn định không?
```

### 4. **Recovery (64→10→64 kbps)** - Mạng sụt rồi phục hồi
```
Bandwidth: 64 → 10 → 64 kbps
Trường hợp: Mất kết nối tạm thời rồi khôi phục
Kiểm che: Thuật toán có khôi phục tốc độ nhanh không?
```

### 5. **Weak (48 kbps)** - Mạng yếu
```
Bandwidth: Khoảng 48 kbps + nhiễu
Trường hợp: 4G yếu, 3G
```

### 6. **Very Weak (5-16 kbps)** - Mạng rất yếu
```
Bandwidth: Khoảng 10 kbps ± 2
Trường hợp: Mạng 2G, vùng sóng rất kém
Lưu ý: Chỉ có thể dùng voice-only, comfort noise
```

### 7. **Random Spikes & Drops** - Mạng ngẫu nhiên
```
Bandwidth: Base 64 kbps với spikes/drops ngẫu nhiên
Trường hợp: Mạng không ổn định, có chuyển tải
```

---

## 📊 Mô Phỏng Chất Lượng Âm Thanh

Khi bitrate giảm, tần số cao được **lọc bỏ** bằng **Low-Pass Filter**:

| Bitrate | Tần số Cutoff | Mô Tả |
|---------|---------------|-------|
| 5 kbps | 800 Hz | Chỉ có voice cơ bản, comfort noise |
| 8 kbps | 2000 Hz | Voice rõ ràng nhưng thiếu treble |
| 16 kbps | 3500 Hz | Voice tốt, nhạc nền mất chi tiết |
| 32 kbps | 5500 Hz | Chất lượng tương đối, nhạc nghe được |
| 64 kbps | 8000 Hz | Khá tốt, chi tiết hợp lý |
| 96 kbps | 11000 Hz | Tốt |
| 128 kbps | 14000 Hz | Rất tốt |
| 192 kbps | 18000 Hz | Cao cấp |
| 256 kbps | 22050 Hz | Lossless (toàn bộ) |

**Công thức Low-Pass Butterworth Filter:**
```
Loại bỏ tần số > cutoff_frequency
Độ trơn: Order 4 (giữ chất lượng)
```

---

## 🎮 Quy Trình Làm Việc Toàn Bộ

```
┌─────────────────────────────────────────────────────┐
│ 1. Upload/Ghi âm thanh                               │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 2. Phân tích Audio Features                         │
│    (RMS, ZCR, Spectral, Complexity)                 │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 3. Phân loại: Speech / Music / Mixed / Silence      │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 4. Xác định Complexity: Thấp / Trung / Cao         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 5. Chọn Base Bitrate từ bảng yêu cầu               │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 6. Điều chỉnh Buffer Level & Available Bandwidth   │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 7. Làm mượt (Smoothing) - Tránh biến đổi đột ngột  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 8. Snapshot to Available Level (5,8,16,32...)      │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 9. Áp dụng Low-Pass Filter theo Bitrate            │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│ 10. Phát âm thanh mô phỏng                          │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Các Tham Số Có Thể Điều Chỉnh

```python
# Trong adaptive_bitrate.py
BITRATE_LEVELS = [5, 8, 16, 32, 64, 96, 128, 192, 256]

BITRATE_REQUIREMENTS = {
    'speech': {'low': 8, 'medium': 16, 'high': 32},
    'music': {'low': 32, 'medium': 96, 'high': 192},
    'mixed': {'low': 16, 'medium': 64, 'high': 128},
    'silence': 8,
}

# Buffer thresholds
LOW_BUFFER = 500  # ms
HIGH_BUFFER = 5000  # ms

# Smoothing factor
SMOOTHING_ALPHA = 0.7  # 70% old bitrate + 30% new
```

---

## 📈 Ví Dụ Thực Tế

### Ví dụ 1: Nói chuyện (Speech) với mạng yếu

```
Input:
- Audio Features: RMS=0.3, ZCR=0.6 → Phân loại: SPEECH
- Complexity: 0.4 → Mức: MEDIUM
- Available Bandwidth: 32 kbps
- Buffer Level: 3000 ms (bình thường)

Quy trình:
1. Base bitrate for SPEECH + MEDIUM = 16 kbps
2. Buffer bình thường → adjusted = 16 kbps
3. Available bandwidth: 32 kbps × 0.9 = 28.8 kbps
4. Min(16, 28.8) = 16 kbps ✓ Đủ bandwidth
5. Smoothing: 0.7×previous + 0.3×16
6. Result: 16 kbps (phát với voice rõ ràng)
```

### Ví dụ 2: Nhạc (Music) với mạng cực yếu

```
Input:
- Audio: Nhạc + tiếng nói
- Complexity: 0.75 → Mức: HIGH
- Available Bandwidth: 10 kbps (mạng rất yếu)
- Buffer Level: 200 ms (thấp)

Quy trình:
1. Base bitrate for MIXED + HIGH = 128 kbps (quá cao!)
2. Buffer thấp → adjusted = 128 × 0.7 = 89.6 kbps
3. Available: 10 × 0.9 = 9 kbps
4. Min(89.6, 9) = 9 kbps ← Bị giới hạn!
5. Snap to level: 8 kbps
6. Result: 8 kbps (voice-only mode, detail mất)
```

---

## 💡 Lợi Ích của Thuật Toán

✅ **Tự động điều chỉnh** - Không cần cấu hình thủ công
✅ **Nhạy cảm với content** - Speech vs Music xử lý khác nhau
✅ **Ổn định** - Làm mượt để tránh "buffer thrashing"
✅ **Tiết kiệm bandwidth** - Tận dụng tối đa cơ sở hạ tầng
✅ **Trải nghiệm liền mạch** - Ít gián đoạn, chất lượng ổn định
✅ **Hỗ trợ ultra-low** - Hoạt động cả ở 5-10 kbps

---

## 🎯 Khi Nào Dùng Bitrate Nào?

| Bitrate | Trường Hợp | Chất Lượng |
|---------|-----------|-----------|
| 5-8 kbps | Voice-only, Comfort noise | ⭐ Rất kém |
| 16 kbps | Voice nghe được | ⭐⭐ Kém |
| 32 kbps | Voice tốt, Music cơ bản | ⭐⭐⭐ Trung bình |
| 64 kbps | Balanced choice | ⭐⭐⭐⭐ Tốt |
| 128 kbps | Chất lượng cao | ⭐⭐⭐⭐⭐ Rất tốt |
| 256 kbps | Lossless, không nén | ⭐⭐⭐⭐⭐⭐ Tuyệt vời |

---

**Tài liệu này giải thích cách hệ thống hoạt động. Xem WEB_CONTENT_EXPLANATION.md để hiểu từng tab hiển thị gì!**

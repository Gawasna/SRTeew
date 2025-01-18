# SRTeew

SRT Subtitle Editor with Easy Workflow - Version 1.0

## Tính năng

- Tải và xử lý file phụ đề .srt
- Tách metadata và nội dung text
- Hỗ trợ nhập bản dịch từ file .txt hoặc paste trực tiếp
- Giao diện dạng bảng hiển thị ID, timestamp và nội dung
- Phân trang và tìm kiếm nội dung
- Xuất file .srt với nội dung đã dịch

## Cài đặt

### Từ Source Code

1. Clone repository:
```bash
git clone https://github.com/Gawasna/SRTeew.git
cd SRTeew
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Chạy ứng dụng:
```bash
python main.py
```

### Từ File Thực thi

1. Tải file SRTeew.exe từ [Releases](https://github.com/Gawasna/SRTeew/releases)
2. Chạy file thực thi

## Build

Để tạo file thực thi:

```bash
python setup.py build
```

File thực thi sẽ được tạo trong thư mục `build`.

## Sử dụng

1. Tải file .srt cần xử lý
2. Xuất nội dung ra file .txt (nếu cần)
3. Chọn dòng bắt đầu bằng cách click
4. Nhập bản dịch:
   - Từ file .txt: Nhấn "Nhập bản dịch"
   - Hoặc paste trực tiếp (Ctrl+V)
5. Xuất file .srt đã dịch

## Phím tắt

- Ctrl + V: Paste nội dung dịch
- Ctrl + Mouse wheel: Zoom in/out
- Ctrl + Plus/Minus: Thay đổi cỡ chữ

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/your-username/SRTeew](https://github.com/Gawasna/SRTeew)
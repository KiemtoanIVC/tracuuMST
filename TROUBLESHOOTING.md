# Hướng dẫn khắc phục sự cố

## Sự cố khi chạy ứng dụng local

### Lỗi "ModuleNotFoundError"

**Vấn đề**: Thiếu thư viện cần thiết.

**Giải pháp**:
```bash
pip install -r requirements.txt
```

### Lỗi "FileNotFoundError"

**Vấn đề**: Không tìm thấy file hoặc thư mục.

**Giải pháp**:
1. Kiểm tra cấu trúc thư mục
2. Đảm bảo bạn đang chạy lệnh từ thư mục gốc của dự án
3. Kiểm tra đường dẫn file trong code

### Lỗi "ConnectionError" khi tra cứu

**Vấn đề**: Không thể kết nối đến API.

**Giải pháp**:
1. Kiểm tra kết nối internet
2. Kiểm tra URL API trong code
3. Kiểm tra xem API có đang hoạt động không
4. Thử lại sau vài phút

### Lỗi "ValueError: Columns must be same length as key"

**Vấn đề**: Lỗi khi tạo DataFrame.

**Giải pháp**:
1. Kiểm tra dữ liệu đầu vào
2. Đảm bảo tất cả các cột có cùng độ dài

## Sự cố khi triển khai lên Streamlit Cloud

### Lỗi "Failed to load app"

**Vấn đề**: Không thể tải ứng dụng.

**Giải pháp**:
1. Kiểm tra logs trong dashboard của ứng dụng
2. Đảm bảo đường dẫn file chính đúng (`app/main_new.py`)
3. Kiểm tra các thư viện trong `requirements.txt`

### Lỗi "ImportError"

**Vấn đề**: Thiếu thư viện hoặc phiên bản không đúng.

**Giải pháp**:
1. Cập nhật file `requirements.txt` với phiên bản chính xác
2. Đảm bảo tất cả các thư viện cần thiết đã được liệt kê

### Lỗi "FileNotFoundError" trên Streamlit Cloud

**Vấn đề**: Không tìm thấy file trên Streamlit Cloud.

**Giải pháp**:
1. Kiểm tra cấu trúc thư mục trong repository
2. Đảm bảo file đã được đẩy lên GitHub
3. Sử dụng đường dẫn tương đối đúng trong code

### Lỗi "KeyError: 'blacklist_data'"

**Vấn đề**: Không tìm thấy secret `blacklist_data`.

**Giải pháp**:
1. Thêm secret `blacklist_data` trong dashboard của ứng dụng
2. Kiểm tra code xử lý secret

## Sự cố khi tích hợp vào website

### Iframe không hiển thị

**Vấn đề**: Iframe không hiển thị trên website.

**Giải pháp**:
1. Kiểm tra URL của ứng dụng Streamlit có chính xác không
2. Đảm bảo ứng dụng Streamlit đang chạy và có thể truy cập được
3. Kiểm tra cài đặt bảo mật của trình duyệt (một số trình duyệt chặn iframe)

### Kích thước không phù hợp

**Vấn đề**: Kích thước iframe không phù hợp.

**Giải pháp**:
1. Điều chỉnh thuộc tính `width` và `height`
2. Sử dụng đơn vị tương đối như % hoặc vh/vw
3. Thêm CSS để làm cho iframe responsive

### Vấn đề về CORS

**Vấn đề**: Lỗi CORS khi tích hợp.

**Giải pháp**:
1. Thêm tham số `?embed=true` vào URL
2. Đảm bảo website của bạn sử dụng HTTPS nếu ứng dụng Streamlit cũng sử dụng HTTPS

## Sự cố với dữ liệu

### Lỗi khi đọc file Excel

**Vấn đề**: Không thể đọc file Excel đã upload.

**Giải pháp**:
1. Kiểm tra định dạng file Excel (phải là .xlsx)
2. Đảm bảo file Excel có cột MST
3. Thử tải lại file mẫu và điền lại

### MST không hiển thị đúng

**Vấn đề**: MST bị mất số 0 ở đầu.

**Giải pháp**:
1. Định dạng cột MST là Text trong Excel
2. Kiểm tra code xử lý MST đã sử dụng `zfill(10)` chưa

### Không tìm thấy thông tin doanh nghiệp

**Vấn đề**: API không trả về thông tin doanh nghiệp.

**Giải pháp**:
1. Kiểm tra MST đã nhập đúng chưa
2. Thử tra cứu MST khác
3. Kiểm tra API có đang hoạt động không

## Liên hệ hỗ trợ

Nếu bạn gặp vấn đề không được đề cập trong tài liệu này, vui lòng liên hệ với quản trị viên để được hỗ trợ.

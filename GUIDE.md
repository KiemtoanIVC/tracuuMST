# Hướng dẫn tổng hợp Hệ thống Tra cứu Doanh nghiệp

## Mục lục

1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt và chạy ứng dụng](#cài-đặt-và-chạy-ứng-dụng)
3. [Triển khai lên Streamlit Cloud](#triển-khai-lên-streamlit-cloud)
4. [Tích hợp vào website](#tích-hợp-vào-website)
5. [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
6. [Tùy chỉnh giao diện](#tùy-chỉnh-giao-diện)
7. [Xử lý sự cố](#xử-lý-sự-cố)
8. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## Giới thiệu

Hệ thống Tra cứu Doanh nghiệp là ứng dụng web được xây dựng bằng Streamlit, cho phép tra cứu thông tin doanh nghiệp theo mã số thuế (MST). Ứng dụng hỗ trợ tra cứu đơn lẻ hoặc hàng loạt, đồng thời kiểm tra trạng thái hoạt động và cảnh báo rủi ro.

### Tính năng chính

- Tra cứu thông tin doanh nghiệp theo MST
- Tra cứu hàng loạt từ file Excel
- Kiểm tra trạng thái hoạt động
- Cảnh báo doanh nghiệp trong danh sách rủi ro
- Xuất báo cáo Excel
- Giao diện hiện đại, thân thiện với người dùng

## Cài đặt và chạy ứng dụng

### Yêu cầu

- Python 3.8+
- Các thư viện trong file requirements.txt

### Cài đặt Local

1. Clone repository này về máy
2. Tạo môi trường ảo:
```
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Cài đặt các thư viện cần thiết:
```
pip install -r requirements.txt
```

4. Chạy ứng dụng:
```
streamlit run app/main_new.py
```

## Triển khai lên Streamlit Cloud

### Bước 1: Chuẩn bị repository GitHub

1. Đảm bảo bạn đã đẩy code lên GitHub repository của bạn
2. Kiểm tra cấu trúc thư mục như sau:
   ```
   tracuuMST/
   ├── app/
   │   ├── main_new.py        # File chính của ứng dụng
   │   ├── database.py        # Module xử lý dữ liệu
   │   └── style.css          # CSS tùy chỉnh
   ├── data/
   │   └── blacklist.csv      # Dữ liệu danh sách rủi ro
   ├── .streamlit/
   │   └── config.toml        # Cấu hình Streamlit
   ├── requirements.txt       # Các thư viện cần thiết
   └── README.md              # Tài liệu hướng dẫn
   ```

### Bước 2: Đăng ký tài khoản Streamlit Cloud

1. Truy cập [Streamlit Cloud](https://streamlit.io/cloud)
2. Nhấn vào "Sign up" và đăng ký tài khoản bằng GitHub
3. Xác nhận email của bạn nếu được yêu cầu

### Bước 3: Triển khai ứng dụng

1. Đăng nhập vào [Streamlit Cloud](https://streamlit.io/cloud)
2. Nhấn vào nút "New app" ở góc trên bên phải
3. Chọn repository GitHub của bạn từ danh sách
4. Cấu hình ứng dụng:
   - **Repository**: Chọn repository của bạn (ví dụ: `username/tracuuMST`)
   - **Branch**: `main` (hoặc branch bạn muốn triển khai)
   - **Main file path**: `app/main_new.py`
   - **App URL**: Chọn URL bạn muốn (ví dụ: `tracuu-doanh-nghiep`)
5. Nhấn "Deploy!"

### Bước 4: Cấu hình Secrets (nếu cần)

Nếu bạn sử dụng danh sách rủi ro, bạn cần cấu hình secrets:

1. Trong dashboard của ứng dụng, chọn "Settings" > "Secrets"
2. Thêm secret với key là `blacklist_data` và value là nội dung của file CSV danh sách rủi ro
3. Định dạng của value phải là nội dung text của file CSV, ví dụ:
   ```
   STT,Ma so thue,Ten cong ty,Ngay cuoi,Note
   1,0123456789,Công ty A,2023-01-01,Cảnh báo về công ty này
   2,9876543210,Công ty B,2023-02-01,Công ty có dấu hiệu rủi ro
   ```
4. Nhấn "Save"

## Tích hợp vào website

### Phương pháp 1: Nhúng bằng iframe

Đây là cách đơn giản nhất để tích hợp ứng dụng Streamlit vào website của bạn.

#### Bước 1: Lấy URL của ứng dụng

Sau khi triển khai ứng dụng lên Streamlit Cloud, bạn sẽ có URL dạng:
```
https://username-appname.streamlit.app
```

#### Bước 2: Thêm iframe vào website

Thêm đoạn code HTML sau vào trang web của bạn:

```html
<iframe 
  src="https://username-appname.streamlit.app/?embed=true" 
  width="100%" 
  height="800px" 
  style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
  allow="camera;microphone"
></iframe>
```

Tùy chỉnh iframe:

- **width**: Điều chỉnh chiều rộng (ví dụ: "100%", "800px")
- **height**: Điều chỉnh chiều cao (ví dụ: "800px", "90vh")
- **style**: Tùy chỉnh CSS (viền, bóng đổ, bo góc, v.v.)
- **?embed=true**: Tham số này giúp ẩn thanh bên của Streamlit

## Hướng dẫn sử dụng

### 1. Tra cứu đơn lẻ

Để tra cứu thông tin một doanh nghiệp:

1. Chọn tab "Tra cứu đơn lẻ"
2. Nhập mã số thuế vào ô nhập liệu
3. Nhấn nút "Tra cứu"
4. Kết quả sẽ hiển thị bên dưới, bao gồm:
   - Tên doanh nghiệp
   - Trạng thái hoạt động
   - Địa chỉ
   - Cơ quan thuế quản lý
   - Loại hình doanh nghiệp
   - Cảnh báo rủi ro (nếu có)

### 2. Tra cứu hàng loạt

Để tra cứu nhiều doanh nghiệp cùng lúc:

1. Chọn tab "Tra cứu hàng loạt"
2. Tải file mẫu Excel bằng cách nhấn nút "Download file mẫu Excel"
3. Mở file Excel và điền danh sách MST cần tra cứu vào cột MST
   - **Lưu ý**: Đảm bảo cột MST được định dạng kiểu Text để giữ số 0 ở đầu
4. Lưu file Excel
5. Upload file đã điền bằng cách nhấn "Browse files" và chọn file Excel
6. Nhấn nút "Tra cứu tất cả"
7. Hệ thống sẽ tra cứu từng MST và hiển thị:
   - Thống kê theo trạng thái
   - Thống kê theo danh sách rủi ro
   - Kết quả chi tiết cho từng doanh nghiệp
8. Bạn có thể tải kết quả về dạng Excel bằng cách nhấn nút "Download kết quả (Excel)"

### Giải thích các trạng thái

- **Đang hoạt động** (✅): Doanh nghiệp đang hoạt động bình thường
- **Tạm ngừng hoạt động** (⚠️): Doanh nghiệp đã tạm ngừng hoạt động, kinh doanh
- **Ngừng hoạt động** (❌): Doanh nghiệp đã ngừng hoạt động hoặc không hoạt động tại địa chỉ đã đăng ký
- **Đã chuyển CQT** (ℹ️): Doanh nghiệp đã chuyển cơ quan thuế quản lý

## Tùy chỉnh giao diện

### Thay đổi logo

Để thay đổi logo của ứng dụng, bạn cần chỉnh sửa file `app/main_new.py`:

1. Tìm dòng sau trong file:
   ```python
   st.image("https://img.icons8.com/color/96/000000/company.png", width=80)
   ```

2. Thay đổi URL thành URL của logo mới:
   ```python
   st.image("https://example.com/your-logo.png", width=80)
   ```

### Thay đổi màu sắc và phong cách

Bạn có thể tùy chỉnh giao diện bằng cách chỉnh sửa file `app/style.css` hoặc file `.streamlit/config.toml`.

Ví dụ cấu hình trong `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1E3A8A" # Màu chủ đạo
backgroundColor = "#F8FAFC" # Màu nền
secondaryBackgroundColor = "#FFFFFF" # Màu nền thứ cấp
textColor = "#1E293B" # Màu chữ
font = "sans serif" # Font chữ
```

## Xử lý sự cố

### Vấn đề khi chạy ứng dụng local

- **Lỗi thư viện**: Đảm bảo đã cài đặt đầy đủ các thư viện trong requirements.txt
- **Lỗi file không tìm thấy**: Kiểm tra đường dẫn file và cấu trúc thư mục
- **Lỗi khi tra cứu**: Kiểm tra kết nối internet và URL API

### Vấn đề khi triển khai lên Streamlit Cloud

- **Lỗi triển khai**: Kiểm tra logs trong dashboard của ứng dụng
- **Lỗi thư viện**: Đảm bảo tất cả các thư viện cần thiết đã được liệt kê trong `requirements.txt`
- **Lỗi file không tìm thấy**: Kiểm tra đường dẫn file chính đã chính xác

### Vấn đề khi tích hợp vào website

- **Iframe không hiển thị**: Kiểm tra URL của ứng dụng Streamlit có chính xác không
- **Kích thước không phù hợp**: Điều chỉnh thuộc tính `width` và `height`
- **Vấn đề về CORS**: Đảm bảo tham số `?embed=true` đã được thêm vào URL

## Tài liệu tham khảo

- [Tài liệu Streamlit](https://docs.streamlit.io/)
- [Tài liệu Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)
- [Cách nhúng ứng dụng Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/embed-your-app)

---

Để biết thêm chi tiết, vui lòng tham khảo các tài liệu sau:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Hướng dẫn chi tiết triển khai
- [INTEGRATION.md](INTEGRATION.md) - Hướng dẫn chi tiết tích hợp
- [USER_GUIDE.md](USER_GUIDE.md) - Hướng dẫn sử dụng chi tiết
- [CUSTOMIZATION.md](CUSTOMIZATION.md) - Hướng dẫn tùy chỉnh giao diện

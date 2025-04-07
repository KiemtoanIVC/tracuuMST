# Hướng dẫn triển khai lên Streamlit Cloud

## Bước 1: Chuẩn bị repository GitHub

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

## Bước 2: Đăng ký tài khoản Streamlit Cloud

1. Truy cập [Streamlit Cloud](https://streamlit.io/cloud)
2. Nhấn vào "Sign up" và đăng ký tài khoản bằng GitHub
3. Xác nhận email của bạn nếu được yêu cầu

## Bước 3: Triển khai ứng dụng

1. Đăng nhập vào [Streamlit Cloud](https://streamlit.io/cloud)
2. Nhấn vào nút "New app" ở góc trên bên phải
3. Chọn repository GitHub của bạn từ danh sách
4. Cấu hình ứng dụng:
   - **Repository**: Chọn repository của bạn (ví dụ: `username/tracuuMST`)
   - **Branch**: `main` (hoặc branch bạn muốn triển khai)
   - **Main file path**: `app/main_new.py`
   - **App URL**: Chọn URL bạn muốn (ví dụ: `tracuu-doanh-nghiep`)
5. Nhấn "Deploy!"

## Bước 4: Cấu hình Secrets (nếu cần)

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

## Bước 5: Tích hợp vào website

Để tích hợp ứng dụng vào website của bạn, bạn có thể sử dụng iframe:

```html
<iframe 
  src="https://username-appname.streamlit.app/?embed=true" 
  width="100%" 
  height="800px" 
  style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
  allow="camera;microphone"
></iframe>
```

Lưu ý:
- Thay `username-appname.streamlit.app` bằng URL thực tế của ứng dụng của bạn
- Tham số `?embed=true` giúp ẩn thanh bên của Streamlit
- Điều chỉnh `width` và `height` theo nhu cầu của bạn

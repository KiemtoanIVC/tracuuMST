# Hệ thống Tra cứu Doanh nghiệp

Ứng dụng web được xây dựng bằng Streamlit để tra cứu thông tin về các doanh nghiệp và kiểm tra danh sách rủi ro.

## Tính năng

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

1. Đăng ký tài khoản tại [Streamlit Cloud](https://streamlit.io/cloud)
2. Kết nối với GitHub repository của bạn
3. Triển khai ứng dụng với các cài đặt sau:
   - Repository: `your-username/tracuuMST`
   - Branch: `main`
   - Main file path: `app/main_new.py`

### Cấu hình Secrets

Nếu bạn có dữ liệu danh sách rủi ro, bạn cần cấu hình secrets trong Streamlit Cloud:

1. Trong dashboard của ứng dụng, chọn "Settings" > "Secrets"
2. Thêm secret với key là `blacklist_data` và value là nội dung của file CSV danh sách rủi ro

## Cấu trúc dự án

```
tracuuMST/
├── app/
│   ├── main_new.py        # File chính của ứng dụng
│   ├── database.py        # Module xử lý dữ liệu
│   └── style.css          # CSS tùy chỉnh
├── data/
│   └── blacklist.csv      # Dữ liệu danh sách rủi ro
├── requirements.txt       # Các thư viện cần thiết
└── README.md              # Tài liệu hướng dẫn
```

## Tùy chỉnh

### Thay đổi logo

Để thay đổi logo, chỉnh sửa dòng sau trong file `app/main_new.py`:

```python
st.image("https://img.icons8.com/color/96/000000/company.png", width=80)
```

### Thay đổi giao diện

Giao diện có thể được tùy chỉnh bằng cách chỉnh sửa file `app/style.css`.
# Hướng dẫn cập nhật ứng dụng

## Cập nhật ứng dụng local

1. Pull code mới từ repository:
```bash
git pull origin main
```

2. Cài đặt các thư viện mới (nếu có):
```bash
pip install -r requirements.txt
```

3. Chạy ứng dụng:
```bash
streamlit run app/main_new.py
```

## Cập nhật ứng dụng trên Streamlit Cloud

1. Thực hiện các thay đổi trong mã nguồn
2. Commit và push các thay đổi lên GitHub:
```bash
git add .
git commit -m "Cập nhật ứng dụng"
git push origin main
```

3. Streamlit Cloud sẽ tự động cập nhật ứng dụng của bạn

## Cập nhật danh sách rủi ro

### Cập nhật local

1. Cập nhật file `data/blacklist.csv`
2. Chạy lại ứng dụng

### Cập nhật trên Streamlit Cloud

1. Trong dashboard của ứng dụng, chọn "Settings" > "Secrets"
2. Cập nhật secret với key là `blacklist_data` và value là nội dung mới của file CSV danh sách rủi ro
3. Nhấn "Save"

## Cập nhật giao diện

1. Chỉnh sửa file `app/style.css` để thay đổi giao diện
2. Chỉnh sửa file `.streamlit/config.toml` để thay đổi theme
3. Commit và push các thay đổi lên GitHub

## Xử lý sự cố khi cập nhật

### Lỗi khi pull code

Nếu gặp lỗi khi pull code:
```bash
git stash
git pull origin main
git stash pop
```

### Lỗi khi chạy ứng dụng sau khi cập nhật

Kiểm tra:
1. Các thư viện mới đã được cài đặt chưa
2. Cấu trúc thư mục có thay đổi không
3. Các file cấu hình có bị thay đổi không

### Lỗi khi triển khai lên Streamlit Cloud

1. Kiểm tra logs trong dashboard của ứng dụng
2. Đảm bảo tất cả các thư viện cần thiết đã được liệt kê trong `requirements.txt`
3. Kiểm tra đường dẫn file chính đã chính xác

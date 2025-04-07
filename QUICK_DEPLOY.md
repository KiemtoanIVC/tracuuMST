# Hướng dẫn nhanh triển khai lên Streamlit Cloud

## Các bước triển khai

1. **Đăng ký tài khoản Streamlit Cloud**
   - Truy cập https://streamlit.io/cloud
   - Đăng ký bằng tài khoản GitHub

2. **Đẩy code lên GitHub**
   - Đảm bảo bạn đã đẩy code lên GitHub repository
   - Kiểm tra file `app/main_new.py` và `app/style.css` đã có trong repository

3. **Triển khai ứng dụng**
   - Đăng nhập vào Streamlit Cloud
   - Nhấn "New app"
   - Chọn repository GitHub của bạn
   - Cấu hình:
     - Main file path: `app/main_new.py`
     - Branch: `main`
   - Nhấn "Deploy!"

4. **Cấu hình Secrets (nếu cần)**
   - Trong dashboard của ứng dụng, chọn "Settings" > "Secrets"
   - Thêm secret với key là `blacklist_data` và value là nội dung của file CSV danh sách rủi ro

5. **Tích hợp vào website**
   - Sử dụng iframe để nhúng ứng dụng:
   ```html
   <iframe 
     src="https://username-appname.streamlit.app/?embed=true" 
     width="100%" 
     height="800px" 
     style="border: none;"
   ></iframe>
   ```

## Kiểm tra

- Truy cập URL của ứng dụng: `https://username-appname.streamlit.app`
- Kiểm tra tất cả các chức năng hoạt động đúng

## Xem hướng dẫn chi tiết

Xem file `DEPLOYMENT.md` để biết hướng dẫn chi tiết hơn.

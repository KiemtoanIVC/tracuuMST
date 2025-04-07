# Hướng dẫn tùy chỉnh giao diện

Tài liệu này hướng dẫn cách tùy chỉnh giao diện của ứng dụng Tra cứu Doanh nghiệp.

## Thay đổi logo

Để thay đổi logo của ứng dụng, bạn cần chỉnh sửa file `app/main_new.py`:

1. Tìm dòng sau trong file:
   ```python
   st.image("https://img.icons8.com/color/96/000000/company.png", width=80)
   ```

2. Thay đổi URL thành URL của logo mới:
   ```python
   st.image("https://example.com/your-logo.png", width=80)
   ```

   Hoặc sử dụng logo local:
   ```python
   st.image("./assets/logo.png", width=80)
   ```

## Thay đổi màu sắc và phong cách

### Cách 1: Chỉnh sửa file CSS

Bạn có thể tùy chỉnh giao diện bằng cách chỉnh sửa file `app/style.css`:

1. Mở file `app/style.css`
2. Chỉnh sửa các thuộc tính CSS để thay đổi màu sắc, font chữ, kích thước, v.v.

Ví dụ, để thay đổi màu chủ đạo:

```css
h1, h2, h3, h4 {
    color: #FF5733; /* Thay đổi màu tiêu đề thành màu cam */
    font-family: 'Arial', sans-serif;
}

.stButton > button {
    background-color: #FF5733; /* Thay đổi màu nút thành màu cam */
    color: white;
}
```

### Cách 2: Sử dụng cấu hình Streamlit

Bạn có thể tùy chỉnh theme của Streamlit bằng cách chỉnh sửa file `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF5733" # Màu chủ đạo
backgroundColor = "#F8F9FA" # Màu nền
secondaryBackgroundColor = "#FFFFFF" # Màu nền thứ cấp
textColor = "#262730" # Màu chữ
font = "sans serif" # Font chữ
```

## Thay đổi bố cục

Để thay đổi bố cục của ứng dụng, bạn cần chỉnh sửa file `app/main_new.py`:

### Thay đổi kích thước cột

Tìm các đoạn code sử dụng `st.columns()` và điều chỉnh tỷ lệ:

```python
# Thay đổi từ
col1, col2 = st.columns([1, 5])

# Thành
col1, col2 = st.columns([1, 3]) # Làm cho cột logo rộng hơn
```

### Thêm hoặc xóa các phần

Bạn có thể thêm hoặc xóa các phần trong ứng dụng bằng cách chỉnh sửa code trong hàm `main()`.

## Thêm trang mới

Để thêm trang mới vào ứng dụng:

1. Tạo file mới trong thư mục `app`, ví dụ: `about.py`
2. Tạo thư mục `app/pages`
3. Di chuyển file `about.py` vào thư mục `app/pages`
4. Streamlit sẽ tự động thêm trang này vào menu điều hướng

Ví dụ nội dung file `app/pages/about.py`:

```python
import streamlit as st

def main():
    st.title("Giới thiệu")
    st.write("Đây là trang giới thiệu về ứng dụng Tra cứu Doanh nghiệp.")

if __name__ == "__main__":
    main()
```

## Thay đổi biểu tượng trạng thái

Để thay đổi biểu tượng hiển thị cho các trạng thái, tìm đoạn code sau trong file `app/main_new.py`:

```python
# Tạo biểu tượng trạng thái
if status_code == "00" or status_code == "04":
    status_icon = "✅"
elif status_code == "05":
    status_icon = "⚠️"
elif status_code in ["06", "07", "03"]:
    status_icon = "❌"
else:
    status_icon = "ℹ️"
```

Và thay đổi các biểu tượng emoji theo ý muốn.

## Thêm footer tùy chỉnh

Để thêm footer tùy chỉnh, tìm đoạn code sau trong file `app/main_new.py`:

```python
# Footer
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("© 2025 Hệ thống Tra cứu Doanh nghiệp | Phiên bản 2.0", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
```

Và thay đổi nội dung theo ý muốn.

## Lưu ý quan trọng

- Sau khi thay đổi, hãy kiểm tra ứng dụng để đảm bảo mọi thứ hoạt động đúng
- Nếu triển khai trên Streamlit Cloud, các thay đổi sẽ được cập nhật tự động khi bạn push code lên GitHub
- Luôn sao lưu code trước khi thực hiện các thay đổi lớn

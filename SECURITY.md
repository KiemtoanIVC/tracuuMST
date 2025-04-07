# Hướng dẫn bảo mật

## Bảo mật dữ liệu

### Danh sách rủi ro

Dữ liệu danh sách rủi ro là thông tin nhạy cảm. Khi triển khai ứng dụng, hãy đảm bảo:

1. **Không đẩy file `data/blacklist.csv` lên GitHub công khai**
2. Sử dụng Streamlit Secrets để lưu trữ dữ liệu này
3. Giới hạn quyền truy cập vào ứng dụng nếu cần thiết

### Cấu hình Secrets trên Streamlit Cloud

1. Trong dashboard của ứng dụng, chọn "Settings" > "Secrets"
2. Thêm secret với key là `blacklist_data` và value là nội dung của file CSV danh sách rủi ro
3. Nhấn "Save"

## Bảo mật ứng dụng

### Giới hạn quyền truy cập

Để giới hạn quyền truy cập vào ứng dụng, bạn có thể:

1. Thêm xác thực người dùng vào ứng dụng:

```python
import streamlit as st

def check_password():
    """Trả về `True` nếu người dùng nhập đúng mật khẩu."""
    def password_entered():
        """Kiểm tra mật khẩu."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Xóa mật khẩu khỏi session state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Lần đầu tiên, hiển thị form nhập mật khẩu
        st.text_input(
            "Mật khẩu", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Mật khẩu không đúng, hiển thị form nhập lại
        st.text_input(
            "Mật khẩu", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Mật khẩu không đúng")
        return False
    else:
        # Mật khẩu đúng
        return True

if check_password():
    # Nội dung ứng dụng ở đây
    st.write("Chào mừng bạn đến với ứng dụng!")
```

2. Thêm secret `password` trong Streamlit Cloud:
   - Key: `password`
   - Value: `your-secure-password`

### Bảo mật khi tích hợp vào website

Khi tích hợp ứng dụng vào website của bạn, hãy đảm bảo:

1. Website của bạn sử dụng HTTPS
2. Nếu ứng dụng chứa thông tin nhạy cảm, hãy giới hạn quyền truy cập vào trang web chứa iframe
3. Sử dụng thuộc tính `sandbox` cho iframe để giới hạn quyền của iframe:

```html
<iframe 
  src="https://username-appname.streamlit.app/?embed=true" 
  width="100%" 
  height="800px" 
  style="border: none;"
  sandbox="allow-same-origin allow-scripts allow-forms"
></iframe>
```

## Bảo mật API

Ứng dụng sử dụng API của Tổng cục Thuế để tra cứu thông tin doanh nghiệp. Để đảm bảo bảo mật:

1. Không lưu trữ hoặc hiển thị thông tin nhạy cảm của doanh nghiệp
2. Không thực hiện quá nhiều request trong thời gian ngắn để tránh bị chặn
3. Xử lý lỗi một cách an toàn, không hiển thị thông tin lỗi chi tiết cho người dùng

## Cập nhật bảo mật

Để đảm bảo ứng dụng luôn được bảo mật:

1. Cập nhật thường xuyên các thư viện trong `requirements.txt`
2. Kiểm tra các lỗ hổng bảo mật trong các thư viện sử dụng
3. Theo dõi các cập nhật bảo mật của Streamlit

## Báo cáo lỗ hổng bảo mật

Nếu bạn phát hiện lỗ hổng bảo mật trong ứng dụng, vui lòng liên hệ với quản trị viên để được hỗ trợ.

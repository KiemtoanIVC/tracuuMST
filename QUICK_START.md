# Hướng dẫn nhanh

## Chạy ứng dụng local

```bash
# Cài đặt thư viện
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app/main_new.py
```

## Triển khai lên Streamlit Cloud

1. Đăng ký tại [Streamlit Cloud](https://streamlit.io/cloud)
2. Kết nối với GitHub repository
3. Triển khai với file path: `app/main_new.py`

## Tích hợp vào website

```html
<iframe 
  src="https://username-appname.streamlit.app/?embed=true" 
  width="100%" 
  height="800px" 
  style="border: none;"
></iframe>
```

## Tài liệu chi tiết

Xem [GUIDE.md](GUIDE.md) để biết hướng dẫn đầy đủ.

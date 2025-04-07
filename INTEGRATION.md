# Hướng dẫn tích hợp ứng dụng vào website

Tài liệu này hướng dẫn cách tích hợp ứng dụng Tra cứu Doanh nghiệp vào website của bạn.

## Phương pháp 1: Nhúng bằng iframe

Đây là cách đơn giản nhất để tích hợp ứng dụng Streamlit vào website của bạn.

### Bước 1: Lấy URL của ứng dụng

Sau khi triển khai ứng dụng lên Streamlit Cloud, bạn sẽ có URL dạng:
```
https://username-appname.streamlit.app
```

### Bước 2: Thêm iframe vào website

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

#### Tùy chỉnh iframe:

- **width**: Điều chỉnh chiều rộng (ví dụ: "100%", "800px")
- **height**: Điều chỉnh chiều cao (ví dụ: "800px", "90vh")
- **style**: Tùy chỉnh CSS (viền, bóng đổ, bo góc, v.v.)
- **?embed=true**: Tham số này giúp ẩn thanh bên của Streamlit

### Ví dụ tích hợp vào trang HTML:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Tra cứu Doanh nghiệp</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #1E3A8A;
        }
        .app-container {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tra cứu Doanh nghiệp</h1>
        <p>Sử dụng công cụ dưới đây để tra cứu thông tin doanh nghiệp theo mã số thuế.</p>
        
        <div class="app-container">
            <iframe 
                src="https://username-appname.streamlit.app/?embed=true" 
                width="100%" 
                height="800px" 
                style="border: none; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
                allow="camera;microphone"
            ></iframe>
        </div>
    </div>
</body>
</html>
```

## Phương pháp 2: Tích hợp vào WordPress

### Sử dụng plugin HTML Custom:

1. Cài đặt plugin "HTML Custom Blocks" hoặc "Custom HTML Widget"
2. Tạo widget mới và thêm code iframe như trên
3. Thêm widget vào sidebar hoặc trang của bạn

### Sử dụng Elementor:

1. Thêm widget "HTML" vào trang
2. Dán code iframe vào widget
3. Tùy chỉnh kích thước và vị trí

## Phương pháp 3: Tích hợp vào React

```jsx
import React from 'react';

const BusinessLookup = () => {
  return (
    <div className="business-lookup-container">
      <h2>Tra cứu Doanh nghiệp</h2>
      <iframe 
        src="https://username-appname.streamlit.app/?embed=true" 
        width="100%" 
        height="800px" 
        style={{
          border: 'none', 
          borderRadius: '8px', 
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
        }}
        allow="camera;microphone"
        title="Business Lookup App"
      />
    </div>
  );
};

export default BusinessLookup;
```

## Phương pháp 4: Tích hợp vào Vue.js

```vue
<template>
  <div class="business-lookup-container">
    <h2>Tra cứu Doanh nghiệp</h2>
    <iframe 
      :src="appUrl" 
      width="100%" 
      height="800px" 
      :style="iframeStyle"
      allow="camera;microphone"
      title="Business Lookup App"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      appUrl: 'https://username-appname.streamlit.app/?embed=true',
      iframeStyle: {
        border: 'none',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }
    }
  }
}
</script>
```

## Xử lý sự cố tích hợp

### Vấn đề về CORS

Nếu bạn gặp vấn đề về CORS (Cross-Origin Resource Sharing), hãy đảm bảo:

1. Tham số `?embed=true` đã được thêm vào URL
2. Ứng dụng Streamlit đã được cấu hình để cho phép CORS (mặc định đã được bật)

### Iframe không hiển thị

Nếu iframe không hiển thị:

1. Kiểm tra URL của ứng dụng Streamlit có chính xác không
2. Đảm bảo ứng dụng Streamlit đang chạy và có thể truy cập được
3. Kiểm tra cài đặt bảo mật của trình duyệt (một số trình duyệt chặn iframe)

### Kích thước không phù hợp

Nếu kích thước iframe không phù hợp:

1. Điều chỉnh thuộc tính `width` và `height`
2. Sử dụng đơn vị tương đối như % hoặc vh/vw
3. Thêm CSS để làm cho iframe responsive:

```css
.responsive-iframe {
  width: 100%;
  height: 80vh;
  min-height: 600px;
}
```

## Tùy chỉnh nâng cao

### Truyền tham số vào ứng dụng

Bạn có thể truyền tham số vào ứng dụng Streamlit thông qua URL:

```html
<iframe src="https://username-appname.streamlit.app/?embed=true&mst=0123456789"></iframe>
```

Trong ứng dụng Streamlit, bạn có thể đọc tham số này:

```python
import streamlit as st

# Đọc tham số từ URL
params = st.experimental_get_query_params()
mst = params.get("mst", [""])[0]

if mst:
    # Tự động điền MST vào ô nhập liệu
    st.text_input("Nhập MST cần tra cứu:", value=mst)
```

### Tùy chỉnh theme cho iframe

Bạn có thể thêm tham số theme vào URL:

```html
<iframe src="https://username-appname.streamlit.app/?embed=true&theme=dark"></iframe>
```

## Kết luận

Việc tích hợp ứng dụng Streamlit vào website của bạn khá đơn giản với iframe. Tuy nhiên, để có trải nghiệm người dùng tốt nhất, hãy đảm bảo:

1. Kích thước iframe phù hợp với nội dung
2. Giao diện ứng dụng Streamlit phù hợp với website của bạn
3. Trang web của bạn responsive để hiển thị tốt trên các thiết bị khác nhau

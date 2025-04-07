# Hướng dẫn sử dụng Hệ thống Tra cứu Doanh nghiệp

## Giới thiệu

Hệ thống Tra cứu Doanh nghiệp là ứng dụng web giúp bạn tra cứu thông tin doanh nghiệp theo mã số thuế (MST). Ứng dụng hỗ trợ tra cứu đơn lẻ hoặc hàng loạt, đồng thời kiểm tra trạng thái hoạt động và cảnh báo rủi ro.

## Các chức năng chính

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

## Giải thích các trạng thái

- **Đang hoạt động** (✅): Doanh nghiệp đang hoạt động bình thường
- **Tạm ngừng hoạt động** (⚠️): Doanh nghiệp đã tạm ngừng hoạt động, kinh doanh
- **Ngừng hoạt động** (❌): Doanh nghiệp đã ngừng hoạt động hoặc không hoạt động tại địa chỉ đã đăng ký
- **Đã chuyển CQT** (ℹ️): Doanh nghiệp đã chuyển cơ quan thuế quản lý

## Cảnh báo rủi ro

Nếu doanh nghiệp nằm trong danh sách rủi ro, hệ thống sẽ hiển thị cảnh báo (⛔) kèm theo thông tin chi tiết về lý do cảnh báo.

## Mẹo sử dụng

1. **Tra cứu đơn lẻ**: Sử dụng khi bạn chỉ cần tra cứu một vài doanh nghiệp
2. **Tra cứu hàng loạt**: Sử dụng khi bạn cần tra cứu nhiều doanh nghiệp (>10)
3. **Xuất Excel**: Luôn xuất kết quả ra Excel để lưu trữ và phân tích sau này
4. **Định dạng MST**: Luôn đảm bảo MST được định dạng kiểu Text trong Excel để giữ số 0 ở đầu

## Xử lý sự cố

- **Không tìm thấy thông tin**: Kiểm tra lại MST đã nhập đúng chưa
- **Lỗi khi upload file**: Đảm bảo file Excel đúng định dạng và có cột MST
- **Kết quả không đầy đủ**: Một số doanh nghiệp có thể không có đầy đủ thông tin trong cơ sở dữ liệu

## Liên hệ hỗ trợ

Nếu bạn gặp vấn đề khi sử dụng hệ thống, vui lòng liên hệ với quản trị viên để được hỗ trợ.

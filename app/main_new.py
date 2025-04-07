import streamlit as st
import pandas as pd
import requests
import urllib3
from database import BusinessDatabase
from io import BytesIO
import base64
import os

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Map trạng thái
TRANG_THAI = {
    "00": "Đang hoạt động",
    "01": "NNT ngừng hoạt động và ĐÃ HOÀN THÀNH thủ tục chấm dứt hiệu lực MST",
    "02": "NNT đã chuyển cơ quan thuế quản lý",
    "03": "NNT ngừng hoạt động nhưng CHƯA HOÀN THÀNH thủ tục chấm dứt hiệu lực MST",
    "04": "NNT đang hoạt động (áp dụng cho hộ kinh doanh, cá nhân kinh doanh chưa đủ thông tin đăng ký thuế)",
    "05": "NNT tạm ngừng hoạt động, kinh doanh",
    "06": "Không hoạt động tại địa chỉ đã đăng ký",
    "07": "NNT chờ làm thủ tục phá sản"
}

# Màu sắc cho trạng thái
STATUS_COLORS = {
    "00": "status-active",    # Đang hoạt động
    "04": "status-active",    # Đang hoạt động (hộ kinh doanh)
    "05": "status-warning",   # Tạm ngừng
    "01": "status-danger",    # Đã chấm dứt
    "03": "status-danger",    # Ngừng hoạt động chưa hoàn thành
    "06": "status-danger",    # Không hoạt động tại địa chỉ
    "07": "status-danger",    # Chờ phá sản
    "02": "status-info"       # Đã chuyển CQT
}

def get_status_description(status_code):
    """Lấy mô tả trạng thái từ mã"""
    return TRANG_THAI.get(status_code, "Không xác định")

def get_status_class(status_code):
    """Lấy class CSS cho trạng thái"""
    return STATUS_COLORS.get(status_code, "status-info")

def load_css():
    """Load CSS từ file"""
    css_file = os.path.join(os.path.dirname(__file__), "style.css")
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def lookup_business(mst):
    """Hàm tra cứu thông tin doanh nghiệp từ API"""
    try:
        url = f"https://hoadondientu.gdt.gov.vn:30000/category/public/dsdkts/{mst}/manager"
        response = requests.get(url, verify=False)
        return response.json()
    except Exception as e:
        st.error(f"Lỗi khi tra cứu MST {mst}: {str(e)}")
        return None

def display_business_info(data):
    """Hiển thị thông tin doanh nghiệp với giao diện hiện đại"""
    if data:
        db = BusinessDatabase()

        # Lấy thông tin trạng thái và cảnh báo
        status_code = data.get('tthai', 'N/A')
        status_desc = get_status_description(status_code)
        status_class = get_status_class(status_code)

        # Tạo biểu tượng trạng thái
        if status_code == "00" or status_code == "04":
            status_icon = "✅"
        elif status_code == "05":
            status_icon = "⚠️"
        elif status_code in ["06", "07", "03"]:
            status_icon = "❌"
        else:
            status_icon = "ℹ️"

        # Kiểm tra blacklist
        blacklist_info = db.get_blacklist_info(data.get('mst'))

        # Tạo card thông tin cơ bản
        st.markdown("<h3 style='color: #1E3A8A;'>Thông tin doanh nghiệp</h3>", unsafe_allow_html=True)

        # Card thông tin cơ bản
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        # Tên và MST
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"<h2 style='margin-bottom: 5px;'>{data.get('tennnt', 'N/A')}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #6B7280; margin-top: 0;'>Mã số thuế: <b>{data.get('mst', 'N/A')}</b></p>", unsafe_allow_html=True)

        with col2:
            # Hiển thị trạng thái với màu sắc tương ứng
            st.markdown(f"<div style='text-align: right;'>", unsafe_allow_html=True)
            st.markdown(f"<p>Trạng thái:</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='{status_class}'>{status_icon} {status_desc}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Địa chỉ
        address_parts = []
        if data.get('dctsdchi'): address_parts.append(data.get('dctsdchi'))
        if data.get('dctsxaten'): address_parts.append(data.get('dctsxaten'))
        if data.get('dctshuyenten'): address_parts.append(data.get('dctshuyenten'))
        if data.get('dctstinhten'): address_parts.append(data.get('dctstinhten'))

        full_address = ", ".join([part for part in address_parts if part and part != 'N/A'])

        st.markdown(f"<p><b>Địa chỉ:</b> {full_address}</p>", unsafe_allow_html=True)

        # Cơ quan thuế quản lý
        st.markdown(f"<p><b>Cơ quan thuế quản lý:</b> {data.get('tencqt', 'N/A')}</p>", unsafe_allow_html=True)

        # Loại hình doanh nghiệp
        business_type = f"{data.get('loainnt', '')} - {data.get('lnnt', '')}"
        st.markdown(f"<p><b>Loại hình:</b> {business_type}</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Hiển thị cảnh báo nếu có
        if blacklist_info is not None:
            st.markdown("<div class='error-box'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: #DC2626; margin-top: 0;'>⛔ Cảnh báo rủi ro</h4>", unsafe_allow_html=True)
            st.markdown(f"<p>{blacklist_info['Note']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Thông tin chi tiết
        with st.expander("Xem thông tin chi tiết"):
            # Bảng thông tin chi tiết
            df2 = pd.DataFrame({
                'Thông tin': [
                    'Mã CQT',
                    'Tên CQT',
                    'Loại NNT',
                    'LNNT',
                    'Địa chỉ',
                    'Tỉnh/TP',
                    'Quận/Huyện',
                    'Phường/Xã'
                ],
                'Giá trị': [
                    data.get('macqt', 'N/A'),
                    data.get('tencqt', 'N/A'),
                    data.get('loainnt', 'N/A'),
                    data.get('lnnt', 'N/A'),
                    data.get('dctsdchi', 'N/A'),
                    data.get('dctstinhten', 'N/A'),
                    data.get('dctshuyenten', 'N/A'),
                    data.get('dctsxaten', 'N/A')
                ]
            })
            st.dataframe(
                df2,
                hide_index=True,
                column_config={
                    'Thông tin': st.column_config.TextColumn('Thông tin', width='medium'),
                    'Giá trị': st.column_config.TextColumn('Giá trị', width='large')
                }
            )

def create_sample_excel():
    """Tạo file mẫu Excel"""
    # Tạo DataFrame mẫu
    sample_df = pd.DataFrame({
        'MST': ['0123456789', '9876543210'],
        'Tên DN': ['Công ty A', 'Công ty B']
    })

    # Tạo buffer để lưu file Excel
    buffer = BytesIO()

    # Tạo ExcelWriter với engine='xlsxwriter' để có thể format
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        sample_df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Lấy workbook và worksheet để format
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Format cột MST là text
        text_format = workbook.add_format({'num_format': '@'})
        worksheet.set_column('A:A', 15, text_format)  # Cột A (MST)
        worksheet.set_column('B:B', 40)  # Cột B (Tên DN)

        # Thêm ghi chú cho cột MST
        worksheet.write_comment('A1', 'Định dạng cột này là Text để giữ số 0 ở đầu MST')

    buffer.seek(0)
    return buffer

def create_excel_result(status_df, blacklist_df, result_df):
    """Tạo file Excel kết quả"""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Sheet thống kê
        status_df.to_excel(writer, sheet_name='Thống kê trạng thái', index=False)
        blacklist_df.to_excel(writer, sheet_name='Thống kê rủi ro', index=False)

        # Sheet kết quả chi tiết
        result_df.to_excel(writer, sheet_name='Kết quả chi tiết', index=False)

        # Format các sheet
        workbook = writer.book

        # Format sheet kết quả chi tiết
        worksheet = writer.sheets['Kết quả chi tiết']
        text_format = workbook.add_format({'num_format': '@'})
        worksheet.set_column('A:A', 15, text_format)  # MST
        worksheet.set_column('B:B', 40)  # Tên DN
        worksheet.set_column('C:C', 30)  # Trạng thái
        worksheet.set_column('D:D', 20)  # Trong danh sách đen
        worksheet.set_column('E:E', 50)  # Ghi chú cảnh báo

    buffer.seek(0)
    return buffer

def main():
    st.set_page_config(
        page_title="Tra cứu Doanh nghiệp",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Load CSS
    load_css()

    # Header với logo và tiêu đề
    col1, col2 = st.columns([1, 5])

    with col1:
        # Logo placeholder - có thể thay bằng logo thực tế
        st.image("https://img.icons8.com/color/96/000000/company.png", width=80)

    with col2:
        st.title("Hệ thống Tra cứu Doanh nghiệp")
        st.markdown("<p style='color: #6B7280; margin-top: -15px; font-family: Nunito, sans-serif;'>Kiểm tra thông tin và trạng thái doanh nghiệp theo mã số thuế</p>", unsafe_allow_html=True)

    # Tạo 2 tab với giao diện hiện đại
    tab1, tab2 = st.tabs(["Tra cứu đơn lẻ", "Tra cứu hàng loạt"])

    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #1E3A8A; font-family: Poppins, sans-serif; font-weight: 600;'>Tra cứu theo Mã số thuế</h3>", unsafe_allow_html=True)

        # Form tra cứu với giao diện đẹp hơn
        mst_input = st.text_input("Nhập MST cần tra cứu:", placeholder="Ví dụ: 0123456789")
        search_button = st.button("Tra cứu", key="single_search_button")

        st.markdown("</div>", unsafe_allow_html=True)

        # Xử lý tra cứu
        if search_button and mst_input:
            with st.spinner('Tra cứu thông tin...'):
                result = lookup_business(mst_input)
                display_business_info(result)

    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #1E3A8A; font-family: Poppins, sans-serif; font-weight: 600;'>Tra cứu hàng loạt</h3>", unsafe_allow_html=True)

        # Hướng dẫn ngắn gọn
        st.markdown("<p style='font-family: Nunito, sans-serif;'>Tải file mẫu Excel, điền danh sách MST, sau đó upload và tra cứu.</p>", unsafe_allow_html=True)

        # Card cho file mẫu và upload
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='color: #1E3A8A; font-family: Poppins, sans-serif; font-weight: 500;'>Bước 1: Tải file mẫu</h4>", unsafe_allow_html=True)
            excel_buffer = create_sample_excel()
            st.download_button(
                "📥 Download file mẫu Excel",
                excel_buffer,
                "mau_tra_cuu.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Upload file
        with col2:
            st.markdown("<h4 style='color: #1E3A8A; font-family: Poppins, sans-serif; font-weight: 500;'>Bước 2: Upload file đã điền</h4>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Chọn file Excel", type=['xlsx'], label_visibility="collapsed")

        st.markdown("</div>", unsafe_allow_html=True)

        # Xử lý file upload
        if uploaded_file is not None:
            try:
                # Đọc file với dtype để chỉ định MST là kiểu string
                df = pd.read_excel(
                    uploaded_file,
                    dtype={'MST': str},  # Đảm bảo MST được đọc như text
                    engine='openpyxl'
                )

                # Kiểm tra cột MST
                if 'MST' not in df.columns:
                    st.error("File phải có cột 'MST'")
                else:
                    # Chuẩn hóa MST: thêm số 0 vào đầu nếu độ dài < 10
                    df['MST'] = df['MST'].apply(lambda x: str(x).zfill(10))

                    # Hiển thị số lượng và nút tra cứu
                    st.markdown(f"<p style='font-family: Nunito, sans-serif;'>Số lượng doanh nghiệp cần tra cứu: <b>{len(df)}</b></p>", unsafe_allow_html=True)
                    search_all_button = st.button("Tra cứu tất cả", key="batch_search_button")

                    # Xử lý tra cứu
                    if search_all_button:
                        results = []
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        # Tra cứu từng MST
                        for i, mst in enumerate(df['MST']):
                            status_text.text(f"Đang tra cứu MST {mst} ({i+1}/{len(df)})")

                            # Đảm bảo MST là string và có đủ 10 chữ số
                            mst = str(mst).zfill(10)
                            result = lookup_business(mst)
                            if result:
                                status_code = result.get('tthai', 'N/A')
                                status_desc = get_status_description(status_code)

                                # Kiểm tra blacklist
                                db = BusinessDatabase()
                                blacklist_info = db.get_blacklist_info(mst)
                                blacklist_status = "Có ⛔" if blacklist_info else "Không"
                                blacklist_note = blacklist_info['Note'] if blacklist_info else ""

                                results.append({
                                    'MST': mst,  # Sử dụng MST đã chuẩn hóa
                                    'Tên DN': result.get('tennnt', 'N/A'),
                                    'Trạng thái': f"{status_desc}",
                                    'Trong danh sách đen': blacklist_status,
                                    'Ghi chú cảnh báo': blacklist_note
                                })

                            # Cập nhật progress bar
                            progress_bar.progress((i + 1) / len(df))

                        # Hiển thị kết quả
                        if results:
                            st.success("✅ Đã tra cứu xong!")
                            result_df = pd.DataFrame(results)

                            # Đảm bảo MST trong kết quả được format đúng
                            result_df['MST'] = result_df['MST'].astype(str).apply(lambda x: x.zfill(10))

                            # Card kết quả
                            st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.markdown("<h3 style='color: #1E3A8A;'>Kết quả tra cứu</h3>", unsafe_allow_html=True)

                            # Thống kê kết quả
                            st.markdown("<h4>Thống kê kết quả tra cứu:</h4>", unsafe_allow_html=True)
                            col1, col2 = st.columns(2)

                            with col1:
                                # Thống kê theo trạng thái
                                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                                st.markdown("<h5 style='margin-top: 0;'>Theo trạng thái:</h5>", unsafe_allow_html=True)
                                status_counts = result_df['Trạng thái'].value_counts()
                                status_df = pd.DataFrame({
                                    'Trạng thái': status_counts.index,
                                    'Số lượng': status_counts.values
                                })
                                st.dataframe(
                                    status_df,
                                    hide_index=True,
                                    column_config={
                                        'Trạng thái': st.column_config.TextColumn('Trạng thái', width='large'),
                                        'Số lượng': st.column_config.NumberColumn('Số lượng', width='small')
                                    }
                                )
                                st.markdown("</div>", unsafe_allow_html=True)

                            with col2:
                                # Thống kê theo danh sách đen
                                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                                st.markdown("<h5 style='margin-top: 0;'>Theo danh sách rủi ro:</h5>", unsafe_allow_html=True)
                                blacklist_counts = result_df['Trong danh sách đen'].value_counts()

                                # Tạo DataFrame với tên rõ ràng hơn
                                blacklist_df = pd.DataFrame({
                                    'Trạng thái': [
                                        'Có trong danh sách rủi ro' if x == 'Có ⛔' else 'Không trong danh sách rủi ro'
                                        for x in blacklist_counts.index
                                    ],
                                    'Số lượng': blacklist_counts.values
                                })

                                # Sắp xếp để "Có trong danh sách" hiển thị trước
                                blacklist_df = blacklist_df.sort_values('Trạng thái', ascending=False)

                                st.dataframe(
                                    blacklist_df,
                                    hide_index=True,
                                    column_config={
                                        'Trạng thái': st.column_config.TextColumn('Trạng thái', width='large'),
                                        'Số lượng': st.column_config.NumberColumn(
                                            'Số lượng',
                                            width='small',
                                            help="Số lượng doanh nghiệp"
                                        )
                                    }
                                )
                                st.markdown("</div>", unsafe_allow_html=True)

                            # Hiển thị kết quả chi tiết
                            st.markdown("<h4>Kết quả chi tiết:</h4>", unsafe_allow_html=True)
                            st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
                            st.dataframe(
                                result_df,
                                column_config={
                                    'MST': st.column_config.TextColumn('MST', width='medium'),
                                    'Tên DN': st.column_config.TextColumn('Tên DN', width='large'),
                                    'Trạng thái': st.column_config.TextColumn('Trạng thái', width='large'),
                                    'Trong danh sách đen': st.column_config.TextColumn('Trong danh sách đen', width='medium'),
                                    'Ghi chú cảnh báo': st.column_config.TextColumn('Ghi chú cảnh báo', width='large')
                                }
                            )
                            st.markdown("</div>", unsafe_allow_html=True)

                            # Nút download kết quả Excel
                            excel_result = create_excel_result(status_df, blacklist_df, result_df)
                            st.download_button(
                                "📥 Download kết quả (Excel)",
                                excel_result,
                                "ket_qua_tra_cuu.xlsx",
                                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )

                            st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Lỗi khi đọc file: {str(e)}")

    # Footer
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.markdown("<span style='font-family: Nunito, sans-serif;'>© Công ty TNHH Kiểm toán IVC |2025 Hệ thống Tra cứu Doanh nghiệp | Phiên bản 2.0</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

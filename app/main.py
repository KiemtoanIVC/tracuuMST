import streamlit as st
import pandas as pd
import requests
import urllib3
from database import BusinessDatabase
from io import BytesIO

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

def get_status_description(status_code):
    """Lấy mô tả trạng thái từ mã"""
    return TRANG_THAI.get(status_code, "Không xác định")

def main():
    st.set_page_config(
        page_title="Tra cứu Doanh nghiệp",
        page_icon="🏢",
        layout="wide"
    )
    
    st.title("🏢 Hệ thống Tra cứu Doanh nghiệp")
    
    # Tạo 2 tab
    tab1, tab2 = st.tabs(["Tra cứu đơn lẻ", "Tra cứu hàng loạt"])
    
    with tab1:
        st.header("Tra cứu theo Mã số thuế")
        mst_input = st.text_input("Nhập MST cần tra cứu:")
        if st.button("Tra cứu") and mst_input:
            result = lookup_business(mst_input)
            display_business_info(result)
            
    with tab2:
        st.header("Tra cứu hàng loạt")
        
        # Hướng dẫn
        st.write("**Hướng dẫn:**")
        st.write("""
        1. Tải file mẫu Excel
        2. Điền danh sách MST cần tra cứu (Lưu ý: cột MST phải định dạng kiểu Text để giữ số 0 ở đầu)
        3. Upload file và nhấn 'Tra cứu tất cả'
        """)
        
        # File mẫu Excel
        def create_sample_excel():
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
        
        # Tạo nút download file mẫu Excel
        excel_buffer = create_sample_excel()
        st.download_button(
            "📥 Download file mẫu Excel",
            excel_buffer,
            "mau_tra_cuu.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Upload file
        st.write("**Upload file Excel chứa danh sách MST:**")
        uploaded_file = st.file_uploader("Chọn file Excel", type=['xlsx'])
        
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
                    return
                
                # Chuẩn hóa MST: thêm số 0 vào đầu nếu độ dài < 10
                df['MST'] = df['MST'].apply(lambda x: str(x).zfill(10))
                
                # Nút tra cứu
                if st.button("Tra cứu tất cả"):
                    results = []
                    progress_bar = st.progress(0)
                    
                    # Tra cứu từng MST
                    for i, mst in enumerate(df['MST']):
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
                        
                        # Thống kê kết quả
                        st.write("**Thống kê kết quả tra cứu:**")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Thống kê theo trạng thái
                            st.write("Theo trạng thái:")
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
                        
                        with col2:
                            # Thống kê theo danh sách đen
                            st.write("Theo danh sách rủi ro:")
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
                        
                        # Hiển thị kết quả chi tiết
                        st.write("**Kết quả chi tiết:**")
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
                        
                        # Tạo file Excel kết quả
                        def create_excel_result():
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
                        
                        # Nút download kết quả Excel
                        excel_result = create_excel_result()
                        st.download_button(
                            "📥 Download kết quả (Excel)",
                            excel_result,
                            "ket_qua_tra_cuu.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
            except Exception as e:
                st.error(f"Lỗi khi đọc file: {str(e)}")

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
    """Hiển thị thông tin doanh nghiệp"""
    if data:
        db = BusinessDatabase()
        
        # Lấy thông tin trạng thái và cảnh báo
        status_code = data.get('tthai', 'N/A')
        status_desc = get_status_description(status_code)
        
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
        status_text = f"{status_icon} {status_desc}"
        if blacklist_info is not None:
            status_text = f"{status_text} ⛔"
        
        # Bảng 1: Thông tin cơ bản
        st.write("**Thông tin cơ bản:**")
        df1 = pd.DataFrame({
            'Mã số thuế': [data.get('mst', 'N/A')],
            'Tên doanh nghiệp': [data.get('tennnt', 'N/A')],
            'Trạng thái': [status_text]
        })
        st.dataframe(
            df1,
            hide_index=True,
            column_config={
                'Mã số thuế': st.column_config.TextColumn('Mã số thuế', width='medium'),
                'Tên doanh nghiệp': st.column_config.TextColumn('Tên doanh nghiệp', width='large'),
                'Trạng thái': st.column_config.TextColumn('Trạng thái', width='large')
            }
        )
        
        # Hiển thị chi tiết cảnh báo nếu có
        if blacklist_info is not None:
            st.error(f"⛔ Chi tiết cảnh báo: {blacklist_info['Note']}")
        
        # Bảng 2: Thông tin chi tiết
        st.write("**Thông tin chi tiết:**")
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

if __name__ == "__main__":
    main() 
import pandas as pd
from datetime import datetime
import os
import streamlit as st
from io import StringIO

class BusinessDatabase:
    def __init__(self):
        self.blacklist_df = None
        self.data_dir = "data"
        self.ensure_data_directory()
        self.load_data()
    
    def ensure_data_directory(self):
        """Đảm bảo thư mục data tồn tại"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_data(self):
        """Load dữ liệu từ file CSV hoặc secrets"""
        try:
            if 'STREAMLIT_SHARING' in os.environ:
                # Khi deploy trên Streamlit Cloud
                blacklist_data = st.secrets['blacklist_data']
                self.blacklist_df = pd.read_csv(StringIO(blacklist_data))
            else:
                # Khi chạy local
                self.blacklist_df = pd.read_csv(
                    f"{self.data_dir}/blacklist.csv",
                    encoding='utf-8'
                )
            self.blacklist_df = self.blacklist_df.loc[:, ~self.blacklist_df.columns.str.contains('^Unnamed')]
        except Exception as e:
            st.error(f"Không tìm thấy dữ liệu danh sách đen! Lỗi: {str(e)}")
            self.blacklist_df = pd.DataFrame(columns=['STT', 'Ma so thue', 'Ten cong ty', 'Ngay cuoi', 'Note'])
    
    def import_from_excel(self, file_path):
        """Import danh sách từ file Excel"""
        try:
            # Đọc file Excel
            df = pd.read_excel(file_path)
            
            # Kiểm tra các cột bắt buộc
            required_columns = ['STT', 'Ma so thue', 'Ten cong ty', 'Ngay cuoi', 'Note']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"File Excel phải có cột '{col}'")
            
            # Gộp với danh sách hiện tại, loại bỏ trùng lặp theo MST
            self.blacklist_df = pd.concat([self.blacklist_df, df]).drop_duplicates(subset=['Ma so thue'])
            
            # Lưu lại
            self.save_data()
            
            return len(df), "Import thành công"
            
        except Exception as e:
            return 0, f"Lỗi khi import: {str(e)}"
    
    def get_blacklist(self):
        """Lấy toàn bộ danh sách đen"""
        return self.blacklist_df
    
    def search_blacklist(self, keyword):
        """Tìm kiếm trong danh sách đen"""
        if not keyword:
            return self.blacklist_df
        
        keyword = str(keyword).lower()
        return self.blacklist_df[
            self.blacklist_df['Ma so thue'].astype(str).str.lower().str.contains(keyword, na=False) |
            self.blacklist_df['Ten cong ty'].astype(str).str.lower().str.contains(keyword, na=False)
        ]
    
    def check_blacklist(self, mst):
        """Kiểm tra MST có trong danh sách đen không"""
        if self.blacklist_df is not None:
            return str(mst) in self.blacklist_df['Ma so thue'].astype(str).values
        return False
    
    def add_to_blacklist(self, business_info):
        """Thêm DN vào danh sách đen"""
        new_record = {
            'mst': business_info['mst'],
            'ten': business_info['ten'],
            'dchi': business_info['dchi'],
            'ngay_phat_hien': datetime.now().strftime('%Y-%m-%d')
        }
        self.blacklist_df = self.blacklist_df.append(new_record, ignore_index=True)
        self.save_data()
    
    def save_data(self):
        """Lưu dữ liệu vào file"""
        self.blacklist_df.to_csv(f"{self.data_dir}/blacklist.csv", index=False)
    
    def get_blacklist_info(self, mst):
        """Lấy thông tin blacklist của một MST"""
        if self.blacklist_df is not None:
            # Tìm dòng có MST tương ứng
            result = self.blacklist_df[self.blacklist_df['Ma so thue'].astype(str) == str(mst)]
            if not result.empty:
                # Trả về dictionary chứa thông tin của dòng đầu tiên
                return result.iloc[0].to_dict()
        return None 
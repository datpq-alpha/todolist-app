import streamlit as st

def setup_page():
    st.set_page_config(page_title="To-Do List App", page_icon="📝", layout="wide")
    st.markdown("""
        <style>
        .main_header { font-size: 30px; font-weight: bold; color: #4CAF50; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown('<p class="main_header">📝 Ứng Dụng Quản Lý Công Việc</p>', unsafe_allow_html=True)
    st.markdown("---")

# Hàm chuyển đổi DataFrame thành CSV để tải xuống
def convert_df_to_csv(df):
    # encode utf-8-sig để Excel đọc được tiếng Việt không bị lỗi font
    return df.to_csv(index=False).encode('utf-8-sig')
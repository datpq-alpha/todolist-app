import streamlit as st
import pandas as pd
import plotly.express as px  # Thư viện vẽ biểu đồ (cần cài đặt: pip install plotly)
from datetime import date, datetime

# Import các module
import init_db
import db_funcs
import ui_helpers

# Khởi tạo DB
init_db.create_table()
ui_helpers.setup_page()
ui_helpers.show_header()

# --- MENU CHÍNH ---
menu = ["Dashboard (Thống kê)", "Quản lý công việc", "Thêm mới"]
choice = st.sidebar.selectbox("Chọn chức năng", menu)
st.sidebar.markdown("---")

# =========================================================
# CHỨC NĂNG 1: THÊM MỚI (ADD)
# =========================================================
if choice == "Thêm mới":
    st.subheader("➕ Thêm công việc mới")
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        task_name = c1.text_input("Tên công việc")
        assignee = c1.text_input("Người phụ trách")
        due_date = c2.date_input("Hạn chót", date.today())
        status = c2.selectbox("Trạng thái", ["Chưa bắt đầu", "Đang làm", "Hoàn thành"])
        notes = st.text_area("Ghi chú")

        if st.form_submit_button("Lưu công việc"):
            if task_name:
                db_funcs.add_task(task_name, status, due_date, assignee, notes)
                st.success("Đã thêm thành công!")
            else:
                st.error("Tên công việc không được để trống!")

# =========================================================
# CHỨC NĂNG 2: QUẢN LÝ CÔNG VIỆC (VIEW, EDIT, DELETE, FILTER)
# =========================================================
elif choice == "Quản lý công việc":
    st.subheader("📋 Danh sách công việc")

    # Load dữ liệu
    df = db_funcs.load_tasks()

    # 1. BỘ LỌC (Filter) - Filter trên giao diện bằng Pandas
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        search_text = st.text_input("🔍 Tìm theo tên công việc")
    with col_filter2:
        filter_status = st.selectbox("Lọc theo trạng thái", ["Tất cả", "Chưa bắt đầu", "Đang làm", "Hoàn thành"])

    # Xử lý lọc
    if search_text:
        df = df[df['task_name'].str.contains(search_text, case=False, na=False)]
    if filter_status != "Tất cả":
        df = df[df['status'] == filter_status]

    # Hiển thị bảng
    st.dataframe(df, use_container_width=True)

    # Nút Export dữ liệu
    csv = ui_helpers.convert_df_to_csv(df)
    st.download_button(
        label="📥 Tải xuống danh sách (CSV)",
        data=csv,
        file_name='danh_sach_cong_viec.csv',
        mime='text/csv',
    )

    st.markdown("---")

    # 2. KHU VỰC CHỈNH SỬA / XÓA (Action Zone)
    st.subheader("🛠 Xử lý công việc")

    # Chọn ID để thao tác
    list_ids = df['id'].tolist()

    if list_ids:
        selected_id = st.selectbox("Chọn ID công việc để Sửa/Xóa", list_ids)

        # Tabs cho Sửa và Xóa
        tab_edit, tab_delete = st.tabs(["✏️ Cập nhật thông tin", "🗑️ Xóa công việc"])

        # --- TAB SỬA ---
        with tab_edit:
            # Lấy thông tin cũ
            task_data = db_funcs.get_task_by_id(selected_id)
            if task_data:
                with st.form("edit_form"):
                    # task_data trả về tuple: (id, name, status, date, assignee, notes)
                    # Index: 0=id, 1=name, 2=status, 3=date, 4=assignee, 5=notes
                    new_name = st.text_input("Tên công việc", value=task_data[1])
                    new_assignee = st.text_input("Người phụ trách", value=task_data[4])

                    # Xử lý ngày tháng (chuyển từ string trong db về dạng date object)
                    try:
                        curr_date = datetime.strptime(task_data[3], '%Y-%m-%d').date()
                    except:
                        curr_date = date.today()

                    new_date = st.date_input("Hạn chót", value=curr_date)

                    # Tìm index của status cũ để set default cho selectbox
                    status_opts = ["Chưa bắt đầu", "Đang làm", "Hoàn thành"]
                    try:
                        idx_status = status_opts.index(task_data[2])
                    except:
                        idx_status = 0
                    new_status = st.selectbox("Trạng thái", status_opts, index=idx_status)

                    new_notes = st.text_area("Ghi chú", value=task_data[5])

                    if st.form_submit_button("Cập nhật"):
                        db_funcs.update_task(selected_id, new_name, new_status, new_date, new_assignee, new_notes)
                        st.success("Cập nhật thành công! Hãy reload lại trang.")
                        st.rerun()  # Tự động load lại trang

        # --- TAB XÓA ---
        with tab_delete:
            st.warning(f"Bạn có chắc muốn xóa công việc có ID = {selected_id} không?")
            if st.button("Xác nhận Xóa"):
                db_funcs.delete_task(selected_id)
                st.success("Đã xóa thành công!")
                st.rerun()
    else:
        st.info("Không có công việc nào để xử lý.")

# =========================================================
# CHỨC NĂNG 3: DASHBOARD (THỐNG KÊ)
# =========================================================
elif choice == "Dashboard (Thống kê)":
    st.subheader("📊 Tổng quan tiến độ")

    df = db_funcs.load_tasks()

    if not df.empty:
        # 1. Các thẻ số liệu (Metrics)
        total = len(df)
        completed = len(df[df['status'] == 'Hoàn thành'])
        in_progress = len(df[df['status'] == 'Đang làm'])

        m1, m2, m3 = st.columns(3)
        m1.metric("Tổng công việc", total)
        m2.metric("Đã hoàn thành", completed)
        m3.metric("Đang thực hiện", in_progress)

        st.markdown("---")

        # 2. Biểu đồ tròn (Pie Chart) - Tỷ lệ hoàn thành
        # c1, c2 = st.columns(2)
        # with c1:
        #     st.write("### Tỷ lệ trạng thái")
        #     # Đếm số lượng theo trạng thái
        #     status_counts = df['status'].value_counts().reset_index()
        #     status_counts.columns = ['Trạng thái', 'Số lượng']
        #
        #     fig = px.pie(status_counts, values='Số lượng', names='Trạng thái',
        #                  color='Trạng thái',
        #                  color_discrete_map={'Hoàn thành': 'green', 'Đang làm': 'orange', 'Chưa bắt đầu': 'gray'})
        #     st.plotly_chart(fig, use_container_width=True)
        #
        # with c2:
        #     st.write("### Phân bố theo người phụ trách")
        #     if 'assignee' in df.columns:
        #         assignee_counts = df['assignee'].value_counts().reset_index()
        #         assignee_counts.columns = ['Người phụ trách', 'Số lượng']
        #         fig2 = px.bar(assignee_counts, x='Người phụ trách', y='Số lượng')
        #         st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu để thống kê.")

# Footer
st.sidebar.info("Học lập trình Python THCS")
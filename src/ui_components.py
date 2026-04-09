# Dành cho Agent/Thành viên: UI Developer
# Lịch sử commit gợi ý: "feat: add UI components for 4 UX paths"

import streamlit as st

def render_emergency_path(data):
    st.error("**CẢNH BÁO NGUY HIỂM**")
    st.write(data.get("giai_thich_ngan", "Dấu hiệu y tế khẩn cấp, vui lòng không chờ đợi!"))
    if st.button("GỌI CẤP CỨU VINMEC (115) NGAY", type="primary", use_container_width=True):
        st.error("Đang kết nối tổng đài cấp cứu...")
    st.warning("Hệ thống AI đã tạm khóa luồng tư vấn thông thường để bảo đảm an toàn.")

def render_uncertain_path(data):
    st.warning("**Hệ thống cần thêm thông tin** (Confidence: {:.0f}%)".format(data.get("confidence_score", 0)*100))
    st.write("Trợ lý AI chưa đủ dữ kiện để phân khoa chính xác. Bác sĩ AI muốn hỏi bạn:")
    cau_hoi = data.get('cau_hoi_them', '')
    if not cau_hoi:
        cau_hoi = 'Vui lòng mô tả chi tiết hơn hoặc chọn các dấu hiệu bạn đang gặp phải bên dưới:'
    st.info(f"*{cau_hoi}*")

def render_happy_path(data):
    st.success(f"**Chuyên khoa đề xuất:** {data.get('chuyen_khoa')}")
    st.progress(data.get("confidence_score", 0))
    st.caption(f"Độ tự tin của AI: {data.get('confidence_score', 0)*100}%")
    st.write(f"**Lý do:** {data.get('giai_thich_ngan')}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ĐẶT LỊCH KHÁM NGAY", type="primary", use_container_width=True):
            st.success("Ghi nhận lịch hẹn!")
    with col2:
        if st.button("Kết quả sai? Sửa triệu chứng", use_container_width=True):
            st.info("Vui lòng gõ bổ sung đính chính vào ô chat bên dưới!")

def render_error(error_msg):
    st.error(f"Lỗi hệ thống AI: {error_msg}")

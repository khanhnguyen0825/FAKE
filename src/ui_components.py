import streamlit as st
import os

# Mapping giữa tên chuyên khoa và file ảnh trong folder map
MAP_MAPPING = {
    "Cơ xương khớp": "co-xuong-khop.png",
    "Da liễu": "da-lieu.png",
    "Nội Tiêu hóa": "noi-tieu-hoa.png",
    "Răng Hàm Mặt": "rang-ham-mat.png",
    "Sản khoa": "san.png",
    "EMERGENCY": None,
}


def render_map_image(chuyen_khoa):
    """Hiển thị bản đồ chỉ đường dựa trên chuyên khoa"""
    if chuyen_khoa in ["KHÁM TỔNG QUÁT", "QUẦY LỄ TÂN"]:
        st.info("💡 **Gợi ý:** Để được hỗ trợ chính xác nhất cho triệu chứng này, mời bạn di chuyển đến **Sảnh chính Tầng 1 (Quầy Lễ Tân)** để nhân viên y tế hướng dẫn trực tiếp.")
        return

    file_name = MAP_MAPPING.get(chuyen_khoa)
    if file_name:
        map_path = os.path.join("map", file_name)
        if os.path.exists(map_path):
            st.write("---")
            st.info(f"**Bản đồ chỉ dẫn tới {chuyen_khoa}:**")
            st.image(
                map_path,
                caption=f"Sơ đồ di chuyển tới {chuyen_khoa}",
                use_container_width=True,
            )
        else:
            st.warning(f"Không tìm thấy file bản đồ: {map_path}")


def render_emergency_path(data):
    st.error("**CẢNH BÁO NGUY HIỂM**")
    st.write(
        data.get("giai_thich_ngan", "Dấu hiệu y tế khẩn cấp, vui lòng không chờ đợi!")
    )
    if st.button(
        "GỌI CẤP CỨU VINMEC (115) NGAY", type="primary", use_container_width=True
    ):
        st.error("Đang kết nối tổng đài cấp cứu...")
    st.warning("Hệ thống AI đã tạm khóa luồng tư vấn thông thường để bảo đảm an toàn.")


def render_uncertain_path(data):
    st.warning(
        "**Hệ thống cần thêm thông tin** (Confidence: {:.0f}%)".format(
            data.get("confidence_score", 0) * 100
        )
    )
    st.write(
        "Trợ lý AI chưa đủ dữ kiện để phân khoa chính xác. Bác sĩ AI muốn hỏi bạn:"
    )
    cau_hoi = data.get("cau_hoi_them", "")
    if not cau_hoi:
        cau_hoi = "Vui lòng mô tả chi tiết hơn hoặc chọn các dấu hiệu bạn đang gặp phải bên dưới:"
    st.info(f"*{cau_hoi}*")


def render_happy_path(data):
    chuyen_khoa = data.get("chuyen_khoa")

    if chuyen_khoa == "QUẦY LỄ TÂN":
        st.info("**Hướng dẫn phân luồng:** Vui lòng tới Quầy Lễ Tân để được hỗ trợ trực tiếp.")
        st.write(f"**Lý do:** {data.get('giai_thich_ngan')}")
        
        if data.get("yeu_cau_chi_duong"):
            render_map_image(chuyen_khoa)
            
        if st.button("Đã hiểu / Quay lại", use_container_width=True):
            st.info("Vui lòng gõ vào ô chat để bắt đầu một hội thoại mới.")
    else:
        st.success(f"**Chuyên khoa đề xuất:** {chuyen_khoa}")
        st.progress(data.get("confidence_score", 0))
        st.caption(f"Độ tự tin của AI: {data.get('confidence_score', 0) * 100}%")
        st.write(f"**Lý do:** {data.get('giai_thich_ngan')}")

        # Chỉ hiển thị bản đồ nếu AI xác nhận đây là yêu cầu chỉ đường (yeu_cau_chi_duong = True)
        if data.get("yeu_cau_chi_duong"):
            render_map_image(chuyen_khoa)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("ĐẶT LỊCH KHÁM NGAY", type="primary", use_container_width=True):
                st.success("Ghi nhận lịch hẹn!")
        with col2:
            if st.button("Kết quả sai? Sửa triệu chứng", use_container_width=True):
                st.info("Vui lòng gõ bổ sung đính chính vào ô chat bên dưới!")


def render_refuse_path(msg):
    st.info(f"**Phản hồi từ AI:** {msg}")


def render_error(error_msg):
    st.error(f"Lỗi hệ thống AI: {error_msg}")


def render_right_sidebar():
    """Injects a custom CSS/HTML right sidebar for instructions and tips"""

    # Clean string for Streamlit markdown
    html_code = (
        "<style>"
        "@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');"
        ".right-sidebar-container {"
        "position: fixed;"
        "right: 25px;"
        "top: 80px;"
        "width: 300px;"
        "height: 85vh;"
        "z-index: 999999;"
        "pointer-events: none;"
        "font-family: 'Outfit', sans-serif;"
        "}"
        ".sidebar-content-wrapper {"
        "pointer-events: auto;"
        "background: rgba(255, 255, 255, 0.85);"
        "backdrop-filter: blur(20px) saturate(180%);"
        "-webkit-backdrop-filter: blur(20px) saturate(180%);"
        "border: 1px solid rgba(209, 213, 219, 0.3);"
        "border-radius: 24px;"
        "padding: 24px;"
        "height: 100%;"
        "display: flex;"
        "flex-direction: column;"
        "box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);"
        "}"
        ".main-title {"
        "font-size: 1.25rem;"
        "font-weight: 700;"
        "background: linear-gradient(90deg, #1E3A8A, #3B82F6);"
        "-webkit-background-clip: text;"
        "-webkit-text-fill-color: transparent;"
        "margin-bottom: 20px;"
        "text-align: center;"
        "}"
        ".guide-section { margin-bottom: 24px; }"
        ".guide-label {"
        "font-size: 0.75rem;"
        "font-weight: 600;"
        "color: #6B7280;"
        "text-transform: uppercase;"
        "letter-spacing: 0.05em;"
        "margin-bottom: 12px;"
        "display: block;"
        "}"
        ".premium-card {"
        "background: #FFFFFF;"
        "border-radius: 16px;"
        "padding: 16px;"
        "margin-bottom: 12px;"
        "border: 1px solid #F3F4F6;"
        "box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);"
        "transition: transform 0.2s ease, box-shadow 0.2s ease;"
        "}"
        ".premium-card:hover {"
        "transform: translateY(-2px);"
        "box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);"
        "}"
        ".card-title {"
        "font-weight: 600;"
        "color: #111827;"
        "font-size: 0.95rem;"
        "margin-bottom: 4px;"
        "display: flex;"
        "align-items: center;"
        "gap: 8px;"
        "}"
        ".card-desc {"
        "color: #4B5563;"
        "font-size: 0.85rem;"
        "line-height: 1.5;"
        "}"
        ".slider-box {"
        "margin-top: auto;"
        "background: #F9FAFB;"
        "border-radius: 12px;"
        "padding: 10px;"
        "overflow: hidden;"
        "}"
        ".marquee {"
        "white-space: nowrap;"
        "overflow: hidden;"
        "display: inline-block;"
        "animation: marquee-scroll 10s linear infinite;"
        "}"
        ".marquee span {"
        "display: inline-block;"
        "padding-right: 40px;"
        "color: #3B82F6;"
        "font-weight: 500;"
        "font-size: 0.85rem;"
        "}"
        "@keyframes marquee-scroll {"
        "0% { transform: translateX(0); }"
        "100% { transform: translateX(-50%); }"
        "}"
        "@media (max-width: 1400px) {"
        ".right-sidebar-container { display: none; }"
        "}"
        "</style>"
        "<div class='right-sidebar-container'>"
        "<div class='sidebar-content-wrapper'>"
        "<div class='guide-section'>"
        "<span class='guide-label'>Hướng dẫn nhập liệu</span>"
        "<div class='premium-card'>"
        "<div class='card-title'> Mô tả chi tiết</div>"
        "<div class='card-desc'>Hãy nói mô tả bệnh mà mình mắc phải ví dụ:Tôi bị phát ban đỏ -> AI sẽ chỉ phòng da liễu.</div>"
        "</div>"
        "<div class='premium-card'>"
        "<div class='card-title'> Cung cấp ngữ cảnh</div>"
        "<div class='card-desc'>Nhập thêm các triệu chứng đi kèm như sốt, ho, hoặc buồn nôn để AI phân loại chính xác hơn.</div>"
        "</div>"
        "<div class='premium-card'>"
        "<div class='card-title'> Câu hỏi ví dụ</div>"
        "<div class='card-desc'>'Tôi bị nổi ban đỏ khắp người và ngứa ngáy, nên đi khám khoa nào?'</div>"
        "</div>"
        "</div>"
        "<div class='slider-box'>"
        "<div class='marquee'>"
        "<span>✨ Số điện thoại cấp cứu: 115</span>"
        "</div>"
        "</div>"
        "</div>"
        "</div>"
    )
    st.markdown(html_code, unsafe_allow_html=True)

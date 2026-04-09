# Dành cho Agent/Thành viên: Leader / Project Manager
# Lịch sử commit gợi ý: "feat: integrate AI triage and Streamlit UI for Demo"

import streamlit as st
import time
import json
from ai_engine import get_triage_result
from ui_components import render_emergency_path, render_uncertain_path, render_happy_path, render_error

st.set_page_config(page_title="V-Triage AI", page_icon="🏥", layout="centered")

st.title("V-Triage: TRỢ LÝ SÀNG LỌC VINMEC")
st.markdown("*Lưu ý: Hệ thống AI chỉ mang tính chất hỗ trợ gợi ý chuyên khoa, không thay thế chẩn đoán của bác sĩ.*")

st.write("---")

# Mảng lưu lịch sử chat đơn giản
if "messages" not in st.session_state:
    st.session_state.messages = []

for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        # Chỉ render giao diện rich UI (như nút bấm, form chọn) cho câu hỏi Bác Sĩ cuối cùng
        if msg["role"] == "assistant" and idx == len(st.session_state.messages) - 1:
            try:
                data = json.loads(msg["content"])
                khoa = data.get("chuyen_khoa")
                conf = float(data.get("confidence_score", 0))
                
                if data.get("error"):
                    st.markdown(msg.get("display"))
                elif khoa == "EMERGENCY":
                    render_emergency_path(data)
                elif khoa == "TỪ CHỐI":
                    render_error(data.get("giai_thich_ngan", "Yêu cầu bị từ chối."))
                elif khoa == "UNKNOWN" or conf < 0.7:
                    render_uncertain_path(data)
                    
                    # Hiện form gợi ý triệu chứng thay vì bắt user gõ
                    options = data.get("cac_lua_chon_goi_y", [])
                    if options:
                        with st.form(key=f"symptom_form_{idx}"):
                            selected = st.multiselect("Vui lòng đánh dấu các triệu chứng có liên quan:", options)
                            if st.form_submit_button("Gửi lựa chọn", type="primary"):
                                if selected:
                                    ans = "Tôi gặp các triệu chứng bổ sung: " + ", ".join(selected)
                                else:
                                    ans = "Tôi không gặp triệu chứng nào ở trên."
                                st.session_state.messages.append({"role": "user", "content": ans})
                                st.rerun()
                else:
                    render_happy_path(data)
            except:
                st.markdown(msg.get("display", msg["content"]))
        else:
            # Các tin nhắn lịch sử thì chỉ hiển thị chữ gọn nhẹ
            st.markdown(msg.get("display", msg["content"]))

user_input = st.chat_input("Mô tả chi tiết triệu chứng của bạn (ví dụ: 'Tôi bị đau răng khôn')...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Không rerun ngày, flow thẳng xuống phía dưới để Trigger AI

# Xử lý Trigger AI
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    
    # Nếu tin nhắn user vừa được add qua ô nhập (chưa đc render trong vòng for), thì vẽ tạm ra
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI đang phân tích triệu chứng..."):
            result = get_triage_result(st.session_state.messages)
            time.sleep(1) # Fake loading
            
            raw_json_str = json.dumps(result, ensure_ascii=False)
            
            if "error" in result:
                st.session_state.messages.append({"role": "assistant", "content": json.dumps({"chuyen_khoa": "TỪ CHỐI", "error": result["error"]}), "display": "Lỗi: " + result["error"]})
            else:
                khoa = result.get("chuyen_khoa")
                if khoa == "EMERGENCY":
                    st.session_state.messages.append({"role": "assistant", "content": raw_json_str, "display": f"**[CẢNH BÁO NGUY HIỂM]** {result.get('giai_thich_ngan', '')}"})
                elif khoa == "TỪ CHỐI":
                    st.session_state.messages.append({"role": "assistant", "content": raw_json_str, "display": f"{result.get('giai_thich_ngan', '')}"})
                elif khoa == "UNKNOWN" or float(result.get("confidence_score", 0)) < 0.7:
                    st.session_state.messages.append({"role": "assistant", "content": raw_json_str, "display": f"{result.get('cau_hoi_them', '')}"})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": raw_json_str, "display": f"Gợi ý khoa: **{khoa}** - {result.get('giai_thich_ngan', '')}"})
            
            st.rerun() # Refresh màn hình để kích hoạt vòng lặp vẽ rich UI ở trên cùng form checkbox

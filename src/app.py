# Dành cho Agent/Thành viên: Leader / Project Manager
# Lịch sử commit gợi ý: "feat: integrate AI triage and Streamlit UI for Demo"

import streamlit as st
import time
import json
from ai_engine import get_triage_result, transcribe_audio_bytes
from ui_components import render_emergency_path, render_uncertain_path, render_happy_path, render_error

st.set_page_config(page_title="V-Triage AI", page_icon="🏥", layout="centered")

st.title("V-Triage: TRỢ LÝ SÀNG LỌC VINMEC")
st.markdown("*Lưu ý: Hệ thống AI chỉ mang tính chất hỗ trợ gợi ý chuyên khoa, không thay thế chẩn đoán của bác sĩ.*")

st.markdown(
    """
    <style>
    /* Reserve room for the fixed prompt bar */
    section.main > div.block-container,
    div[data-testid="stAppViewBlockContainer"] > div {
        padding-bottom: 8.5rem !important;
    }

    /* Make the form wrapper invisible so it doesn't show as an extra box */
    div[data-testid="stForm"],
    div[data-testid="stForm"] > div,
    div[data-testid="stForm"] > div > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Prompt bar layout */
    div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"]:has(div[data-testid="stAudioInput"]) {
        background: color-mix(in srgb, var(--secondary-background-color) 92%, black 8%);
        border: 1px solid rgba(220, 80, 80, 0.55);
        border-radius: 12px;
        padding: 1px 6px;
        align-items: center;
        gap: 6px;
        overflow: hidden;
        width: 100%;
        max-width: 100%;
        margin-left: 0;
        margin-right: 0;
        position: fixed;
        left: 50%;
        bottom: 1.35rem;
        transform: translateX(-50%);
        width: min(46rem, calc(100vw - 1.4rem));
        max-width: calc(100vw - 1.4rem);
        z-index: 2000;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.28);
        backdrop-filter: blur(8px);
    }

    /* Remove white cards inside the connected prompt bar */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stAudioInput"]) div[data-testid="stTextInput"],
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stAudioInput"]) div[data-testid="stTextInput"] > div,
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stAudioInput"]) div[data-testid="stTextInput"] > div > div,
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stAudioInput"]) div[data-testid="stTextInput"] div[data-baseweb="input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stAudioInput"]) div[data-testid="stTextInput"] input {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        color: var(--text-color) !important;
        min-height: 28px !important;
        padding-left: 4px !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        line-height: 1.1 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stAudioInput"]) div[data-testid="stTextInput"] input::placeholder {
        color: rgba(127, 127, 127, 0.9) !important;
    }

    /* Hide helper text like "Press enter to apply" under the prompt input */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stAudioInput"]) div[data-testid="stTextInput"] p {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
    }

    div[data-testid="stAudioInput"] {
        margin-top: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    div[data-testid="stAudioInput"] > div,
    div[data-testid="stAudioInput"] > div > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    div[data-testid="stAudioInput"] button,
    div[data-testid="stButton"] button {
        border-radius: 10px !important;
        min-height: 28px !important;
        height: 28px !important;
    }

    div[data-testid="stAudioInput"] button {
        border-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    div[data-testid="stAudioInput"] button:hover,
    div[data-testid="stAudioInput"] button:focus,
    div[data-testid="stAudioInput"] button:active {
        border-color: transparent !important;
        box-shadow: none !important;
    }

    /* Prevent the send text from bleeding into the mic column */
    div[data-testid="stButton"] {
        overflow: hidden;
    }
    div[data-testid="stButton"] button {
        width: 100% !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    /* Restore the submit button to orange like before */
    div[data-testid="stButton"] button[kind="formSubmitButton"] {
        background: rgb(255, 107, 53) !important;
        color: #ffffff !important;
        border: 1px solid rgb(255, 107, 53) !important;
    }

    div[data-testid="stButton"] button[kind="formSubmitButton"]:hover,
    div[data-testid="stButton"] button[kind="formSubmitButton"]:focus,
    div[data-testid="stButton"] button[kind="formSubmitButton"]:active {
        background: rgb(235, 89, 28) !important;
        color: #ffffff !important;
        border: 1px solid rgb(235, 89, 28) !important;
        box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.write("---")

# Mảng lưu lịch sử chat đơn giản
if "messages" not in st.session_state:
    st.session_state.messages = []
if "draft_input" not in st.session_state:
    st.session_state.draft_input = ""
if "pending_draft_text" not in st.session_state:
    st.session_state.pending_draft_text = None
if "last_audio_sig" not in st.session_state:
    st.session_state.last_audio_sig = None

# Apply deferred text updates before rendering the input widget.
if st.session_state.pending_draft_text is not None:
    st.session_state.draft_input = st.session_state.pending_draft_text
    st.session_state.pending_draft_text = None

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

# Thanh nhập: text + mic + gửi trên cùng 1 hàng
with st.form(key="prompt_bar_form", clear_on_submit=True):
    input_cols = st.columns([10.6, 0.9, 0.7], vertical_alignment="center")
    with input_cols[0]:
        st.text_input(
            "Mô tả chi tiết triệu chứng của bạn",
            key="draft_input",
            placeholder="Ví dụ: Tôi bị đau răng khôn",
            label_visibility="collapsed",
        )
    with input_cols[1]:
        audio_input = st.audio_input("Mic", label_visibility="collapsed")
    with input_cols[2]:
        submitted = st.form_submit_button("➤", type="primary", use_container_width=True, help="Gửi")

if audio_input is not None:
    audio_bytes = audio_input.getvalue()
    audio_sig = hash(audio_bytes)
    if audio_sig != st.session_state.last_audio_sig:
        with st.spinner("Đang chuyển giọng nói thành văn bản..."):
            transcribed = transcribe_audio_bytes(audio_bytes)

        if "error" in transcribed:
            st.warning("Không thể chuyển giọng nói: " + transcribed["error"])
        else:
            st.session_state.pending_draft_text = transcribed.get("text", "")
            st.toast("Đã điền nội dung nói vào ô prompt.")

        st.session_state.last_audio_sig = audio_sig
        st.rerun()

submitted_input = None
if submitted:
    candidate = st.session_state.draft_input.strip()
    if candidate:
        submitted_input = candidate
        st.session_state.messages.append({"role": "user", "content": submitted_input})
    else:
        st.warning("Vui lòng nhập hoặc nói triệu chứng trước khi gửi.")

# Xử lý Trigger AI
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    
    # Nếu tin nhắn user vừa được add qua ô nhập (chưa đc render trong vòng for), thì vẽ tạm ra
    if submitted_input:
        with st.chat_message("user"):
            st.markdown(submitted_input)

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

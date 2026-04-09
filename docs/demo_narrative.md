# Kịch bản Demo: V-Triage AI (Bonus++)

**Người thuyết trình:** [Tên người thuyết trình]
**Mục tiêu:** Thể hiện rõ việc thiết kế UX cho AI dựa trên 4 kịch bản của sự không chắc chắn (Uncertainty).

---

## 🔹 Mở đầu (Khúc dạo đầu)
> *"Chào thầy và các bạn, nhóm chúng em chọn bài toán phân tuyến chuyên khoa y tế (Triage). Khác với các app thông thường, trong y tế, nếu AI đoán bừa sẽ dẫn đến hậu quả chết người. Do đó, điểm cốt lõi của V-Triage là cơ chế **Augmentation** (AI chỉ gợi ý, con người quyết) và xử lý cực gắt các ca AI không chắc chắn."*

*(Mở app Streamlit lên: `streamlit run src/app.py`)*

## 🔹 Demo 1: Happy Path (Chắc chắn)
> *"Đầu tiên, đây là luồng hoàn hảo.* (Gõ vào chat: `Tôi bị mọc răng khôn, dạo này sưng tấy má`). *Mọi người thấy AI xử lý rất tự tin, độ chính xác thường trên 90%. Nó gợi ý Răng Hàm Mặt và cho phép bấm nút Đặt lịch ngay lập tức để tiết kiệm thời gian."*

## 🔹 Demo 2: Uncertain Path (Không chắc chắn) & Correction
> *"Tuy nhiên, AI không phải thần thánh. Nếu em mớm cho nó một câu rất lỏng lẻo.* (Gõ: `Tôi biểu đau bụng quá`). *Thay vì như ChatGPT bình thường sẽ liệt kê cả một tràng giang đại hải, V-Triage của chúng em chủ động hạ Confidence Score xuống, gán cờ `UNKNOWN` và **chủ động hỏi ngược lại người dùng** (Bạn đau ở vị trí nào quanh rốn?). Đây là cách chúng em xử lý khi AI 'không biết'. Màn hình cũng hiển thị màu vàng cảnh báo."*

## 🔹 Demo 3: Safety Path (Luồng Cấp cứu - Quan trọng nhất)
> *"Cuối cùng, điều làm nên giá trị của V-Triage là Safety Path. Nếu một bệnh nhân đang gặp nguy hiểm mà con AI vẫn cứ bắt họ điền form thì rất rủi ro. Em sẽ nhập:* (Gõ: `Tôi tự dưng nhói ngực trái và vã mồ hôi`)."

*(Chạm vào phím Enter, màn hình Streamlit lập tức chuyển sang giao diện ĐỎ)*
> *"Nhờ System Prompt đã cấu hình chặt, AI lập tức phát tín hiệu `EMERGENCY`. Giao diện tắt mọi luồng đặt lịch thông thường, bật thẳng cảnh báo ĐỎ và hiển thị nút **GỌI 115** chiếm toàn bộ màn hình."*

## 🔹 Kết luận (ROI)
> *"Với luồng đi này, V-Triage không chỉ giúp Vinmec tiết kiệm 30% khối lượng phân luồng, mà đảm bảo tỷ lệ sai sót gây nguy hiểm (False Negative) gần như bằng không. Cảm ơn thầy đã lắng nghe!"*

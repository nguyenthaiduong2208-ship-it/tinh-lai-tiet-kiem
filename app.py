import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.caption("Tính toán theo lãi đơn và lãi kép")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

st.subheader("📋 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han_thang = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

loai_lai = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Chuyển đổi
    lai_suat_nam = lai_suat / 100
    lai_suat_thang = lai_suat_nam / 12

    # Thời gian gửi tính theo năm
    so_nam = ky_han_thang / 12

    # ---------------------------------
    # LÃI ĐƠN
    # ---------------------------------
    if loai_lai == "Lãi đơn":

        # Công thức:
        # I = P * r * t
        tong_lai = so_tien * lai_suat_nam * so_nam

        tong_tien = so_tien + tong_lai

        # Lãi theo kỳ nhận
        if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
            tien_lai_dinh_ky = so_tien * lai_suat_thang

        elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
            tien_lai_dinh_ky = so_tien * lai_suat_thang * 3

        else:
            tien_lai_dinh_ky = tong_lai

    # ---------------------------------
    # LÃI KÉP
    # ---------------------------------
    else:

        # Số kỳ ghép lãi
        if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
            so_ky = ky_han_thang
            lai_suat_ky = lai_suat_nam / 12

        elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
            so_ky = ky_han_thang / 3
            lai_suat_ky = lai_suat_nam / 4

        else:
            # Nếu lãnh cuối kỳ, tính theo kỳ hạn năm
            so_ky = so_nam
            lai_suat_ky = lai_suat_nam

        # Trường hợp lãnh cuối kỳ:
        # Tiền lãi được cộng dồn toàn bộ đến cuối kỳ.
        if hinh_thuc_lanh == "Lãnh lãi cuối kỳ":

            tong_tien = so_tien * (1 + lai_suat_nam) ** so_nam
            tong_lai = tong_tien - so_tien
            tien_lai_dinh_ky = tong_lai

        else:

            tong_tien = so_tien * (1 + lai_suat_ky) ** so_ky
            tong_lai = tong_tien - so_tien

            # Lãi của kỳ đầu tiên
            tien_lai_dinh_ky = so_tien * lai_suat_ky

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.success("✅ Tính toán hoàn tất!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            f"{tien_lai_dinh_ky:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            f"{tong_lai:,.0f} VNĐ"
        )

    st.metric(
        "💰 Tổng tiền gốc + lãi",
        f"{tong_tien:,.0f} VNĐ"
    )

    st.divider()

    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================

    st.subheader("📝 Thông tin khoản gửi")

    st.write(f"**Số tiền gửi:** {so_tien:,.0f} VNĐ")
    st.write(f"**Kỳ hạn:** {ky_han_thang} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức tính:** {loai_lai}")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_lanh}")

    # =========================
    # GIẢI THÍCH
    # =========================

    with st.expander("📚 Xem công thức tính"):

        if loai_lai == "Lãi đơn":

            st.markdown("""
            **Công thức lãi đơn:**

            **Tiền lãi = Tiền gốc × Lãi suất × Thời gian**

            Trong đó:

            - Tiền gốc = số tiền gửi ban đầu
            - Lãi suất = lãi suất theo năm
            - Thời gian = số năm gửi

            Lãi không được cộng vào tiền gốc để tiếp tục sinh lãi.
            """)

        else:

            st.markdown("""
            **Công thức lãi kép:**

            **Tổng tiền = Tiền gốc × (1 + lãi suất kỳ)ⁿ**

            Trong đó:

            - Tiền gốc = số tiền gửi ban đầu
            - Lãi suất kỳ = lãi suất tương ứng với mỗi kỳ nhập lãi
            - n = số kỳ nhập lãi

            Phần lãi của mỗi kỳ được cộng vào tiền gốc
            và tiếp tục sinh lãi ở các kỳ sau.
            """)

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "💡 Công cụ mang tính chất tham khảo. "
    "Lãi suất thực tế của ngân hàng có thể áp dụng quy định và phương pháp tính khác."
)

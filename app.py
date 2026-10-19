
import streamlit as st

st.set_page_config(
    page_title="Tiny Farm 🌱",
    page_icon="🌱",
    layout="centered"
)

# ---------- KHỞI TẠO GAME ----------
if "farm" not in st.session_state:
    st.session_state.farm = [
        {"crop": None, "age": 0, "water": False}
        for _ in range(9)
    ]
    st.session_state.coins = 20
    st.session_state.seeds = 3
    st.session_state.harvest = 0
    st.session_state.day = 1
    st.session_state.message = "Chào mừng đến với nông trại!"

farm = st.session_state.farm

st.title("🌱 Tiny Farm")
st.caption("Một góc vườn nhỏ, một ngày bình yên.")

# ---------- THANH THÔNG TIN ----------
a, b, c = st.columns(3)
a.metric("🪙 Tiền", st.session_state.coins)
b.metric("🌰 Hạt giống", st.session_state.seeds)
c.metric("🥕 Cà rốt", st.session_state.harvest)

st.info(f"☀️ Ngày {st.session_state.day} · {st.session_state.message}")

st.subheader("🌿 Khu vườn của bạn")
st.write("Chọn một ô đất để trồng, tưới hoặc thu hoạch.")

# ---------- KHU VƯỜN ----------
icons = {
    None: "🟫",
    "carrot": "🌱"
}

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        i = row * 3 + col
        plot = farm[i]

        if plot["crop"] is None:
            label = "🟫\nĐất trống"
        elif plot["age"] >= 3:
            label = "🥕\nThu hoạch!"
        elif plot["water"]:
            label = "💧🌿\nĐang lớn"
        else:
            label = "🌱\nCây non"

        if cols[col].button(label, key=f"plot_{i}", use_container_width=True):
            st.session_state.selected = i

# ---------- THAO TÁC VỚI Ô ĐẤT ----------
if "selected" not in st.session_state:
    st.session_state.selected = 0

idx = st.session_state.selected
plot = farm[idx]

st.divider()
st.subheader(f"🪴 Ô đất số {idx + 1}")

if plot["crop"] is None:
    st.write("Ô đất đang trống.")
    if st.button(
        "🌰 Gieo cà rốt",
        disabled=st.session_state.seeds <= 0,
        use_container_width=True
    ):
        plot["crop"] = "carrot"
        plot["age"] = 0
        plot["water"] = False
        st.session_state.seeds -= 1
        st.session_state.message = "Bạn đã gieo một hạt cà rốt!"
        st.rerun()

else:
    if plot["age"] >= 3:
        st.write("🥕 Cà rốt đã chín, có thể thu hoạch.")
        if st.button("🧺 Thu hoạch", use_container_width=True):
            plot["crop"] = None
            plot["age"] = 0
            plot["water"] = False
            st.session_state.harvest += 1
            st.session_state.message = "Thu hoạch thành công!"
            st.rerun()
    else:
        st.write(f"🌱 Giai đoạn phát triển: {plot['age']}/3")
        if not plot["water"]:
            if st.button("💧 Tưới nước", use_container_width=True):
                plot["water"] = True
                st.session_state.message = "Đã tưới cây. Hãy qua ngày để cây lớn!"
                st.rerun()
        else:
            st.success("Cây đã được tưới nước.")

# ---------- QUA NGÀY ----------
st.divider()
st.subheader("🌤️ Chăm sóc nông trại")

if st.button("🌞 Kết thúc ngày", use_container_width=True):
    for plot in farm:
        if plot["crop"] is not None and plot["water"]:
            plot["age"] = min(3, plot["age"] + 1)
            plot["water"] = False

    st.session_state.day += 1
    st.session_state.message = "Một ngày mới bắt đầu!"
    st.rerun()

# ---------- CỬA HÀNG ----------
st.divider()
st.subheader("🏡 Cửa hàng nông trại")
st.write("🌰 Hạt cà rốt — 5 xu/gói")

if st.button(
    "Mua 1 gói hạt giống (5 xu)",
    disabled=st.session_state.coins < 5,
    use_container_width=True
):
    st.session_state.coins -= 5
    st.session_state.seeds += 1
    st.session_state.message = "Bạn đã mua một gói hạt giống!"
    st.rerun()

if st.button(
    "💰 Bán 1 cà rốt (+10 xu)",
    disabled=st.session_state.harvest < 1,
    use_container_width=True
):
    st.session_state.harvest -= 1
    st.session_state.coins += 10
    st.session_state.message = "Đã bán cà rốt và nhận 10 xu!"
    st.rerun()

st.caption("Tiny Farm · Phiên bản thử nghiệm 0.1")

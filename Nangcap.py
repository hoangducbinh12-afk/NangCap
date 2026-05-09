import streamlit as st
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN CHUẨN APP CŨ ---
st.set_page_config(page_title="HỆ THỐNG ROOT 18 BIẾN PRO", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; max-width: 600px !important; }
    .stButton>button { width: 100%; border-radius: 5px; height: 35px; }
    .main-title { text-align: center; font-size: 22px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    .dan-box-1 { background-color: #e8f5e9; padding: 10px; border-radius: 5px; border: 1px solid #c8e6c9; color: #2e7d32; font-family: monospace; font-weight: bold; margin-bottom: 5px; font-size: 13px; }
    .dan-box-2 { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #bbdefb; color: #1565c0; font-family: monospace; font-weight: bold; margin-bottom: 5px; font-size: 13px; }
    .root-display { text-align: center; background: #fafafa; padding: 8px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 15px; font-weight: bold; color: #d32f2f; font-size: 12px; }
    .stTable td, .stTable th { font-size: 10px !important; padding: 1px !important; text-align: center !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU ROOT ---
ROOT_DATA = {
    1: {"chạm": [1,6,0,5,2,7,3,8,4,9], "đầu": [1,6,0,5,4,9,2,7,3,8], "đuôi": [1,6,2,7,0,5,4,9,3,8], "tổng": [1,6,2,7,4,9,0,5,3,8], "hiệu": [0,5,1,6,2,7,4,9,3,8]},
    2: {"chạm": [2,7,1,6,3,8,4,9,0,5], "đầu": [2,7,1,6,5,0,3,8,4,9], "đuôi": [2,7,3,8,1,6,5,0,4,9], "tổng": [2,7,3,8,5,0,1,6,4,9], "hiệu": [0,5,2,7,1,6,3,8,4,9]},
    3: {"chạm": [3,8,2,7,4,9,0,5,1,6], "đầu": [3,8,2,7,6,1,4,9,5,0], "đuôi": [3,8,4,9,2,7,6,1,5,0], "tổng": [3,8,4,9,1,6,2,7,0,5], "hiệu": [0,5,3,8,4,9,1,6,2,7]},
    4: {"chạm": [4,9,3,8,0,5,1,6,2,7], "đầu": [4,9,3,8,7,2,5,0,6,1], "đuôi": [4,9,5,0,3,8,7,2,6,1], "tổng": [4,9,0,5,2,7,1,6,3,8], "hiệu": [0,5,4,9,1,6,2,7,3,8]},
    5: {"chạm": [5,0,4,9,2,7,1,6,3,8], "đầu": [5,0,2,7,3,8,4,9,1,6], "đuôi": [5,0,4,9,1,6,2,7,3,8], "tổng": [5,0,8,3,2,7,4,9,1,6], "hiệu": [0,5,1,6,4,9,2,7,3,8]},
    6: {"chạm": [6,1,5,0,3,8,2,7,4,9], "đầu": [6,1,5,0,9,4,7,2,8,3], "đuôi": [6,1,7,2,5,0,9,4,8,3], "tổng": [6,1,9,4,3,8,5,0,2,7], "hiệu": [0,5,1,6,2,7,3,8,4,9]},
    7: {"chạm": [7,2,6,1,4,9,3,8,0,5], "đầu": [7,2,6,1,0,5,8,3,9,4], "đuôi": [7,2,8,3,6,1,0,5,9,4], "tổng": [7,2,0,5,4,9,6,1,3,8], "hiệu": [0,5,2,7,3,8,4,9,1,6]},
    8: {"chạm": [8,3,7,2,5,0,4,9,1,6], "đầu": [8,3,7,2,1,6,9,4,0,5], "đuôi": [8,3,9,4,7,2,1,6,0,5], "tổng": [8,3,1,6,5,0,7,2,4,9], "hiệu": [0,5,3,8,2,7,1,6,4,9]},
    9: {"chạm": [9,4,8,3,6,1,5,0,2,7], "đầu": [9,4,8,3,2,7,0,5,1,6], "đuôi": [9,4,0,5,8,3,2,7,1,6], "tổng": [9,4,2,7,6,1,8,3,5,0], "hiệu": [0,5,4,9,3,8,2,7,1,6]}
}

BO_MAP = {"00":[0,5,50,55],"01":[1,10,6,60,51,15,56,65],"02":[2,20,7,70,52,25,57,75],"03":[3,30,8,80,53,35,58,85],"04":[4,40,9,90,54,45,59,95],"11":[11,16,61,66],"12":[12,21,17,71,62,26,67,76],"13":[13,31,18,81,63,36,68,86],"14":[14,41,19,91,64,46,69,96],"22":[22,27,72,77],"23":[23,32,28,82,73,37,78,87],"24":[24,42,29,92,74,47,79,97],"33":[33,38,83,88],"34":[34,43,39,93,84,48,89,98],"44":[44,49,94,99]}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]

def get_root(s):
    try:
        nums = [int(x) for x in str(s) if x.isdigit()]
        if not nums: return 0
        t = sum(nums)
        while t > 9: t = sum(int(x) for x in str(t))
        return t
    except: return 0

def find_idx(n, mapping):
    for i, nums in enumerate(mapping.values()):
        if n in nums: return i
    return 0

# --- KHỞI TẠO ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    st.session_state.bo = [0]*15
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0, 0]
    st.session_state.ls, st.session_state.db, st.session_state.ky_in = [], {}, 1
    st.session_state.num_1, st.session_state.num_2 = 10, 36
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

def cap_nhat():
    raw = st.session_state.gdb_in
    if not raw or len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv = n//10, n%10
    st.session_state.rd, st.session_state.rk, st.session_state.rg = get_root(st.session_state.date_in), get_root(st.session_state.ky_in), get_root(raw)
    
    # Update Khan
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==((dv+duv)%10) else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==((dv-duv+10)%10) else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- UI CHÍNH ---
st.markdown("<div class='main-title'>💎 HỆ THỐNG THỐNG KÊ 18 BIẾN PRO</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("💾 SAO LƯU CLOUD")
    if st.button("LƯU BẢN SAO MỚI"):
        st.session_state.db[datetime.now().strftime("%H:%M:%S")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k not in ['db']}
        st.toast("Đã lưu!")
    if st.session_state.db:
        sel = st.selectbox("Bản lưu:", list(st.session_state.db.keys())[::-1])
        if st.button("HỒI PHỤC DỮ LIỆU"):
            for k, v in st.session_state.db[sel].items(): st.session_state[k] = v
            st.rerun()
    st.divider()
    if st.button("RESET TẤT CẢ", type="primary"): st.session_state.clear(); st.rerun()

# --- NHẬP LIỆU ---
c1, c2, c3 = st.columns([1.5, 1.5, 1.2])
with c1: st.text_input("GĐB vừa nổ:", value="000000", key="gdb_in")
with c2: st.text_input("Ngày (ddmmyyyy):", value="09092009", key="date_in")
with c3:
    st.write("Kỳ quay:")
    ck1, ck2, ck3 = st.columns([1, 2, 1])
    with ck1: 
        if st.button("➖"): st.session_state.ky_in -= 1
    with ck2: st.session_state.ky_in = st.number_input("K", value=st.session_state.ky_in, label_visibility="collapsed")
    with ck3: 
        if st.button("➕"): st.session_state.ky_in += 1

st.markdown(f"<div class='root-display'>Root Ngày: {st.session_state.rd} | Root Kỳ: {st.session_state.rk} | Root GĐB: {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🚀 CẬP NHẬT TỔNG LỰC", on_click=cap_nhat, type="primary", use_container_width=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚡ Lọc Dàn", "📊 Bảng A", "🔢 Kiểm Root", "🎲 Ma Trận B", "🛠️ Sửa Tay"])

with tab1:
    cn1, cn2 = st.columns(2)
    with cn1: num_1 = st.number_input("Dàn 1:", 1, 100, 10, key="n1")
    with cn2: num_2 = st.number_input("Dàn 2:", 1, 100, 36, key="n2")
    
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    f_list = []
    for i in range(100):
        d, du, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.so_he[1 if i not in SO_THUONG else 0]
        def gs(r, c, v): return ROOT_DATA[r][c].index(v) if r in ROOT_DATA else 0
        sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("đầu",d),("đuôi",du),("tổng",t),("hiệu",h),("chạm",d),("chạm",du)])
        f_list.append({"s": f"{d}{du}", "d": sk + sr})
    df_f = pd.DataFrame(f_list).sort_values(by=["d", "s"], ascending=[True, True])
    
    d1_s, d2_s = ", ".join(df_f.head(num_1)["s"].tolist()), ", ".join(df_f.head(num_2)["s"].tolist())
    st.markdown(f"<div class='dan-box-1'>{d1_s}</div>", unsafe_allow_html=True)
    if st.button("📋 Copy Dàn 1"): st.write(f'<script>navigator.clipboard.writeText("{d1_s}")</script>', unsafe_allow_html=True); st.toast("Dàn 1")
    st.markdown(f"<div class='dan-box-2'>{d2_s}</div>", unsafe_allow_html=True)
    if st.button("📋 Copy Dàn 2"): st.write(f'<script>navigator.clipboard.writeText("{d2_s}")</script>', unsafe_allow_html=True); st.toast("Dàn 2")

with tab2:
    st.write("**BẢNG A: CHI TIẾT KHAN (K) & ROOT (R)**")
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    for lbl, k, cat in [("ĐẦU","dau","đầu"),("ĐUÔI","duoi","đuôi"),("TỔNG","tong","tổng"),("HIỆU","hieu","hiệu"),("CHẠM","cham","chạm")]:
        khan = st.session_state[k]
        roots = [sum(ROOT_DATA[r][cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) for i in range(10)]
        st.write(f"*{lbl}*")
        st.table(pd.DataFrame([khan, roots], columns=[str(x) for x in range(10)], index=["K", "R"]))
    st.write("*8 BIẾN PHỤ*")
    st.table(pd.DataFrame({"DAU C/L": st.session_state.d_cl, "DUOI C/L": st.session_state.u_cl, "HE SO": st.session_state.so_he}, index=["0/CHAN/THG", "1/LE/HE"]))

with tab3:
    for n, rv in [("NGÀY", st.session_state.rd), ("KỲ", st.session_state.rk), ("GĐB", st.session_state.rg)]:
        if rv in ROOT_DATA:
            st.write(f"**MÃ ROOT {n}: {rv}**")
            ck = {cat: [ROOT_DATA[rv][cat].index(i) for i in range(10)] for cat in ["đầu","đuôi","tổng","hiệu","chạm"]}
            st.table(pd.DataFrame(ck, index=[str(x) for x in range(10)]).T)

with tab4:
    m_data = [[next(x for x in f_list if x["s"] == f"{d}{du}")["d"] for du in range(10)] for d in range(10)]
    st.table(pd.DataFrame(m_data, columns=[str(i) for i in range(10)], index=[str(i) for i in range(10)]))

with tab5:
    st.write("**SỬA TAY KHAN**")
    ca, cb = st.columns(2)
    with ca:
        for i in range(10): st.session_state.dau[i] = st.number_input(f"Dau {i}", value=st.session_state.dau[i], key=f"s_d_{i}")
    with cb:
        for i in range(10): st.session_state.duoi[i] = st.number_input(f"Duoi {i}", value=st.session_state.duoi[i], key=f"s_u_{i}")

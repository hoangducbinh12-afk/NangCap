import streamlit as st
import pandas as pd
from datetime import datetime

# --- CAU HINH GIAO DIEN (DỰA TRÊN APP TOÀN DIỆN) ---
st.set_page_config(page_title="18 BIẾN PRO - TOÀN DIỆN", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 650px !important; padding-top: 1rem !important; }
    .stTable td, .stTable th { font-size: 11px !important; padding: 2px !important; text-align: center !important; font-weight: bold !important; border: 1px solid #eee !important; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 20px; font-weight: bold; margin-bottom: 10px; }
    .root-label { font-size: 11px; font-weight: bold; color: #d32f2f; text-align: center; background: #fff5f5; padding: 5px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #ffe3e3; }
    .dan-box-1 { background-color: #e8f5e9; padding: 10px; border-radius: 5px; border: 1px solid #c8e6c9; color: #2e7d32; font-family: monospace; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    .dan-box-2 { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #bbdefb; color: #1565c0; font-family: monospace; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    .stTabs [data-baseweb="tab"] { padding: 8px 10px; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU ROOT ---
ROOT_DATA = {
    1: {"cham": [1,6,0,5,2,7,3,8,4,9], "dau": [1,6,0,5,4,9,2,7,3,8], "duoi": [1,6,2,7,0,5,4,9,3,8], "tong": [1,6,2,7,4,9,0,5,3,8], "hieu": [0,5,1,6,2,7,4,9,3,8]},
    2: {"cham": [2,7,1,6,3,8,4,9,0,5], "dau": [2,7,1,6,5,0,3,8,4,9], "duoi": [2,7,3,8,1,6,5,0,4,9], "tong": [2,7,3,8,5,0,1,6,4,9], "hieu": [0,5,2,7,1,6,3,8,4,9]},
    3: {"cham": [3,8,2,7,4,9,0,5,1,6], "dau": [3,8,2,7,6,1,4,9,5,0], "duoi": [3,8,4,9,2,7,6,1,5,0], "tong": [3,8,4,9,1,6,2,7,0,5], "hieu": [0,5,3,8,4,9,1,6,2,7]},
    4: {"cham": [4,9,3,8,0,5,1,6,2,7], "dau": [4,9,3,8,7,2,5,0,6,1], "duoi": [4,9,5,0,3,8,7,2,6,1], "tong": [4,9,0,5,2,7,1,6,3,8], "hieu": [0,5,4,9,1,6,2,7,3,8]},
    5: {"cham": [5,0,4,9,2,7,1,6,3,8], "dau": [5,0,2,7,3,8,4,9,1,6], "duoi": [5,0,4,9,1,6,2,7,3,8], "tong": [5,0,8,3,2,7,4,9,1,6], "hieu": [0,5,1,6,4,9,2,7,3,8]},
    6: {"cham": [6,1,5,0,3,8,2,7,4,9], "dau": [6,1,5,0,9,4,7,2,8,3], "duoi": [6,1,7,2,5,0,9,4,8,3], "tong": [6,1,9,4,3,8,5,0,2,7], "hieu": [0,5,1,6,2,7,3,8,4,9]},
    7: {"cham": [7,2,6,1,4,9,3,8,0,5], "dau": [7,2,6,1,0,5,8,3,9,4], "duoi": [7,2,8,3,6,1,0,5,9,4], "tong": [7,2,0,5,4,9,6,1,3,8], "hieu": [0,5,2,7,3,8,4,9,1,6]},
    8: {"cham": [8,3,7,2,5,0,4,9,1,6], "dau": [8,3,7,2,1,6,9,4,0,5], "duoi": [8,3,9,4,7,2,1,6,0,5], "tong": [8,3,1,6,5,0,7,2,4,9], "hieu": [0,5,3,8,2,7,1,6,4,9]},
    9: {"cham": [9,4,8,3,6,1,5,0,2,7], "dau": [9,4,8,3,2,7,0,5,1,6], "duoi": [9,4,0,5,8,3,2,7,1,6], "tong": [9,4,2,7,6,1,8,3,5,0], "hieu": [0,5,4,9,3,8,2,7,1,6]}
}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]

# --- HELPER ---
def get_root(s):
    try:
        t = sum(int(x) for x in str(s) if x.isdigit())
        while t > 9: t = sum(int(x) for x in str(t))
        return t
    except: return 0

# --- KHỞI TẠO STATE ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0, 0]
    st.session_state.ls, st.session_state.db, st.session_state.ky_quay = [], {}, 1
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

def cap_nhat_logic():
    raw = st.session_state.gdb_in
    if not raw or len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv = n//10, n%10
    tv, hv = (dv + duv) % 10, (dv - duv + 10) % 10
    
    st.session_state.rd = get_root(st.session_state.date_in)
    st.session_state.rk = get_root(st.session_state.ky_quay)
    st.session_state.rg = get_root(raw)
    
    # Cập nhật điểm Khan
    for i in range(10):
        st.session_state.dau[i] = 0 if i == dv else st.session_state.dau[i] + 1
        st.session_state.duoi[i] = 0 if i == duv else st.session_state.duoi[i] + 1
        st.session_state.tong[i] = 0 if i == tv else st.session_state.tong[i] + 1
        st.session_state.hieu[i] = 0 if i == hv else st.session_state.hieu[i] + 1
        st.session_state.cham[i] = 0 if (i == dv or i == duv) else st.session_state.cham[i] + 1
    
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.t_cl[tv%2]=0; st.session_state.t_cl[(tv+1)%2]+=1
    st.session_state.d_tb[1 if dv>=5 else 0]=0; st.session_state.d_tb[0 if dv>=5 else 1]+=1
    st.session_state.u_tb[1 if duv>=5 else 0]=0; st.session_state.u_tb[0 if duv>=5 else 1]+=1
    st.session_state.t_tb[1 if tv>=5 else 0]=0; st.session_state.t_tb[0 if tv>=5 else 1]+=1
    st.session_state.h_tb[1 if hv>=5 else 0]=0; st.session_state.h_tb[0 if hv>=5 else 1]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- UI CHÍNH ---
st.markdown("<div class='main-title'>💎 HỆ THỐNG THỐNG KÊ 18 BIẾN PRO</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ QUẢN LÝ")
    if st.button("💾 LƯU BẢN SAO", use_container_width=True):
        st.session_state.db[datetime.now().strftime("%H:%M:%S")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k not in ['db']}
        st.toast("Đã lưu!")
    if st.session_state.db:
        sel = st.selectbox("Chọn bản lưu:", list(st.session_state.db.keys())[::-1])
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("🚀 NẠP"):
                for k, v in st.session_state.db[sel].items(): st.session_state[k] = v
                st.rerun()
        with c2: 
            if st.button("🗑️ XÓA"): del st.session_state.db[sel]; st.rerun()
    st.divider()
    if st.button("❌ RESET ALL", type="primary", use_container_width=True): st.session_state.clear(); st.rerun()

# NHẬP LIỆU
col1, col2, col3 = st.columns([1, 1, 0.8])
with col1: st.text_input("GĐB vừa nổ:", value="000000", key="gdb_in")
with col2: st.text_input("Ngày:", value="09092009", key="date_in")
with col3: st.number_input("Kỳ quay:", value=st.session_state.ky_quay, step=1, key="ky_quay")

st.markdown(f"<div class='root-label'>Root Ngày: {st.session_state.rd} | Root Kỳ: {st.session_state.rk} | Root GĐB: {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🔥 CẬP NHẬT TỔNG LỰC", on_click=cap_nhat_logic, type="primary", use_container_width=True)

t1, t2, t3, t4, t5 = st.tabs(["⚡ Lọc Dàn", "📊 Bảng A", "🔢 Kiểm Tra Root", "🎲 Ma Trận B", "🛠️ Sửa Tay"])

with t1:
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    calc = []
    for i in range(100):
        d, du, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.t_cl[t%2]+st.session_state.d_tb[1 if d>=5 else 0]+st.session_state.u_tb[1 if du>=5 else 0]+st.session_state.t_tb[1 if t>=5 else 0]+st.session_state.h_tb[1 if h>=5 else 0]+st.session_state.so_he[1 if i not in SO_THUONG else 0]
        def gs(r, c, v): return ROOT_DATA[r][c].index(v) if r in ROOT_DATA else 0
        sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        calc.append({"s": f"{d}{du}", "d": sk + sr})
    df_s = pd.DataFrame(calc).sort_values(by=["d", "s"])
    
    ca, cb = st.columns(2)
    with ca:
        n1 = st.number_input("Dàn 1:", 1, 100, 10)
        d1 = ", ".join(df_s.head(int(n1))["s"].tolist())
        st.markdown(f"<div class='dan-box-1'>{d1}</div>", unsafe_allow_html=True)
        if st.button("📋 COPY D1"): st.write(f'<script>navigator.clipboard.writeText("{d1}")</script>', unsafe_allow_html=True); st.toast("D1")
    with cb:
        n2 = st.number_input("Dàn 2:", 1, 100, 36)
        d2 = ", ".join(df_s.head(int(n2))["s"].tolist())
        st.markdown(f"<div class='dan-box-2'>{d2}</div>", unsafe_allow_html=True)
        if st.button("📋 COPY D2"): st.write(f'<script>navigator.clipboard.writeText("{d2}")</script>', unsafe_allow_html=True); st.toast("D2")

with t2:
    st.write("**BẢNG A: ĐIỂM TỔNG HỢP (KHAN + ROOT)**")
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    
    def get_row(key, cat):
        return [st.session_state[key][i] + sum(ROOT_DATA[r][cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) for i in range(10)]
    
    # 10 Biến chính
    rows = {
        "DAU": get_row("dau", "dau"), "DUOI": get_row("duoi", "duoi"),
        "TONG": get_row("tong", "tong"), "HIEU": get_row("hieu", "hieu"), "CHAM": get_row("cham", "cham")
    }
    st.table(pd.DataFrame(rows).T)
    
    # 8 Biến phụ
    st.write("**8 BIẾN PHỤ 50/50 (KHÔNG DẤU)**")
    sub_rows = {
        "DAU C/L": st.session_state.d_cl + [0]*8, "DUOI C/L": st.session_state.u_cl + [0]*8,
        "TONG C/L": st.session_state.t_cl + [0]*8, "DAU B/T": st.session_state.d_tb + [0]*8,
        "DUOI B/T": st.session_state.u_tb + [0]*8, "TONG B/T": st.session_state.t_tb + [0]*8,
        "HIEU B/T": st.session_state.h_tb + [0]*8, "SO HE": st.session_state.so_he + [0]*8
    }
    st.table(pd.DataFrame(sub_rows).T.iloc[:, :2].rename(columns={0: "0/BE/THG", 1: "1/LE/HE"}))

with t3:
    for n, rv in [("NGAY", st.session_state.rd), ("KY", st.session_state.rk), ("GDB", st.session_state.rg)]:
        if rv in ROOT_DATA:
            st.write(f"**ROOT {n}: {rv}**")
            ck = {cat: [ROOT_DATA[rv][cat].index(i) for i in range(10)] for cat in ["dau","duoi","tong","hieu","cham"]}
            st.table(pd.DataFrame(ck).T)

with t4:
    m_data = [[next(x for x in calc if x["s"] == f"{d}{du}")["d"] for du in range(10)] for d in range(10)]
    st.table(pd.DataFrame(m_data, columns=[str(i) for i in range(10)], index=[str(i) for i in range(10)]))

with t5:
    st.write("**SỬA TAY KHAN**")
    for k, lbl in [('dau','Dau'),('duoi','Duoi'),('tong','Tong'),('hieu','Hieu'),('cham','Cham')]:
        with st.expander(f"Sua {lbl}"):
            cols = st.columns(5)
            for i in range(10):
                with cols[i%5]: st.session_state[k][i] = st.number_input(f"{i}", value=st.session_state[k][i], key=f"e_{k}_{i}")

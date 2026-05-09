import streamlit as st
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="18 BIEN PRO", layout="centered")

# CSS để làm đẹp giao diện mà không gây lỗi hiển thị code
st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding-top: 1rem !important; }
    .stTable td, .stTable th { font-size: 11px !important; padding: 2px !important; text-align: center !important; font-weight: bold !important; border: 1px solid #eee !important; }
    .dan-box-1 { background-color: #e8f5e9; padding: 10px; border-radius: 5px; border: 1px solid #c8e6c9; color: #2e7d32; font-family: monospace; font-size: 12px; font-weight: bold; margin-top:5px; }
    .dan-box-2 { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #bbdefb; color: #1565c0; font-family: monospace; font-size: 12px; font-weight: bold; margin-top:5px; }
    .root-label { font-size: 12px; font-weight: bold; color: #d32f2f; text-align: center; background: #fff5f5; padding: 8px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #ffe3e3; }
    div[data-testid="stExpander"] p { font-size: 13px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU ---
BO_MAP = {"00":[0,5,50,55],"01":[1,10,6,60,51,15,56,65],"02":[2,20,7,70,52,25,57,75],"03":[3,30,8,80,53,35,58,85],"04":[4,40,9,90,54,45,59,95],"11":[11,16,61,66],"12":[12,21,17,71,62,26,67,76],"13":[13,31,18,81,63,36,68,86],"14":[14,41,19,91,64,46,69,96],"22":[22,27,72,77],"23":[23,32,28,82,73,37,78,87],"24":[24,42,29,92,74,47,79,97],"33":[33,38,83,88],"34":[34,43,39,93,84,48,89,98],"44":[44,49,94,99]}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]
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

# --- LOGIC ---
def get_root(s):
    try:
        t = sum(int(x) for x in str(s) if x.isdigit())
        while t > 9: t = sum(int(x) for x in str(t))
        return t
    except: return 0

def find_idx(n, mapping):
    for i, nums in enumerate(mapping.values()):
        if n in nums: return i
    return -1

# --- KHOI TAO ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    st.session_state.bo = [0]*15
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0, 0]
    st.session_state.ls, st.session_state.db_cloud, st.session_state.ky_quay = [], {}, 1
    st.session_state.n1, st.session_state.n2 = 10, 36
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

def cap_nhat_diem():
    raw = st.session_state.gdb_in
    if not raw or len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv = n//10, n%10
    st.session_state.rd, st.session_state.rk, st.session_state.rg = get_root(st.session_state.date_in), get_root(st.session_state.ky_quay), get_root(raw)
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==((dv+duv)%10) else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==((dv-duv+10)%10) else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    for i in range(15): st.session_state.bo[i] = 0 if i==find_idx(n, BO_MAP) else st.session_state.bo[i]+1
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- UI CHÍNH ---
st.title("💎 HE THONG 18 BIEN PRO")

with st.sidebar:
    st.header("⚙️ QUAN LY")
    if st.button("💾 LUU CLOUD"):
        st.session_state.db_cloud[datetime.now().strftime("%H:%M")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k != 'db_cloud'}
    if st.session_state.db_cloud:
        sel = st.selectbox("Ban sao:", list(st.session_state.db_cloud.keys())[::-1])
        c_load, c_del = st.columns(2)
        with c_load: 
            if st.button("🚀 NAP"):
                for k, v in st.session_state.db_cloud[sel].items(): st.session_state[k] = v
                st.rerun()
        with c_del:
            if st.button("🗑️ XOA"): del st.session_state.db_cloud[sel]; st.rerun()
    if st.button("❌ RESET ALL"): st.session_state.clear(); st.rerun()

# NHẬP LIỆU
c1, c2, c3 = st.columns([1.5, 1.5, 1.2])
with c1: st.text_input("GDB vua no:", value="000000", key="gdb_in")
with c2: st.text_input("Ngay:", "09092009", key="date_in")
with c3:
    st.write("Ky:")
    ck1, ck2, ck3 = st.columns([1, 1.5, 1])
    with ck1: 
        if st.button("➖", key="km"): st.session_state.ky_quay -= 1; st.rerun()
    with ck2: st.session_state.ky_quay = st.number_input("K", value=st.session_state.ky_quay, label_visibility="collapsed")
    with ck3: 
        if st.button("➕", key="kp"): st.session_state.ky_quay += 1; st.rerun()

st.markdown(f"<div class='root-label'>Root Ngay: {st.session_state.rd} | Root Ky: {st.session_state.rk} | Root GDB: {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🔥 CAP NHAT TONG LUC", on_click=cap_nhat_diem, type="primary", use_container_width=True)

tabs = st.tabs(["⚡ Dan", "📊 Bang A", "🔢 Root", "🛠️ Sua"])

with tabs[0]:
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    calc = []
    for i in range(100):
        d, du = i//10, i%10
        def gs(r, c, v): return ROOT_DATA[r][c].index(v) if r in ROOT_DATA else 0
        sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",(d+du)%10),("hieu",(d-du+10)%10),("cham",d),("cham",du)])
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[(d+du)%10]+st.session_state.hieu[(d-du+10)%10]+((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+st.session_state.bo[find_idx(i, BO_MAP)]+st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.so_he[1 if i not in SO_THUONG else 0]
        calc.append({"s": f"{d}{du}", "d": sk + sr})
    df_f = pd.DataFrame(calc).sort_values(by=["d", "s"])
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write("Dan 1:")
        c1a, c1b, c1c = st.columns([1,1.5,1])
        with c1a: 
            if st.button("➖", key="d1m"): st.session_state.n1 -= 1; st.rerun()
        with c1b: st.session_state.n1 = st.number_input("N1", value=st.session_state.n1, label_visibility="collapsed")
        with c1c:
            if st.button("➕", key="d1p"): st.session_state.n1 += 1; st.rerun()
        d1_s = ", ".join(df_f.head(st.session_state.n1)["s"].tolist())
        st.markdown(f"<div class='dan-box-1'>{d1_s}</div>", unsafe_allow_html=True)
        if st.button("📋 COPY D1"): st.write(f'<script>navigator.clipboard.writeText("{d1_s}")</script>', unsafe_allow_html=True); st.toast("Copied D1")
    with col_d2:
        st.write("Dan 2:")
        c2a, c2b, c2c = st.columns([1,1.5,1])
        with c2a:
            if st.button("➖", key="d2m"): st.session_state.n2 -= 1; st.rerun()
        with c2b: st.session_state.n2 = st.number_input("N2", value=st.session_state.n2, label_visibility="collapsed")
        with c2c:
            if st.button("➕", key="d2p"): st.session_state.n2 += 1; st.rerun()
        d2_s = ", ".join(df_f.head(st.session_state.n2)["s"].tolist())
        st.markdown(f"<div class='dan-box-2'>{d2_s}</div>", unsafe_allow_html=True)
        if st.button("📋 COPY D2"): st.write(f'<script>navigator.clipboard.writeText("{d2_s}")</script>', unsafe_allow_html=True); st.toast("Copied D2")

with tabs[1]:
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    def show_r(lbl, k, cat, names):
        st.write(f"**{lbl}**")
        khan = st.session_state[k]
        rt = [sum(ROOT_DATA[r][cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) for i in range(10)] if cat else [0]*len(khan)
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        st.table(pd.DataFrame([khan, rt], columns=names, index=["K", "R"]))
        st.markdown('</div>', unsafe_allow_html=True)

    for lbl, k, cat in [("DAU","dau","dau"),("DUOI","duoi","duoi"),("TONG","tong","tong"),("HIEU","hieu","hieu"),("CHAM","cham","cham")]:
        show_r(lbl, k, cat, range(10))
    
    st.write("**8 BIEN PHU 50/50**")
    st.table(pd.DataFrame({"DAU C/L":st.session_state.d_cl, "DUOI C/L":st.session_state.u_cl, "HE SO":st.session_state.so_he}, index=["0/CHAN/THG","1/LE/HE"]))

with tabs[2]:
    for n, rv in [("NGAY", rd), ("KY", rk), ("GDB", rg)]:
        if rv in ROOT_DATA:
            st.write(f"**ROOT {n}: {rv}**")
            ck = {cat: [ROOT_DATA[rv][cat].index(i) for i in range(10)] for cat in ["dau","duoi","tong","hieu","cham"]}
            st.table(pd.DataFrame(ck).T)

with tabs[3]:
    st.write("**SUA TAY 18 BIEN (KHONG DAU)**")
    if st.button("💾 LUU TAT CA"): st.rerun()
    for k, lbl in [('dau','DAU'),('duoi','DUOI'),('tong','TONG'),('hieu','HIEU'),('cham','CHAM')]:
        with st.expander(f"SUA {lbl}"):
            cols = st.columns(5)
            for i in range(10):
                with cols[i%5]: st.session_state[k][i] = st.number_input(f"{i}", value=st.session_state[k][i], key=f"e_{k}_{i}")
    with st.expander("SUA 8 BIEN PHU"):
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.session_state.d_cl = [st.number_input("DAU CHAN", value=st.session_state.d_cl[0]), st.number_input("DAU LE", value=st.session_state.d_cl[1])]
            st.session_state.so_he = [st.number_input("THUONG", value=st.session_state.so_he[0]), st.number_input("HE", value=st.session_state.so_he[1])]

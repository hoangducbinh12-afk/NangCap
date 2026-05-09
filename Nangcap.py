import streamlit as st
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN MOBILE FIRST ---
st.set_page_config(page_title="18 BIEN PRO - TOAN DIEN", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 500px !important; padding-top: 1rem !important; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 18px; font-weight: bold; margin-bottom: 10px; display: block !important; }
    .stTable td, .stTable th { font-size: 10px !important; padding: 1px !important; text-align: center !important; font-weight: bold !important; border: 1px solid #f0f0f0 !important; }
    .dan-box-1 { background-color: #e8f5e9; padding: 8px; border-radius: 4px; border: 1px solid #c8e6c9; color: #2e7d32; font-family: monospace; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
    .dan-box-2 { background-color: #e3f2fd; padding: 8px; border-radius: 4px; border: 1px solid #bbdefb; color: #1565c0; font-family: monospace; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
    .root-label { font-size: 11px; font-weight: bold; color: #d32f2f; text-align: center; background: #fff5f5; padding: 5px; border-radius: 5px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU BẢN ĐỒ ---
BO_MAP = {"00":[0,5,50,55],"01":[1,10,6,60,51,15,56,65],"02":[2,20,7,70,52,25,57,75],"03":[3,30,8,80,53,35,58,85],"04":[4,40,9,90,54,45,59,95],"11":[11,16,61,66],"12":[12,21,17,71,62,26,67,76],"13":[13,31,18,81,63,36,68,86],"14":[14,41,19,91,64,46,69,96],"22":[22,27,72,77],"23":[23,32,28,82,73,37,78,87],"24":[24,42,29,92,74,47,79,97],"33":[33,38,83,88],"34":[34,43,39,93,84,48,89,98],"44":[44,49,94,99]}
GIAP_MAP = {"Ty":[0,12,24,36,48,60,72,84,96],"Suu":[1,13,25,37,49,61,73,85,97],"Dan":[2,14,26,38,50,62,74,86,98],"Mao":[3,15,27,39,51,63,75,87,99],"Thin":[4,16,28,40,52,64,76,88],"Ty.":[5,17,29,41,53,65,77,89],"Ngo":[6,18,30,42,54,66,78,90],"Mui":[7,19,31,43,55,67,79,91],"Than":[8,20,32,44,56,68,80,92],"Dau":[9,21,33,45,57,69,81,93],"Tuat":[10,22,34,46,58,70,82,94],"Hoi":[11,23,35,47,59,71,83,95]}
DANG_MAP = {"kep":[0,55,11,66,22,77,33,88,44,99,5,50,16,61,27,72,38,83,49,94],"sat kep":[1,10,12,21,23,32,34,43,45,54,56,65,67,76,78,87,89,98,9,90],"cach 1":[2,20,8,80,13,31,19,91,24,42,35,53,46,64,57,75,79,97,68,86],"cach 2":[3,30,18,81,25,52,47,74,69,96,7,70,14,41,29,92,36,63,58,85],"cach 3":[4,40,6,60,15,51,17,71,28,82,26,62,37,73,39,93,48,84,59,95]}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]

# --- ROOT DATA ---
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

# --- HELPERS ---
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

# --- KHỞI TẠO STATE ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    for k in ['bo','chanle','beto','giap','dang']: st.session_state[k] = [0]*20 # Buffer dư
    st.session_state.bo = [0]*15; st.session_state.giap = [0]*12; st.session_state.dang = [0]*5
    for k in ['d_cl','u_cl','so_he']: st.session_state[k] = [0, 0]
    st.session_state.ls, st.session_state.db, st.session_state.ky_quay = [], {}, 1
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

def cap_nhat_logic():
    raw = st.session_state.gdb_in
    if not raw or len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv = n//10, n%10
    st.session_state.rd, st.session_state.rk, st.session_state.rg = get_root(st.session_state.date_in), get_root(st.session_state.ky_quay), get_root(raw)
    
    # Update Khan
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==((dv+duv)%10) else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==((dv-duv+10)%10) else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    for i in range(15): st.session_state.bo[i] = 0 if i==find_idx(n, BO_MAP) else st.session_state.bo[i]+1
    for i in range(12): st.session_state.giap[i] = 0 if i==find_idx(n, GIAP_MAP) else st.session_state.giap[i]+1
    for i in range(5): st.session_state.dang[i] = 0 if i==find_idx(n, DANG_MAP) else st.session_state.dang[i]+1
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- MAIN UI ---
st.markdown("<div class='main-title'>💎 HỆ THỐNG THỐNG KÊ 18 BIẾN PRO</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("💾 QUẢN LÝ")
    if st.button("LƯU BẢN SAO"):
        st.session_state.db[datetime.now().strftime("%H:%M")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k not in ['db']}
    if st.session_state.db:
        sel = st.selectbox("Bản lưu:", list(st.session_state.db.keys())[::-1])
        c1, c2 = st.columns(2)
        with c1: 
            if st.button("NẠP"):
                for k, v in st.session_state.db[sel].items(): st.session_state[k] = v
                st.rerun()
        with c2: 
            if st.button("XÓA"): del st.session_state.db[sel]; st.rerun()
    st.divider()
    if st.button("RESET TẤT CẢ", type="primary"): st.session_state.clear(); st.rerun()

c1, c2, c3 = st.columns([1, 1, 0.8])
with c1: st.text_input("GĐB:", value="000000", key="gdb_in")
with c2: st.text_input("Ngày:", value="09092009", key="date_in")
with c3: st.number_input("Kỳ:", value=st.session_state.ky_quay, step=1, key="ky_quay")

st.markdown(f"<div class='root-label'>Root Ngày: {st.session_state.rd} | Root Kỳ: {st.session_state.rk} | Root GĐB: {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🚀 CẬP NHẬT TỔNG LỰC", on_click=cap_nhat_logic, type="primary", use_container_width=True)

tabs = st.tabs(["⚡ Lọc Dàn", "📊 Bảng A", "🔢 Kiểm Root", "🎲 Ma Trận B", "🛠️ Sửa Tay"])

with tabs[0]:
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    calc = []
    for i in range(100):
        d, du = i//10, i%10
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[(d+du)%10]+st.session_state.hieu[(d-du+10)%10]+((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+st.session_state.bo[find_idx(i, BO_MAP)]+st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.so_he[1 if i not in SO_THUONG else 0]+st.session_state.giap[find_idx(i, GIAP_MAP)]+st.session_state.dang[find_idx(i, DANG_MAP)]
        def gs(r, c, v): return ROOT_DATA[r][c].index(v) if r in ROOT_DATA else 0
        sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",(d+du)%10),("hieu",(d-du+10)%10),("cham",d),("cham",du)])
        calc.append({"s": f"{d}{du}", "d": sk + sr})
    df_f = pd.DataFrame(calc).sort_values(by=["d", "s"])
    ca, cb = st.columns(2)
    with ca:
        n1 = st.number_input("Dàn 1:", 1, 100, 10)
        d1 = ", ".join(df_f.head(int(n1))["s"].tolist())
        st.markdown(f"<div class='dan-box-1'>{d1}</div>", unsafe_allow_html=True)
        if st.button("📋 Copy D1"): st.write(f'<script>navigator.clipboard.writeText("{d1}")</script>', unsafe_allow_html=True)
    with cb:
        n2 = st.number_input("Dàn 2:", 1, 100, 36)
        d2 = ", ".join(df_f.head(int(n2))["s"].tolist())
        st.markdown(f"<div class='dan-box-2'>{d2}</div>", unsafe_allow_html=True)
        if st.button("📋 Copy D2"): st.write(f'<script>navigator.clipboard.writeText("{d2}")</script>', unsafe_allow_html=True)

with tabs[1]:
    st.write("**BẢNG A: KHAN (K) & ROOT (R)**")
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    def show_row(lbl, k, cat):
        khan = st.session_state[k]
        rt = [sum(ROOT_DATA[r][cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) for i in range(len(khan))]
        st.write(f"*{lbl}*")
        st.table(pd.DataFrame([khan, rt], columns=[str(i) for i in range(len(khan))], index=["K", "R"]))

    for lbl, k, cat in [("DAU","dau","dau"),("DUOI","duoi","duoi"),("TONG","tong","tong"),("HIEU","hieu","hieu"),("CHAM","cham","cham")]:
        show_row(lbl, k, cat)
    
    st.write("*BO*")
    st.table(pd.DataFrame([st.session_state.bo], columns=[x for x in BO_MAP.keys()], index=["K"]))
    st.write("*8 BIEN PHU*")
    st.table(pd.DataFrame({"DAU C/L":st.session_state.d_cl, "DUOI C/L":st.session_state.u_cl, "HE SO":st.session_state.so_he}, index=["0/CHAN/THG","1/LE/HE"]))

with tabs[2]:
    for n, rv in [("NGAY", st.session_state.rd), ("KY", st.session_state.rk), ("GDB", st.session_state.rg)]:
        if rv in ROOT_DATA:
            st.write(f"**ROOT {n}: {rv}**")
            ck = {cat: [ROOT_DATA[rv][cat].index(i) for i in range(10)] for cat in ["dau","duoi","tong","hieu","cham"]}
            st.table(pd.DataFrame(ck).T)

with tabs[3]:
    m_data = [[next(x for x in calc if x["s"] == f"{d}{du}")["d"] for du in range(10)] for d in range(10)]
    st.table(pd.DataFrame(m_data, columns=[str(i) for i in range(10)], index=[str(i) for i in range(10)]))

with tabs[4]:
    st.write("**SUA TAY KHAN**")
    for k, lbl in [('dau','Dau'),('duoi','Duoi'),('tong','Tong'),('hieu','Hieu'),('cham','Cham')]:
        with st.expander(f"Sua {lbl}"):
            cols = st.columns(5)
            for i in range(10):
                with cols[i%5]: st.session_state[k][i] = st.number_input(f"{lbl} {i}", value=st.session_state[k][i], key=f"e_{k}_{i}")

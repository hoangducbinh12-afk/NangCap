import streamlit as st
import pandas as pd
from datetime import datetime

# --- CAU HINH GIAO DIEN MOBILE ---
st.set_page_config(page_title="18 BIEN PRO - TOAN DIEN", layout="centered")

st.markdown("""
    <style>
    .stTable td, .stTable th { font-size: 11px !important; padding: 2px !important; text-align: center !important; font-weight: bold !important; border: 1px solid #eee !important; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 20px; font-weight: bold; margin-bottom: 10px; display: block !important; }
    .history-container { overflow-x: auto; white-space: nowrap; border: 1px solid #ddd; padding: 5px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 10px; }
    .dan-box-1 { background-color: #e8f5e9; padding: 10px; border-radius: 5px; border: 1px solid #c8e6c9; color: #2e7d32; font-family: monospace; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    .dan-box-2 { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #bbdefb; color: #1565c0; font-family: monospace; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    .root-label { font-size: 11px; font-weight: bold; color: #d32f2f; text-align: center; background: #fff5f5; padding: 5px; border-radius: 5px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DINH NGHIA MAPS (GIỮ NGUYÊN) ---
BO_MAP = {"bo 00": [0, 5, 50, 55], "bo 01": [1, 10, 6, 60, 51, 15, 56, 65], "bo 02": [2, 20, 7, 70, 52, 25, 57, 75], "bo 03": [3, 30, 8, 80, 53, 35, 58, 85], "bo 04": [4, 40, 9, 90, 54, 45, 59, 95], "bo 11": [11, 16, 61, 66], "bo 12": [12, 21, 17, 71, 62, 26, 67, 76], "bo 13": [13, 31, 18, 81, 63, 36, 68, 86], "bo 14": [14, 41, 19, 91, 64, 46, 69, 96], "bo 22": [22, 27, 72, 77], "bo 23": [23, 32, 28, 82, 73, 37, 78, 87], "bo 24": [24, 42, 29, 92, 74, 47, 79, 97], "bo 33": [33, 38, 83, 88], "bo 34": [34, 43, 39, 93, 84, 48, 89, 98], "bo 44": [44, 49, 94, 99]}
CHAN_LE_MAP = {"chan chan": [0, 22, 44, 66, 88, 2, 20, 4, 40, 6, 60, 8, 80, 24, 42, 26, 62, 28, 82, 46, 64, 48, 84, 68, 86], "chan le": [1, 3, 5, 7, 9, 21, 23, 25, 27, 29, 41, 43, 45, 47, 49, 61, 63, 65, 67, 69, 81, 83, 85, 87, 89], "le le": [11, 33, 55, 77, 99, 13, 31, 15, 51, 17, 71, 19, 91, 35, 53, 37, 73, 39, 93, 57, 75, 59, 95, 79, 97], "le chan": [10, 12, 14, 16, 18, 30, 32, 34, 36, 38, 50, 52, 54, 56, 58, 70, 72, 74, 76, 78, 90, 92, 94, 96, 98]}
BE_TO_MAP = {"be be": [0, 11, 22, 33, 44, 1, 10, 2, 20, 3, 30, 4, 40, 12, 21, 13, 31, 14, 41, 23, 32, 24, 42, 34, 43], "be to": [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29, 35, 36, 37, 38, 39, 45, 46, 47, 48, 49], "to be": [90, 91, 92, 93, 94, 80, 81, 82, 83, 84, 70, 71, 72, 73, 74, 60, 61, 62, 63, 64, 50, 51, 52, 53, 54], "to to": [55, 66, 77, 88, 99, 56, 65, 57, 75, 58, 85, 59, 95, 67, 76, 68, 86, 69, 96, 78, 87, 79, 97, 89, 98]}
GIAP_MAP = {"Ty": [0, 12, 24, 36, 48, 60, 72, 84, 96], "Suu": [1, 13, 25, 37, 49, 61, 73, 85, 97], "Dan": [2, 14, 26, 38, 50, 62, 74, 86, 98], "Mao": [3, 15, 27, 39, 51, 63, 75, 87, 99], "Thin": [4, 16, 28, 40, 52, 64, 76, 88], "Ty.": [5, 17, 29, 41, 53, 65, 77, 89], "Ngo": [6, 18, 30, 42, 54, 66, 78, 90], "Mui": [7, 19, 31, 43, 55, 67, 79, 91], "Than": [8, 20, 32, 44, 56, 68, 80, 92], "Dau": [9, 21, 33, 45, 57, 69, 81, 93], "Tuat": [10, 22, 34, 46, 58, 70, 82, 94], "Hoi": [11, 23, 35, 47, 59, 71, 83, 95]}
DANG_MAP = {"kep": [0, 55, 11, 66, 22, 77, 33, 88, 44, 99, 5, 50, 16, 61, 27, 72, 38, 83, 49, 94], "sat kep": [1, 10, 12, 21, 23, 32, 34, 43, 45, 54, 56, 65, 67, 76, 78, 87, 89, 98, 9, 90], "cach 1": [2, 20, 8, 80, 13, 31, 19, 91, 24, 42, 35, 53, 46, 64, 57, 75, 79, 97, 68, 86], "cach 2": [3, 30, 18, 81, 25, 52, 47, 74, 69, 96, 7, 70, 14, 41, 29, 92, 36, 63, 58, 85], "cach 3": [4, 40, 6, 60, 15, 51, 17, 71, 28, 82, 26, 62, 37, 73, 39, 93, 48, 84, 59, 95]}
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
    for i, (name, nums) in enumerate(mapping.items()):
        if n in nums: return i
    return -1

# --- KHOI TAO STATE ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    for k in ['bo','chanle','beto','giap','dang']: st.session_state[k] = [0]*20
    st.session_state.bo = [0]*15; st.session_state.chanle = [0]*4; st.session_state.beto = [0]*4; st.session_state.giap = [0]*12; st.session_state.dang = [0]*5
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0, 0]
    st.session_state.ls, st.session_state.db_cloud, st.session_state.pt, st.session_state.ky_quay = [], {}, False, 1
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

# --- LOGIC ---
def cap_nhat_diem():
    n = st.session_state.so_moi_ve
    dv, duv = n // 10, n % 10
    tv, hv = (dv + duv) % 10, (dv - duv + 10) % 10
    
    st.session_state.rd = get_root(st.session_state.date_in)
    st.session_state.rk = get_root(st.session_state.ky_quay)
    st.session_state.rg = get_root(n)
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg

    # Cap nhat Khan
    for i in range(10):
        st.session_state.dau[i] = 0 if i == dv else st.session_state.dau[i] + 1
        st.session_state.duoi[i] = 0 if i == duv else st.session_state.duoi[i] + 1
        st.session_state.tong[i] = 0 if i == tv else st.session_state.tong[i] + 1
        st.session_state.hieu[i] = 0 if i == hv else st.session_state.hieu[i] + 1
        st.session_state.cham[i] = 0 if (i == dv or i == duv) else st.session_state.cham[i] + 1
    for i in range(15): st.session_state.bo[i] = 0 if i == find_idx(n, BO_MAP) else st.session_state.bo[i] + 1
    for i in range(4): st.session_state.chanle[i] = 0 if i == find_idx(n, CHAN_LE_MAP) else st.session_state.chanle[i] + 1
    for i in range(4): st.session_state.beto[i] = 0 if i == find_idx(n, BE_TO_MAP) else st.session_state.beto[i] + 1
    for i in range(12): st.session_state.giap[i] = 0 if i == find_idx(n, GIAP_MAP) else st.session_state.giap[i] + 1
    for i in range(5): st.session_state.dang[i] = 0 if i == find_idx(n, DANG_MAP) else st.session_state.dang[i] + 1
    
    # 8 Bien phu moi
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.t_cl[tv%2]=0; st.session_state.t_cl[(tv+1)%2]+=1
    st.session_state.d_tb[1 if dv>=5 else 0]=0; st.session_state.d_tb[0 if dv>=5 else 1]+=1
    st.session_state.u_tb[1 if duv>=5 else 0]=0; st.session_state.u_tb[0 if duv>=5 else 1]+=1
    st.session_state.t_tb[1 if tv>=5 else 0]=0; st.session_state.t_tb[0 if tv>=5 else 1]+=1
    st.session_state.h_tb[1 if hv>=5 else 0]=0; st.session_state.h_tb[0 if hv>=5 else 1]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- UI ---
st.markdown("<div class='main-title'>💎 HỆ THỐNG 18 BIẾN PRO - TOÀN DIỆN</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ QUẢN LÝ")
    if st.button("💾 LƯU CLOUD (BACKUP)", use_container_width=True):
        now_str = datetime.now().strftime("%H:%M:%S %d/%m")
        st.session_state.db_cloud[now_str] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k != 'db_cloud'}
        st.success("Đã lưu!")
    if st.session_state.db_cloud:
        sel = st.selectbox("Bản sao:", list(st.session_state.db_cloud.keys())[::-1])
        if st.button("🚀 NẠP BAN"):
            for k, v in st.session_state.db_cloud[sel].items(): st.session_state[k] = v
            st.rerun()
    if st.button("❌ RESET ALL", use_container_width=True): st.session_state.clear(); st.rerun()

# NHẬP LIỆU
c1, c2, c3 = st.columns([1.2, 1.2, 1])
with c1: st.number_input("Số vừa về:", 0, 99, step=1, format="%02d", key="so_moi_ve")
with c2: st.text_input("Ngày:", "09092009", key="date_in")
with c3: st.number_input("Kỳ:", value=st.session_state.ky_quay, step=1, key="ky_quay")

st.markdown(f"<div class='root-label'>Root Ngày: {st.session_state.rd} | Root Kỳ: {st.session_state.rk} | Root GĐB: {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🔥 CẬP NHẬT TỔNG LỰC", on_click=cap_nhat_diem, type="primary", use_container_width=True)

t1, t2, t3, t4, t5 = st.tabs(["⚡ Dàn", "📊 Bảng A", "🔢 Root", "🔢 Ma Trận", "🛠️ Sửa"])

with t1:
    calc = []
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    for i in range(100):
        d, du = i // 10, i % 10
        t, h = (d+du)%10, (d-du+10)%10
        def rs(r, cat, v): return ROOT_DATA[r][cat].index(v) if r in ROOT_DATA else 0
        s_root = sum(rs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        s_khan = st.session_state.dau[d] + st.session_state.duoi[du] + st.session_state.tong[t] + st.session_state.hieu[h] + ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du])) + st.session_state.bo[find_idx(i, BO_MAP)] + st.session_state.chanle[find_idx(i, CHAN_LE_MAP)] + st.session_state.beto[find_idx(i, BE_TO_MAP)] + st.session_state.giap[find_idx(i, GIAP_MAP)] + st.session_state.dang[find_idx(i, DANG_MAP)] + st.session_state.d_cl[d%2] + st.session_state.u_cl[du%2] + st.session_state.so_he[1 if i not in SO_THUONG else 0]
        calc.append({"s": f"{d}{du}", "d": s_khan + s_root})
    df_s = pd.DataFrame(calc).sort_values(by=["d", "s"])
    
    ca, cb = st.columns(2)
    with ca:
        n1 = st.number_input("Dàn 1:", 1, 100, 10, key="dn1")
        d1 = ", ".join(df_s.head(int(n1))["s"].tolist())
        st.markdown(f"<div class='dan-box-1'>{d1}</div>", unsafe_allow_html=True)
        if st.button("📋 COPY D1"): st.write(f'<script>navigator.clipboard.writeText("{d1}")</script>', unsafe_allow_html=True); st.toast("D1")
    with cb:
        n2 = st.number_input("Dàn 2:", 1, 100, 36, key="dn2")
        d2 = ", ".join(df_s.head(int(n2))["s"].tolist())
        st.markdown(f"<div class='dan-box-2'>{d2}</div>", unsafe_allow_html=True)
        if st.button("📋 COPY D2"): st.write(f'<script>navigator.clipboard.writeText("{d2}")</script>', unsafe_allow_html=True); st.toast("D2")

with t2:
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    def show_split_row(lbl, k, cat, names):
        st.write(f"**{lbl}**")
        khan = st.session_state[k]
        rt = [sum(ROOT_DATA[r][cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) for i in range(len(khan))]
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        st.table(pd.DataFrame([khan, rt], columns=names, index=["K", "R"]))
        st.markdown('</div>', unsafe_allow_html=True)

    for lbl, k, cat in [("DAU","dau","dau"),("DUOI","duoi","duoi"),("TONG","tong","tong"),("HIEU","hieu","hieu"),("CHAM","cham","cham")]:
        show_split_row(lbl, k, cat, range(10))
    
    show_split_row("BO", "bo", "dau", [x.split()[1] for x in BO_MAP.keys()]) # Tam dung dau cho cat de khong loi index
    
    for lbl, k, names in [("CHAN LE", "chanle", list(CHAN_LE_MAP.keys())), ("BE TO", "beto", list(BE_TO_MAP.keys())), ("12 GIAP", "giap", list(GIAP_MAP.keys())), ("DANG SO", "dang", list(DANG_MAP.keys()))]:
        st.write(f"**{lbl}**")
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        st.table(pd.DataFrame([st.session_state[k]], columns=names, index=["K"]))
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("**8 BIEN PHU MOI**")
    st.table(pd.DataFrame({
        "DAU C/L": st.session_state.d_cl, "DUOI C/L": st.session_state.u_cl, "TONG C/L": st.session_state.t_cl,
        "DAU B/T": st.session_state.d_tb, "DUOI B/T": st.session_state.u_tb, "TONG B/T": st.session_state.t_tb,
        "HIEU B/T": st.session_state.h_tb, "HE SO": st.session_state.so_he
    }, index=["0/BÉ/THG", "1/LẺ/HỆ"]))

with t3:
    for n, rv in [("NGÀY", st.session_state.rd), ("KỲ", st.session_state.rk), ("GĐB", st.session_state.rg)]:
        if rv in ROOT_DATA:
            st.write(f"**ROOT {n}: {rv}**")
            ck = {cat: [ROOT_DATA[rv][cat].index(i) for i in range(10)] for cat in ["dau","duoi","tong","hieu","cham"]}
            st.table(pd.DataFrame(ck).T)

with t4:
    m_data = [[next(x for x in calc if x["s"] == f"{d}{du}")["d"] for du in range(10)] for d in range(10)]
    st.dataframe(pd.DataFrame(m_data, columns=[str(i) for i in range(10)], index=[str(i) for i in range(10)]), use_container_width=True)

with t5:
    if st.button("💾 LUU SUA TAY"): st.rerun()
    for k, lbl in [('dau','Dau'),('duoi','Duoi'),('tong','Tong'),('hieu','Hiệu'),('cham','Cham')]:
        with st.expander(f"Sua {lbl}"):
            cols = st.columns(5)
            for i in range(len(st.session_state[k])):
                with cols[i%5]: st.session_state[k][i] = st.number_input(f"{i}", value=st.session_state[k][i], key=f"e_{k}_{i}")

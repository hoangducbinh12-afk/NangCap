import streamlit as st
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN CHUẨN TOÀN DIỆN ---
st.set_page_config(page_title="ROOT 18 BIẾN PRO", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 500px !important; padding-top: 1rem !important; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
    
    /* Bảng A phong cách Toàn Diện */
    .stTable td, .stTable th { 
        font-size: 10px !important; 
        padding: 2px !important; 
        text-align: center !important; 
        border: 1px solid #f0f0f0 !important;
    }
    .stTable th { background-color: #f8f9fa !important; font-weight: bold !important; color: #1E3A8A !important; }
    
    /* Box dàn số chuẩn màu */
    .dan-box-1 { background-color: #e8f5e9; padding: 10px; border-radius: 5px; border: 1px solid #c8e6c9; color: #2e7d32; font-family: monospace; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    .dan-box-2 { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #bbdefb; color: #1565c0; font-family: monospace; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    
    /* Root display */
    .root-label { font-size: 11px; font-weight: bold; color: #d32f2f; text-align: center; background: #fff5f5; padding: 5px; border-radius: 5px; margin-bottom: 10px; }
    
    /* Nút bấm nhỏ gọn */
    .stButton>button { height: 32px !important; font-size: 12px !important; border-radius: 4px !important; }
    label { font-size: 12px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU GỐC ---
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

def get_root(s):
    try:
        t = sum(int(x) for x in str(s) if x.isdigit())
        while t > 9: t = sum(int(x) for x in str(t))
        return t
    except: return 0

# --- KHỞI TẠO ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    for k in ['d_cl','u_cl','t_cl','d_tb','u_tb','t_tb','h_tb','so_he']: st.session_state[k] = [0, 0]
    st.session_state.ls, st.session_state.db = [], {}
    st.session_state.ky_quay, st.session_state.num_1, st.session_state.num_2 = 1, 10, 36
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

def cap_nhat():
    raw = st.session_state.gdb_in
    if not raw or len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv = n//10, n%10
    st.session_state.rd = get_root(st.session_state.date_in)
    st.session_state.rk = get_root(st.session_state.ky_quay)
    st.session_state.rg = get_root(raw)
    
    # Khan chính
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==((dv+duv)%10) else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==((dv-duv+10)%10) else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    # 8 Biến phụ
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.t_cl[((dv+duv)%10)%2]=0; st.session_state.t_cl[(((dv+duv)%10)+1)%2]+=1
    st.session_state.d_tb[1 if dv>=5 else 0]=0; st.session_state.d_tb[0 if dv>=5 else 1]+=1
    st.session_state.u_tb[1 if duv>=5 else 0]=0; st.session_state.u_tb[0 if duv>=5 else 1]+=1
    st.session_state.t_tb[1 if ((dv+duv)%10)>=5 else 0]=0; st.session_state.t_tb[0 if ((dv+duv)%10)>=5 else 1]+=1
    st.session_state.h_tb[1 if ((dv-duv+10)%10)>=5 else 0]=0; st.session_state.h_tb[0 if ((dv-duv+10)%10)>=5 else 1]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- MAIN UI ---
st.markdown("<div class='main-title'>💎 HỆ THỐNG THỐNG KÊ 18 BIẾN PRO</div>", unsafe_allow_html=True)

with st.sidebar:
    st.write("### 💾 QUẢN LÝ CLOUD")
    if st.button("LƯU BẢN SAO"):
        st.session_state.db[datetime.now().strftime("%H:%M:%S")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k not in ['db']}
        st.toast("Đã lưu!")
    if st.session_state.db:
        sel = st.selectbox("Bản lưu:", list(st.session_state.db.keys())[::-1])
        if st.button("HỒI PHỤC"):
            for k, v in st.session_state.db[sel].items(): st.session_state[k] = v
            st.rerun()
    st.divider()
    if st.button("XÓA DỮ LIỆU"): st.session_state.clear(); st.rerun()

c1, c2, c3 = st.columns([1, 1, 0.8])
with c1: st.text_input("GĐB:", value="000000", key="gdb_in")
with c2: st.text_input("Ngày:", value="09092009", key="date_in")
with c3: st.number_input("Kỳ:", value=st.session_state.ky_quay, step=1, key="ky_quay")

st.markdown(f"<div class='root-label'>Root Ngày: {st.session_state.rd} | Root Kỳ: {st.session_state.rk} | Root GĐB: {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🚀 CẬP NHẬT TỔNG LỰC", on_click=cap_nhat, type="primary", use_container_width=True)

tabs = st.tabs(["⚡ Dàn", "📊 Bảng A", "🔢 Kiểm Root", "🎲 Ma Trận B", "🛠️ Sửa Tay"])

with tabs[0]:
    cn1, cn2 = st.columns(2)
    with cn1: num_1 = st.number_input("Số quân Dàn 1:", 1, 100, 10)
    with cn2: num_2 = st.number_input("Số quân Dàn 2:", 1, 100, 36)
    
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    f_list = []
    for i in range(100):
        d, du, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        def rs(r, cat, v): return ROOT_DATA[r][cat].index(v) if r in ROOT_DATA else 0
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.so_he[1 if i not in SO_THUONG else 0]
        sr = sum(rs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        f_list.append({"s": f"{d}{du}", "d": sk + sr})
    df_f = pd.DataFrame(f_list).sort_values(by=["d", "s"], ascending=[True, True])
    
    for idx, num in enumerate([num_1, num_2]):
        d_str = ", ".join(df_f.head(num)["s"].tolist())
        st.markdown(f"<div class='dan-box-{idx+1}'>{d_str}</div>", unsafe_allow_html=True)
        if st.button(f"📋 COPY DÀN {idx+1}"):
            st.write(f'<script>navigator.clipboard.writeText("{d_str}")</script>', unsafe_allow_html=True)
            st.toast(f"Dàn {idx+1}")

with tabs[1]:
    st.write("**BẢNG A: CHI TIẾT 18 BIẾN (KHÔNG DẤU)**")
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    
    def get_v(key, root_cat):
        return [st.session_state[key][i] + sum(ROOT_DATA[r][root_cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) for i in range(10)]
    
    data_a = {
        "DAU": get_v("dau", "dau"), "DUOI": get_v("duoi", "duoi"),
        "TONG": get_v("tong", "tong"), "HIEU": get_v("hieu", "hieu"), "CHAM": get_v("cham", "cham")
    }
    st.table(pd.DataFrame(data_a, index=[str(x) for x in range(10)]).T)
    
    st.write("**8 BIẾN PHỤ 50/50**")
    data_p = {
        "DAU C/L": st.session_state.d_cl, "DUOI C/L": st.session_state.u_cl, "TONG C/L": st.session_state.t_cl,
        "DAU B/T": st.session_state.d_tb, "DUOI B/T": st.session_state.u_tb, "TONG B/T": st.session_state.t_tb,
        "HIEU B/T": st.session_state.h_tb, "HE SO": st.session_state.so_he
    }
    st.table(pd.DataFrame(data_p, index=["0/BÉ/THG", "1/LẺ/HỆ"]))

with tabs[2]:
    for n, rv in [("NGÀY", st.session_state.rd), ("KỲ", st.session_state.rk), ("GĐB", st.session_state.rg)]:
        if rv in ROOT_DATA:
            st.write(f"**ROOT {n}: {rv}**")
            ck = {cat: [ROOT_DATA[rv][cat].index(i) for i in range(10)] for cat in ["dau","duoi","tong","hieu","cham"]}
            st.table(pd.DataFrame(ck).T)

with tabs[3]:
    m_data = [[next(x for x in f_list if x["s"] == f"{d}{du}")["d"] for du in range(10)] for d in range(10)]
    st.table(pd.DataFrame(m_data, columns=[str(i) for i in range(10)], index=[str(i) for i in range(10)]))

with tabs[4]:
    st.write("**SỬA TAY KHAN**")
    for i in range(10): st.session_state.dau[i] = st.number_input(f"Dau {i}", value=st.session_state.dau[i])

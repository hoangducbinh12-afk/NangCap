import streamlit as st
import pandas as pd
from datetime import datetime

# --- TỐI ƯU GIAO DIỆN PHONG CÁCH APP CŨ ---
st.set_page_config(page_title="ROOT 18 BIEN PRO", layout="centered")

st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 1rem; }
    .stTable td, .stTable th { font-size: 11px !important; padding: 1px !important; text-align: center !important; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
    .root-label { font-size: 12px; font-weight: bold; color: #d32f2f; text-align: center; }
    .history-container { overflow-x: auto; white-space: nowrap; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU GỐC ROOT DATA (0-9đ TỪ TRÁI SANG PHẢI) ---
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

# --- DỮ LIỆU KHÁC ---
BO_MAP = {"00":[0,5,50,55],"01":[1,10,6,60,51,15,56,65],"02":[2,20,7,70,52,25,57,75],"03":[3,30,8,80,53,35,58,85],"04":[4,40,9,90,54,45,59,95],"11":[11,16,61,66],"12":[12,21,17,71,62,26,67,76],"13":[13,31,18,81,63,36,68,86],"14":[14,41,19,91,64,46,69,96],"22":[22,27,72,77],"23":[23,32,28,82,73,37,78,87],"24":[24,42,29,92,74,47,79,97],"33":[33,38,83,88],"34":[34,43,39,93,84,48,89,98],"44":[44,49,94,99]}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]

# --- HÀM TÍNH ---
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

# --- KHỞI TẠO (MẶC ĐỊNH 0) ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    st.session_state.bo = [0]*15
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0]*2
    st.session_state.ls = []
    st.session_state.db = {}

# --- CẬP NHẬT ---
def cap_nhat():
    raw = st.session_state.gdb_in
    if len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv, tv, hv = n//10, n%10, (n//10+n%10)%10, (n//10-n%10+10)%10
    rd, rk, rg = get_root(st.session_state.date_in), get_root(st.session_state.ky_in), get_root(raw)
    
    tmp = []
    for i in range(100):
        d, du, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+ \
             ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+ \
             st.session_state.bo[find_idx(i, BO_MAP)] + \
             st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.t_cl[t%2]+ \
             st.session_state.d_tb[1 if d>=5 else 0]+st.session_state.u_tb[1 if du>=5 else 0]+ \
             st.session_state.t_tb[1 if t>=5 else 0]+st.session_state.h_tb[1 if h>=5 else 0]+st.session_state.so_he[1 if i not in SO_THUONG else 0]
        
        def gs(r, c, v): return ROOT_DATA[r][c].index(v) if r in ROOT_DATA else 0
        sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("đầu",d),("đuôi",du),("tổng",t),("hiệu",h),("chạm",d),("chạm",du)])
        tmp.append({"s": f"{d}{du}", "d": sk + sr})
    
    df = pd.DataFrame(tmp).sort_values(by=["d","s"]).reset_index(drop=True)
    st.session_state.ls.insert(0, {"Số": f"{n:02d}", "Hạng": df[df['s']==f"{n:02d}"].index[0]+1, "Điểm": df[df['s']==f"{n:02d}"].iloc[0]['d']})
    
    # Update Khan
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==tv else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==hv else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    for i in range(15): st.session_state.bo[i] = 0 if i==find_idx(n, BO_MAP) else st.session_state.bo[i]+1
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.t_cl[tv%2]=0; st.session_state.t_cl[(tv+1)%2]+=1
    st.session_state.d_tb[1 if dv>=5 else 0]=0; st.session_state.d_tb[0 if dv>=5 else 1]+=1
    st.session_state.u_tb[1 if duv>=5 else 0]=0; st.session_state.u_tb[0 if duv>=5 else 1]+=1
    st.session_state.t_tb[1 if tv>=5 else 0]=0; st.session_state.t_tb[0 if tv>=5 else 1]+=1
    st.session_state.h_tb[1 if hv>=5 else 0]=0; st.session_state.h_tb[0 if hv>=5 else 1]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- GIAO DIỆN ---
st.markdown("<div class='main-title'>💎 ROOT 18 BIẾN SIÊU CẤP</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("💾 QUẢN LÝ")
    if st.button("LƯU DỮ LIỆU"):
        st.session_state.db[datetime.now().strftime("%H:%M")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k not in ['db']}
        st.toast("Đã lưu!")
    if st.session_state.db:
        sel = st.selectbox("Bản lưu:", list(st.session_state.db.keys())[::-1])
        if st.button("NẠP LẠI"):
            for k, v in st.session_state.db[sel].items(): st.session_state[k] = v
            st.rerun()
    st.divider()
    if st.button("RESET TẤT CẢ", type="primary"): st.session_state.clear(); st.rerun()

# NHẬP LIỆU (MẶC ĐỊNH RỖNG/0)
c1, c2, c3 = st.columns(3)
with c1: st.text_input("Ngày:", "", key="date_in")
with c2: st.text_input("Kỳ:", "", key="ky_in")
with c3: st.text_input("GĐB:", "", key="gdb_in")

rd, rk, rg = get_root(st.session_state.date_in), get_root(st.session_state.ky_in), get_root(st.session_state.gdb_in)
st.markdown(f"<p class='root-label'>Root Ngày: {rd} | Root Kỳ: {rk} | Root GĐB: {rg}</p>", unsafe_allow_html=True)
st.button("🔥 CẬP NHẬT KẾT QUẢ", on_click=cap_nhat, type="primary", use_container_width=True)

t1, t2, t3, t4 = st.tabs(["⚡ Dàn", "📊 Bảng A", "🔢 Bảng B", "🕒 LS"])

with t1:
    f_list = []
    for i in range(100):
        d, du, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+ \
             ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+ \
             st.session_state.bo[find_idx(i, BO_MAP)] + \
             st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.t_cl[t%2]+ \
             st.session_state.d_tb[1 if d>=5 else 0]+st.session_state.u_tb[1 if du>=5 else 0]+ \
             st.session_state.t_tb[1 if t>=5 else 0]+st.session_state.h_tb[1 if h>=5 else 0]+st.session_state.so_he[1 if i not in SO_THUONG else 0]
        
        def gs(r, c, v): return ROOT_DATA[r][c].index(v) if r in ROOT_DATA else 0
        sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("đầu",d),("đuôi",du),("tổng",t),("hiệu",h),("chạm",d),("chạm",du)])
        f_list.append({"s": f"{d}{du}", "d": sk + sr})
    df_f = pd.DataFrame(f_list).sort_values(by=["d", "s"], ascending=[False, True])
    st.success(", ".join(df_f.head(10)["s"].tolist()))
    st.info(", ".join(df_f.head(36)["s"].tolist()))

with t2:
    st.write("**BẢNG A: ĐIỂM TỔNG (KHAN + 3 ROOT)**")
    for lbl, k, cat in [("ĐẦU","dau","đầu"),("ĐUÔI","duoi","đuôi"),("TỔNG","tong","tổng"),("HIỆU","hieu","hiệu"),("CHẠM","cham","chạm")]:
        st.write(f"*{lbl}*")
        def calc_final(idx, key, category):
            r_points = sum(ROOT_DATA[r][category].index(idx) if r in ROOT_DATA else 0 for r in [rd,rk,rg])
            return st.session_state[key][idx] + r_points
        final_vals = [calc_final(i, k, cat) for i in range(10)]
        st.table(pd.DataFrame([final_vals], columns=[str(x) for x in range(10)], index=[""]))
    
    st.write("**BIẾN 50/50**")
    c = st.columns(4)
    c[0].write(f"Đầu C/L: {st.session_state.d_cl}")
    c[1].write(f"Đuôi C/L: {st.session_state.u_cl}")
    c[2].write(f"Tổng C/L: {st.session_state.t_cl}")
    c[3].write(f"Hệ/Th: {st.session_state.so_he}")

with t3:
    m_data = []
    for d in range(10):
        row = []
        for du in range(10):
            idx = d*10+du; t, h = (d+du)%10, (d-du+10)%10
            sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+ \
                 ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+ \
                 st.session_state.bo[find_idx(idx, BO_MAP)] + \
                 st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.t_cl[t%2]+ \
                 st.session_state.d_tb[1 if d>=5 else 0]+st.session_state.u_tb[1 if du>=5 else 0]+ \
                 st.session_state.t_tb[1 if t>=5 else 0]+st.session_state.h_tb[1 if h>=5 else 0]+st.session_state.so_he[1 if idx not in SO_THUONG else 0]
            def gs(r, c, v): return ROOT_DATA[r][c].index(v) if r in ROOT_DATA else 0
            sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("đầu",d),("đuôi",du),("tổng",t),("hiệu",h),("chạm",d),("chạm",du)])
            row.append(sk + sr)
        m_data.append(row)
    st.table(pd.DataFrame(m_data, columns=[str(i) for i in range(10)], index=[str(i) for i in range(10)]))

with t4:
    if st.session_state.ls:
        st.table(pd.DataFrame(st.session_state.ls))

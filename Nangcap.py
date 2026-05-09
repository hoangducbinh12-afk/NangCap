import streamlit as st
import pandas as pd
from datetime import datetime

# --- TỐI ƯU GIAO DIỆN ---
st.set_page_config(page_title="ROOT 18 BIẾN SIÊU CẤP", layout="centered")

st.markdown("""
    <style>
    .stTable td, .stTable th { font-size: 10px !important; padding: 1px !important; text-align: center !important; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
    .root-label { font-size: 12px; font-weight: bold; color: #d32f2f; text-align: center; background: #fdf2f2; padding: 5px; border-radius: 5px; margin-bottom: 10px; }
    .section-title { font-size: 13px; font-weight: bold; color: #1E3A8A; margin-top: 10px; border-left: 4px solid #1E3A8A; padding-left: 5px; }
    .dan-box { background: #f0f7ff; padding: 8px; border-radius: 5px; border: 1px solid #cce3ff; margin-top: 5px; font-size: 12px; }
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
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0]*2
    st.session_state.ls = []
    st.session_state.db = {}
    st.session_state.ky_quay = 1
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

# --- XỬ LÝ CẬP NHẬT ---
def cap_nhat():
    raw = st.session_state.gdb_in
    if len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv, tv, hv = n//10, n%10, (n//10+n%10)%10, (n//10-n%10+10)%10
    
    st.session_state.rd = get_root(st.session_state.date_in)
    st.session_state.rk = get_root(st.session_state.ky_quay)
    st.session_state.rg = get_root(raw)
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    
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
    
    df = pd.DataFrame(tmp).sort_values(by=["d","s"], ascending=[True, True]).reset_index(drop=True)
    st.session_state.ls.insert(0, {"Số": f"{n:02d}", "Hạng": df[df['s']==f"{n:02d}"].index[0]+1, "Điểm": df[df['s']==f"{n:02d}"].iloc[0]['d']})
    
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

# --- UI ---
st.markdown("<div class='main-title'>💎 SIÊU HỆ THỐNG ROOT 18 BIẾN</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("💾 QUẢN LÝ")
    if st.button("LƯU BẢN SAO LƯU", use_container_width=True):
        st.session_state.db[datetime.now().strftime("%H:%M:%S")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k not in ['db']}
        st.toast("Đã lưu thành công!")
    if st.session_state.db:
        st.divider()
        sel = st.selectbox("Chọn bản sao lưu:", list(st.session_state.db.keys())[::-1])
        c_l, c_r = st.columns(2)
        with c_l:
            if st.button("HỒI PHỤC", use_container_width=True):
                for k, v in st.session_state.db[sel].items(): st.session_state[k] = v
                st.rerun()
        with c_r:
            if st.button("XÓA BẢN NÀY", use_container_width=True):
                del st.session_state.db[sel]; st.rerun()
    st.divider()
    if st.button("RESET TẤT CẢ", type="primary", use_container_width=True):
        st.session_state.clear(); st.rerun()

# NHẬP LIỆU
c1, c2, c3 = st.columns([2, 2, 2])
with c1: st.text_input("Ngày (09092009):", "", key="date_in")
with c2: 
    st.write("Kỳ quay:")
    ck1, ck2, ck3 = st.columns([1, 2, 1])
    with ck1: 
        if st.button("➖"): st.session_state.ky_quay -= 1; st.rerun()
    with ck2: st.session_state.ky_quay = st.number_input("Kỳ", value=st.session_state.ky_quay, label_visibility="collapsed")
    with ck3: 
        if st.button("➕"): st.session_state.ky_quay += 1; st.rerun()
with c3: st.text_input("GĐB (6 số):", "", key="gdb_in")

st.markdown(f"<div class='root-label'>Root Ngày: {st.session_state.rd} | Root Kỳ: {st.session_state.rk} | Root GĐB: {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🔥 CẬP NHẬT TỔNG LỰC", on_click=cap_nhat, type="primary", use_container_width=True)

t1, t2, t3, t4, t5 = st.tabs(["⚡ Dàn", "📊 Bảng A", "🔢 Kiểm Tra Root", "🎲 Ma Trận B", "🕒 LS"])

with t1:
    c_n1, c_n2 = st.columns(2)
    with c_n1: 
        num_1 = st.number_input("Số quân Dàn 1:", 1, 100, 10)
    with c_n2: 
        num_2 = st.number_input("Số quân Dàn 2:", 1, 100, 36)
    
    # Tính điểm để lấy dàn (luôn tính dựa trên state hiện tại)
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
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
    
    df_f = pd.DataFrame(f_list).sort_values(by=["d", "s"], ascending=[True, True])
    
    st.markdown(f"<div class='dan-box'><b>Dàn {num_1} (Thấp -> Cao):</b><br>{', '.join(df_f.head(num_1)['s'].tolist())}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='dan-box'><b>Dàn {num_2} (Thấp -> Cao):</b><br>{', '.join(df_f.head(num_2)['s'].tolist())}</div>", unsafe_allow_html=True)

with t2:
    st.markdown("<div class='section-title'>NHẬP TAY / CHỈNH SỬA BẢNG A (KHAN)</div>", unsafe_allow_html=True)
    # Cho phép sửa tay từng biến
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.session_state.dau = [st.number_input(f"Đầu {i}", value=v, step=1, key=f"in_d_{i}") for i, v in enumerate(st.session_state.dau)]
        st.session_state.tong = [st.number_input(f"Tổng {i}", value=v, step=1, key=f"in_t_{i}") for i, v in enumerate(st.session_state.tong)]
    with col_a2:
        st.session_state.duoi = [st.number_input(f"Đuôi {i}", value=v, step=1, key=f"in_u_{i}") for i, v in enumerate(st.session_state.duoi)]
        st.session_state.hieu = [st.number_input(f"Hiệu {i}", value=v, step=1, key=f"in_h_{i}") for i, v in enumerate(st.session_state.hieu)]
    
    st.write("**Biến Bộ & Chạm**")
    st.session_state.bo = [st.number_input(f"Bộ {list(BO_MAP.keys())[i]}", value=v, step=1) for i, v in enumerate(st.session_state.bo)]
    st.session_state.cham = [st.number_input(f"Chạm {i}", value=v, step=1) for i, v in enumerate(st.session_state.cham)]

with t3:
    st.markdown("<div class='section-title'>KIỂM TRA ĐIỂM THƯỞNG THEO ROOT</div>", unsafe_allow_html=True)
    for n, r_v in [("NGÀY", st.session_state.rd), ("KỲ", st.session_state.rk), ("GĐB", st.session_state.rg)]:
        if r_v in ROOT_DATA:
            st.write(f"**MÃ ROOT {n}: {r_v}**")
            check = {cat: [ROOT_DATA[r_v][cat].index(i) for i in range(10)] for cat in ["đầu","đuôi","tổng","hiệu","chạm"]}
            st.table(pd.DataFrame(check, index=[str(x) for x in range(10)]).T)

with t4:
    m_data = []
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
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

with t5:
    if st.session_state.ls: st.table(pd.DataFrame(st.session_state.ls))

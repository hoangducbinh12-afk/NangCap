import streamlit as st
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN TỐI ƯU ---
st.set_page_config(page_title="HỆ THỐNG ROOT 18 BIẾN PRO", layout="centered")

st.markdown("""
    <style>
    /* Tổng thể */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 700px !important; }
    .main-title { text-align: center; font-size: 22px; font-weight: bold; color: #333; margin-bottom: 10px; }
    
    /* Font chữ bảng A và B (Không dấu) */
    .stTable td, .stTable th { font-size: 11px !important; padding: 1px !important; text-align: center !important; font-family: sans-serif !important; }
    
    /* Box Dàn số */
    .dan-box-1 { background-color: #e8f5e9; padding: 8px; border-radius: 4px; border: 1px solid #c8e6c9; color: #2e7d32; font-family: monospace; font-size: 13px; margin-bottom: 5px; }
    .dan-box-2 { background-color: #e3f2fd; padding: 8px; border-radius: 4px; border: 1px solid #bbdefb; color: #1565c0; font-family: monospace; font-size: 13px; margin-bottom: 5px; }
    
    /* Root Display */
    .root-display { text-align: center; background: #fff5f5; padding: 5px; border-radius: 5px; border: 1px solid #ffe3e3; margin-bottom: 10px; font-weight: bold; color: #d32f2f; font-size: 12px; }
    
    /* Nút bấm gọn */
    .stButton>button { height: 32px !important; padding: 0px 10px !important; font-size: 13px !important; }
    div[data-baseweb="tab-list"] { gap: 10px !important; }
    div[data-baseweb="tab"] { padding: 5px 10px !important; font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU ROOT (CẤU TRÚC KHÔNG DẤU BÊN TRONG) ---
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
    st.session_state.ls, st.session_state.db = [], {}
    st.session_state.ky_in, st.session_state.num_1, st.session_state.num_2 = 0, 10, 36
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

def cap_nhat():
    raw = st.session_state.gdb_in
    if not raw or raw == "000000": return
    n = int(raw[-2:])
    dv, duv, tv, hv = n//10, n%10, (n//10+n%10)%10, (n//10-n%10+10)%10
    st.session_state.rd = get_root(st.session_state.date_in)
    st.session_state.rk = get_root(st.session_state.ky_in)
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
        sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        tmp.append({"s": f"{d}{du}", "d": sk + sr})
    
    df = pd.DataFrame(tmp).sort_values(by=["d","s"], ascending=[True, True]).reset_index(drop=True)
    st.session_state.ls.insert(0, {"SO": f"{n:02d}", "HANG": df[df['s']==f"{n:02d}"].index[0]+1, "DIEM": df[df['s']==f"{n:02d}"].iloc[0]['d']})
    
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

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ☁️ CLOUD STORAGE")
    if st.button("💾 SAO LƯU DỮ LIỆU"):
        st.session_state.db[datetime.now().strftime("%H:%M:%S")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k not in ['db']}
        st.toast("Đã lưu!")
    if st.session_state.db:
        sel = st.selectbox("Bản lưu:", list(st.session_state.db.keys())[::-1])
        if st.button("🔄 PHỤC HỒI"):
            for k, v in st.session_state.db[sel].items(): st.session_state[k] = v
            st.rerun()
    st.divider()
    if st.button("🗑️ XÓA SẠCH DỮ LIỆU"): st.session_state.clear(); st.rerun()

# --- MAIN UI ---
st.markdown("<div class='main-title'>💎 HỆ THỐNG THỐNG KÊ 18 BIẾN PRO</div>", unsafe_allow_html=True)

st.write("Số vừa nổ:")
cg1, cg2, cg3 = st.columns([1, 4, 1])
with cg1: 
    if st.button("➖", key="sg"): 
        try: st.session_state.gdb_in = str(int(st.session_state.gdb_in)-1).zfill(6)
        except: pass
with cg2: st.text_input("GĐB", value="000000", key="gdb_in", label_visibility="collapsed")
with cg3: 
    if st.button("➕", key="ag"): 
        try: st.session_state.gdb_in = str(int(st.session_state.gdb_in)+1).zfill(6)
        except: pass

ci1, ci2 = st.columns(2)
with ci1: st.text_input("Ngày (09092009):", value="", key="date_in")
with ci2:
    st.write("Kỳ quay:")
    ck1, ck2, ck3 = st.columns([1, 2, 1])
    with ck1: 
        if st.button("➖", key="sk"): st.session_state.ky_in -= 1
    with ck2: st.session_state.ky_in = st.number_input("K", value=st.session_state.ky_in, label_visibility="collapsed")
    with ck3: 
        if st.button("➕", key="ak"): st.session_state.ky_in += 1

st.markdown(f"<div class='root-display'>ROOT NGÀY: {st.session_state.rd} | ROOT KỲ: {st.session_state.rk} | ROOT GĐB: {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🚀 CẬP NHẬT", on_click=cap_nhat, type="primary", use_container_width=True)

tabs = st.tabs(["⚡ Lọc Dàn", "📊 Bảng A", "🎲 Ma Trận B", "🛠️ Sửa Tay", "🕒 Lịch Sử"])

with tabs[0]:
    cn1, cn2 = st.columns(2)
    with cn1:
        st.write("Dàn 1:")
        dn1, dn2, dn3 = st.columns([1, 2, 1])
        with dn1: 
            if st.button("➖", key="s1"): st.session_state.num_1 -= 1
        with dn2: st.session_state.num_1 = st.number_input("N1", value=st.session_state.num_1, label_visibility="collapsed")
        with dn3: 
            if st.button("➕", key="a1"): st.session_state.num_1 += 1
    with cn2:
        st.write("Dàn 2:")
        dn4, dn5, dn6 = st.columns([1, 2, 1])
        with dn4: 
            if st.button("➖", key="s2"): st.session_state.num_2 -= 1
        with dn5: st.session_state.num_2 = st.number_input("N2", value=st.session_state.num_2, label_visibility="collapsed")
        with dn6: 
            if st.button("➕", key="a2"): st.session_state.num_2 += 1

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
        sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        f_list.append({"s": f"{d}{du}", "d": sk + sr})
    df_f = pd.DataFrame(f_list).sort_values(by=["d", "s"], ascending=[True, True])
    
    d1_str = ", ".join(df_f.head(st.session_state.num_1)["s"].tolist())
    d2_str = ", ".join(df_f.head(st.session_state.num_2)["s"].tolist())

    st.markdown(f"<div class='dan-box-1'>{d1_str}</div>", unsafe_allow_html=True)
    st.button("📋 COPY DÀN 1", key="cp1")
    st.markdown(f"<div class='dan-box-2'>{d2_str}</div>", unsafe_allow_html=True)
    st.button("📋 COPY DÀN 2", key="cp2")

with tabs[1]:
    st.write("**BẢNG A (KHÔNG DẤU BÊN TRONG)**")
    for lbl, k, cat in [("DAU","dau","dau"),("DUOI","duoi","duoi"),("TONG","tong","tong"),("HIEU","hieu","hieu"),("CHAM","cham","cham")]:
        vals = [st.session_state[k][i] + sum(ROOT_DATA[r][cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) for i in range(10)]
        st.write(f"*{lbl}*")
        st.table(pd.DataFrame([vals], columns=[str(x) for x in range(10)], index=[""]))

with tabs[2]:
    st.write("**MA TRAN B (KHÔNG DẤU BÊN TRONG)**")
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
            sr = sum(gs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
            row.append(sk + sr)
        m_data.append(row)
    st.table(pd.DataFrame(m_data, columns=[str(i) for i in range(10)], index=[str(i) for i in range(10)]))

with tabs[3]:
    st.write("**SỬA TAY ĐIỂM KHAN**")
    c1, c2 = st.columns(2)
    with c1:
        for i in range(10): st.session_state.dau[i] = st.number_input(f"Đầu {i}", value=st.session_state.dau[i])
        for i in range(10): st.session_state.cham[i] = st.number_input(f"Chạm {i}", value=st.session_state.cham[i])
    with c2:
        for i in range(10): st.session_state.duoi[i] = st.number_input(f"Đuôi {i}", value=st.session_state.duoi[i])
        for i in range(15): st.session_state.bo[i] = st.number_input(f"Bộ {list(BO_MAP.keys())[i]}", value=st.session_state.bo[i])
    
    st.write("**SỬA TAY 8 BIẾN 50/50**")
    cb1, cb2 = st.columns(2)
    with cb1:
        st.session_state.d_cl = [st.number_input("Đầu Chẵn", value=st.session_state.d_cl[0]), st.number_input("Đầu Lẻ", value=st.session_state.d_cl[1])]
        st.session_state.u_cl = [st.number_input("Đuôi Chẵn", value=st.session_state.u_cl[0]), st.number_input("Đuôi Lẻ", value=st.session_state.u_cl[1])]
        st.session_state.t_cl = [st.number_input("Tổng Chẵn", value=st.session_state.t_cl[0]), st.number_input("Tổng Lẻ", value=st.session_state.t_cl[1])]
        st.session_state.so_he = [st.number_input("Thường", value=st.session_state.so_he[0]), st.number_input("Hệ", value=st.session_state.so_he[1])]
    with cb2:
        st.session_state.d_tb = [st.number_input("Đầu Bé", value=st.session_state.d_tb[0]), st.number_input("Đầu To", value=st.session_state.d_tb[1])]
        st.session_state.u_tb = [st.number_input("Đuôi Bé", value=st.session_state.u_tb[0]), st.number_input("Đuôi To", value=st.session_state.u_tb[1])]
        st.session_state.t_tb = [st.number_input("Tổng Bé", value=st.session_state.t_tb[0]), st.number_input("Tổng To", value=st.session_state.t_tb[1])]
        st.session_state.h_tb = [st.number_input("Hiệu Bé", value=st.session_state.h_tb[0]), st.number_input("Hiệu To", value=st.session_state.h_tb[1])]

with tabs[4]:
    if st.session_state.ls:
        st.write("**LỊCH SỬ KẾT QUẢ**")
        st.table(pd.DataFrame(st.session_state.ls))

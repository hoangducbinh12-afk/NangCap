import streamlit as st
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN MOBILE ---
st.set_page_config(page_title="ROOT 18 BIẾN SIÊU CẤP", layout="wide")

st.markdown("""
    <style>
    .stTable td, .stTable th { font-size: 10px !important; padding: 1px !important; text-align: center !important; }
    .main-title { text-align: center; color: #d32f2f; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
    .root-res { color: #1E3A8A; font-weight: bold; font-size: 13px; background: #e3f2fd; padding: 3px; border-radius: 5px; text-align: center; margin-bottom: 5px; }
    .card { background: #fdfdfd; border: 1px solid #ddd; padding: 8px; border-radius: 8px; margin-bottom: 8px; }
    .history-container { overflow-x: auto; white-space: nowrap; border: 1px solid #eee; padding: 5px; background: #fff; }
    .compact-text { font-size: 12px !important; font-weight: bold; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU GỐC (ROOT_DATA giữ nguyên như ảnh) ---
BO_MAP = {
    "Bộ 00": [0, 5, 50, 55], "Bộ 01": [1, 10, 6, 60, 51, 15, 56, 65], "Bộ 02": [2, 20, 7, 70, 52, 25, 57, 75],
    "Bộ 03": [3, 30, 8, 80, 53, 35, 58, 85], "Bộ 04": [4, 40, 9, 90, 54, 45, 59, 95], "Bộ 11": [11, 16, 61, 66],
    "Bộ 12": [12, 21, 17, 71, 62, 26, 67, 76], "Bộ 13": [13, 31, 18, 81, 63, 36, 68, 86], "Bộ 14": [14, 41, 19, 91, 64, 46, 69, 96],
    "Bộ 22": [22, 27, 72, 77], "Bộ 23": [23, 32, 28, 82, 73, 37, 78, 87], "Bộ 24": [24, 42, 29, 92, 74, 47, 79, 97],
    "Bộ 33": [33, 38, 83, 88], "Bộ 34": [34, 43, 39, 93, 84, 48, 89, 98], "Bộ 44": [44, 49, 94, 99]
}
GIAP_MAP = {
    "Tý": [0, 12, 24, 36, 48, 60, 72, 84, 96], "Sửu": [1, 13, 25, 37, 49, 61, 73, 85, 97],
    "Dần": [2, 14, 26, 38, 50, 62, 74, 86, 98], "Mão": [3, 15, 27, 39, 51, 63, 75, 87, 99],
    "Thìn": [4, 16, 28, 40, 52, 64, 76, 88], "Tỵ.": [5, 17, 29, 41, 53, 65, 77, 89],
    "Ngọ": [6, 18, 30, 42, 54, 66, 78, 90], "Mùi": [7, 19, 31, 43, 55, 67, 79, 91],
    "Thân": [8, 20, 32, 44, 56, 68, 80, 92], "Dậu": [9, 21, 33, 45, 57, 69, 81, 93],
    "Tuất": [10, 22, 34, 46, 58, 70, 82, 94], "Hợi": [11, 23, 35, 47, 59, 71, 83, 95]
}
DANG_MAP = {
    "Kép": [0, 55, 11, 66, 22, 77, 33, 88, 44, 99, 5, 50, 16, 61, 27, 72, 38, 83, 49, 94],
    "Sát kép": [1, 10, 12, 21, 23, 32, 34, 43, 45, 54, 56, 65, 67, 76, 78, 87, 89, 98, 9, 90],
    "Cách 1": [2, 20, 8, 80, 13, 31, 19, 91, 24, 42, 35, 53, 46, 64, 57, 75, 79, 97, 68, 86],
    "Cách 2": [3, 30, 18, 81, 25, 52, 47, 74, 69, 96, 7, 70, 14, 41, 29, 92, 36, 63, 58, 85],
    "Cách 3": [4, 40, 6, 60, 15, 51, 17, 71, 28, 82, 26, 62, 37, 73, 39, 93, 48, 84, 59, 95]
}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]

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

def get_root(s):
    nums = [int(x) for x in str(s) if x.isdigit()]
    if not nums: return 1
    t = sum(nums); [t := sum(int(x) for x in str(t)) while t > 9]; return t if t > 0 else 1

def find_idx(n, mapping):
    for i, (name, nums) in enumerate(mapping.items()):
        if n in nums: return i
    return 0

if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    st.session_state['bo'], st.session_state['giap'], st.session_state['dang'] = [0]*15, [0]*12, [0]*5
    for k in ['d_cl','u_cl','t_cl','d_tb','u_tb','t_tb','h_tb','so_he']: st.session_state[k] = [0]*2
    st.session_state.ls = []

def cap_nhat():
    raw = st.session_state.gdb_in
    if len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv = n//10, n%10
    tv, hv = (dv+duv)%10, (dv-duv+10)%10
    r_d, r_k, r_g = get_root(st.session_state.date_in), get_root(st.session_state.ky_in), get_root(raw)
    
    tmp = []
    for i in range(100):
        d, du = i//10, i%10
        t, h = (d+du)%10, (d-du+10)%10
        sk = st.session_state.dau[d] + st.session_state.duoi[du] + st.session_state.tong[t] + st.session_state.hieu[h] + \
             ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du])) + \
             st.session_state.bo[find_idx(i, BO_MAP)] + st.session_state.giap[find_idx(i, GIAP_MAP)] + st.session_state.dang[find_idx(i, DANG_MAP)] + \
             st.session_state.d_cl[d%2] + st.session_state.u_cl[du%2] + st.session_state.t_cl[t%2] + \
             st.session_state.d_tb[1 if d>=5 else 0] + st.session_state.u_tb[1 if du>=5 else 0] + \
             st.session_state.t_tb[1 if t>=5 else 0] + st.session_state.h_tb[1 if h>=5 else 0] + \
             st.session_state.so_he[1 if i not in SO_THUONG else 0]
        sr = sum(ROOT_DATA[r][c].index(v) for r in [r_d, r_k, r_g] for c, v in [("đầu",d),("đuôi",du),("tổng",t),("hiệu",h),("chạm",d),("chạm",du)])
        tmp.append({"s": f"{d}{du}", "d": sk + sr})
    
    df = pd.DataFrame(tmp).sort_values(by=["d","s"]).reset_index(drop=True)
    st.session_state.ls.insert(0, {"Số": f"{n:02d}", "Hạng": df[df['s']==f"{n:02d}"].index[0]+1, "Điểm": df[df['s']==f"{n:02d}"].iloc[0]['d']})
    
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==tv else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==hv else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    for i in range(15): st.session_state.bo[i] = 0 if i==find_idx(n, BO_MAP) else st.session_state.bo[i]+1
    for i in range(12): st.session_state.giap[i] = 0 if i==find_idx(n, GIAP_MAP) else st.session_state.giap[i]+1
    for i in range(5): st.session_state.dang[i] = 0 if i==find_idx(n, DANG_MAP) else st.session_state.dang[i]+1
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.t_cl[tv%2]=0; st.session_state.t_cl[(tv+1)%2]+=1
    st.session_state.d_tb[1 if dv>=5 else 0]=0; st.session_state.d_tb[0 if dv>=5 else 1]+=1
    st.session_state.u_tb[1 if duv>=5 else 0]=0; st.session_state.u_tb[0 if duv>=5 else 1]+=1
    st.session_state.t_tb[1 if tv>=5 else 0]=0; st.session_state.t_tb[0 if tv>=5 else 1]+=1
    st.session_state.h_tb[1 if hv>=5 else 0]=0; st.session_state.h_tb[0 if hv>=5 else 1]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

st.markdown("<div class='main-title'>💎 HỆ THỐNG ROOT 18 BIẾN SIÊU CẤP</div>", unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.text_input("Ngày:", "10052026", key="date_in")
        st.markdown(f"<div class='root-res'>Root: {get_root(st.session_state.date_in)}</div>", unsafe_allow_html=True)
    with c2: 
        st.text_input("Kỳ:", "1", key="ky_in")
        st.markdown(f"<div class='root-res'>Root: {get_root(st.session_state.ky_in)}</div>", unsafe_allow_html=True)
    with c3: 
        st.text_input("GĐB:", "000000", key="gdb_in")
        st.markdown(f"<div class='root-res'>Root: {get_root(st.session_state.gdb_in)}</div>", unsafe_allow_html=True)
    st.button("🔥 CẬP NHẬT & TÍNH TOÁN", on_click=cap_nhat, type="primary", use_container_width=True)

t1, t2, t3, t4 = st.tabs(["⚡ Dàn", "📊 Bảng A", "🔢 Ma Trận B", "🕒 Lịch Sử"])

with t1:
    r_d, r_k, r_g = get_root(st.session_state.date_in), get_root(st.session_state.ky_in), get_root(st.session_state.gdb_in)
    f_list = []
    for i in range(100):
        d, du = i//10, i%10
        t, h = (d+du)%10, (d-du+10)%10
        sk = st.session_state.dau[d] + st.session_state.duoi[du] + st.session_state.tong[t] + st.session_state.hieu[h] + \
             ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du])) + \
             st.session_state.bo[find_idx(i, BO_MAP)] + st.session_state.giap[find_idx(i, GIAP_MAP)] + st.session_state.dang[find_idx(i, DANG_MAP)] + \
             st.session_state.d_cl[d%2] + st.session_state.u_cl[du%2] + st.session_state.t_cl[t%2] + \
             st.session_state.d_tb[1 if d>=5 else 0] + st.session_state.u_tb[1 if du>=5 else 0] + \
             st.session_state.t_tb[1 if t>=5 else 0] + st.session_state.h_tb[1 if h>=5 else 0] + \
             st.session_state.so_he[1 if i not in SO_THUONG else 0]
        sr = sum(ROOT_DATA[r][c].index(v) for r in [r_d, r_k, r_g] for c, v in [("đầu",d),("đuôi",du),("tổng",t),("hiệu",h),("chạm",d),("chạm",du)])
        f_list.append({"s": f"{d}{du}", "d": sk + sr})
    df_f = pd.DataFrame(f_list).sort_values(by=["d", "s"], ascending=[False, True])
    st.success(", ".join(df_f.head(10)["s"].tolist()))
    st.info(", ".join(df_f.head(36)["s"].tolist()))

with t2:
    st.markdown("<p class='compact-text'>BẢNG A: KHAN + ĐIỂM THƯỞNG ROOT</p>", unsafe_allow_html=True)
    r_d, r_k, r_g = get_root(st.session_state.date_in), get_root(st.session_state.ky_in), get_root(st.session_state.gdb_in)
    
    for lbl, k, cat in [("ĐẦU", "dau", "đầu"), ("ĐUÔI", "duoi", "đuôi"), ("TỔNG", "tong", "tổng"), ("HIỆU", "hieu", "hiệu"), ("CHẠM", "cham", "chạm")]:
        st.write(f"**{lbl}**")
        vals = []
        for i in range(10):
            # Tính điểm thưởng Root cho từng vị trí 0-9
            tr_root = ROOT_DATA[r_d][cat].index(i) + ROOT_DATA[r_k][cat].index(i) + ROOT_DATA[r_g][cat].index(i)
            vals.append(st.session_state[k][i] + tr_root)
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        st.table(pd.DataFrame([vals], columns=[str(x) for x in range(10)], index=["Tổng"]))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<p class='compact-text'>BIẾN ĐỐI XỨNG (50/50)</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='card'><b>Đầu C/L</b><br>{st.session_state.d_cl}</div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card'><b>Đuôi C/L</b><br>{st.session_state.u_cl}</div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card'><b>Tổng C/L</b><br>{st.session_state.t_cl}</div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='card'><b>Hệ/Thường</b><br>{st.session_state.so_he}</div>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    with c5: st.markdown(f"<div class='card'><b>Đầu B/T</b><br>{st.session_state.d_tb}</div>", unsafe_allow_html=True)
    with c6: st.markdown(f"<div class='card'><b>Đuôi B/T</b><br>{st.session_state.u_tb}</div>", unsafe_allow_html=True)
    with c7: st.markdown(f"<div class='card'><b>Tổng B/T</b><br>{st.session_state.t_tb}</div>", unsafe_allow_html=True)
    with c8: st.markdown(f"<div class='card'><b>Hiệu B/T</b><br>{st.session_state.h_tb}</div>", unsafe_allow_html=True)

with t3:
    m_data = []
    for d in range(10):
        row = []
        for du in range(10):
            idx = d * 10 + du
            t, h = (d+du)%10, (d-du+10)%10
            sk = st.session_state.dau[d] + st.session_state.duoi[du] + st.session_state.tong[t] + st.session_state.hieu[h] + \
                 ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du])) + \
                 st.session_state.bo[find_idx(idx, BO_MAP)] + st.session_state.giap[find_idx(idx, GIAP_MAP)] + st.session_state.dang[find_idx(idx, DANG_MAP)] + \
                 st.session_state.d_cl[d%2] + st.session_state.u_cl[du%2] + st.session_state.t_cl[t%2] + \
                 st.session_state.d_tb[1 if d>=5 else 0] + st.session_state.u_tb[1 if du>=5 else 0] + \
                 st.session_state.t_tb[1 if t>=5 else 0] + st.session_state.h_tb[1 if h>=5 else 0] + \
                 st.session_state.so_he[1 if idx not in SO_THUONG else 0]
            sr = sum(ROOT_DATA[r][c].index(v) for r in [r_d, r_k, r_g] for c, v in [("đầu",d),("đuôi",du),("tổng",t),("hiệu",h),("chạm",d),("chạm",du)])
            row.append(sk + sr)
        m_data.append(row)
    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    st.table(pd.DataFrame(m_data, columns=[str(i) for i in range(10)], index=[str(i) for i in range(10)]))
    st.markdown('</div>', unsafe_allow_html=True)

with t4:
    if st.session_state.ls: st.table(pd.DataFrame(st.session_state.ls))

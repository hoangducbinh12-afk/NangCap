import streamlit as st
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN MOBILE ---
st.set_page_config(page_title="HỆ THỐNG MÃ ROOT 18 BIẾN", layout="centered")

st.markdown("""
    <style>
    .stTable td, .stTable th { font-size: 11px !important; padding: 1px !important; text-align: center !important; font-weight: bold !important; }
    .main-title { text-align: center; color: #d32f2f; font-size: 20px; font-weight: bold; }
    .root-box { background-color: #f0f4f8; padding: 10px; border-radius: 10px; border: 1px solid #1E3A8A; margin-bottom: 10px; }
    .history-container { overflow-x: auto; white-space: nowrap; border: 1px solid #ddd; padding: 5px; background-color: #f8f9fa; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU CỐ ĐỊNH (KHÔNG DẤU) ---
BO_MAP = {
    "00": [0, 5, 50, 55], "01": [1, 10, 6, 60, 51, 15, 56, 65], "02": [2, 20, 7, 70, 52, 25, 57, 75],
    "03": [3, 30, 8, 80, 53, 35, 58, 85], "04": [4, 40, 9, 90, 54, 45, 59, 95], "11": [11, 16, 61, 66],
    "12": [12, 21, 17, 71, 62, 26, 67, 76], "13": [13, 31, 18, 81, 63, 36, 68, 86], "14": [14, 41, 19, 91, 64, 46, 69, 96],
    "22": [22, 27, 72, 77], "23": [23, 32, 28, 82, 73, 37, 78, 87], "24": [24, 42, 29, 92, 74, 47, 79, 97],
    "33": [33, 38, 83, 88], "34": [34, 43, 39, 93, 84, 48, 89, 98], "44": [44, 49, 94, 99]
}
GIAP_MAP = {
    "Ty": [0, 12, 24, 36, 48, 60, 72, 84, 96], "Suu": [1, 13, 25, 37, 49, 61, 73, 85, 97],
    "Dan": [2, 14, 26, 38, 50, 62, 74, 86, 98], "Mao": [3, 15, 27, 39, 51, 63, 75, 87, 99],
    "Thin": [4, 16, 28, 40, 52, 64, 76, 88], "Ty.": [5, 17, 29, 41, 53, 65, 77, 89],
    "Ngo": [6, 18, 30, 42, 54, 66, 78, 90], "Mui": [7, 19, 31, 43, 55, 67, 79, 91],
    "Than": [8, 20, 32, 44, 56, 68, 80, 92], "Dau": [9, 21, 33, 45, 57, 69, 81, 93],
    "Tuat": [10, 22, 34, 46, 58, 70, 82, 94], "Hoi": [11, 23, 35, 47, 59, 71, 83, 95]
}
DANG_MAP = {
    "kep": [0, 55, 11, 66, 22, 77, 33, 88, 44, 99, 5, 50, 16, 61, 27, 72, 38, 83, 49, 94],
    "sat kep": [1, 10, 12, 21, 23, 32, 34, 43, 45, 54, 56, 65, 67, 76, 78, 87, 89, 98, 9, 90],
    "cach 1": [2, 20, 8, 80, 13, 31, 19, 91, 24, 42, 35, 53, 46, 64, 57, 75, 79, 97, 68, 86],
    "cach 2": [3, 30, 18, 81, 25, 52, 47, 74, 69, 96, 7, 70, 14, 41, 29, 92, 36, 63, 58, 85],
    "cach 3": [4, 40, 6, 60, 15, 51, 17, 71, 28, 82, 26, 62, 37, 73, 39, 93, 48, 84, 59, 95]
}
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

# --- HÀM BỔ TRỢ ---
def get_root(s):
    nums = [int(x) for x in str(s) if x.isdigit()]
    if not nums: return 1
    t = sum(nums)
    while t > 9: t = sum(int(x) for x in str(t))
    return t if t > 0 else 1

def find_idx(n, mapping):
    for i, (name, nums) in enumerate(mapping.items()):
        if n in nums: return i
    return 0

# --- KHỞI TẠO STATE ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    st.session_state['bo'], st.session_state['giap'], st.session_state['dang'] = [0]*15, [0]*12, [0]*5
    for k in ['d_cl','u_cl','t_cl','d_tb','u_tb','t_tb','h_tb','so_he']: st.session_state[k] = [0]*2
    st.session_state.ls = []
    st.session_state.db = {}

# --- LOGIC CẬP NHẬT ---
def cap_nhat():
    raw = st.session_state.gdb_in
    if len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv = n//10, n%10
    tv, hv = (dv+duv)%10, (dv-duv+10)%10
    
    # Tính Hạng (Ma Trận B tổng lực)
    r_d, r_k, r_g = get_root(st.session_state.date_in), get_root(st.session_state.ky_in), get_root(raw)
    tmp = []
    for i in range(100):
        d, du = i//10, i%10
        t, h = (d+du)%10, (d-du+10)%10
        # Điểm Khan
        sk = st.session_state.dau[d] + st.session_state.duoi[du] + st.session_state.tong[t] + st.session_state.hieu[h] + \
             ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du])) + \
             st.session_state.bo[find_idx(i, BO_MAP)] + st.session_state.giap[find_idx(i, GIAP_MAP)] + st.session_state.dang[find_idx(i, DANG_MAP)] + \
             st.session_state.d_cl[d%2] + st.session_state.u_cl[du%2] + st.session_state.t_cl[t%2] + \
             st.session_state.d_tb[1 if d>=5 else 0] + st.session_state.u_tb[1 if du>=5 else 0] + \
             st.session_state.t_tb[1 if t>=5 else 0] + st.session_state.h_tb[1 if h>=5 else 0] + \
             st.session_state.so_he[1 if i not in SO_THUONG else 0]
        # Điểm Root (Trái -> Phải = 0 -> 9đ)
        sr = sum(ROOT_DATA[r][c].index(v) for r in [r_d, r_k, r_g] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        tmp.append({"s": f"{d}{du}", "d": sk + sr})
    
    df = pd.DataFrame(tmp).sort_values(by=["d","s"]).reset_index(drop=True)
    st.session_state.ls.insert(0, {"S": f"{n:02d}", "H": df[df['s']==f"{n:02d}"].index[0]+1, "D": df[df['s']==f"{n:02d}"].iloc[0]['d']})
    
    # Cập nhật Khan Bảng A
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==tv else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==hv else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    # Cập nhật các biến khác...
    for i in range(15): st.session_state.bo[i] = 0 if i==find_idx(n, BO_MAP) else st.session_state.bo[i]+1
    for i in range(12): st.session_state.giap[i] = 0 if i==find_idx(n, GIAP_MAP) else st.session_state.giap[i]+1
    for i in range(5): st.session_state.dang[i] = 0 if i==find_idx(n, DANG_MAP) else st.session_state.dang[i]+1
    # 50/50
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.t_cl[tv%2]=0; st.session_state.t_cl[(tv+1)%2]+=1
    st.session_state.d_tb[1 if dv>=5 else 0]=0; st.session_state.d_tb[0 if dv>=5 else 1]+=1
    st.session_state.u_tb[1 if duv>=5 else 0]=0; st.session_state.u_tb[0 if duv>=5 else 1]+=1
    st.session_state.t_tb[1 if tv>=5 else 0]=0; st.session_state.t_tb[0 if tv>=5 else 1]+=1
    st.session_state.h_tb[1 if hv>=5 else 0]=0; st.session_state.h_tb[0 if hv>=5 else 1]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- GIAO DIỆN ---
st.markdown("<div class='main-title'>💎 SIÊU HỆ THỐNG 18 BIẾN ROOT</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='root-box'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.text_input("Ngày (09092009):", "10052026", key="date_in")
    with c2: st.text_input("Kỳ quay:", "1", key="ky_in")
    with c3: st.text_input("GĐB (6 số):", "000000", key="gdb_in")
    st.button("🔥 CẬP NHẬT TỔNG LỰC", on_click=cap_nhat, type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with st.sidebar:
    if st.button("💾 LƯU CLOUD"):
        st.session_state.db[datetime.now().strftime("%H:%M")] = {k: list(st.session_state[k]) for k in st.session_state.keys() if k not in ['db','ls']}
        st.session_state.db[datetime.now().strftime("%H:%M")]['ls'] = list(st.session_state.ls)
    if st.session_state.db:
        sel = st.selectbox("Bản lưu:", list(st.session_state.db.keys())[::-1])
        if st.button("🔄 NẠP"):
            for k, v in st.session_state.db[sel].items(): st.session_state[k] = v
            st.rerun()
    st.divider()
    if st.button("🗑️ RESET"): st.session_state.clear(); st.rerun()

t1, t2, t3 = st.tabs(["⚡ Dàn", "📊 Bảng A", "🕒 Lịch Sử"])

with t1:
    f_list = []
    r_d, r_k, r_g = get_root(st.session_state.date_in), get_root(st.session_state.ky_in), get_root(st.session_state.gdb_in)
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
        sr = sum(ROOT_DATA[r][c].index(v) for r in [r_d, r_k, r_g] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        f_list.append({"s": f"{d}{du}", "d": sk + sr})
    df_f = pd.DataFrame(f_list).sort_values(by=["d", "s"], ascending=[False, True])
    st.success(", ".join(df_f.head(10)["s"].tolist()))
    st.info(", ".join(df_f.head(36)["s"].tolist()))

with t2:
    for lbl, k, names in [
        ("ĐẦU", "dau", range(10)), ("ĐUÔI", "duoi", range(10)), ("TỔNG", "tong", range(10)),
        ("HIỆU", "hieu", range(10)), ("CHẠM", "cham", range(10)), 
        ("BỘ", "bo", list(BO_MAP.keys())), ("12 GIÁP", "giap", list(GIAP_MAP.keys())), ("DẠNG", "dang", list(DANG_MAP.keys()))
    ]:
        st.write(f"**{lbl}**")
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        st.table(pd.DataFrame([st.session_state[k]], columns=names, index=[""]))
        st.markdown('</div>', unsafe_allow_html=True)
    st.write("**Khan 50/50**")
    st.write(f"Đầu C/L: {st.session_state.d_cl} | Đuôi C/L: {st.session_state.u_cl} | Tổng C/L: {st.session_state.t_cl}")
    st.write(f"Đầu B/T: {st.session_state.d_tb} | Đuôi B/T: {st.session_state.u_tb} | Tổng B/T: {st.session_state.t_tb}")
    st.write(f"Hiệu B/T: {st.session_state.h_tb} | Thường/Hệ: {st.session_state.so_he}")

with t3:
    if st.session_state.ls: st.table(pd.DataFrame(st.session_state.ls))
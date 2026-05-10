import streamlit as st
import pandas as pd
import json
from datetime import datetime

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="18 BIẾN PRO - FULL BẢNG A", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 650px !important; padding-top: 1rem !important; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 20px; font-weight: bold; margin-bottom: 15px; }
    .stTable td, .stTable th { font-size: 11px !important; padding: 3px !important; text-align: center !important; font-weight: bold !important; border: 1px solid #eee !important; }
    .root-display { font-size: 11px; font-weight: bold; color: #d32f2f; text-align: center; background: #fff5f5; padding: 6px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #ffe3e3; }
    </style>
    <html lang="vi" class="notranslate" translate="no"></html>
    """, unsafe_allow_html=True)

# --- 2. DỮ LIỆU CỐ ĐỊNH ---
DANG_5 = {"KEP":[0,55,11,66,22,77,33,88,44,99,5,50,16,61,27,72,38,83,49,94], "SAT KEP":[1,10,12,21,23,32,34,43,45,54,56,65,67,76,78,87,89,98,9,90], "CACH 1":[2,20,8,80,13,31,19,91,24,42,35,53,46,64,57,75,79,97,68,86], "CACH 2":[3,30,18,81,25,52,47,74,69,96,7,70,14,41,29,92,36,63,58,85], "CACH 3":[4,40,6,60,15,51,17,71,28,82,26,62,37,73,39,93,48,84,59,95]}
CL_4 = {"CHAN CHAN":[0,22,44,66,88,2,20,4,40,6,60,8,80,24,42,26,62,28,82,46,64,48,84,68,86], "CHAN LE":[1,3,5,7,9,21,23,25,27,29,41,43,45,47,49,61,63,65,67,69,81,83,85,87,89], "LE LE":[11,33,55,77,99,13,31,15,51,17,71,19,91,35,53,37,73,39,93,57,75,59,95,79,97], "LE CHAN":[10,12,14,16,18,30,32,34,36,38,50,52,54,56,58,70,72,74,76,78,90,92,94,96,98]}
BT_4 = {"BE BE":[0,11,22,33,44,1,10,2,20,3,30,4,40,12,21,13,31,14,41,23,32,24,42,34,43], "BE TO":[5,6,7,8,9,15,16,17,18,19,25,26,27,28,29,35,36,37,38,39,45,46,47,48,49], "TO BE":[90,91,92,93,94,80,81,82,83,84,70,71,72,73,74,60,61,62,63,64,50,51,52,53,54], "TO TO":[55,66,77,88,99,56,65,57,75,58,85,59,95,67,76,68,86,69,96,78,87,79,97,89,98]}
BO_MAP = {"00":[0,5,50,55],"01":[1,10,6,60,51,15,56,65],"02":[2,20,7,70,52,25,57,75],"03":[3,30,8,80,53,35,58,85],"04":[4,40,9,90,54,45,59,95],"11":[11,16,61,66],"12":[12,21,17,71,62,26,67,76],"13":[13,31,18,81,63,36,68,86],"14":[14,41,19,91,64,46,69,96],"22":[22,27,72,77],"23":[23,32,28,82,73,37,78,87],"24":[24,42,29,92,74,47,79,97],"33":[33,38,83,88],"34":[34,43,39,93,84,48,89,98],"44":[44,49,94,99]}
GIAP_12 = {"TI":[0,12,24,36,48,60,72,84,96],"SUU":[1,13,25,37,49,61,73,85,97],"DAN":[2,14,26,38,50,62,74,86,98],"MAO":[3,15,27,39,51,63,75,87,99],"THIN":[4,16,28,40,52,64,76,88],"TY":[5,17,29,41,53,65,77,89],"NGO":[6,18,30,42,54,66,78,90],"MUI":[7,19,31,43,55,67,79,91],"THAN":[8,20,32,44,56,68,80,92],"DAU":[9,21,33,45,57,69,81,93],"TUAT":[10,22,34,46,58,70,82,94],"HOI":[11,23,35,47,59,71,83,95]}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]

ROOT_DATA = {
    1:{"cham":[1,6,0,5,2,7,3,8,4,9],"dau":[1,6,0,5,4,9,2,7,3,8],"duoi":[1,6,2,7,0,5,4,9,3,8],"tong":[1,6,2,7,4,9,0,5,3,8],"hieu":[0,5,1,6,2,7,4,9,3,8]},
    2:{"cham":[2,7,1,6,3,8,4,9,0,5],"dau":[2,7,1,6,5,0,3,8,4,9],"duoi":[2,7,3,8,1,6,5,0,4,9],"tong":[2,7,3,8,5,0,1,6,4,9],"hieu":[0,5,2,7,1,6,3,8,4,9]},
    3:{"cham":[3,8,2,7,4,9,0,5,1,6],"dau":[3,8,2,7,6,1,4,9,5,0],"duoi":[3,8,4,9,2,7,6,1,5,0],"tong":[3,8,4,9,1,6,2,7,0,5],"hieu":[0,5,3,8,4,9,1,6,2,7]},
    4:{"cham":[4,9,3,8,0,5,1,6,2,7],"dau":[4,9,3,8,7,2,5,0,6,1],"duoi":[4,9,5,0,3,8,7,2,6,1],"tong":[4,9,0,5,2,7,1,6,3,8],"hieu":[0,5,4,9,1,6,2,7,3,8]},
    5:{"cham":[5,0,4,9,2,7,1,6,3,8],"dau":[5,0,2,7,3,8,4,9,1,6],"duoi":[5,0,4,9,1,6,2,7,3,8],"tong":[5,0,8,3,2,7,4,9,1,6],"hieu":[0,5,1,6,4,9,2,7,3,8]},
    6:{"cham":[6,1,5,0,3,8,2,7,4,9],"dau":[6,1,5,0,9,4,7,2,8,3],"duoi":[6,1,7,2,5,0,9,4,8,3],"tong":[6,1,9,4,3,8,5,0,2,7],"hieu":[0,5,1,6,2,7,3,8,4,9]},
    7:{"cham":[7,2,6,1,4,9,3,8,0,5],"dau":[7,2,6,1,0,5,8,3,9,4],"duoi":[7,2,8,3,6,1,0,5,9,4],"tong":[7,2,0,5,4,9,6,1,3,8],"hieu":[0,5,2,7,3,8,4,9,1,6]},
    8:{"cham":[8,3,7,2,5,0,4,9,1,6],"dau":[8,3,7,2,1,6,9,4,0,5],"duoi":[8,3,9,4,7,2,1,6,0,5],"tong":[8,3,1,6,5,0,7,2,4,9],"hieu":[0,5,3,8,2,7,1,6,4,9]},
    9:{"cham":[9,4,8,3,6,1,5,0,2,7],"dau":[9,4,8,3,2,7,0,5,1,6],"duoi":[9,4,0,5,8,3,2,7,1,6],"tong":[9,4,2,7,6,1,8,3,5,0],"hieu":[0,5,4,9,3,8,2,7,1,6]}
}

# --- 3. HELPERS ---
def get_root_val(s):
    try:
        t = sum(int(x) for x in str(s) if x.isdigit());
        while t > 9: t = sum(int(x) for x in str(t))
        return t
    except: return 0

def find_idx(n, mapping):
    for i, (name, nums) in enumerate(mapping.items()):
        if n in nums: return i
    return -1

# --- 4. KHỞI TẠO STATE ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    st.session_state.bo = [0]*15; st.session_state.giap = [0]*12
    st.session_state.dang5 = [0]*5; st.session_state.cl4 = [0]*4; st.session_state.bt4 = [0]*4
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0, 0]
    st.session_state.db_cloud = {}; st.session_state.ky_quay = 1
    st.session_state.n1 = 10; st.session_state.n2 = 36
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0
    st.session_state.ls = []

def get_full_matrix():
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    res = []
    for i in range(100):
        d, du, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+ \
             ((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+ \
             st.session_state.bo[find_idx(i, BO_MAP)]+st.session_state.giap[find_idx(i, GIAP_12)]+ \
             st.session_state.dang5[find_idx(i, DANG_5)]+st.session_state.cl4[find_idx(i, CL_4)]+st.session_state.bt4[find_idx(i, BT_4)]+ \
             st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.t_cl[t%2]+ \
             st.session_state.d_tb[1 if d>=5 else 0]+st.session_state.u_tb[1 if du>=5 else 0]+ \
             st.session_state.t_tb[1 if t>=5 else 0]+st.session_state.h_tb[1 if h>=5 else 0]+ \
             st.session_state.so_he[1 if i not in SO_THUONG else 0]
        def rs(r, cat, v): return ROOT_DATA[r][cat].index(v) if r in ROOT_DATA else 0
        sr = sum(rs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        res.append({"s": f"{d}{du}", "d": sk + sr})
    return res

def cap_nhat_logic():
    raw = st.session_state.gdb_in
    if not raw or len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv, tv, hv = n//10, n%10, (n//10+n%10)%10, (n//10-n%10+10)%10
    m_data = get_full_matrix(); df_rank = pd.DataFrame(m_data).sort_values(by=["d", "s"]).reset_index(drop=True)
    st.session_state.ls.insert(0, {"Số về": f"{n:02d}", "Vị trí": df_rank[df_rank['s'] == f"{n:02d}"].index[0]+1, "Kỳ": st.session_state.ky_quay})
    st.session_state.rd, st.session_state.rk, st.session_state.rg = get_root_val(st.session_state.date_in), get_root_val(st.session_state.ky_quay), get_root_val(raw)
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==tv else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==hv else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    for i in range(15): st.session_state.bo[i] = 0 if i==find_idx(n, BO_MAP) else st.session_state.bo[i]+1
    for i in range(12): st.session_state.giap[i] = 0 if i==find_idx(n, GIAP_12) else st.session_state.giap[i]+1
    for i in range(5): st.session_state.dang5[i] = 0 if i==find_idx(n, DANG_5) else st.session_state.dang5[i]+1
    for i in range(4): st.session_state.cl4[i] = 0 if i==find_idx(n, CL_4) else st.session_state.cl4[i]+1
    for i in range(4): st.session_state.bt4[i] = 0 if i==find_idx(n, BT_4) else st.session_state.bt4[i]+1
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.t_cl[tv%2]=0; st.session_state.t_cl[(tv+1)%2]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1
    st.session_state.d_tb[1 if dv>=5 else 0]=0; st.session_state.d_tb[0 if dv>=5 else 1]+=1
    st.session_state.u_tb[1 if duv>=5 else 0]=0; st.session_state.u_tb[0 if duv>=5 else 1]+=1
    st.session_state.t_tb[1 if tv>=5 else 0]=0; st.session_state.t_tb[0 if tv>=5 else 1]+=1
    st.session_state.h_tb[1 if hv>=5 else 0]=0; st.session_state.h_tb[0 if hv>=5 else 1]+=1

# --- 5. UI ---
st.markdown("<h2 class='main-title'>💎 18 BIẾN PRO - FULL OPTION</h2>", unsafe_allow_html=True)

# NHẬP LIỆU
c1, c2, c3 = st.columns([1.5, 1.5, 1.8])
with c1: st.text_input("GĐB:", value="000000", key="gdb_in")
with c2: st.text_input("Ngày:", datetime.now().strftime("%d%m%Y"), key="date_in")
with c3: st.number_input("Kỳ quay:", value=st.session_state.ky_quay, key="ky_w", step=1)
st.session_state.ky_quay = st.session_state.ky_w

st.markdown(f"<div class='root-display'>Root: Ngày {st.session_state.rd} | Kỳ {st.session_state.rk} | GĐB {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🔥 CẬP NHẬT TỔNG LỰC", on_click=cap_nhat_logic, type="primary", use_container_width=True)

tabs = st.tabs(["⚡ Dàn", "📊 Bảng A", "🎲 Bảng B", "🕒 Lịch Sử", "💾 Sao Lưu"])

current_m = get_full_matrix(); df_final = pd.DataFrame(current_m).sort_values(by=["d", "s"])

with tabs[0]:
    cn1, cn2 = st.columns(2)
    with cn1:
        st.session_state.n1 = st.number_input("Dàn 1:", 1, 100, st.session_state.n1, key="n1_w")
        st.success(", ".join(df_final.head(st.session_state.n1)["s"].tolist()))
    with cn2:
        st.session_state.n2 = st.number_input("Dàn 2:", 1, 100, st.session_state.n2, key="n2_w")
        st.info(", ".join(df_final.head(st.session_state.n2)["s"].tolist()))

with tabs[1]:
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    def table_r(lbl, k, cat, cols):
        st.write(f"**{lbl}**")
        kh = st.session_state[k]
        rt = [sum(ROOT_DATA[r][cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) if cat else 0 for i in range(len(kh))]
        st.table(pd.DataFrame([kh, rt], columns=cols, index=["K", "R"]))

    # Các biến chính
    for l, k, c in [("ĐẦU","dau","dau"),("ĐUÔI","duoi","duoi"),("TỔNG","tong","tong"),("HIỆU","hieu","hieu"),("CHẠM","cham","cham")]: 
        table_r(l, k, c, range(10))
    
    # Bộ và Giáp
    table_r("BỘ (15)", "bo", None, list(BO_MAP.keys()))
    table_r("GIÁP (12)", "giap", None, list(GIAP_12.keys()))
    
    # 5 Dạng và 13 Biến thể (Dạng kép/cách, Chẵn lẻ 4, Bé to 4)
    st.write("**5 DẠNG KÉP/CÁCH**")
    st.table(pd.DataFrame([st.session_state.dang5], columns=list(DANG_5.keys()), index=["K"]))
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.write("**CHẴN LẺ 4**")
        st.table(pd.DataFrame([st.session_state.cl4], columns=list(CL_4.keys()), index=["K"]))
    with col_v2:
        st.write("**BÉ TO 4**")
        st.table(pd.DataFrame([st.session_state.bt4], columns=list(BT_4.keys()), index=["K"]))

    # 8 Biến phụ
    st.write("**8 BIẾN PHỤ (50/50)**")
    phu_data = {
        "ĐẦU C/L": st.session_state.d_cl, "ĐUÔI C/L": st.session_state.u_cl, "TỔNG C/L": st.session_state.t_cl,
        "HỆ SỐ": st.session_state.so_he, "ĐẦU B/T": st.session_state.d_tb, "ĐUÔI B/T": st.session_state.u_tb,
        "TỔNG B/T": st.session_state.t_tb, "HIỆU B/T": st.session_state.h_tb
    }
    st.table(pd.DataFrame(phu_data, index=["0 (Bé/Chẵn/Thường)", "1 (To/Lẻ/Hệ)"]))

with tabs[2]:
    m_vals = [[next(x['d'] for x in current_m if x['s'] == f"{d}{du}") for du in range(10)] for d in range(10)]
    st.table(pd.DataFrame(m_vals, columns=range(10), index=range(10)))

with tabs[3]:
    if st.session_state.ls: st.table(pd.DataFrame(st.session_state.ls))
    else: st.info("Chưa có lịch sử.")

with tabs[4]:
    st.subheader("💾 Quản lý")
    sv = {k: st.session_state[k] for k in ['dau','duoi','tong','hieu','cham','bo','giap','dang5','cl4','bt4','d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb','ls','ky_quay','rd','rk','rg']}
    st.download_button("📥 TẢI DỮ LIỆU (.json)", data=json.dumps(sv), file_name="backup_18bien.json", use_container_width=True)
    up = st.file_uploader("📤 UPLOAD DỮ LIỆU", type="json")
    if up and st.button("🚀 XÁC NHẬN KHÔI PHỤC"):
        ld = json.load(up)
        for k, v in ld.items():
            if k not in ['gdb_in', 'date_in', 'ky_w', 'n1_w', 'n2_w']: st.session_state[k] = v
        st.rerun()

import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CẤU HÌNH GIAO DIỆN CHUẨN ---
st.set_page_config(page_title="18 BIEN PRO - TOAN DIEN", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 580px !important; padding-top: 1rem !important; }
    .main-title { text-align: center; color: #1E3A8A; font-size: 20px; font-weight: bold; margin-bottom: 15px; }
    .stTable td, .stTable th { font-size: 10px !important; padding: 2px !important; text-align: center !important; font-weight: bold !important; border: 1px solid #eee !important; }
    .dan-box-1 { background-color: #e8f5e9; padding: 10px; border-radius: 5px; border: 1px solid #c8e6c9; color: #2e7d32; font-family: monospace; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    .dan-box-2 { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border: 1px solid #bbdefb; color: #1565c0; font-family: monospace; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    .root-display { font-size: 11px; font-weight: bold; color: #d32f2f; text-align: center; background: #fff5f5; padding: 6px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #ffe3e3; }
    /* Fix nut bam +/- nho cho phan loc dan */
    .small-btn button { height: 30px !important; width: 100% !important; padding: 0px !important; font-size: 14px !important; }
    .history-container { overflow-x: auto; white-space: nowrap; border: 1px solid #ddd; padding: 5px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 10px; }
    </style>
    <html lang="vi" class="notranslate" translate="no"></html>
    """, unsafe_allow_html=True)

# --- 2. DỮ LIỆU NHÓM SỐ ---
BO_MAP = {"00":[0,5,50,55],"01":[1,10,6,60,51,15,56,65],"02":[2,20,7,70,52,25,57,75],"03":[3,30,8,80,53,35,58,85],"04":[4,40,9,90,54,45,59,95],"11":[11,16,61,66],"12":[12,21,17,71,62,26,67,76],"13":[13,31,18,81,63,36,68,86],"14":[14,41,19,91,64,46,69,96],"22":[22,27,72,77],"23":[23,32,28,82,73,37,78,87],"24":[24,42,29,92,74,47,79,97],"33":[33,38,83,88],"34":[34,43,39,93,84,48,89,98],"44":[44,49,94,99]}
CHAN_LE_4 = {"CHAN CHAN":[0,22,44,66,88,2,20,4,40,6,60,8,80,24,42,26,62,28,82,46,64,48,84,68,86], "CHAN LE":[1,3,5,7,9,21,23,25,27,29,41,43,45,47,49,61,63,65,67,69,81,83,85,87,89], "LE LE":[11,33,55,77,99,13,31,15,51,17,71,19,91,35,53,37,73,39,93,57,75,59,95,79,97], "LE CHAN":[10,12,14,16,18,30,32,34,36,38,50,52,54,56,58,70,72,74,76,78,90,92,94,96,98]}
BE_TO_4 = {"BE BE":[0,11,22,33,44,1,10,2,20,3,30,4,40,12,21,13,31,14,41,23,32,24,42,34,43], "BE TO":[5,6,7,8,9,15,16,17,18,19,25,26,27,28,29,35,36,37,38,39,45,46,47,48,49], "TO BE":[90,91,92,93,94,80,81,82,83,84,70,71,72,73,74,60,61,62,63,64,50,51,52,53,54], "TO TO":[55,66,77,88,99,56,65,57,75,58,85,59,95,67,76,68,86,69,96,78,87,79,97,89,98]}
GIAP_12 = {"TI":[0,12,24,36,48,60,72,84,96],"SUU":[1,13,25,37,49,61,73,85,97],"DAN":[2,14,26,38,50,62,74,86,98],"MAO":[3,15,27,39,51,63,75,87,99],"THIN":[4,16,28,40,52,64,76,88],"TY":[5,17,29,41,53,65,77,89],"NGO":[6,18,30,42,54,66,78,90],"MUI":[7,19,31,43,55,67,79,91],"THAN":[8,20,32,44,56,68,80,92],"DAU":[9,21,33,45,57,69,81,93],"TUAT":[10,22,34,46,58,70,82,94],"HOI":[11,23,35,47,59,71,83,95]}
DANG_5 = {"KEP":[0,55,11,66,22,77,33,88,44,99,5,50,16,61,27,72,38,83,49,94], "SAT KEP":[1,10,12,21,23,32,34,43,45,54,56,65,67,76,78,87,89,98,09,90], "CACH 1":[2,20,8,80,13,31,19,91,24,42,35,53,46,64,57,75,79,97,68,86], "CACH 2":[3,30,18,81,25,52,47,74,69,96,07,70,14,41,29,92,36,63,58,85], "CACH 3":[4,40,06,60,15,51,17,71,28,82,26,62,37,73,39,93,48,84,59,95]}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]

ROOT_DATA = {
    1: {"cham":[1,6,0,5,2,7,3,8,4,9], "dau":[1,6,0,5,4,9,2,7,3,8], "duoi":[1,6,2,7,0,5,4,9,3,8], "tong":[1,6,2,7,4,9,0,5,3,8], "hieu":[0,5,1,6,2,7,4,9,3,8]},
    2: {"cham":[2,7,1,6,3,8,4,9,0,5], "dau":[2,7,1,6,5,0,3,8,4,9], "duoi":[2,7,3,8,1,6,5,0,4,9], "tong":[2,7,3,8,5,0,1,6,4,9], "hieu":[0,5,2,7,1,6,3,8,4,9]},
    3: {"cham":[3,8,2,7,4,9,0,5,1,6], "dau":[3,8,2,7,6,1,4,9,5,0], "duoi":[3,8,4,9,2,7,6,1,5,0], "tong":[3,8,4,9,1,6,2,7,0,5], "hieu":[0,5,3,8,4,9,1,6,2,7]},
    4: {"cham":[4,9,3,8,0,5,1,6,2,7], "dau":[4,9,3,8,7,2,5,0,6,1], "duoi":[4,9,5,0,3,8,7,2,6,1], "tong":[4,9,0,5,2,7,1,6,3,8], "hieu":[0,5,4,9,1,6,2,7,3,8]},
    5: {"cham":[5,0,4,9,2,7,1,6,3,8], "dau":[5,0,2,7,3,8,4,9,1,6], "duoi":[5,0,4,9,1,6,2,7,3,8], "tong":[5,0,8,3,2,7,4,9,1,6], "hieu":[0,5,1,6,4,9,2,7,3,8]},
    6: {"cham":[6,1,5,0,3,8,2,7,4,9], "dau":[6,1,5,0,9,4,7,2,8,3], "duoi":[6,1,7,2,5,0,9,4,8,3], "tong":[6,1,9,4,3,8,5,0,2,7], "hieu":[0,5,1,6,2,7,3,8,4,9]},
    7: {"cham":[7,2,6,1,4,9,3,8,0,5], "dau":[7,2,6,1,0,5,8,3,9,4], "duoi":[7,2,8,3,6,1,0,5,9,4], "tong":[7,2,0,5,4,9,6,1,3,8], "hieu":[0,5,2,7,3,8,4,9,1,6]},
    8: {"cham":[8,3,7,2,5,0,4,9,1,6], "dau":[8,3,7,2,1,6,9,4,0,5], "duoi":[8,3,9,4,7,2,1,6,0,5], "tong":[8,3,1,6,5,0,7,2,4,9], "hieu":[0,5,3,8,2,7,1,6,4,9]},
    9: {"cham":[9,4,8,3,6,1,5,0,2,7], "dau":[9,4,8,3,2,7,0,5,1,6], "duoi":[9,4,0,5,8,3,2,7,1,6], "tong":[9,4,2,7,6,1,8,3,5,0], "hieu":[0,5,4,9,3,8,2,7,1,6]}
}

# --- 3. HELPERS ---
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

# --- 4. KHỞI TẠO STATE ---
if 'dau' not in st.session_state:
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    st.session_state.bo = [0]*15; st.session_state.cl4 = [0]*4; st.session_state.bt4 = [0]*4; st.session_state.giap = [0]*12; st.session_state.dang = [0]*5
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0, 0]
    st.session_state.db_cloud, st.session_state.ky_quay, st.session_state.n1, st.session_state.n2 = {}, 1, 10, 36
    st.session_state.rd, st.session_state.rk, st.session_state.rg, st.session_state.ls = 0, 0, 0, []

def cap_nhat_logic():
    raw = st.session_state.gdb_in
    if not raw or len(raw) < 2: return
    n = int(raw[-2:])
    dv, duv = n//10, n%10
    # Tinh toan ma tran hien tai de lay Hang (Vị trí)
    rd, rk, rg = get_root(st.session_state.date_in), get_root(st.session_state.ky_quay), get_root(raw)
    res_list = []
    for i in range(100):
        d, du, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        def rs(r, cat, v): return ROOT_DATA[r][cat].index(v) if r in ROOT_DATA else 0
        sk = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+st.session_state.bo[find_idx(i, BO_MAP)]+st.session_state.cl4[find_idx(i, CHAN_LE_4)]+st.session_state.bt4[find_idx(i, BE_TO_4)]+st.session_state.giap[find_idx(i, GIAP_12)]+st.session_state.dang[find_idx(i, DANG_5)]+st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.t_cl[t%2]+st.session_state.so_he[1 if i not in SO_THUONG else 0]+st.session_state.d_tb[1 if d>=5 else 0]+st.session_state.u_tb[1 if du>=5 else 0]+st.session_state.t_tb[1 if t>=5 else 0]+st.session_state.h_tb[1 if h>=5 else 0]
        sr = sum(rs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        res_list.append({"s": f"{d}{du}", "d": sk + sr})
    df_rank = pd.DataFrame(res_list).sort_values(by=["d", "s"]).reset_index(drop=True)
    vị_tri = df_rank[df_rank['s'] == f"{n:02d}"].index[0] + 1
    
    # Luu lich su
    st.session_state.ls.insert(0, {"Số về": f"{n:02d}", "Vị trí": vị_tri})
    
    # Cap nhat Root hien thi
    st.session_state.rd, st.session_state.rk, st.session_state.rg = rd, rk, rg
    
    # Cap nhat Khan
    for i in range(10):
        st.session_state.dau[i] = 0 if i==dv else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==duv else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==((dv+duv)%10) else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==((dv-duv+10)%10) else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==dv or i==duv) else st.session_state.cham[i]+1
    for i in range(15): st.session_state.bo[i] = 0 if i==find_idx(n, BO_MAP) else st.session_state.bo[i]+1
    for i in range(4): st.session_state.cl4[i] = 0 if i==find_idx(n, CHAN_LE_4) else st.session_state.cl4[i]+1
    for i in range(4): st.session_state.bt4[i] = 0 if i==find_idx(n, BE_TO_4) else st.session_state.bt4[i]+1
    for i in range(12): st.session_state.giap[i] = 0 if i==find_idx(n, GIAP_12) else st.session_state.giap[i]+1
    for i in range(5): st.session_state.dang[i] = 0 if i==find_idx(n, DANG_5) else st.session_state.dang[i]+1
    st.session_state.d_cl[dv%2]=0; st.session_state.d_cl[(dv+1)%2]+=1
    st.session_state.u_cl[duv%2]=0; st.session_state.u_cl[(duv+1)%2]+=1
    st.session_state.t_cl[((dv+duv)%10)%2]=0; st.session_state.t_cl[(((dv+duv)%10)+1)%2]+=1
    st.session_state.d_tb[1 if dv>=5 else 0]=0; st.session_state.d_tb[0 if dv>=5 else 1]+=1
    st.session_state.u_tb[1 if duv>=5 else 0]=0; st.session_state.u_tb[0 if duv>=5 else 1]+=1
    st.session_state.t_tb[1 if ((dv+duv)%10)>=5 else 0]=0; st.session_state.t_tb[0 if ((dv+duv)%10)>=5 else 1]+=1
    st.session_state.h_tb[1 if ((dv-duv+10)%10)>=5 else 0]=0; st.session_state.h_tb[0 if ((dv-duv+10)%10)>=5 else 1]+=1
    st.session_state.so_he[1 if n not in SO_THUONG else 0]=0; st.session_state.so_he[0 if n not in SO_THUONG else 1]+=1

# --- 5. UI CHÍNH ---
st.markdown("<div class='main-title'>💎 HE THONG 18 BIEN PRO - TOAN DIEN</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ QUAN LY")
    if st.button("💾 LUU CLOUD"):
        st.session_state.db_cloud[datetime.now().strftime("%H:%M")] = {k: list(st.session_state[k]) if isinstance(st.session_state[k], list) else st.session_state[k] for k in st.session_state.keys() if k != 'db_cloud'}
    if st.session_state.db_cloud:
        sel = st.selectbox("Ban sao:", list(st.session_state.db_cloud.keys())[::-1])
        cl1, cl2 = st.columns(2)
        with cl1: 
            if st.button("🚀 NAP"):
                for k, v in st.session_state.db_cloud[sel].items(): st.session_state[k] = v
                st.rerun()
        with cl2:
            if st.button("🗑️ XOA"): del st.session_state.db_cloud[sel]; st.rerun()
    if st.button("❌ RESET ALL"): st.session_state.clear(); st.rerun()

# NHAP LIEU (BO NUT +/- O KY QUAY)
c1, c2, c3 = st.columns([1.5, 1.5, 1.8])
with c1: st.text_input("GDB vua no:", value="000000", key="gdb_in")
with c2: st.text_input("Ngay (ddmmyyyy):", value="09052026", key="date_in")
with c3: st.number_input("Ky quay (full so):", value=st.session_state.ky_quay, key="ky_quay")

st.markdown(f"<div class='root-display'>Root: Ngay {st.session_state.rd} | Ky {st.session_state.rk} | GDB {st.session_state.rg}</div>", unsafe_allow_html=True)
st.button("🔥 CAP NHAT TONG LUC", on_click=cap_nhat_logic, type="primary", use_container_width=True)

tabs = st.tabs(["⚡ Dan", "📊 Bang A", "🔢 Root", "🛠️ Sua", "🕒 Lich Su"])

with tabs[0]:
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    res_list = []
    for i in range(100):
        d, du, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        def rs(r, cat, v): return ROOT_DATA[r][cat].index(v) if r in ROOT_DATA else 0
        s_root = sum(rs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",du),("tong",t),("hieu",h),("cham",d),("cham",du)])
        s_khan = st.session_state.dau[d]+st.session_state.duoi[du]+st.session_state.tong[t]+st.session_state.hieu[h]+((st.session_state.cham[d]*2) if d==du else (st.session_state.cham[d]+st.session_state.cham[du]))+st.session_state.bo[find_idx(i, BO_MAP)]+st.session_state.cl4[find_idx(i, CHAN_LE_4)]+st.session_state.bt4[find_idx(i, BE_TO_4)]+st.session_state.giap[find_idx(i, GIAP_12)]+st.session_state.dang[find_idx(i, DANG_5)]+st.session_state.d_cl[d%2]+st.session_state.u_cl[du%2]+st.session_state.t_cl[t%2]+st.session_state.so_he[1 if i not in SO_THUONG else 0]+st.session_state.d_tb[1 if d>=5 else 0]+st.session_state.u_tb[1 if du>=5 else 0]+st.session_state.t_tb[1 if t>=5 else 0]+st.session_state.h_tb[1 if h>=5 else 0]
        res_list.append({"s": f"{d}{du}", "d": s_khan + s_root})
    df_f = pd.DataFrame(res_list).sort_values(by=["d", "s"])
    
    col_n1, col_n2 = st.columns(2)
    for i, k in enumerate(["n1", "n2"]):
        with [col_n1, col_n2][i]:
            st.write(f"Dan {i+1}:")
            st.markdown(f"<div class='small-btn'>", unsafe_allow_html=True)
            cn1, cn2, cn3 = st.columns([1, 2, 1])
            with cn1: 
                if st.button("➖", key=f"m{k}"): st.session_state[k] -= 1; st.rerun()
            with cn2: st.session_state[k] = st.number_input(f"v{k}", value=st.session_state[k], label_visibility="collapsed")
            with cn3: 
                if st.button("➕", key=f"p{k}"): st.session_state[k] += 1; st.rerun()
            st.markdown(f"</div>", unsafe_allow_html=True)
            d_str = ", ".join(df_f.head(st.session_state[k])["s"].tolist())
            st.markdown(f"<div class='dan-box-{i+1} notranslate'>{d_str}</div>", unsafe_allow_html=True)
            if st.button(f"📋 COPY D{i+1}", key=f"cp{k}"):
                st.write(f'<script>navigator.clipboard.writeText("{d_str}")</script>', unsafe_allow_html=True); st.toast("Copied!")

with tabs[1]:
    def show_split(lbl, k, cat, names):
        st.write(f"**{lbl}**")
        khan, rt = st.session_state[k], [sum(ROOT_DATA[r][cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg]) for i in range(len(st.session_state[k]))] if cat else [0]*len(st.session_state[k])
        st.markdown('<div class="history-container notranslate">', unsafe_allow_html=True)
        st.table(pd.DataFrame([khan, rt], columns=names, index=["K", "R"]))
        st.markdown('</div>', unsafe_allow_html=True)
    for lbl, k, cat in [("DAU","dau","dau"),("DUOI","duoi","duoi"),("TONG","tong","tong"),("HIEU","hieu","hieu"),("CHAM","cham","cham")]: show_split(lbl, k, cat, range(10))
    show_split("BO", "bo", None, [x for x in BO_MAP.keys()])
    st.write("**8 BIEN PHU MOI**")
    st.table(pd.DataFrame({"DAU C/L":st.session_state.d_cl, "DUOI C/L":st.session_state.u_cl, "TONG C/L":st.session_state.t_cl, "HE SO":st.session_state.so_he}, index=["0/CHAN/THG","1/LE/HE"]))

with tabs[2]:
    for n, rv in [("NGAY", rd), ("KY", rk), ("GDB", rg)]:
        if rv in ROOT_DATA:
            st.write(f"**ROOT {n}: {rv}**")
            ck = {cat: [ROOT_DATA[rv][cat].index(i) for i in range(10)] for cat in ["dau","duoi","tong","hieu","cham"]}
            st.table(pd.DataFrame(ck).T)

with tabs[3]:
    st.write("**SUA TAY 18 BIEN**")
    if st.button("💾 LUU TAT CA"): st.rerun()
    for k, lbl in [('dau','DAU'),('duoi','DUOI'),('tong','TONG'),('hieu','HIEU'),('cham','CHAM')]:
        with st.expander(f"SUA {lbl}"):
            cols = st.columns(5)
            for i in range(10):
                with cols[i%5]: st.session_state[k][i] = st.number_input(f"{i}", value=st.session_state[k][i], key=f"e_{k}_{i}")

with tabs[4]:
    st.write("**LICH SU SO VE**")
    if st.session_state.ls:
        st.table(pd.DataFrame(st.session_state.ls))
    else: st.info("Chua co du lieu.")

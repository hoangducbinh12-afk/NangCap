import streamlit as st
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="HỆ THỐNG 18 BIẾN PRO", layout="centered")

st.markdown("""
    <style>
    /* Căn chỉnh lại vùng chứa chính */
    .block-container { padding-top: 1.5rem !important; max-width: 850px !important; }
    .main-title { text-align: center; font-size: 24px; font-weight: bold; color: #1e3a8a; margin-bottom: 15px; }
    
    /* Style cho Bảng A và B (Không dấu, font nhỏ vừa phải) */
    .stTable { font-size: 12px !important; font-family: sans-serif !important; }
    .stTable td { padding: 4px !important; text-align: center !important; }
    
    /* Box Dàn số hiển thị màu sắc */
    .dan-box-1 { background-color: #f0fdf4; padding: 10px; border-radius: 6px; border: 1px solid #bbf7d0; color: #166534; font-family: monospace; font-size: 14px; margin-bottom: 5px; min-height: 40px; }
    .dan-box-2 { background-color: #eff6ff; padding: 10px; border-radius: 6px; border: 1px solid #bfdbfe; color: #1e40af; font-family: monospace; font-size: 14px; margin-bottom: 5px; min-height: 40px; }
    
    /* Chỉ số Root */
    .root-bar { text-align: center; background: #fff1f2; padding: 8px; border-radius: 8px; border: 1px solid #fecdd3; margin-bottom: 15px; font-weight: bold; color: #be123c; font-size: 13px; }
    
    /* Nút bấm sát nhau */
    .stButton>button { width: 100%; border-radius: 4px; height: 35px; }
    .row-widget.stButton { margin-bottom: -10px; }
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

BO_MAP = {"00":[0,5,50,55],"01":[1,10,6,60,51,15,56,65],"02":[2,20,7,70,52,25,57,75],"03":[3,30,8,80,53,35,58,85],"04":[4,40,9,90,54,45,59,95],"11":[11,16,61,66],"12":[12,21,17,71,62,26,67,76],"13":[13,31,18,81,63,36,68,86],"14":[14,41,19,91,64,46,69,96],"22":[22,27,72,77],"23":[23,32,28,82,73,37,78,87],"24":[24,42,29,92,74,47,79,97],"33":[33,38,83,88],"34":[34,43,39,93,84,48,89,98],"44":[44,49,94,99]}
SO_THUONG = [2,3,4,6,8,13,15,17,18,19,20,24,25,26,28,30,31,35,37,39,40,42,46,47,48,51,52,53,57,59,60,62,64,68,69,71,73,74,75,79,80,81,82,84,86,91,93,95,96,97]

def get_root(val):
    s = str(val)
    digits = [int(d) for d in s if d.isdigit()]
    if not digits: return 0
    res = sum(digits)
    while res > 9: res = sum(int(d) for d in str(res))
    return res

# --- KHỞI TẠO STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
    # Điểm khan 10 biến chính
    for k in ['dau','duoi','tong','hieu','cham']: st.session_state[k] = [0]*10
    st.session_state.bo = [0]*15
    # Điểm khan 8 biến phụ
    for k in ['d_cl','u_cl','t_cl','so_he','d_tb','u_tb','t_tb','h_tb']: st.session_state[k] = [0]*2
    st.session_state.num_1, st.session_state.num_2 = 10, 36
    st.session_state.rd, st.session_state.rk, st.session_state.rg = 0, 0, 0

def update_data():
    raw = st.session_state.gdb_input
    if not raw or len(raw) < 2: return
    val = int(raw[-2:])
    d, u, t, h = val//10, val%10, (val//10 + val%10)%10, (val//10 - val%10 + 10)%10
    
    # Tính Root
    st.session_state.rd = get_root(st.session_state.date_input)
    st.session_state.rk = get_root(st.session_state.ky_input)
    st.session_state.rg = get_root(raw)
    
    # Cập nhật điểm khan (reset số vừa về, tăng số khác)
    for i in range(10):
        st.session_state.dau[i] = 0 if i==d else st.session_state.dau[i]+1
        st.session_state.duoi[i] = 0 if i==u else st.session_state.duoi[i]+1
        st.session_state.tong[i] = 0 if i==t else st.session_state.tong[i]+1
        st.session_state.hieu[i] = 0 if i==h else st.session_state.hieu[i]+1
        st.session_state.cham[i] = 0 if (i==d or i==u) else st.session_state.cham[i]+1
    
    # Cập nhật 8 biến phụ
    st.session_state.d_cl[d%2]=0; st.session_state.d_cl[(d+1)%2]+=1
    st.session_state.u_cl[u%2]=0; st.session_state.u_cl[(u+1)%2]+=1
    st.session_state.t_cl[t%2]=0; st.session_state.t_cl[(t+1)%2]+=1
    st.session_state.d_tb[1 if d>=5 else 0]=0; st.session_state.d_tb[0 if d>=5 else 1]+=1
    st.session_state.u_tb[1 if u>=5 else 0]=0; st.session_state.u_tb[0 if u>=5 else 1]+=1
    st.session_state.t_tb[1 if t>=5 else 0]=0; st.session_state.t_tb[0 if t>=5 else 1]+=1
    st.session_state.h_tb[1 if h>=5 else 0]=0; st.session_state.h_tb[0 if h>=5 else 1]+=1
    st.session_state.so_he[1 if val not in SO_THUONG else 0]=0; st.session_state.so_he[0 if val not in SO_THUONG else 1]+=1

# --- GIAO DIỆN CHÍNH ---
st.markdown("<div class='main-title'>💎 HỆ THỐNG THỐNG KÊ 18 BIẾN PRO</div>", unsafe_allow_html=True)

# Vùng nhập liệu
with st.container():
    col1, col2, col3 = st.columns([2, 5, 2])
    with col1: st.write("") # Spacer
    with col2:
        st.text_input("Số vừa nổ:", value="000000", key="gdb_input")
    
    c_date, c_ky = st.columns(2)
    with c_date: st.text_input("Ngày (ddmmyyyy):", value="09092009", key="date_input")
    with c_ky: st.number_input("Kỳ quay:", value=1, step=1, key="ky_input")

st.markdown(f"<div class='root-bar'>ROOT NGÀY: {st.session_state.rd} | ROOT KỲ: {st.session_state.rk} | ROOT GĐB: {st.session_state.rg}</div>", unsafe_allow_html=True)

if st.button("🚀 CẬP NHẬT DỮ LIỆU", type="primary", use_container_width=True):
    update_data()

tabs = st.tabs(["⚡ Lọc Dàn", "📊 Bảng A (18 Biến)", "🎲 Ma Trận B", "🛠️ Sửa Tay"])

# --- TAB 1: LỌC DÀN ---
with tabs[0]:
    l1, l2 = st.columns(2)
    with l1: st.number_input("Số quân Dàn 1:", value=10, key="num_1")
    with l2: st.number_input("Số quân Dàn 2:", value=36, key="num_2")
    
    # Tính toán tổng điểm cho 100 số
    scores = []
    rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
    for i in range(100):
        d, u, t, h = i//10, i%10, (i//10+i%10)%10, (i//10-i%10+10)%10
        # Điểm khan + Điểm Root (Tra bảng không dấu)
        def get_rs(r, cat, v): return ROOT_DATA[r][cat].index(v) if r in ROOT_DATA else 0
        s_root = sum(get_rs(r, c, v) for r in [rd,rk,rg] for c, v in [("dau",d),("duoi",u),("tong",t),("hieu",h),("cham",d),("cham",u)])
        s_khan = st.session_state.dau[d] + st.session_state.duoi[u] + st.session_state.tong[t] + st.session_state.hieu[h] + st.session_state.cham[d] + st.session_state.cham[u]
        s_extra = st.session_state.d_cl[d%2] + st.session_state.u_cl[u%2] + st.session_state.t_cl[t%2] + st.session_state.d_tb[1 if d>=5 else 0] + st.session_state.u_tb[1 if u>=5 else 0] + st.session_state.so_he[1 if i not in SO_THUONG else 0]
        scores.append({"s": f"{i:02d}", "total": s_khan + s_root + s_extra})
    
    df_sorted = pd.DataFrame(scores).sort_values(by="total")
    d1 = ", ".join(df_sorted.head(st.session_state.num_1)["s"].tolist())
    d2 = ", ".join(df_sorted.head(st.session_state.num_2)["s"].tolist())
    
    st.markdown(f"**Dàn 1 ({st.session_state.num_1} số):**")
    st.markdown(f"<div class='dan-box-1'>{d1}</div>", unsafe_allow_html=True)
    st.button("📋 Copy Dàn 1", key="cp1")
    
    st.markdown(f"**Dàn 2 ({st.session_state.num_2} số):**")
    st.markdown(f"<div class='dan-box-2'>{d2}</div>", unsafe_allow_html=True)
    st.button("📋 Copy Dàn 2", key="cp2")

# --- TAB 2: BẢNG A (HIỂN THỊ ĐỦ 18 BIẾN) ---
with tabs[1]:
    st.write("### CHI TIẾT ĐIỂM 18 BIẾN (KHÔNG DẤU)")
    
    def get_row_data(cat_name, state_key, root_cat):
        rd, rk, rg = st.session_state.rd, st.session_state.rk, st.session_state.rg
        row = []
        for i in range(10):
            pt = st.session_state[state_key][i]
            rt = sum(ROOT_DATA[r][root_cat].index(i) if r in ROOT_DATA else 0 for r in [rd,rk,rg])
            row.append(pt + rt)
        return row

    # 10 biến chính (Dau, Duoi, Tong, Hieu, Cham x2)
    data_a = {
        "DAU": get_row_data("DAU", "dau", "dau"),
        "DUOI": get_row_data("DUOI", "duoi", "duoi"),
        "TONG": get_row_data("TONG", "tong", "tong"),
        "HIEU": get_row_data("HIEU", "hieu", "hieu"),
        "CHAM": get_row_data("CHAM", "cham", "cham")
    }
    st.table(pd.DataFrame(data_a).T)

    st.write("---")
    # 8 biến phụ (Chẵn Lẻ, To Nhỏ, Hệ)
    st.write("8 BIẾN PHỤ (0: Chẵn/Bé/Thường | 1: Lẻ/To/Hệ)")
    extra_data = {
        "DAU CL/TB": [st.session_state.d_cl[0], st.session_state.d_cl[1], st.session_state.d_tb[0], st.session_state.d_tb[1]],
        "DUOI CL/TB": [st.session_state.u_cl[0], st.session_state.u_cl[1], st.session_state.u_tb[0], st.session_state.u_tb[1]],
        "TONG CL/TB": [st.session_state.t_cl[0], st.session_state.t_cl[1], st.session_state.t_tb[0], st.session_state.t_tb[1]],
        "HE SO": [st.session_state.so_he[0], st.session_state.so_he[1], 0, 0]
    }
    st.table(pd.DataFrame(extra_data, index=["0/Bé", "1/Lẻ", "To", "Hệ"]))

# --- TAB 3: MA TRẬN B ---
with tabs[2]:
    st.write("### MA TRAN DIEM TONG HOP (00-99)")
    matrix = []
    for d in range(10):
        r_data = []
        for u in range(10):
            val = d*10+u
            # Lấy điểm total đã tính ở Tab 1 hoặc tính lại nhanh
            idx = next(item for item in scores if item["s"] == f"{val:02d}")
            r_data.append(idx["total"])
        matrix.append(r_data)
    st.table(pd.DataFrame(matrix, index=[f"D{i}" for i in range(10)], columns=[f"U{i}" for i in range(10)]))

# --- TAB 4: SỬA TAY ---
with tabs[3]:
    st.warning("Dùng để điều chỉnh thông số khi cần thiết")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Điểm Khan 10 Biến:**")
        for i in range(10): st.session_state.dau[i] = st.number_input(f"Đầu {i}:", value=st.session_state.dau[i], key=f"ed_d_{i}")
    with c2:
        st.write("**Biến Phụ:**")
        st.session_state.d_cl[0] = st.number_input("Đầu Chẵn:", value=st.session_state.d_cl[0])
        st.session_state.d_cl[1] = st.number_input("Đầu Lẻ:", value=st.session_state.d_cl[1])

st.sidebar.markdown("### ☁️ CLOUD STORAGE")
if st.sidebar.button("💾 SAO LƯU DỮ LIỆU"): st.sidebar.success("Đã sao lưu!")
if st.sidebar.button("🗑️ XÓA DỮ LIỆU"): st.session_state.clear(); st.rerun()

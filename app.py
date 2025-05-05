import streamlit as st
import json

# 加载数据
with open('pokemon_data.json', 'r', encoding='utf-8') as f:
    pokemon_list = json.load(f)

gen_map = {
    "第一世代": 1, "第二世代": 2, "第三世代": 3,
    "第四世代": 4, "第五世代": 5, "第六世代": 6,
    "第七世代": 7, "第八世代": 8, "第九世代": 9
}

# 比较函数
def compare(val, symbol, poke_val):
    if val is None or poke_val is None:
        return True
    if symbol == "🔼":
        return poke_val > val
    elif symbol == "=":
        return poke_val == val
    elif symbol == "🔽":
        return poke_val < val
    return True

st.title("宝可梦筛选器")

# 输入部分
attr_include = st.text_input("包含属性 (逗号分隔)")
attr_exclude = st.text_input("排除属性 (逗号分隔)")
egg_include = st.text_input("包含蛋组 (逗号分隔)")
egg_exclude = st.text_input("排除蛋组 (逗号分隔)")
ability = st.text_input("特性")
effort_include = st.selectbox("包含努力值", ["", "HP", "攻击", "防御", "特攻", "特防", "速度"])
effort_exclude = st.text_input("排除努力值")
gender = st.selectbox("性别比例", ["", "7♂:1♀", "1♂:1♀", "1♂:3♀", "1♂:0♀", "0♂:1♀", "无性别"])
mega = st.selectbox("超级进化", ["", "有超级进化", "无超级进化"])
gmax = st.selectbox("超极巨化", ["", "有超极巨化", "无超极巨化"])
evolution = st.selectbox("进化阶段", ["", "无进化树", "一段", "二段", "最终"])

# 数值比较部分（放一行里）
col1, col2 = st.columns(2)
with col1:
    total_cmp = st.selectbox("种族值总和符号", ["🔼", "=", "🔽"])
    total_val = st.number_input("种族值总和", value=0)
with col2:
    speed_cmp = st.selectbox("速度符号", ["🔼", "=", "🔽"])
    speed_val = st.number_input("速度", value=0)

col3, col4 = st.columns(2)
with col3:
    height_cmp = st.selectbox("身高符号", ["🔼", "=", "🔽"])
    height_val = st.number_input("身高(m)", value=0.0)
with col4:
    weight_cmp = st.selectbox("体重符号", ["🔼", "=", "🔽"])
    weight_val = st.number_input("体重(kg)", value=0.0)

col5, col6 = st.columns(2)
with col5:
    hatch_cmp = st.selectbox("孵化周期符号", ["🔼", "=", "🔽"])
    hatch_val = st.number_input("孵化周期", value=0)
with col6:
    gen_cmp = st.selectbox("世代符号", ["🔼", "=", "🔽"])
    gen_val = st.number_input("世代", value=0)

# 搜索按钮
if st.button("🔍 搜索"):
    results = []
    for p in pokemon_list:
        attrs = p['属性'].split("/") if isinstance(p['属性'], str) else p['属性']
        eggs = p['蛋组'].split("/") if isinstance(p['蛋组'], str) else p['蛋组']

        if attr_include and not any(a in attrs for a in attr_include.split(",")):
            continue
        if attr_exclude and any(a in attrs for a in attr_exclude.split(",")):
            continue
        if egg_include and not any(e in eggs for e in egg_include.split(",")):
            continue
        if egg_exclude and any(e in eggs for e in egg_exclude.split(",")):
            continue
        if ability and ability not in p['特性']:
            continue
        if effort_include and effort_include not in p['努力值奖励']:
            continue
        if effort_exclude and effort_exclude in p['努力值奖励']:
            continue
        if gender and p['性别比例'] != gender:
            continue
        if mega and p['超级进化'] != mega:
            continue
        if gmax and p['超极巨化'] != gmax:
            continue
        if evolution and p['进化'] != evolution:
            continue

        poke_gen = gen_map.get(p.get('初登场世代', ""), 0)
        if not compare(total_val, total_cmp, p['种族值总和']):
            continue
        if not compare(speed_val, speed_cmp, p['速度种族值']):
            continue
        if not compare(height_val, height_cmp, p['身高(m)']):
            continue
        if not compare(weight_val, weight_cmp, p['体重(kg)']):
            continue
        if not compare(hatch_val, hatch_cmp, p['孵化周期']):
            continue
        if not compare(gen_val, gen_cmp, poke_gen):
            continue

        results.append(f"{p['编号']} {p['中文名']}")

    if results:
        st.markdown("<br>".join(results), unsafe_allow_html=True)
    else:
        st.write("未找到符合条件的宝可梦。")

# 重置按钮
if st.button("🔄 重置"):
    st.experimental_rerun()


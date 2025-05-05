import streamlit as st
import json

# 加载数据
with open('pokemon_data.json', 'r', encoding='utf-8') as f:
    pokemon_list = json.load(f)

compare_symbols = ["🔼", "=", "🔽"]

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

# 输入框替代多选框
attr_include = st.text_input("包含属性（用 / 分隔，例如 火/水）")
attr_exclude = st.text_input("排除属性（用 / 分隔，例如 电/冰）")
egg_include = st.text_input("包含蛋组（用 / 分隔，例如 怪兽/水中1）")
egg_exclude = st.text_input("排除蛋组（用 / 分隔，例如 飞行/虫）")

specify_undiscovered = st.checkbox("指定未发现蛋组")
ability = st.text_input("特性")
effort_include = st.selectbox("努力值包含", ["", "HP", "攻击", "防御", "特攻", "特防", "速度"])
effort_exclude = st.text_input("排除努力值")
gender = st.selectbox("性别比例", ["", "7♂:1♀", "1♂:1♀", "1♂:3♀", "1♂:0♀", "0♂:1♀", "无性别"])
mega = st.selectbox("超级进化", ["", "有", "无"])
gmax = st.selectbox("超极巨化", ["", "有", "无"])
evolution = st.selectbox("进化阶段", ["", "无进化树", "一段", "二段", "最终"])

# 数值对比 + 符号 一列展示
st.subheader("数值条件")
col1, col2, col3 = st.columns(3)
with col1:
    total_cmp = st.selectbox("种族值总和 符号", compare_symbols)
    total_val = st.number_input("数值", step=1)
with col2:
    speed_cmp = st.selectbox("速度 符号", compare_symbols)
    speed_val = st.number_input("数值", step=1, key="speed")
with col3:
    weight_cmp = st.selectbox("体重 符号", compare_symbols)
    weight_val = st.number_input("数值", step=1, key="weight")

col4, col5, col6 = st.columns(3)
with col4:
    height_cmp = st.selectbox("身高 符号", compare_symbols)
    height_val = st.number_input("数值", step=1, key="height")
with col5:
    hatch_cmp = st.selectbox("孵化周期 符号", compare_symbols)
    hatch_val = st.number_input("数值", step=1, key="hatch")
with col6:
    gen_cmp = st.selectbox("世代 符号", compare_symbols)
    gen_val = st.number_input("数值", step=1, key="gen")

# 搜索按钮
if st.button("🔍 搜索"):
    results = []
    for p in pokemon_list:
        # 属性、蛋组处理
        attrs = p['属性'].split("/") if isinstance(p['属性'], str) else p['属性']
        eggs = p['蛋组'].split("/") if isinstance(p['蛋组'], str) else p['蛋组']
        if attr_include and not any(a in attrs for a in attr_include.split("/")):
            continue
        if attr_exclude and any(a in attrs for a in attr_exclude.split("/")):
            continue
        if egg_include and not any(e in eggs for e in egg_include.split("/")):
            continue
        if egg_exclude and any(e in eggs for e in egg_exclude.split("/")):
            continue
        if specify_undiscovered and "未发现组" not in eggs:
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
        if evolution and p.get('进化', '') != evolution:
            continue
        if not compare(total_val, total_cmp, p['种族值总和']):
            continue
        if not compare(speed_val, speed_cmp, p['速度种族值']):
            continue
        if not compare(height_val, height_cmp, p['身高(m)']):
            continue
        if not compare(weight_val, weight_cmp, p['体重(kg)']):
            continue
        if not compare(gen_val, gen_cmp, p.get('初登场世代', 0)):
            continue
        results.append(f"{p['编号']} {p['中文名']}")

    if results:
        st.markdown("<br>".join(results), unsafe_allow_html=True)
    else:
        st.write("未找到符合条件的宝可梦。")

# 重置按钮（刷新页面）
if st.button("🔄 重置"):
    st.experimental_rerun()

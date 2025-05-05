import streamlit as st
import json

# 加载数据
with open('pokemon_data.json', 'r', encoding='utf-8') as f:
    pokemon_list = json.load(f)

# 世代映射
gen_map = {
    "第一世代": 1, "第二世代": 2, "第三世代": 3, "第四世代": 4,
    "第五世代": 5, "第六世代": 6, "第七世代": 7, "第八世代": 8, "第九世代": 9
}

# 初始化 session 状态
if 'result' not in st.session_state:
    st.session_state.result = pokemon_list

st.title("宝可梦筛选器（干净版）")

# 筛选条件区
attrs = st.multiselect("属性（多选）", ['草', '火', '水', '电', '冰', '格斗', '毒', '地面', '飞行', '超能力', '虫', '岩石', '幽灵', '龙', '恶', '钢', '妖精'])
exclude_attrs = st.multiselect("排除属性", ['草', '火', '水', '电', '冰', '格斗', '毒', '地面', '飞行', '超能力', '虫', '岩石', '幽灵', '龙', '恶', '钢', '妖精'])

eggs = st.multiselect("蛋组（多选）", ['怪兽', '水中1', '水中2', '水中3', '虫', '飞行', '地面', '妖精', '植物', '人形', '矿物', '不定形', '龙', '未发现组'])
exclude_eggs = st.multiselect("排除蛋组", ['怪兽', '水中1', '水中2', '水中3', '虫', '飞行', '地面', '妖精', '植物', '人形', '矿物', '不定形', '龙', '未发现组'])
specify_undiscovered = st.checkbox("指定未发现蛋组")

ability = st.text_input("特性包含")
effort = st.text_input("努力值包含")
exclude_effort = st.text_input("排除努力值")

gender = st.selectbox("性别比例", ["", "7♂:1♀", "1♂:1♀", "1♂:3♀", "1♂:0♀", "0♂:1♀", "无性别"])
mega = st.selectbox("超级进化", ["", "有超级进化", "无超级进化"])
gmax = st.selectbox("超极巨化", ["", "有超极巨化", "无超极巨化"])
evolution = st.selectbox("进化阶段", ["", "无进化树", "一段", "二段", "最终"])

def num_filter(label):
    cmp = st.selectbox(f"{label} 比较符", [">", "=", "<"], key=label)
    val = st.number_input(f"{label} 数值", value=0)
    return cmp, val

cmp_total, val_total = num_filter("种族值总和")
cmp_speed, val_speed = num_filter("速度")
cmp_height, val_height = num_filter("身高(m)")
cmp_weight, val_weight = num_filter("体重(kg)")
cmp_hatch, val_hatch = num_filter("孵化周期")
cmp_gen, val_gen = num_filter("世代")

# 搜索与重置按钮
col1, col2 = st.columns(2)
if col1.button("🔍 搜索"):
    result = []
    for p in pokemon_list:
        p_attrs = p['属性'].split("/") if isinstance(p['属性'], str) else p['属性']
        p_eggs = p['蛋组'].split("/") if isinstance(p['蛋组'], str) else p['蛋组']

        if attrs and not any(a in p_attrs for a in attrs):
            continue
        if exclude_attrs and any(a in p_attrs for a in exclude_attrs):
            continue
        if specify_undiscovered and '未发现组' not in p_eggs:
            continue
        if eggs and not any(e in p_eggs for e in eggs):
            continue
        if exclude_eggs and any(e in p_eggs for e in exclude_eggs):
            continue
        if ability and ability not in p['特性']:
            continue
        if effort and effort not in p['努力值奖励']:
            continue
        if exclude_effort and exclude_effort in p['努力值奖励']:
            continue
        if gender and p['性别比例'] != gender:
            continue
        if mega and p['超级进化'] != mega:
            continue
        if gmax and p['超极巨化'] != gmax:
            continue
        if evolution and p['进化'] != evolution:
            continue

        def compare(cmp, val, poke_val):
            try:
                poke_val = float(poke_val)
            except:
                return True
            if cmp == ">":
                return poke_val > val
            elif cmp == "=":
                return poke_val == val
            else:
                return poke_val < val

        if not compare(cmp_total, val_total, p['种族值总和']):
            continue
        if not compare(cmp_speed, val_speed, p['速度种族值']):
            continue
        if not compare(cmp_height, val_height, p['身高(m)']):
            continue
        if not compare(cmp_weight, val_weight, p['体重(kg)']):
            continue
        if not compare(cmp_hatch, val_hatch, p['孵化周期']):
            continue
        poke_gen = gen_map.get(p.get('初登场世代', ""), 0)
        if not compare(cmp_gen, val_gen, poke_gen):
            continue

        result.append(p)
    st.session_state.result = result

if col2.button("🔄 重置"):
    st.session_state.result = pokemon_list

# 输出结果
if st.session_state.result:
    st.write(f"### 共找到 {len(st.session_state.result)} 个宝可梦")
    for p in st.session_state.result:
        st.markdown(f"- **{p['编号']} {p['中文名']}**")
else:
    st.warning("❌ 没有找到符合条件的宝可梦。")

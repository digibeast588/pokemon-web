import streamlit as st
import json

# 读取数据
with open('pokemon_data.json', 'r', encoding='utf-8') as f:
    pokemon_list = json.load(f)

# 自动提取特性、属性、蛋组
all_abilities = sorted(set(sum([p['特性'].split("/") if isinstance(p['特性'], str) else p['特性'] for p in pokemon_list], [])))
all_attributes = sorted(set(sum([p['属性'].split("/") if isinstance(p['属性'], str) else p['属性'] for p in pokemon_list], [])))
all_eggs = sorted(set(sum([p['蛋组'].split("/") if isinstance(p['蛋组'], str) else p['蛋组'] for p in pokemon_list], [])))

effort_list = ["HP", "攻击", "防御", "特攻", "特防", "速度"]
gen_map = {"第一世代":1,"第二世代":2,"第三世代":3,"第四世代":4,"第五世代":5,"第六世代":6,"第七世代":7,"第八世代":8,"第九世代":9}

def compare(val, cmp, poke_val):
    if val is None or poke_val is None:
        return True
    return poke_val > val if cmp == "🔼" else poke_val == val if cmp == "=" else poke_val < val

# UI
st.title("Pokemon Flexible Searcher")

attr_incl = st.multiselect("属性包含", all_attributes)
attr_excl = st.multiselect("属性排除", all_attributes)

egg_incl = st.multiselect("蛋组包含", all_eggs)
egg_excl = st.multiselect("蛋组排除", all_eggs)
undiscovered_only = st.checkbox("指定未发现蛋组")

ability_selected = st.multiselect("特性", all_abilities)
effort_include = st.multiselect("努力值包含", effort_list)
effort_exclude = st.multiselect("排除努力值", effort_list)

gender = st.selectbox("性别比例", ["", "7♂:1♀", "1♂:1♀", "1♂:3♀", "1♂:0♀", "0♂:1♀", "无性别"])
mega = st.selectbox("超级进化", ["", "有超级进化", "无超级进化"])
gmax = st.selectbox("超极巨化", ["", "有超极巨化", "无超极巨化"])
evolution = st.selectbox("进化阶段", ["", "无进化树", "一段", "二段", "最终"])

# 数值 + 对比符
num_fields = [("种族值总和", "total"), ("速度", "speed"), ("身高(m)", "height"), ("体重(kg)", "weight"), ("孵化周期", "hatch"), ("世代", "gen")]
num_inputs = {}
for label, key in num_fields:
    val = st.number_input(f"{label}数值", value=0)
    cmp = st.selectbox(f"{label}比较符", ["🔼", "=", "🔽"])
    num_inputs[key] = (val, cmp)

if st.button("🔍 搜索"):
    results = []
    for p in pokemon_list:
        attrs = p['属性'].split("/") if isinstance(p['属性'], str) else p['属性']
        eggs = p['蛋组'].split("/") if isinstance(p['蛋组'], str) else p['蛋组']
        evo = p.get('进化', '') or "未知"

        # 属性包含、排除
        if attr_incl and not any(a in attrs for a in attr_incl):
            continue
        if attr_excl and any(a in attrs for a in attr_excl):
            continue

        # 蛋组包含、排除、未发现
        if undiscovered_only:
            if "未发现组" not in eggs:
                continue
        else:
            if egg_incl and not any(e in eggs for e in egg_incl):
                continue
            if egg_excl and any(e in eggs for e in egg_excl):
                continue

        # 特性
        if ability_selected and not any(ab in p['特性'] for ab in ability_selected):
            continue

        # 努力值
        if effort_include and not any(eff in p['努力值奖励'] for eff in effort_include):
            continue
        if effort_exclude and any(eff in p['努力值奖励'] for eff in effort_exclude):
            continue

        # 性别
        if gender and p['性别比例'] != gender:
            continue

        # 超进化、极巨化
        if mega and p['超级进化'] != mega:
            continue
        if gmax and p['超极巨化'] != gmax:
            continue

        # 进化阶段
        if evolution and evo != evolution:
            continue

        # 数值比较
        poke_gen_num = gen_map.get(p.get('初登场世代', ""), 0)
        checks = [
            compare(num_inputs['total'][0], num_inputs['total'][1], p['种族值总和']),
            compare(num_inputs['speed'][0], num_inputs['speed'][1], p['速度种族值']),
            compare(num_inputs['height'][0], num_inputs['height'][1], p['身高(m)']),
            compare(num_inputs['weight'][0], num_inputs['weight'][1], p['体重(kg)']),
            compare(num_inputs['hatch'][0], num_inputs['hatch'][1], p['孵化周期']),
            compare(num_inputs['gen'][0], num_inputs['gen'][1], poke_gen_num),
        ]
        if not all(checks):
            continue

        results.append(f"{p['编号']} {p['中文名']}")

    if results:
        st.success("筛选结果：")
        st.write("\n".join(results))
    else:
        st.warning("未找到符合条件的宝可梦。")

if st.button("🔄 重置"):
    st.experimental_rerun()


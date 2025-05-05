import streamlit as st
import json

# 读取数据
with open('pokemon_data.json', 'r', encoding='utf-8') as f:
    pokemon_list = json.load(f)

# 提取唯一值
all_abilities = sorted(set(sum([p['特性'].split("/") if isinstance(p['特性'], str) else p['特性'] for p in pokemon_list], [])))
all_attributes = sorted(set(sum([p['属性'].split("/") if isinstance(p['属性'], str) else p['属性'] for p in pokemon_list], [])))
all_eggs = sorted(set(sum([p['蛋组'].split("/") if isinstance(p['蛋组'], str) else p['蛋组'] for p in pokemon_list], [])))
effort_list = ["HP", "攻击", "防御", "特攻", "特防", "速度"]
gen_map = {"第一世代":1,"第二世代":2,"第三世代":3,"第四世代":4,"第五世代":5,"第六世代":6,"第七世代":7,"第八世代":8,"第九世代":9}

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

st.title("宝可梦筛选器 (一行版)")

with st.form("filter_form"):
    st.subheader("属性包含")
    attr_incl = [attr for attr in all_attributes if st.checkbox(attr, key=f"incl_{attr}")]
    st.subheader("属性排除")
    attr_excl = [attr for attr in all_attributes if st.checkbox(attr, key=f"excl_{attr}")]

    st.subheader("蛋组包含")
    egg_incl = [egg for egg in all_eggs if st.checkbox(egg, key=f"incl_{egg}")]
    st.subheader("蛋组排除")
    egg_excl = [egg for egg in all_eggs if st.checkbox(egg, key=f"excl_{egg}")]
    undiscovered_only = st.checkbox("指定未发现蛋组")

    ability_selected = st.multiselect("特性包含", all_abilities)
    effort_include = st.multiselect("努力值包含", effort_list)
    effort_exclude = st.multiselect("排除努力值", effort_list)

    gender = st.selectbox("性别比例", ["", "7♂:1♀", "1♂:1♀", "1♂:3♀", "1♂:0♀", "0♂:1♀", "无性别"])
    mega = st.selectbox("超级进化", ["", "有超级进化", "无超级进化"])
    gmax = st.selectbox("超极巨化", ["", "有超极巨化", "无超极巨化"])
    evolution = st.selectbox("进化阶段", ["", "无进化树", "一段", "二段", "最终"])

    def num_filter(label):
        col1, col2 = st.columns([1, 2])
        with col1:
            symbol = st.selectbox(f"{label}", ["🔼", "=", "🔽"], key=f"{label}_symbol")
        with col2:
            val = st.number_input(f"{label} 数值", value=0, key=f"{label}_val")
        return val, symbol

    val_total, cmp_total = num_filter("种族值总和")
    val_speed, cmp_speed = num_filter("速度")
    val_height, cmp_height = num_filter("身高(m)")
    val_weight, cmp_weight = num_filter("体重(kg)")
    val_hatch, cmp_hatch = num_filter("孵化周期")
    val_gen, cmp_gen = num_filter("世代")

    submit = st.form_submit_button("🔍 搜索")

if submit:
    results = []
    for p in pokemon_list:
        attrs = p['属性'].split("/") if isinstance(p['属性'], str) else p['属性']
        eggs = p['蛋组'].split("/") if isinstance(p['蛋组'], str) else p['蛋组']
        evo = p.get('进化', '') or "未知"

        if attr_incl and not any(a in attrs for a in attr_incl):
            continue
        if attr_excl and any(a in attrs for a in attr_excl):
            continue

        if undiscovered_only:
            if "未发现组" not in eggs:
                continue
        else:
            if egg_incl and not any(e in eggs for e in egg_incl):
                continue
            if egg_excl and any(e in eggs for e in egg_excl):
                continue

        if ability_selected and not any(ab in p['特性'] for ab in ability_selected):
            continue

        if effort_include and not any(eff in p['努力值奖励'] for eff in effort_include):
            continue
        if effort_exclude and any(eff in p['努力值奖励'] for eff in effort_exclude):
            continue

        if gender and p['性别比例'] != gender:
            continue
        if mega and p['超级进化'] != mega:
            continue
        if gmax and p['超极巨化'] != gmax:
            continue
        if evolution and evo != evolution:
            continue

        poke_gen_num = gen_map.get(p.get('初登场世代', ""), 0)
        checks = [
            compare(val_total, cmp_total, p['种族值总和']),
            compare(val_speed, cmp_speed, p['速度种族值']),
            compare(val_height, cmp_height, p['身高(m)']),
            compare(val_weight, cmp_weight, p['体重(kg)']),
            compare(val_hatch, cmp_hatch, p['孵化周期']),
            compare(val_gen, cmp_gen, poke_gen_num),
        ]
        if not all(checks):
            continue

        results.append(f"{p['编号']} {p['中文名']}")

    if results:
        st.success("筛选结果：")
        st.write("\n".join(results))
    else:
        st.warning("未找到符合条件的宝可梦。")

# 重置按钮修复
if st.button("🔄 重置"):
    try:
        st.session_state.clear()
        st.experimental_rerun()
    except:
        st.warning("当前环境不支持自动重置，请手动刷新页面。")


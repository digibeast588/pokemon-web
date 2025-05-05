import streamlit as st
import json

# 加载数据
with open('pokemon_data.json', 'r', encoding='utf-8') as f:
    pokemon_list = json.load(f)

# 初始化 session_state
if "current_list" not in st.session_state:
    st.session_state.current_list = pokemon_list.copy()

# 定义对比函数
def compare(val, cmp_symbol, poke_val):
    if poke_val is None:
        return True
    if val is None:
        return True
    if cmp_symbol == "🔼":
        return poke_val > val
    elif cmp_symbol == "=":
        return poke_val == val
    elif cmp_symbol == "🔽":
        return poke_val < val
    return True

# 左侧 sidebar
st.sidebar.title("宝可梦筛选器")

# 关键词
keyword = st.sidebar.text_input("名字关键字")

# 属性、蛋组多选
attrs = ["一般", "火", "水", "草", "电", "冰", "格斗", "毒", "地面",
         "飞行", "超能力", "虫", "岩石", "幽灵", "龙", "恶", "钢", "妖精"]
attr_include = st.sidebar.multiselect("包含属性", options=attrs)
attr_exclude = st.sidebar.multiselect("排除属性", options=attrs)

egg_groups = ["陆上", "水中1", "水中2", "水中3", "飞行", "虫", "矿物", 
              "妖精", "植物", "怪兽", "人型", "龙", "不定形", "未发现"]
egg_include = st.sidebar.multiselect("包含蛋组", options=egg_groups)
egg_exclude = st.sidebar.multiselect("排除蛋组", options=egg_groups)
specify_undiscovered = st.sidebar.checkbox("指定未发现蛋组")

# 特性、努力值
ability = st.sidebar.text_input("特性")
effort = st.sidebar.text_input("努力值")
effort_exclude = st.sidebar.text_input("排除努力值")  # ⭐ 新增排除努力值

# 性别、超级进化、超极巨化、进化阶段
gender = st.sidebar.selectbox("性别比例", ["", "7♂:1♀", "1♂:1♀", "1♂:3♀", "1♂:0♀", "0♂:1♀", "无性别"])
mega = st.sidebar.selectbox("超级进化", ["", "有超级进化", "无超级进化"])
gmax = st.sidebar.selectbox("超极巨化", ["", "有超极巨化", "无超极巨化"])
evolution = st.sidebar.selectbox("进化阶段", ["", "无进化树", "一段", "二段", "最终"])

# 数值 + 对比符
total_cmp = st.sidebar.selectbox("种族值总和条件", ["🔼", "=", "🔽"])
total_val = st.sidebar.number_input("种族值总和", min_value=0, max_value=1000, value=0)

speed_cmp = st.sidebar.selectbox("速度条件", ["🔼", "=", "🔽"])
speed_val = st.sidebar.number_input("速度值", min_value=0, max_value=200, value=0)

height_cmp = st.sidebar.selectbox("身高条件(m)", ["🔼", "=", "🔽"])
height_val = st.sidebar.number_input("身高(m)", min_value=0.0, max_value=20.0, value=0.0)

weight_cmp = st.sidebar.selectbox("体重条件(kg)", ["🔼", "=", "🔽"])
weight_val = st.sidebar.number_input("体重(kg)", min_value=0.0, max_value=1000.0, value=0.0)

hatch_cmp = st.sidebar.selectbox("孵化周期条件", ["🔼", "=", "🔽"])
hatch_val = st.sidebar.number_input("孵化周期", min_value=1, max_value=40, value=1)

gen_cmp = st.sidebar.selectbox("初登场世代条件", ["🔼", "=", "🔽"])
gen_val = st.sidebar.number_input("初登场世代", min_value=1, max_value=9, value=1)

# 搜索、重置按钮
if st.sidebar.button("🔍 搜索"):
    result = []
    for p in st.session_state.current_list:
        if keyword and keyword not in p['中文名'] and keyword.lower() not in p['英文名'].lower():
            continue

        attrs_p = p['属性'].split("/") if isinstance(p['属性'], str) else p['属性']
        eggs_p = p['蛋组'].split("/") if isinstance(p['蛋组'], str) else p['蛋组']

        if attr_include and not any(a in attrs_p for a in attr_include):
            continue
        if attr_exclude and any(a in attrs_p for a in attr_exclude):
            continue

        if specify_undiscovered:
            if "未发现组" not in eggs_p:
                continue
        else:
            if egg_include and not any(e in eggs_p for e in egg_include):
                continue
            if egg_exclude and any(e in eggs_p for e in egg_exclude):
                continue

        if ability and ability not in p['特性']:
            continue
        if effort and effort not in p['努力值奖励']:
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

        if not compare(total_val, total_cmp, p['种族值总和']):
            continue
        if not compare(speed_val, speed_cmp, p['速度种族值']):
            continue
        if not compare(height_val, height_cmp, p['身高(m)']):
            continue
        if not compare(weight_val, weight_cmp, p['体重(kg)']):
            continue

        gen_map = {"第一世代": 1, "第二世代": 2, "第三世代": 3, "第四世代": 4,
                   "第五世代": 5, "第六世代": 6, "第七世代": 7, "第八世代": 8, "第九世代": 9}
        gen_txt = p.get('初登场世代', "")
        poke_gen_num = gen_map.get(gen_txt, 0)
        if not compare(gen_val, gen_cmp, poke_gen_num):
            continue

        result.append(p)

    st.session_state.current_list = result.copy()
    st.experimental_rerun()

if st.sidebar.button("🔄 重置"):
    st.session_state.current_list = pokemon_list.copy()
    st.experimental_rerun()

# 主界面显示结果
st.title("宝可梦搜索结果")
st.write(f"共找到 {len(st.session_state.current_list)} 条结果")

for p in st.session_state.current_list:
    with st.expander(f"{p['编号']} {p['中文名']} / {p['英文名']}"):
        st.write(f"属性：{p['属性']}")
        st.write(f"蛋组：{p['蛋组']}")
        st.write(f"特性：{p['特性']}")
        st.write(f"努力值奖励：{p['努力值奖励']}")
        st.write(f"性别比例：{p['性别比例']}")
        st.write(f"超级进化：{p['超级进化']}")
        st.write(f"超极巨化：{p['超极巨化']}")
        st.write(f"进化：{p['进化']}")
        st.write(f"种族值总和：{p['种族值总和']}")
        st.write(f"速度：{p['速度种族值']}")
        st.write(f"身高：{p['身高(m)']} m")
        st.write(f"体重：{p['体重(kg)']} kg")
        st.write(f"孵化周期：{p['孵化周期']}")
        st.write(f"初登场世代：{p['初登场世代']}")
        if '图片路径' in p:
            st.image(p['图片路径'], width=200)

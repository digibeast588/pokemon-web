let pokemonData = [];
let resultList = document.getElementById('resultList');
let pokemonImage = document.getElementById('pokemonImage');

// 加载数据
fetch('https://github.com/digibeast588/pokemon-web/releases/download/pokemonster/pokemon_data.json
')
    .then(response => response.json())
    .then(data => {
        pokemonData = data;
        populateSelects();
    });

function populateSelects() {
    let allTypes = ['一般', '火', '水', '电', '草', '冰', '格斗', '毒', '地面',
        '飞行', '超能', '虫', '岩石', '幽灵', '龙', '恶', '钢', '妖精'];
    let eggGroups = ['怪兽组', '水中1组', '水中2组', '水中3组', '虫组', '飞行组',
        '陆上组', '妖精组', '植物组', '人型组', '矿物组', '不定形组', '未发现组', '百变怪组', '龙组'];
    let genders = ["", "7♂:1♀", "1♂:1♀", "1♂:3♀", "1♂:0♀", "0♂:1♀", "无性别"];

    fillSelect('attr1', allTypes);
    fillSelect('attr2', allTypes);
    fillSelect('egg1', eggGroups);
    fillSelect('egg2', eggGroups);
    fillSelect('genderSelect', genders);
}

function fillSelect(id, items) {
    let select = document.getElementById(id);
    items.forEach(item => {
        let opt = document.createElement('option');
        opt.value = item;
        opt.textContent = item;
        select.appendChild(opt);
    });
}

document.getElementById('searchBtn').addEventListener('click', searchPokemon);
document.getElementById('resetBtn').addEventListener('click', () => location.reload());

function searchPokemon() {
    let results = pokemonData.filter(p => {
        return matchBasic(p) && matchNumeric(p) && matchSpecial(p) && matchForm(p);
    });

    resultList.innerHTML = '';
    results.forEach(p => {
        let li = document.createElement('li');
        li.textContent = `${p.编号} ${p.中文名}`;
        li.addEventListener('click', () => {
            let imgPath = p.图片路径;
            if (imgPath) pokemonImage.src = imgPath;
        });
        resultList.appendChild(li);
    });
}

function getVal(id) { return document.getElementById(id).value; }
function isChecked(id) { return document.getElementById(id).checked; }

function matchBasic(p) {
    let attr1 = getVal('attr1');
    let attr2 = getVal('attr2');
    if (attr1 && !p.属性.includes(attr1)) return false;
    if (attr2 && !p.属性.includes(attr2)) return false;
    if (isChecked('attr1Exclude') && p.属性.includes(attr1)) return false;
    if (isChecked('attr2Exclude') && p.属性.includes(attr2)) return false;

    let ability = getVal('abilityInput');
    if (ability && !p.特性.includes(ability)) return false;
    if (isChecked('abilityExclude') && p.特性.includes(ability)) return false;

    let effort = getVal('effortInput');
    if (effort && !p.努力值奖励.includes(effort)) return false;
    if (isChecked('effortExclude') && p.努力值奖励.includes(effort)) return false;

    let egg1 = getVal('egg1');
    let egg2 = getVal('egg2');
    if (egg1 && !p.蛋组.includes(egg1)) return false;
    if (egg2 && !p.蛋组.includes(egg2)) return false;
    if (isChecked('egg1Exclude') && p.蛋组.includes(egg1)) return false;
    if (isChecked('egg2Exclude') && p.蛋组.includes(egg2)) return false;

    let gender = getVal('genderSelect');
    if (gender && p.性别比例 !== gender) return false;
    if (isChecked('genderExclude') && p.性别比例 === gender) return false;

    return true;
}

function matchNumeric(p) {
    let fields = ['speed', 'total', 'height', 'weight', 'hatch', 'gen'];
    for (let f of fields) {
        let val = Number(getVal(f + 'Input'));
        let cmp = getVal(f + 'Cmp');
        if (!compareNumber(p[fieldMap(f)], val, cmp)) return false;
    }
    return true;
}

const fieldMap = {
    speed: '速度种族值',
    total: '种族值总和',
    height: '身高(m)',
    weight: '体重(kg)',
    hatch: '孵化周期',
    gen: '初登场世代'
};

function compareNumber(pokeVal, val, cmp) {
    if (!val) return true;
    if (cmp === '>') return pokeVal > val;
    if (cmp === '=') return pokeVal === val;
    if (cmp === '<') return pokeVal < val;
    return true;
}

function matchSpecial(p) {
    let special = getVal('specialSelect');
    if (special && p.特殊类别 !== special) return false;

    let mega = getVal('megaSelect');
    if (mega && p.超级进化 !== mega) return false;

    let gmax = getVal('gmaxSelect');
    if (gmax && p.超极巨化 !== gmax) return false;

    let stage = getVal('stageSelect');
    if (stage) {
        if (isChecked('stageExclude')) {
            if (p.进化 === stage) return false;
        } else if (p.进化 !== stage) return false;
    }

    return true;
}

function matchForm(p) {
    let form = getVal('formSelect');
    if (form === 'no_form_diff' && p.编号 >= 10001) return false;
    if (form === 'with_form_diff' && p.编号 >= 10001) return true;
    return true;
}

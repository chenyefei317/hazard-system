import streamlit as st
import os

# ----------------- 1. 页面基本配置与代码/菜单隐藏 -----------------
st.set_page_config(
    page_title="职业危害告知书分发系统",
    page_icon="📋",
    layout="centered"
)

# 隐藏右上角菜单、底部 Streamlit 标识以及顶部装饰线
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;} 
footer {visibility: hidden;}    
header {visibility: hidden;}    
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ----------------- 2. 增加公司 Logo -----------------
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
else:
    st.caption("【系统提示：请在项目根目录放置 logo.png 以显示公司Logo】")

# ----------------- 3. 标题与《职业病防治法》要求说明 -----------------
st.title("📋 岗位职业危害告知书分发系统")

with st.expander("📢 《职业病防治法》及相关法规要求说明", expanded=True):
    st.info("""
    根据国家职业卫生相关法规规范，企业与员工需共同履行以下告知与防护义务：
    * **上岗与定期培训**：用人单位应当对劳动者进行上岗前的职业卫生培训和在岗期间的定期职业卫生培训，普及职业卫生知识[cite: 4]。
    * **场所公告与标识**：产生职业病危害的用人单位，应当在醒目位置设置公告栏，公布有关职业病防治的规章制度、操作规程、职业病危害事故应急救援措施和工作场所职业病危害因素检测结果[cite: 5]。同时在醒目位置设置图形、警示线等警示标识和中文警示说明[cite: 5]。
    * **防护用品配备与使用**：用人单位应当为劳动者提供符合国家职业卫生标准的职业病防护用品，并督促、指导劳动者按照使用规则正确佩戴、使用，不得发放钱物替代发放职业病防护用品[cite: 5]。
    """)

st.markdown("---")

# ----------------- 4. 数据库配置 (PDF格式) -----------------
DEPARTMENT_DATA = {
    "技术部": {
        "file_name": "职业危害告知书 - 技术部.pdf",
        "description": "涉及技术研发、打样测试及设备调试等过程中的危害暴露与防护要求。",
        "key_hazards": "微弱电磁辐射、激光、粉尘、挥发性化学品试剂、机械运转伤害等",
        "target_audience": "技术工程师、研发员、测试员、打样技术员"
    },
    "品管部": {
        "file_name": "职业危害告知书 - 品管部.pdf",
        "description": "涉及来料抽检、理化实验室检测、生产过程巡检等环节的危害管控与健康监护。",
        "key_hazards": "化学检测试剂、噪音（巡检车间）、微量粉尘、实验室挥发性气体等",
        "target_audience": "QA/QC人员、巡检员、实验室化验员"
    },
    "生产部": {
        "file_name": "职业危害告知书 - 生产部.pdf",
        "description": "生产车间一线岗位，严格落实接触粉尘、高温、噪声等职业病危害因素的告知制度。",
        "key_hazards": "生产性粉尘、生产性噪声、高温作业、机械性伤害、有机溶剂等",
        "target_audience": "车间操作工、班组长、物料运转员、机修维护工"
    }
}

ATTACHMENT_DIR = "attachments"

# ----------------- 5. 页面交互渲染 -----------------
departments = list(DEPARTMENT_DATA.keys())
selected_dept = st.selectbox(
    "👉 请在下方选择您所属的部门或工作区域：",
    options=["-- 请选择部门 --"] + departments,
    index=0
)

if selected_dept != "-- 请选择部门 --":
    dept_info = DEPARTMENT_DATA[selected_dept]
    file_path = os.path.join(ATTACHMENT_DIR, dept_info["file_name"])

    st.success(f"已选中：【{selected_dept}】")

    with st.container():
        st.subheader("📌 岗位职业健康须知概要")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**适用群体**：`{dept_info['target_audience']}`")
            st.markdown(f"**文件名称**：`{dept_info['file_name']}`")
        with col2:
            st.markdown(f"**主要涉及危害因素**：\n{dept_info['key_hazards']}")

        st.info(f"**说明**：{dept_info['description']}")

    st.markdown("### 📥 附件下载与签署")

    # 校验文件是否存在并提供下载
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            file_data = f.read()

        st.download_button(
            label="⬇️ 点击按钮下载 pdf告知书附件",
            data=file_data,
            file_name=dept_info["file_name"],
            mime="application/pdf",
            type="primary"
        )
        st.caption("按要求完成签署后交至人事行政部备案。")
    else:
        st.error(
            f"❌ 未在系统目录中检测到文件：`{file_path}`。\n"
            f"请将 `{dept_info['file_name']}` (PDF格式) 放置在 `{ATTACHMENT_DIR}` 文件夹中。"
        )

# ----------------- 6. 底部版权与声明 -----------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 13px;'>
        <strong style='color: #d9534f;'>备注：内部文件，严禁商业用途</strong><br><br>
        EHS发布 by Yefei
    </div>
    """,
    unsafe_allow_html=True
)

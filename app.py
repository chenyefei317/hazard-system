import streamlit as st
import os

# ----------------- 1. 页面基本配置与样式隐藏 -----------------
st.set_page_config(
    page_title="职业危害告知书分发系统",
    page_icon="📋",
    layout="centered"
)

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

# ----------------- 3. 标题与《职业病防治法》法规依据说明 -----------------
st.title("📋 岗位职业危害告知书分发系统")

with st.expander("📢 依据《职业病防治法》及国家规范的法定要求说明", expanded=True):
    st.info("""
    本系统及告知流程严格依据以下国家法律法规和标准建设执行：
    * **《中华人民共和国职业病防治法》及《用人单位职业病危害告知与警示标识管理规范》（安总厅安健〔2014〕111号）**：
      * **第 六 条**：产生职业病危害的用人单位应将工作过程中可能接触的危害因素种类、程度、后果、防护设施、个人防护用品、健康检查和待遇等**如实告知劳动者，不得隐瞒或者欺骗**[cite: 4, 6]。
      * **第 七 条**：劳动合同时应当写明职业病危害相关内容；格式合同文本内容不完善的，**应以合同附件形式签署职业病危害告知书**[cite: 4, 6]。
      * **第 九 条**：用人单位应对劳动者进行**上岗前及定期职业卫生培训**，经考试合格后方可上岗作业[cite: 4, 6]。
      * **第 十 一 条**：应按照规定组织接触职业病危害作业的劳动者进行**上岗前、在岗期间和离岗时的职业健康检查**，并将结果书面告知劳动者[cite: 5]。
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
            f"❌ 未在系统目录中检测到文件：`{file_path}`。\n\n"
            f"**排查建议**：\n"
            f"1. 请确认您的电脑或 GitHub 仓库中有一个名为 `attachments` 的文件夹。\n"
            f"2. 请检查该文件夹内是否有名为 `{dept_info['file_name']}` 的 PDF 文件（注意核对文件名是否完全一致，不能有多余的空格或字符错误）。"
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

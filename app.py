import streamlit as st
import os

# ----------------- 1. 页面基本配置 -----------------
st.set_page_config(
    page_title="职业危害告知书在线签署与分发系统",
    page_icon="📋",
    layout="centered"
)

# ----------------- 2. 数据库配置 -----------------
# 针对上传的 3 个部门告知书文件进行配置
DEPARTMENT_DATA = {
    "技术部": {
        "file_name": "职业危害告知书 - 技术部.doc",
        "description": "涉及技术研发、打样测试及设备调试等过程中的危害暴露与防护要求。",
        "key_hazards": "微弱电磁辐射、激光、粉尘、挥发性化学品试剂、机械运转伤害等",
        "target_audience": "技术工程师、研发员、测试员、打样技术员"
    },
    "品管部": {
        "file_name": "职业危害告知书 - 品管部.doc",
        "description": "涉及来料抽检、理化实验室检测、生产过程巡检等环节的危害管控与健康监护。",
        "key_hazards": "化学检测试剂、噪音（巡检车间）、微量粉尘、实验室挥发性气体等",
        "target_audience": "QA/QC人员、巡检员、实验室化验员"
    },
    "生产部": {
        "file_name": "职业危害告知书 - 生产部.doc",
        "description": "生产车间一线岗位，严格落实接触粉尘、高温、噪声等职业病危害因素的告知制度。",
        "key_hazards": "生产性粉尘、生产性噪声、高温作业、机械性伤害、有机溶剂等",
        "target_audience": "车间操作工、班组长、物料运转员、机修维护工"
    }
}

# 附件存放根目录（默认相对路径）
ATTACHMENT_DIR = "attachments"

# ----------------- 3. 页面渲染 -----------------
st.title("📋 岗位职业危害告知书分发系统")
st.caption("依据《中华人民共和国职业病防治法》及最新职业健康监护技术标准建设")
st.markdown("---")

st.markdown("""
> **入场/上岗人员须知：**
> 1. 根据国家法律法规要求，用人单位必须向劳动者如实告知工作岗位可能产生的职业危害；
> 2. 请在下方选择您**所属的部门/岗位**，认真查阅相关告知内容；
> 3. 点击按钮下载 Word 告知书附件，按要求完成签署后交至安全部/HR备案。
""")

# 下拉选择部门
departments = list(DEPARTMENT_DATA.keys())
selected_dept = st.selectbox(
    "👉 请选择您所属的部门或工作区域：",
    options=["-- 请选择部门 --"] + departments,
    index=0
)

# ----------------- 4. 详情展示与下载逻辑 -----------------
if selected_dept != "-- 请选择部门 --":
    dept_info = DEPARTMENT_DATA[selected_dept]
    file_path = os.path.join(ATTACHMENT_DIR, dept_info["file_name"])

    st.success(f"已选中：【{selected_dept}】")

    # 信息公示面板
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
            label=f"⬇️ 点击下载《{dept_info['file_name']}》",
            data=file_data,
            file_name=dept_info["file_name"],
            mime="application/msword",
            type="primary"
        )
        st.caption("注：下载完成后请使用 WPS 或 Microsoft Word 打开，核对个人信息并手写签名。")
    else:
        st.error(
            f"❌ 未在系统目录中检测到文件：`{file_path}`。\n"
            f"请将 `{dept_info['file_name']}` 放置在项目根目录下的 `{ATTACHMENT_DIR}` 文件夹中。"
        )

# 页面底部说明
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 13px;'>"
    "EHS安全环境健康部 & 人力资源部 联合发布"
    "</div>",
    unsafe_allow_html=True
)

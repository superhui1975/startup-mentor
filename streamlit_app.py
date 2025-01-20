import streamlit as st
import pandas as pd
from docx import Document
from startup_advisor import StartupAdvisor
from growth_strategies import GrowthStrategist
from coaching_system import StartupCoach
from document_processor import DocumentProcessor
import io

class StartupMentorSystem:
    def __init__(self):
        self.advisor = StartupAdvisor()
        self.strategist = GrowthStrategist()
        self.coach = StartupCoach()
        self.doc_processor = DocumentProcessor()
        st.set_page_config(page_title="创业指导系统", layout="wide")

    def start_consultation(self, startup_info):
        needs_analysis = self.advisor.analyze_needs(startup_info)
        coaching_session = self.coach.create_coaching_session("需求探索")
        solution = self.advisor.provide_solution()
        business_model = self.advisor.design_business_model()
        growth_plan = self.strategist.create_growth_plan(business_model)
        
        return {
            "需求分析": needs_analysis,
            "解决方案": solution,
            "商业模式": business_model,
            "增长计划": growth_plan,
            "指导记录": coaching_session
        }

    def run(self):
        st.title("创业指导系统")
        
        # 侧边栏信息
        with st.sidebar:
            st.header("关于系统")
            st.write("""
            本系统使用一堆创业模型进行分析，包括：
            1. 需求分析
            2. 解决方案
            3. 商业模式
            4. 增长策略
            5. 竞争壁垒
            """)
        
        # 主要标签页
        tab1, tab2, tab3 = st.tabs(["项目信息", "分析结果", "历史记录"])
        
        with tab1:
            col1, col2 = st.columns([2,1])
            
            with col1:
                # 手动输入表单
                st.subheader("项目基本信息")
                project_name = st.text_input("项目名称")
                project_stage = st.selectbox("项目阶段", ["概念阶段", "产品研发", "市场验证", "规模化"])
                funding_status = st.selectbox("融资情况", ["未融资", "天使轮", "A轮", "B轮及以上"])
                industry = st.text_input("行业领域")
                target_users = st.text_input("目标客户")
                core_product = st.text_area("核心产品/服务描述")
                current_challenges = st.text_area("当前进展和面临的主要问题")
            
            with col2:
                # 文件上传部分
                st.subheader("项目文件上传")
                uploaded_file = st.file_uploader(
                    "上传项目相关文件（支持 PDF、DOCX、TXT）",
                    type=["pdf", "docx", "txt"],
                    help="上传项目计划书、商业计划书等相关文件，系统将自动分析"
                )
                
                if uploaded_file is not None:
                    st.success(f"文件 {uploaded_file.name} 上传成功！")
                    
                    # 读取文件内容
                    if uploaded_file.type == "application/pdf":
                        st.info("PDF文件已接收，系统将进行分析")
                        # TODO: 添加PDF处理逻辑
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        doc = Document(uploaded_file)
                        text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                        st.info("Word文档已接收，系统将进行分析")
                    else:  # txt文件
                        text_content = uploaded_file.getvalue().decode("utf-8")
                        st.info("文本文件已接收，系统将进行分析")
            
            # 分析按钮
            if st.button("开始分析", type="primary"):
                with st.spinner("正在分析中..."):
                    # 收集所有输入信息
                    project_info = {
                        "项目名称": project_name,
                        "项目阶段": project_stage,
                        "融资情况": funding_status,
                        "行业领域": industry,
                        "目标客户": target_users,
                        "核心产品描述": core_product,
                        "当前挑战": current_challenges
                    }
                    
                    # 如果有上传文件，添加文件内容到分析
                    if uploaded_file is not None:
                        project_info["上传文件"] = uploaded_file.name
                        # TODO: 添加文件内容处理逻辑
                    
                    # 切换到分析结果标签
                    tab2.write("## 分析结果")
                    # TODO: 添加分析逻辑
                    
        with tab2:
            st.info('请在"项目信息"标签页填写信息并点击"开始分析"')
            
        with tab3:
            st.info("历史记录功能开发中...")

if __name__ == "__main__":
    system = StartupMentorSystem()
    system.run() 

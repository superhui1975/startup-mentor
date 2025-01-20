import streamlit as st
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

def main():
    st.set_page_config(page_title="创业指导系统", layout="wide")
    
    st.title("创业指导系统")
    st.write("基于一堂创业模型的智能分析系统")
    
    # 侧边栏
    with st.sidebar:
        st.header("关于系统")
        st.write("""
        本系统使用一堂创业模型进行分析，包括：
        1. 需求分析
        2. 解决方案
        3. 商业模式
        4. 增长策略
        5. 竞争壁垒
        """)
    
    # 主界面
    tabs = st.tabs(["项目信息", "分析结果", "历史记录"])
    
    # 项目信息标签页
    with tabs[0]:
        with st.form("project_info"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("项目名称")
                industry = st.text_input("行业领域")
                target_customers = st.text_input("目标客户")
            
            with col2:
                business_stage = st.selectbox(
                    "项目阶段",
                    ["概念阶段", "产品研发", "市场验证", "规模化", "成熟运营"]
                )
                funding_status = st.selectbox(
                    "融资情况",
                    ["未融资", "天使轮", "Pre-A轮", "A轮", "B轮及以上"]
                )
            
            core_product = st.text_area("核心产品/服务描述")
            current_status = st.text_area("当前进展和面临的主要问题")
            
            submitted = st.form_submit_button("开始分析")
    
    # 分析结果标签页
    with tabs[1]:
        if submitted:
            with st.spinner("正在分析中..."):
                mentor_system = StartupMentorSystem()
                
                analysis = mentor_system.start_consultation({
                    "项目名称": project_name,
                    "行业领域": industry,
                    "目标客户": target_customers,
                    "项目阶段": business_stage,
                    "融资情况": funding_status,
                    "核心产品": core_product,
                    "当前进展": current_status
                })
                
                # 显示分析结果
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("需求分析")
                    st.write(analysis["需求分析"])
                    
                    st.subheader("解决方案")
                    st.write(analysis["解决方案"])
                
                with col2:
                    st.subheader("商业模式")
                    st.write(analysis["商业模式"])
                    
                    st.subheader("增长策略")
                    st.write(analysis["增长计划"])
                
                # 生成报告下载按钮
                st.download_button(
                    "下载完整分析报告",
                    data=io.BytesIO(b"Report content").getvalue(),
                    file_name=f"{project_name}-创业分析报告.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
    
    # 历史记录标签页
    with tabs[2]:
        st.info("即将推出历史记录功能...")

if __name__ == "__main__":
    main() 
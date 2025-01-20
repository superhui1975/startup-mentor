import streamlit as st
import pandas as pd
from docx import Document
import io
from PyPDF2 import PdfReader
import requests
from typing import Dict, Any

class StartupMentorSystem:
    def __init__(self):
        st.set_page_config(page_title="创业指导系统", layout="wide")
        # 设置 302AI API key
        if 'AI302_API_KEY' not in st.secrets:
            st.sidebar.warning('请设置 302AI API Key')
        else:
            self.api_key = st.secrets['AI302_API_KEY']
            self.api_url = "https://api.302.ai/v1/chat/completions"  # 302AI的API地址
    
    def analyze_with_claude(self, project_info: Dict[str, Any]) -> Dict[str, str]:
        """使用 Claude 分析项目信息"""
        # 构建 prompt
        prompt = f"""作为一个创业顾问，请分析以下创业项目：
        
项目名称：{project_info.get('项目名称', 'N/A')}
项目阶段：{project_info.get('项目阶段', 'N/A')}
融资情况：{project_info.get('融资情况', 'N/A')}
行业领域：{project_info.get('行业领域', 'N/A')}
目标客户：{project_info.get('目标客户', 'N/A')}
核心产品：{project_info.get('核心产品描述', 'N/A')}
当前挑战：{project_info.get('当前挑战', 'N/A')}

请从以下几个方面进行分析：
1. 需求分析：评估市场需求的真实性和规模
2. 解决方案：分析产品/服务的创新性和可行性
3. 商业模式：评估商业模式的合理性和盈利能力
4. 增长策略：建议合适的市场策略和增长路径
5. 竞争分析：分析竞争优势和潜在风险

对于每个方面，请给出具体的建议和可执行的行动方案。"""

        if "上传文件" in project_info and "文件内容" in project_info:
            prompt += f"\n\n此外，请结合以下项目文件内容进行分析：\n{project_info['文件内容'][:2000]}"

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "claude-3-opus-20240229",  # 使用最新的 Claude 3 模型
                "messages": [
                    {"role": "system", "content": "你是一位经验丰富的创业顾问，擅长分析创业项目并提供专业建议。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()  # 检查请求是否成功
            
            # 解析返回结果
            result = response.json()
            analysis = result['choices'][0]['message']['content']
            
            # 将分析结果分段
            sections = analysis.split('\n\n')
            result = {}
            current_section = ""
            
            for section in sections:
                if "需求分析" in section:
                    result["需求分析"] = section
                elif "解决方案" in section:
                    result["解决方案"] = section
                elif "商业模式" in section:
                    result["商业模式"] = section
                elif "增长策略" in section:
                    result["增长策略"] = section
                elif "竞争分析" in section:
                    result["竞争分析"] = section
            
            return result
            
        except Exception as e:
            st.error(f"分析过程中出现错误：{str(e)}")
            return {}

    def extract_text_from_pdf(self, pdf_file) -> str:
        """从PDF文件中提取文本"""
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text

    def run(self):
        st.title("创业指导系统")
        
        # 侧边栏信息
        with st.sidebar:
            st.header("关于系统")
            st.write("""
            本系统使用 Claude 模型进行创业项目分析，包括：
            1. 需求分析
            2. 解决方案
            3. 商业模式
            4. 增长策略
            5. 竞争分析
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
                    try:
                        if uploaded_file.type == "application/pdf":
                            text_content = self.extract_text_from_pdf(uploaded_file)
                            st.info("PDF文件已接收，系统将进行分析")
                        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            doc = Document(uploaded_file)
                            text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                            st.info("Word文档已接收，系统将进行分析")
                        else:  # txt文件
                            text_content = uploaded_file.getvalue().decode("utf-8")
                            st.info("文本文件已接收，系统将进行分析")
                    except Exception as e:
                        st.error(f"文件处理出错：{str(e)}")
                        text_content = ""
            
            # 分析按钮
            if st.button("开始分析", type="primary"):
                if not project_name:
                    st.error("请至少输入项目名称")
                    return
                    
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
                    if uploaded_file is not None and 'text_content' in locals():
                        project_info["上传文件"] = uploaded_file.name
                        project_info["文件内容"] = text_content
                    
                    # 使用 Claude 进行分析
                    analysis_result = self.analyze_with_claude(project_info)
                    
                    if analysis_result:
                        # 在分析结果标签页显示结果
                        tab2.write("## 分析结果")
                        
                        # 创建两列布局显示结果
                        col1, col2 = tab2.columns(2)
                        
                        with col1:
                            st.subheader("需求分析")
                            st.write(analysis_result.get("需求分析", ""))
                            
                            st.subheader("解决方案")
                            st.write(analysis_result.get("解决方案", ""))
                            
                            st.subheader("商业模式")
                            st.write(analysis_result.get("商业模式", ""))
                            
                        with col2:
                            st.subheader("增长策略")
                            st.write(analysis_result.get("增长策略", ""))
                            
                            st.subheader("竞争分析")
                            st.write(analysis_result.get("竞争分析", ""))
                        
                        # 生成并提供下载报告
                        report_content = "\n\n".join([
                            f"# {project_name} - 创业项目分析报告\n",
                            "## 需求分析",
                            analysis_result.get("需求分析", ""),
                            "## 解决方案",
                            analysis_result.get("解决方案", ""),
                            "## 商业模式",
                            analysis_result.get("商业模式", ""),
                            "## 增长策略",
                            analysis_result.get("增长策略", ""),
                            "## 竞争分析",
                            analysis_result.get("竞争分析", "")
                        ])
                        
                        tab2.download_button(
                            "下载完整分析报告",
                            report_content,
                            file_name=f"{project_name}-创业分析报告.md",
                            mime="text/markdown"
                        )
                    
        with tab2:
            st.info('请在"项目信息"标签页填写信息并点击"开始分析"')
            
        with tab3:
            st.info("历史记录功能开发中...")

if __name__ == "__main__":
    system = StartupMentorSystem()
    system.run() 

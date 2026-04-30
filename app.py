import streamlit as st
import os
from dotenv import load_dotenv
from langchain.tools import tool
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

load_dotenv()

st.set_page_config(page_title="DeepCode Audit | 企业级代码审计中枢", layout="wide")

st.title("🛡️ DeepCode Audit")
st.subheader("自动化代码审计与反思修复引擎")
st.markdown("---")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 引擎配置")
    api_key = st.text_input("API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    api_base = st.text_input("Base URL", value=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"))
    model = st.selectbox("核心推理模型", ["kimi-2.5", "gpt-4o", "gpt-4-turbo", "claude-3-5-sonnet", "deepseek-chat"])
    if st.button("保存并初始化"):
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = api_base
        st.success("引擎初始化成功")

# 模拟工具
@tool("SecurityVulnerabilityDatabase")
def security_tool(query: str) -> str:
    """查询已知的代码安全漏洞模式。"""
    return "警告：发现潜在的 SQL 拼接风险，可能导致 SQL 注入攻击。建议使用预编译语句。"

# UI 主体
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📥 待审计代码 (Input)")
    code_input = st.text_area("请粘贴 PR 变更内容或代码片段：", height=400, value="""def get_user_data(user_id):
    # 这里的查询逻辑存在风险
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    result = db.execute(query)
    return result""")

with col2:
    st.markdown("### 📑 审计报告 (Output)")
    if st.button("🚀 执行多 Agent 深度审计"):
        if not api_key:
            st.error("请先在左侧配置 API Key")
        else:
            llm = ChatOpenAI(model=model, temperature=0.1)
            
            # Agents 定义
            architect = Agent(role='首席架构师', goal='分析代码全局意图和架构合理性', backstory='拥有15年架构经验，关注系统健壮性。', llm=llm)
            reviewer = Agent(role='资深代码审计员', goal='发现逻辑缺陷和代码规范问题', backstory='对代码质量有近乎洁癖的要求。', llm=llm)
            security = Agent(role='安全专家', goal='挖掘潜在的安全漏洞', backstory='擅长渗透测试和代码审计。', tools=[security_tool], llm=llm)
            developer = Agent(role='高级开发工程师', goal='根据审计反馈进行代码修复与重构', backstory='擅长编写高性能、安全的代码。', llm=llm)

            # Tasks
            t1 = Task(description=f"分析代码业务意图:\n{code_input}", agent=architect, expected_output="业务逻辑简报")
            t2 = Task(description="进行代码质量和规范审计", agent=reviewer, expected_output="质量审计列表")
            t3 = Task(description="进行安全性渗透审计，查找漏洞", agent=security, expected_output="安全漏洞报告")
            t4 = Task(description="汇总所有专家意见，输出最终的修复后代码，并说明修改原因。", agent=developer, context=[t1, t2, t3], expected_output="修复后的代码及说明")

            with st.status("多 Agent 深度推理中...", expanded=True) as status:
                st.write("🕵️ 架构师正在分析上下文...")
                crew = Crew(agents=[architect, reviewer, security, developer], tasks=[t1, t2, t3, t4], process=Process.sequential)
                final_report = crew.kickoff()
                status.update(label="审计完成!", state="complete")
            
            st.info(final_report)

st.markdown("---")
st.caption("Powered by Multi-Agent Reflection Architecture")

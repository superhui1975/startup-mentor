class StartupCoach:
    def __init__(self):
        self.question_bank = {
            "需求探索": [
                "您的创业愿景是什么？",
                "目标客户群体的痛点是什么？",
                "您认为产品的核心竞争力在哪里？"
            ],
            "方案验证": [
                "这个解决方案是否足够差异化？",
                "实施过程中可能遇到哪些挑战？",
                "如何确保方案的可执行性？"
            ]
        }
        self.coaching_sessions = []
        
    def ask_probing_questions(self, area):
        """提出启发式问题"""
        return self.question_bank.get(area, [])
        
    def analyze_documents(self, documents):
        """分析上传的创业相关文档"""
        # 文档分析逻辑
        pass 
        
    def create_coaching_session(self, focus_area):
        """创建指导会话"""
        session = {
            "主题": focus_area,
            "问题列表": self.generate_question_sequence(focus_area),
            "关键洞察": [],
            "行动建议": []
        }
        self.coaching_sessions.append(session)
        return session
        
    def generate_question_sequence(self, focus_area):
        """生成问题序列"""
        base_questions = self.question_bank.get(focus_area, [])
        return self._customize_questions(base_questions)
        
    def record_insights(self, session_id, insight):
        """记录关键洞察"""
        if session_id < len(self.coaching_sessions):
            self.coaching_sessions[session_id]["关键洞察"].append(insight)
            
    def generate_action_items(self, session_id):
        """生成行动建议"""
        if session_id < len(self.coaching_sessions):
            session = self.coaching_sessions[session_id]
            return self._create_action_plan(session["关键洞察"]) 
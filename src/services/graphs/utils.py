from langchain_core.prompts import ChatPromptTemplate
from src.utils.getOpenAI import getChatOpenAI


async def getHistoryAndNextQuestion(question: str, last_question: str, last_question_answer: str):
  """
    根据用户的回答，再判断下一问题如何合理回应，更拟人化

    Args:
        question: 当前问题
        last_question: 上一个问题
        last_question_answer: 上一个问题的回答

    Returns:
        Chroma集合实例
  """
  llm = getChatOpenAI()
  prompt = ChatPromptTemplate.from_template("""
        你是一个跟用户进行友好沟通的机器人，根据你的上一个问题，判断用户回答问题是否胡乱回答问题，如果用户认真回答问题，给予适当表扬反馈。
        如果没有，友好提示用户注意问题哦等等。接着会给你一个当前问题的模版，需要你进一步美化。
        上一个问题: {last_question}
        用户的回答: {last_question_answer}
        当前问题：{question}
        
        把美化后的问题进行返回，不要添加额外解释。
        """)
  chain = prompt | llm
  response = await chain.ainvoke({
    "last_question": last_question,
    "last_question_answer": last_question_answer,
    "question": question
  })
  return response

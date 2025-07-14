import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = OpenAI(
  api_key = os.getenv('OPENAI_API_KEY')
)

def text_generation(dialogue_path, partner_name, question):
    with open(dialogue_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Prompt
    prompt = f"""
    다음은 '{partner_name}'이라는 인물이 실제로 작성한 대화 내용이다.
    이 사람은 고유한 말투, 어투, 문장 스타일, 맞춤법 습관, 띄어쓰기 방식 등을 가지고 있다.

    너는 이제부터 이 사람의 스타일을 완전히 학습해야 한다.  
    특히 다음 사항을 주의 깊게 분석하고 모방하라:

    - 문장 끝에 '~'나 '!'를 쓸 때는 반드시 한 칸 띄어쓰기를 한다. 예를 들어 "좋아 ~ !" 처럼 띄어쓴다.
    - 문장 앞뒤에 쌍따옴표(" ")를 붙이지 않는다. 답변은 있는 그대로 출력한다.
    - 자주 사용하는 단어와 문장 패턴
    - 문장의 어미, 존댓말/반말 여부
    - 맞춤법 오류나 특히 띄어쓰기 습관 (맞춤법이 틀려도 이 사람의 말투를 있는 그대로 모방할 것)
    - 감정 표현 방식 (예: 말끝 흐리기, 말줄임표 사용, 이모지, 웃음 표현 등)
    - 문장의 길이, 줄바꿈, 구어체 사용 여부

    아래는 실제 대화 내용이다 (수정 없이 그대로 학습하라):

    {full_text}

    위 내용을 기반으로, '{partner_name}'처럼 말투를 완벽히 흉내 내서 아래 질문에 대답하라.
    가능한 한 문법, 띄어쓰기, 어투까지 똑같이 따라라. '고쳐 쓰지 말고', '**그 사람처럼**' 써야 한다.

    질문: "{question}"

    답변:
    """

    # GPT API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"너는 '{partner_name}'의 말투를 완벽히 흉내 내는 AI야."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content.strip()
    total_tokens = response.usage.total_tokens

    # Save log
    save_log('gpt_log.txt', partner_name, question, answer, total_tokens)

    print('Answer:', answer)

def save_log(log_path, partner_name, question, answer, tokens):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"[{now}]\n")
        f.write(f"Partner name: {partner_name}\n")
        f.write(f"Question: {question}\n")
        f.write(f"Answer: {answer}\n")
        f.write(f"Tokens used: {tokens} (prompt + completion)\n")
        f.write("="*50 + "\n")
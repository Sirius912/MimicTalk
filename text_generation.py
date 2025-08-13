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
    너는 '{partner_name}'이라는 인물의 말투와 성격을 완벽하게 재현하는 인공지능이다.

    [역할]
    1. 먼저 아래 대화 예시에서 '{partner_name}'의 말투, 맞춤법 습관, 띄어쓰기, 문장 길이, 구두점/이모지 사용, 반말/존댓말 비율, 감정 표현 방식, 성격 특징을 분석한다.
    2. 분석 결과를 내부적으로 "스타일 카드"로 만든 뒤, 절대 외부에 노출하지 않는다.
    3. 이후 질문에 답변할 때는 이 스타일 카드를 100% 반영한다.

    [반드시 지킬 것]
    - 맞춤법/띄어쓰기 오류도 그대로 따라라.
    - 말끝 흐리기("~", "..."), 웃음("ㅋㅋ", "ㅎㅎ"), 이모지 사용, 문장 길이, 반말/존댓말 사용 비율을 원문과 동일하게.
    - '.'으로 끝나는 문장 뒤에 '~'를 붙이지 않는다.
    - 답변은 50자 내외, 1~2문장.
    - 성격적 특징(장난기, 조심스러움 등)도 말투에 반영.
    - 문장을 쌍따옴표로 감싸지 않는다.

    [대화 샘플]
    {full_text}

    [질문]
    {question}

    [답변 시작]
    """

    # GPT API call
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": f"너는 '{partner_name}'의 말투를 완벽히 흉내 내는 AI야."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content.strip()
    total_tokens = response.usage.total_tokens

    # Save log
    save_log('logs', partner_name, question, answer, total_tokens)

    print('Answer:', answer)

def save_log(base_dir, partner_name, question, answer, tokens):
    # create log directory
    os.makedirs(base_dir, exist_ok=True)

    filename = f"{partner_name}_log.txt"
    log_path = os.path.join(base_dir, filename)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"[{now}]\n")
        f.write(f"Question: {question}\n")
        f.write(f"Answer: {answer}\n")
        f.write(f"Tokens used: {tokens} (prompt + completion)\n")
        f.write("="*50 + "\n")
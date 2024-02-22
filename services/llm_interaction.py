# Currently, using Hugging face API, will resort to our self hosted shit later
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

question = "Who won the FIFA World Cup in the year 1994? "

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

HUGGINGFACEHUB_API_TOKEN = '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'
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(
    repo_id=repo_id, max_length=128, temperature=0.5, token=HUGGINGFACEHUB_API_TOKEN
)
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.run(question))
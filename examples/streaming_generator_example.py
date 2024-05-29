import os
from salesgpt.agents import SalesGPT
from langchain.chat_models import ChatOpenAI

def load_environment_variables():
    """
    Load environment variables from the .env file and set the OPENAI_API_KEY in the os environment.
    """
    with open('.env', 'r') as f:
        env_file = f.readlines()
    envs_dict = {key.strip("'"): value.strip("\n") for key, value in [(i.split('=')) for i in env_file]}
    os.environ['OPENAI_API_KEY'] = envs_dict['OPENAI_API_KEY']

def create_sales_agent():
    """
    Create a SalesGPT agent with specified parameters.
    
    Returns:
        SalesGPT: The created SalesGPT agent.
    """
    llm = ChatOpenAI(temperature=0.9)
    
    sales_agent = SalesGPT.from_llm(llm, verbose=False,
                                    salesperson_name="Ted Lasso",
                                    salesperson_role="Sales Representative",
                                    company_name="Sleep Haven",
                                    company_business='''Sleep Haven 
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible. 
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories 
                                    that are designed to meet the unique 
                                    needs of our customers.''')
    
    sales_agent.seed_agent()
    
    return sales_agent

def operate_on_generator(sales_agent, model_name="gpt-3.5-turbo-0613"):
    """
    Operate on the streaming LLM output in near-real time.
    
    Args:
        sales_agent (SalesGPT): The SalesGPT agent to use for generating text.
        model_name (str): The name of the model to use for generation.
    """
    generator = sales_agent.step(return_streaming_generator=True, model_name=model_name)
    
    # Operate on streaming LLM output
    for chunk in generator:
        print(chunk)

if __name__ == "__main__":
    load_environment_variables()
    sales_agent = create_sales_agent()
    operate_on_generator(sales_agent)
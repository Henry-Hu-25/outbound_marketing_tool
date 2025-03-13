from langsmith import Client
from langsmith.evaluation import LangChainStringEvaluator, evaluate
from langsmith.schemas import DataType

def setup_evaluation_dataset(email_content):
    """Set up evaluation dataset for email content"""
    client = Client()
    dataset_name = "outbound_cold_emails"
    
    if not client.has_dataset(dataset_name = dataset_name):
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            data_type=DataType.kv,
            description="This dataset contains outbound email drafts"
        )
    
    client.create_example(
        dataset_name=dataset_name,
        inputs={"inputs": email_content}
    )
    
    return dataset_name

def evaluate_email(dataset_name):
    """Evaluate email content"""
    evaluator_conciseness = LangChainStringEvaluator(
        "criteria",
        config={
            "criteria": "conciseness"
        }
    )
    
    evaluator_clarity = LangChainStringEvaluator(
        "criteria",
        config={
            "criteria": {
                "clarity": "Does the email clearly communicate the value proposition?"
            }
        }
    )
    
    evaluator_personalization = LangChainStringEvaluator(
        "criteria",
        config={
            "criteria": {
                "personalization": "Is the email properly personalized to the client?"
            }
        }
    )
    
    evaluator_call_to_action = LangChainStringEvaluator(
        "criteria",
        config={
            "criteria": {
                "call_to_action": "Is there a clear and compelling call to action?"
            }
        }
    )
    
    results = evaluate(
        lambda input: input["inputs"],
        data=dataset_name,
        evaluators=[
            evaluator_conciseness, 
            evaluator_clarity, 
            evaluator_personalization, 
            evaluator_call_to_action
        ],
        experiment_prefix="gpt4",
        metadata={"Trial": "1"}
    )
    
    return results 
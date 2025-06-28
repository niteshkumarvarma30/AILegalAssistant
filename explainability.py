def explain_answer(answer, docs):
    # Dummy implementation: highlight first doc as most influential
    return {"influential_docs": [docs[0]] if docs else [], "explanation": "First doc influenced the answer."}

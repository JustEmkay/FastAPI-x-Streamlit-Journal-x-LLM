import ollama


async def summarize_journal(prompt: str) -> str:
    client = ollama.AsyncClient()
    response = await client.chat(model='gemma2:2b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

async def summer(journal_data) -> str:
    """
    Input: dict = {
        ... : ...,
        ... : ..., ...
    }
    Return: summarization of journal as string.
    """
    
    prompt = f"""
Please summarize the following journal entry in a reflective and concise manner:

Completed tasks:
- {'; '.join(journal_data['completed'])}

Tasks not completed:
- {'; '.join(journal_data['not_completed'])}

Mood: {journal_data['mood']}
Productivity: {journal_data['productivity']}
Stress level: {journal_data['stress_level']}
Social interaction: {journal_data['social_interaction']}
Energy level: {journal_data['energy_level']}

Lessons learned:
- {journal_data['lessons']}

Things I am thankful for:
- {'; '.join(journal_data['thankful'])}

Things that sucked:
- {journal_data['sucks']}
"""

    summary = await summarize_journal(prompt) 
    return summary


if __name__ == "__main__":
    
    
    journal_data = {
    'completed': ['do two leet code questions', 'Go for cloth store'],
    'not_completed': ['read 20 pages'],
    'mood': 4,
    'productivity': 4,
    'stress_level': 1,
    'social_interaction': 5,
    'energy_level': 3,
    'lessons': 'try every combination of shirt before buying',
    'thankful': ['I have caring parenting', 'warming home'],
    'sucks': 'waking up at 5 am'
    }
    
    
    
    
    summer(journal_data)
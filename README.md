# Streamlit Journal + FastAPI (AI powered journal summarization) 

## Purpose
* Write Daily simple journal . 
* Track Journal.
* Get AI generated Summery of journal.
* Import & Export. 

## Installation 
* Create a environment 
```
python -m venv <env name>
```
* Activate environment and run below code
```
(<env name>)$ pip install -r requirements.txt
```
 ! Please Note:
  * to get AI journal summerization you should install [ollama](https://ollama.com/) | [Ollama Doc](https://github.com/ollama/ollama) .
  * After install required model . (Im using gemma2 2billion model, need on less resources to run locally comparing to other models.)
  	* warning : to run smaller ollama models (ai model) you need minimum 8GB RAM .  	
    ```
    # install gemma 2 model and run locally
    ollama run gemma2:2b
    ```
  * You can change model by editing "model" in [summer.py](summer.py) file
    ```
    async def summarize_journal(prompt: str) -> str:
    client = ollama.AsyncClient()
    response = await client.chat(model='gemma2:2b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']
    ```


## How to run

#### To run streamlit app
```
streamlit run web.py 
```
#### To run FastAPI
```
uvicorn test:app
```

## Why I did this project ?
* learn about Fastapi.
* Hand on work with Large Language model.
* to learn Hosting on raspberry pi.


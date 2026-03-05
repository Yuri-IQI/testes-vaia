from code_assistant import CodeAssistant

assistant = CodeAssistant()

def execute_code(query, retries=3):
    current_retries = 0
    
    try:
        context = "You are an assistant that generates matplotlib charts"
        code = assistant.generate_code(context, query)
        
        if current_retries == retries:
            print("Maximum retries reached. Unable to execute the code.")
            return
        
        exec(assistant.parse_code("python", code))
        
    except Exception as e:
        query_with_exception = query + f"\n\n# Exception: {str(e)}"
        execute_code(query_with_exception, current_retries + 1)
        
execute_code(
    "create a simple matplotlib plot with x values from 0 to 10 and y values as the square of x",
    1
)
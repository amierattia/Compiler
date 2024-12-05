from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Lexical Analysis
def lexical_analysis(code):
    # Regex pattern to capture keywords, identifiers, operators, literals, and punctuation.
    pattern = r"(?P<Keyword>\bint\b|\bstring\b|\bbool\b|\bif\b|\belse\b|\bfor\b|\bwhile\b|\bfloat\b|\bdouble\b|\bchar\b)|(?P<Identifier>[a-zA-Z_]\w*)|(?P<Number>\b\d+\b)|(?P<FloatNumber>\b\d+\.\d+\b)|(?P<StringLiteral>\"[^\"]*\")|(?P<Operator>[=+\-*/;(){}])|(?P<Punctuation>[,.;])"
    regex = re.compile(pattern)
    matches = regex.finditer(code)

    tokens = []
    for match in matches:
        for group_name in regex.groupindex.keys():
            if match.group(group_name):
                tokens.append(f"{group_name}: {match.group(group_name)}")
    return tokens

# Syntax Analysis
def syntax_analysis(tokens):
    # Check for a valid variable declaration with assignment: e.g., int x = 10;
    if len(tokens) == 5:
        if tokens[0].startswith("Keyword") and tokens[1].startswith("Identifier") and tokens[2].startswith("Operator") and (tokens[3].startswith("Number") or tokens[3].startswith("StringLiteral") or tokens[3].startswith("FloatNumber")) and tokens[4].startswith("Operator"):
            return True, "Syntax is correct!"
    
    # Check if the structure is for an invalid syntax
    return False, "Syntax error: Invalid syntax structure."

# Semantic Analysis
def semantic_analysis(variable_type, value):
    if variable_type == "int":
        try:
            int(value)  # Check if value is a valid integer
            return True, ""
        except ValueError:
            return False, "Semantic error: Value is not an integer."
    elif variable_type == "string":
        if value.startswith('"') and value.endswith('"'):
            return True, ""
        return False, "Semantic error: Value must be a valid string surrounded by double quotes."
    elif variable_type == "bool":
        if value.lower() in ['true', 'false']:
            return True, ""
        return False, "Semantic error: Value must be 'true' or 'false'."
    elif variable_type == "float":
        try:
            float(value)  # Check if value is a valid float
            return True, ""
        except ValueError:
            return False, "Semantic error: Value is not a valid float."
    elif variable_type == "char":
        if len(value) == 1:
            return True, ""
        return False, "Semantic error: Char must be a single character."
    return False, "Unsupported variable type."

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        code = request.form["code"]
        tokens = lexical_analysis(code)
        is_syntax_correct, syntax_error = syntax_analysis(tokens)

        if is_syntax_correct:
            # Determine the variable type based on the first token (Keyword)
            variable_type = tokens[0].split(":")[1].strip()
            value = tokens[3].split(":")[1].strip()  # Extracting value from the token
            is_semantic_correct, semantic_error = semantic_analysis(variable_type, value)
        else:
            is_semantic_correct = False
            semantic_error = syntax_error

        result = {
            "tokens": tokens,
            "is_syntax_correct": is_syntax_correct,
            "is_semantic_correct": is_semantic_correct,
            "semantic_error": semantic_error,
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

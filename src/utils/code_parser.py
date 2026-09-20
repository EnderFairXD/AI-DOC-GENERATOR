import ast

def analyze_python_code(code_string: str) -> dict:
    """
    Parsea código Python usando AST y extrae de forma estructurada
    las clases, métodos, funciones y docstrings.
    """
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return {"error": f"Error de sintaxis en el código: {str(e)}"}

    structure = {
        "funciones": [],
        "clases": []
    }

    for node in ast.walk(tree):
        # Detectar funciones globales
        if isinstance(node, ast.FunctionDef) and not isinstance(getattr(node, 'parent', None), ast.ClassDef):
            args = [arg.arg for arg in node.args.args]
            structure["funciones"].append({
                "nombre": node.name,
                "argumentos": args,
                "docstring": ast.get_docstring(node) or "Sin documentación interna."
            })
        
        # Detectar clases
        elif isinstance(node, ast.ClassDef):
            metodos = []
            for sub_node in node.body:
                if isinstance(sub_node, ast.FunctionDef):
                    m_args = [arg.arg for arg in sub_node.args.args]
                    metodos.append({
                        "nombre": sub_node.name,
                        "argumentos": m_args,
                        "docstring": ast.get_docstring(sub_node) or "Sin documentación interna."
                    })
            
            structure["clases"].append({
                "nombre": node.name,
                "metodos": metodos,
                "docstring": ast.get_docstring(node) or "Sin documentación interna."
            })

    return structure
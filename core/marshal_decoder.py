import ast
import marshal
import dis
import io
import types

def find_marshal_payloads(source_code: str):
    payloads = []
    try:
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr == 'loads' and node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, (bytes, bytearray)):
                        if len(arg.value) > 50:
                            payloads.append(bytes(arg.value))
                elif isinstance(func, ast.Name) and func.id == 'loads' and node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, (bytes, bytearray)):
                        if len(arg.value) > 50:
                            payloads.append(bytes(arg.value))
    except:
        pass
    return payloads

def try_unwrap(data, max_depth=12):
    if not isinstance(data, (bytes, bytearray)):
        return None
    current = bytes(data)
    for _ in range(max_depth):
        try:
            obj = marshal.loads(current)
            if isinstance(obj, types.CodeType):
                return obj
            if isinstance(obj, (bytes, bytearray)):
                current = bytes(obj)
                continue
        except:
            pass
        try:
            import zlib, base64, bz2, lzma
            for mod in [zlib, bz2, lzma]:
                try:
                    d = mod.decompress(current)
                    if isinstance(d, (bytes, bytearray)) and d != current:
                        current = bytes(d)
                        break
                except:
                    continue
            d = base64.b64decode(current, validate=False)
            if isinstance(d, (bytes, bytearray)) and len(d) > 0:
                current = bytes(d)
        except:
            pass
        break
    try:
        obj = marshal.loads(current)
        if isinstance(obj, types.CodeType):
            return obj
    except:
        pass
    return None

def extract_code_info(code_obj, depth=0, max_depth=6):
    if depth > max_depth or not isinstance(code_obj, types.CodeType):
        return None
    output = io.StringIO()
    dis.dis(code_obj, file=output)
    strings, nested = [], []
    for const in code_obj.co_consts:
        if isinstance(const, str) and const.strip():
            strings.append(const[:300] if len(const) > 300 else const)
        elif isinstance(const, types.CodeType):
            n = extract_code_info(const, depth + 1, max_depth)
            if n: nested.append(n)
    return {
        "name": code_obj.co_name,
        "disassembly": output.getvalue(),
        "strings": strings,
        "nested_functions": nested
    }

def generate_decoded_output(info):
    if not info:
        return "# ERROR"
    lines = ["=" * 70, "MARSHAL DEOBFUSCATOR v2.5", "=" * 70]
    lines.append(f"[+] Module: {info['name']}")
    if info.get('strings'):
        lines.append("\n--- EXTRACTED STRINGS ---")
        for i, s in enumerate(info['strings'][:20]):
            lines.append(f"[{i:02d}] {s}")
    lines.append("\n--- DISASSEMBLY ---")
    lines.append(info['disassembly'])
    return "\n".join(lines)

def decode_python_file(source_code: str, filename: str):
    from core.marshal_decoder import find_marshal_payloads, try_unwrap, extract_code_info, generate_decoded_output
    payloads = find_marshal_payloads(source_code)
    if not payloads:
        return {"success": False, "error": "No marshal payload found."}
    for payload in payloads:
        code_obj = try_unwrap(payload)
        if code_obj:
            info = extract_code_info(code_obj)
            if info:
                return {"success": True, "code": generate_decoded_output(info), "original_filename": filename}
    return {"success": False, "error": "Failed to decode."}
```
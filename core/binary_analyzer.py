import re

def decode_binary_file(data: bytes, filename: str):
    try:
        strings = re.findall(b'[\x20-\x7E]{8,}', data)
        string_list = [s.decode('utf-8', errors='ignore') for s in strings[:100]]

        marshal_output = ""
        for magic in [b'\xe3', b'\x63']:
            idx = data.find(magic)
            if idx != -1:
                try:
                    import marshal
                    import types
                    import dis
                    import io
                    obj = marshal.loads(data[idx:idx+300000])
                    if isinstance(obj, types.CodeType):
                        output = io.StringIO()
                        dis.dis(obj, file=output)
                        marshal_output = output.getvalue()
                        break
                except:
                    pass

        output = ""
        if marshal_output:
            output += "=== EMBEDDED PYTHON BYTECODE ===\n" + marshal_output + "\n\n"
        if string_list:
            output += "=== EXTRACTED STRINGS ===\n" + "\n".join(string_list)

        if output.strip():
            return {"success": True, "code": output, "original_filename": filename}
        return {"success": False, "error": "No useful data found."}
    except Exception as e:
        return {"success": False, "error": str(e)}
```
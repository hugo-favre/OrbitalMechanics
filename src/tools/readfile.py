def read_input_file(filename):
    params = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, val = line.split("=", 1)
                key, val = key.strip(), val.strip()
                try:
                    params[key] = float(val)
                except ValueError:
                    params[key] = val

            elif ":" in line:
                key, val = line.split(":", 1)
                key, val = key.strip(), val.strip()
                params[key] = [p.strip().lower() for p in val.split(",") if p.strip()]
    
    return params

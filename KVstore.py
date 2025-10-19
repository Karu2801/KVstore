import os
import sys

DB_FILE = "data.db"
pairs = []

def replay_log():
    if not os.path.exists(DB_FILE):
        open(DB_FILE, "a").close()
        return
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("SET "):
                parts = line.split(" ", 2)
                if len(parts) == 3:
                    pairs.append((parts[1], parts[2]))

def append_set(k, v, fh):
    fh.write(f"SET {k} {v}\n")
    fh.flush()
    os.fsync(fh.fileno())

def get_value(k):
    for i in range(len(pairs) - 1, -1, -1):
        if pairs[i][0] == k:
            return pairs[i][1]
    return None

def main():
    replay_log()
    with open(DB_FILE, "a", encoding="utf-8") as fh:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if line == "EXIT":
                return
            if line.startswith("SET "):
                parts = line.split(" ", 2)
                if len(parts) != 3:
                    continue
                append_set(parts[1], parts[2], fh)
                pairs.append((parts[1], parts[2]))
                continue
            if line.startswith("GET "):
                parts = line.split(" ", 1)
                if len(parts) != 2:
                    continue
                v = get_value(parts[1])
                print(v if v is not None else "NULL", flush=True)

if __name__ == "__main__":
    main()

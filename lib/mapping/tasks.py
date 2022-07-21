from flask import jsonify


def return_example_tasks_config():
    return jsonify({"tasks": {
        "server": {"task_type": "server"},
        "task1": {
            "enabled": True,
            "task_type": "read",
            "task_line": "{datetime} {param1} {param2} {param3}",
            "task_repeat": 60,
            "report_name": "{device_name}_{task_name}_{datetime}",
            "report_path": "~",
            "report_type": "text"
        },
        }}
    )

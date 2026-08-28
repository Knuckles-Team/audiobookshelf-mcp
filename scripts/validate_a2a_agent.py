#!/usr/bin/env python3
import asyncio
import json
import uuid

import httpx

A2A_URL = "http://localhost:9016/a2a/"


def _build_message_payload(q: str) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "kind": "message",
                "role": "user",
                "parts": [{"kind": "text", "text": q}],
                "messageId": str(uuid.uuid4()),
            }
        },
        "id": 1,
    }


def _build_poll_payload(task_id) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": "tasks/get",
        "params": {"id": task_id},
        "id": 2,
    }


def _print_agent_response_parts(last_msg: dict | None) -> None:
    """Print the agent's response parts (or a fallback) for the final history message."""
    if last_msg and "parts" in last_msg:
        print("\n--- Agent Response ---")
        for part in last_msg["parts"]:
            if "text" in part:
                print(part["text"])
            elif "content" in part:
                print(part["content"])
    elif last_msg:
        print(f"Final Message (No parts): {last_msg}")
    else:
        print("\n--- No Agent Response Found in History ---")


def _last_non_user_message(history: list) -> dict | None:
    for msg in reversed(history):
        if msg.get("role") != "user":
            return msg
    return None


def _print_task_history(poll_data: dict) -> None:
    """Print the agent's final response from the finished task's history, if present."""
    result = poll_data["result"]
    if "history" not in result:
        return
    history = result["history"]
    if not history:
        return
    _print_agent_response_parts(_last_non_user_message(history))


async def _poll_once(client: httpx.AsyncClient, url: str, task_id) -> dict | None:
    """Send one tasks/get poll; return the decoded body, or None on a failed poll."""
    poll_resp = await client.post(
        url, json=_build_poll_payload(task_id), headers={"Content-Type": "application/json"}
    )
    if poll_resp.status_code != 200:
        print(f"Polling Failed: {poll_resp.status_code}")
        print(f"Polling Error Details: {poll_resp.text}")
        return None
    return poll_resp.json()


def _report_finished_task(poll_data: dict, state: str) -> None:
    print(f"\nTask Finished with state: {state}")
    _print_task_history(poll_data)
    print(f"Full Result Debug:\n{json.dumps(poll_data, indent=2)}")


async def _poll_task(client: httpx.AsyncClient, url: str, task_id) -> dict | None:
    """Poll tasks/get until the task leaves an active state; return the final poll_data."""
    while True:
        await asyncio.sleep(2)
        poll_data = await _poll_once(client, url, task_id)
        if poll_data is None:
            return None
        if "result" not in poll_data:
            print("Starting polling error key check...")
            if "error" in poll_data:
                print(f"Polling Error: {poll_data['error']}")
            return None
        state = poll_data["result"]["status"]["state"]
        print(f"Task State: {state}")
        if state not in ("submitted", "running", "working"):
            _report_finished_task(poll_data, state)
            return poll_data


async def _follow_up_on_response(client: httpx.AsyncClient, url: str, data: dict) -> None:
    """If ``data`` carries a submitted task id, poll it; always report a top-level error."""
    if "result" in data and "id" in data["result"]:
        task_id = data["result"]["id"]
        print(f"\nTask Submitted with ID: {task_id}. Polling for result...")
        await _poll_task(client, url, task_id)
    if "error" in data:
        print(f"JSON-RPC Error: {data['error']}")


async def _handle_ok_response(client: httpx.AsyncClient, url: str, resp: httpx.Response) -> None:
    """Handle a 200 response: parse JSON (or print raw text) and follow up on a task."""
    try:
        data = resp.json()
    except json.JSONDecodeError:
        print(f"Response (Text):\n{resp.text}")
        return
    print(f"Response (JSON):\n{json.dumps(data, indent=2)}")
    await _follow_up_on_response(client, url, data)


async def _ask_question(client: httpx.AsyncClient, url: str, q: str) -> None:
    """Send one question via message/send and drive the full response/poll flow."""
    print(f"\n\n\nUser: {q}")
    print("--- Sending Request ---")
    payload = _build_message_payload(q)
    try:
        print(f"Trying POST {url} with JSON-RPC (message/send)...")
        resp = await client.post(
            url, json=payload, headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            await _handle_ok_response(client, url, resp)
        else:
            print(f"Error: {resp.status_code}")
            print(resp.text)
    except httpx.RequestError as e:
        print(f"Connection failed to {url}: {e}")


async def main():
    print(f"Validating A2A Agent at {A2A_URL}...")

    questions = [
        "Can you get me the commits for project id 171?",
    ]

    async with httpx.AsyncClient(timeout=10000.0) as client:
        for q in questions:
            await _ask_question(client, A2A_URL, q)


if __name__ == "__main__":
    asyncio.run(main())

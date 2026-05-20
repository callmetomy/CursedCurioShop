import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TRIPO_TASK_URL = "https://api.tripo3d.ai/v2/openapi/task"


def build_text_to_model_payload(
    *,
    prompt: str,
    model_version: str | None = None,
    negative_prompt: str = (
        "low quality, blurry, distorted, extra limbs, human body, gore, text, logo, watermark"
    ),
) -> dict[str, Any]:
    payload = {
        "type": "text_to_model",
        "prompt": prompt,
        "negative_prompt": negative_prompt,
    }
    if model_version:
        payload["model_version"] = model_version
    return payload


@dataclass(frozen=True)
class TripoClient:
    api_key: str
    base_url: str = TRIPO_TASK_URL

    def build_submit_request(self, payload: dict[str, Any]) -> urllib.request.Request:
        return urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

    def build_status_request(self, task_id: str) -> urllib.request.Request:
        return urllib.request.Request(
            f"{self.base_url}/{task_id}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            method="GET",
        )

    def submit_text_to_model(self, prompt: str, model_version: str | None = None) -> dict[str, Any]:
        return self._send_json(
            self.build_submit_request(
                build_text_to_model_payload(prompt=prompt, model_version=model_version)
            )
        )

    def get_task(self, task_id: str) -> dict[str, Any]:
        return self._send_json(self.build_status_request(task_id))

    def wait_for_task(
        self,
        task_id: str,
        *,
        poll_seconds: int = 10,
        timeout_seconds: int = 300,
    ) -> dict[str, Any]:
        started = time.monotonic()
        while True:
            response = self.get_task(task_id)
            status = extract_status(response)
            if status in {"success", "failed", "cancelled", "banned", "unknown"}:
                return response
            if time.monotonic() - started > timeout_seconds:
                return response
            time.sleep(poll_seconds)

    def download_model(self, url: str, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(request, timeout=120) as response:
            output_path.write_bytes(response.read())
        return output_path

    def _send_json(self, request: urllib.request.Request) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Tripo API HTTP {error.code}: {body}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"Tripo API network error: {error.reason}") from error

        return json.loads(body)


def extract_task_id(response: dict[str, Any]) -> str | None:
    data = response.get("data")
    if isinstance(data, dict):
        task_id = data.get("task_id")
        if isinstance(task_id, str):
            return task_id
    task_id = response.get("task_id")
    if isinstance(task_id, str):
        return task_id
    return None


def extract_status(response: dict[str, Any]) -> str:
    data = response.get("data")
    if isinstance(data, dict):
        status = data.get("status")
        if isinstance(status, str):
            return status.lower()
    status = response.get("status")
    if isinstance(status, str):
        return status.lower()
    return "unknown"


def extract_model_url(response: dict[str, Any]) -> str | None:
    data = response.get("data")
    if not isinstance(data, dict):
        return None
    output = data.get("output")
    if not isinstance(output, dict):
        return None

    for key in ("pbr_model", "model"):
        value = output.get(key)
        if isinstance(value, str) and value.startswith("http"):
            return value
    return None

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.asset_pipeline.env import load_env_file
from tools.asset_pipeline.providers.tripo import TripoClient, build_text_to_model_payload


class TripoProviderTests(unittest.TestCase):
    def test_load_env_file_reads_values_without_shell_expansion(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "TRIPO_API_KEY=tsk_example\n"
                "EMPTY_VALUE=\n"
                "# COMMENTED=value\n",
                encoding="utf-8",
            )

            values = load_env_file(env_path)

            self.assertEqual(values["TRIPO_API_KEY"], "tsk_example")
            self.assertEqual(values["EMPTY_VALUE"], "")
            self.assertNotIn("COMMENTED", values)

    def test_build_text_to_model_payload_uses_game_asset_defaults(self):
        payload = build_text_to_model_payload(
            prompt="A cursed porcelain teacup game prop.",
        )

        self.assertEqual(payload["type"], "text_to_model")
        self.assertNotIn("model_version", payload)
        self.assertEqual(payload["prompt"], "A cursed porcelain teacup game prop.")
        self.assertIn("negative_prompt", payload)

    def test_tripo_client_builds_authorized_request_without_exposing_key(self):
        client = TripoClient(api_key="tsk_secret")
        request = client.build_submit_request(
            build_text_to_model_payload(prompt="A small antique key.")
        )

        self.assertEqual(request.full_url, "https://api.tripo3d.ai/v2/openapi/task")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.headers["Authorization"], "Bearer tsk_secret")
        decoded = json.loads(request.data.decode("utf-8"))
        self.assertEqual(decoded["type"], "text_to_model")


if __name__ == "__main__":
    unittest.main()

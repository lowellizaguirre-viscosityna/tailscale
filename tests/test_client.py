import json
import unittest

from tailtray.client import CommandResult, TailscaleClient, TailscaleError


class FakeRunner:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, args):
        self.calls.append(tuple(args))
        return self.responses.pop(0)


def result(payload, returncode=0, stderr=""):
    stdout = json.dumps(payload) if not isinstance(payload, str) else payload
    return CommandResult(returncode, stdout, stderr)


class TailscaleClientTests(unittest.TestCase):
    def test_status_maps_current_preference_names(self):
        runner = FakeRunner([
            result({"BackendState": "Running", "Self": {"LoginName": "me@example.com"}, "CurrentTailnet": {"Name": "work"}}),
            result({"CorpDNS": True, "RouteAll": False}),
        ])
        status = TailscaleClient(runner=runner).status()
        self.assertTrue(status.is_running)
        self.assertEqual(status.account_name, "me@example.com")
        self.assertEqual(status.tailnet_name, "work")
        self.assertTrue(status.accept_dns)
        self.assertFalse(status.accept_routes)
        self.assertEqual(runner.calls, [("tailscale", "status", "--json"), ("tailscale", "debug", "prefs")])

    def test_profile_list_and_switch_use_argument_arrays(self):
        runner = FakeRunner([result([
            {"id": "one", "nickname": "Personal", "tailnet": "personal", "account": "me@example.com", "selected": False},
            {"id": "two", "nickname": "Work", "tailnet": "work", "account": "me@example.com", "selected": True},
        ]), result("")])
        client = TailscaleClient(runner=runner)
        profiles = client.profiles()
        self.assertEqual([(profile.label, profile.active) for profile in profiles], [("Personal — me@example.com (personal)", False), ("Work — me@example.com (work)", True)])
        client.switch_profile("two")
        self.assertEqual(runner.calls[-1], ("tailscale", "switch", "two"))

    def test_profile_list_falls_back_to_tailscale_text_output(self):
        runner = FakeRunner([result("ID  TAILNET  ACCOUNT\nabc  work  me@example.com *\ndef  personal  me@example.com")])
        profiles = TailscaleClient(runner=runner).profiles()
        self.assertEqual([(profile.identifier, profile.label, profile.active) for profile in profiles], [("abc", "work me@example.com", True), ("def", "personal me@example.com", False)])

    def test_toggles_only_send_their_own_flag(self):
        runner = FakeRunner([result(""), result("")])
        client = TailscaleClient(runner=runner)
        client.set_accept_dns(False)
        client.set_accept_routes(True)
        self.assertEqual(runner.calls, [("tailscale", "set", "--accept-dns=false"), ("tailscale", "set", "--accept-routes=true")])

    def test_running_toggle_uses_up_and_down(self):
        runner = FakeRunner([result(""), result("")])
        client = TailscaleClient(runner=runner)
        client.set_running(True)
        client.set_running(False)
        self.assertEqual(runner.calls, [("tailscale", "up"), ("tailscale", "down")])

    def test_start_does_not_change_dns_or_route_preferences(self):
        runner = FakeRunner([result("")])
        TailscaleClient(runner=runner).set_running(True)
        self.assertEqual(runner.calls, [("tailscale", "up")])

    def test_failure_is_actionable(self):
        runner = FakeRunner([CommandResult(1, "", "permission denied")])
        with self.assertRaisesRegex(TailscaleError, "operator"):
            TailscaleClient(runner=runner).status()

    def test_preferences_write_denial_explains_operator_setup(self):
        runner = FakeRunner([CommandResult(1, "", "prefs write access denied")])
        with self.assertRaisesRegex(TailscaleError, "tailscale set --operator"):
            TailscaleClient(runner=runner).set_accept_dns(True)

    def test_invalid_json_is_rejected(self):
        runner = FakeRunner([result("not json")])
        with self.assertRaisesRegex(TailscaleError, "invalid JSON"):
            TailscaleClient(runner=runner).status()


if __name__ == "__main__":
    unittest.main()

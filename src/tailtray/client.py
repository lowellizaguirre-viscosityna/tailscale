"""Safe, testable access to the local `tailscale` command-line client."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .models import Profile, TailscaleStatus


class TailscaleError(RuntimeError):
    """An actionable failure returned while invoking or parsing Tailscale."""


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


Runner = Callable[[Sequence[str]], CommandResult]
COMMAND_TIMEOUT_SECONDS = 45


def _default_runner(args: Sequence[str]) -> CommandResult:
    try:
        completed = subprocess.run(list(args), check=False, capture_output=True, text=True,
                                   timeout=COMMAND_TIMEOUT_SECONDS, shell=False)
    except FileNotFoundError as error:
        raise TailscaleError("The `tailscale` command was not found on this computer.") from error
    except subprocess.TimeoutExpired as error:
        raise TailscaleError(f"Tailscale did not respond within {COMMAND_TIMEOUT_SECONDS} seconds.") from error
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


class TailscaleClient:
    """Invoke a fixed set of Tailscale commands without shell interpolation."""

    def __init__(self, executable: str = "tailscale", runner: Runner | None = None) -> None:
        self._executable = executable
        self._runner = runner or _default_runner

    def status(self) -> TailscaleStatus:
        payload = self._json_command("status", "--json")
        # `status --json` describes connection state but does not reliably expose
        # editable preferences. `debug prefs` is the CLI's JSON representation of
        # `CorpDNS` and `RouteAll` for the installed profile.
        try:
            prefs = _mapping(self._json_command("debug", "prefs"))
        except TailscaleError:
            prefs = {}
        self_info = _mapping(payload.get("Self"))
        tailnet = _mapping(payload.get("CurrentTailnet"))
        return TailscaleStatus(
            backend_state=str(payload.get("BackendState", "Unknown")),
            account_name=_first_text(self_info, "LoginName", "UserProfile", "DisplayName"),
            tailnet_name=_first_text(tailnet, "Name", "MagicDNSSuffix"),
            accept_dns=_first_bool(prefs, "AcceptDNS", "CorpDNS"),
            accept_routes=_first_bool(prefs, "AcceptRoutes", "RouteAll"),
        )

    def profiles(self) -> list[Profile]:
        result = self._command("switch", "--list", "--json")
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            return _profiles_from_text(result.stdout)
        raw_profiles: Any = payload if isinstance(payload, list) else (
            payload.get("Profiles") or payload.get("Accounts") or payload.get("profiles") or []
        )
        if not isinstance(raw_profiles, list):
            raise TailscaleError("Tailscale returned an unrecognized workspace list.")
        current = ""
        if isinstance(payload, Mapping):
            current_value = payload.get("Current") or payload.get("CurrentID") or payload.get("CurrentProfileID")
            if isinstance(current_value, Mapping):
                current_value = current_value.get("ID") or current_value.get("id")
            if current_value is not None:
                current = str(current_value)
        profiles: list[Profile] = []
        for entry in raw_profiles:
            if not isinstance(entry, Mapping):
                continue
            identifier = _first_text(entry, "ID", "Id", "id", "ProfileID")
            if not identifier:
                continue
            nickname = _first_text(entry, "nickname", "Nickname", "name", "Name", "displayName", "DisplayName")
            account = _first_text(entry, "account", "Account", "loginName", "LoginName")
            tailnet = _first_text(entry, "tailnet", "Tailnet")
            label = nickname or account or tailnet or identifier
            if nickname and account and account != nickname:
                label = f"{nickname} — {account}"
            if tailnet and tailnet not in label:
                label = f"{label} ({tailnet})"
            profiles.append(Profile(identifier, label, bool(entry.get("selected") or entry.get("Selected") or entry.get("current") or entry.get("Current") or entry.get("isCurrent") or entry.get("IsCurrent") or identifier == current)))
        return profiles

    def switch_profile(self, profile_id: str) -> None:
        if not profile_id:
            raise TailscaleError("No workspace was selected.")
        self._command("switch", profile_id)

    def set_running(self, enabled: bool) -> None:
        """Connect with the saved configuration, or disconnect from the tailnet."""
        self._command("up" if enabled else "down")

    def set_accept_dns(self, enabled: bool) -> None:
        self._command("set", f"--accept-dns={'true' if enabled else 'false'}")

    def set_accept_routes(self, enabled: bool) -> None:
        self._command("set", f"--accept-routes={'true' if enabled else 'false'}")

    def _json_command(self, *arguments: str) -> Any:
        result = self._command(*arguments)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise TailscaleError("Tailscale returned invalid JSON. See diagnostics for details.") from error

    def _command(self, *arguments: str) -> CommandResult:
        result = self._runner((self._executable, *arguments))
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            if "prefs write access denied" in detail.lower() or "permission denied" in detail.lower():
                raise TailscaleError(
                    "Tailscale denied permission to change settings. In a terminal, run "
                    "`sudo tailscale set --operator=\"$USER\"`, then restart TailTray."
                )
            raise TailscaleError(detail or f"Tailscale failed with exit status {result.returncode}.")
        return result


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _first_text(values: Mapping[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = values.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _first_bool(values: Mapping[str, Any], *keys: str) -> bool | None:
    for key in keys:
        value = values.get(key)
        if isinstance(value, bool):
            return value
    return None


def _profiles_from_text(output: str) -> list[Profile]:
    """Parse the human-readable alpha `switch --list` output as a fallback."""
    profiles: list[Profile] = []
    for line in output.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("id") or set(line) == {"-"}:
            continue
        columns = line.split()
        if len(columns) < 2:
            continue
        identifier = columns[0]
        active = line.endswith("*")
        label = " ".join(columns[1:]).rstrip("*").rstrip()
        profiles.append(Profile(identifier, label or identifier, active))
    if not profiles:
        raise TailscaleError("Tailscale returned an unrecognized workspace list.")
    return profiles

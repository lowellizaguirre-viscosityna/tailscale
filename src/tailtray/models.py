"""Application data that is independent of the GTK user interface."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TailscaleStatus:
    backend_state: str
    account_name: str | None
    tailnet_name: str | None
    accept_dns: bool | None
    accept_routes: bool | None

    @property
    def is_running(self) -> bool:
        return self.backend_state == "Running"


@dataclass(frozen=True)
class Profile:
    identifier: str
    label: str
    active: bool = False

"""GTK/Ayatana AppIndicator presentation for TailTray."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AyatanaAppIndicator3", "0.1")
from gi.repository import AyatanaAppIndicator3 as AppIndicator, GLib, Gtk  # noqa: E402

from .client import TailscaleClient, TailscaleError
from .models import Profile, TailscaleStatus


class TrayApplication:
    def __init__(self) -> None:
        self.client = TailscaleClient()
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="tailtray")
        self.status: TailscaleStatus | None = None
        self.error: str | None = None
        self.busy = False
        self.diagnostics: list[str] = []
        asset_dir = Path(__file__).resolve().parents[2] / "assets"
        self.indicator = AppIndicator.Indicator.new("tailtray", "tailtray-red", AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_icon_theme_path(str(asset_dir))
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self._rebuild_menu()

    def run(self) -> None:
        self.refresh()
        GLib.timeout_add_seconds(10, self._poll)
        Gtk.main()

    def _poll(self) -> bool:
        self.refresh()
        return True

    def refresh(self, *_unused: object) -> None:
        if not self.busy:
            self._submit("Refresh status", self.client.status, self._apply_status)

    def _apply_status(self, status: object) -> None:
        self.status = status if isinstance(status, TailscaleStatus) else None
        self.error = None

    def _show_profiles(self, *_unused: object) -> None:
        self._submit("List workspaces", self.client.profiles, self._open_profile_picker)

    def _open_profile_picker(self, profiles: object) -> None:
        available = profiles if isinstance(profiles, list) else []
        if not available:
            self._dialog("Switch workspace", "Tailscale did not return any saved workspaces.")
            return
        dialog = Gtk.Dialog(title="Switch workspace", flags=0)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Switch", Gtk.ResponseType.ACCEPT)
        content = dialog.get_content_area()
        content.set_border_width(12)
        content.add(Gtk.Label(label="Choose a Tailscale workspace:"))
        selected = available[0].identifier
        group_anchor: Gtk.RadioButton | None = None
        profile_buttons: list[tuple[Gtk.RadioButton, str]] = []
        for profile in available:
            button = Gtk.RadioButton.new_with_label_from_widget(group_anchor, profile.label)
            group_anchor = group_anchor or button
            button.set_active(profile.active)
            if profile.active:
                selected = profile.identifier
            profile_buttons.append((button, profile.identifier))
            content.add(button)
        dialog.show_all()
        response = dialog.run()
        for button, profile_id in profile_buttons:
            if button.get_active():
                selected = profile_id
                break
        dialog.destroy()
        if response == Gtk.ResponseType.ACCEPT:
            self._submit("Switch workspace", lambda: self.client.switch_profile(selected), lambda _: self.refresh())

    def _toggle_running(self, item: Gtk.CheckMenuItem) -> None:
        enabled = item.get_active()
        action = "Start Tailscale" if enabled else "Stop Tailscale"
        self._submit(action, lambda: self.client.set_running(enabled), lambda _: self.refresh())

    def _toggle_dns(self, item: Gtk.CheckMenuItem) -> None:
        enabled = item.get_active()
        self._submit("Update DNS preference", lambda: self.client.set_accept_dns(enabled), lambda _: self.refresh())

    def _toggle_routes(self, item: Gtk.CheckMenuItem) -> None:
        enabled = item.get_active()
        self._submit("Update route preference", lambda: self.client.set_accept_routes(enabled), lambda _: self.refresh())

    def _submit(self, label: str, action: Callable[[], object], success: Callable[[object], None] | None = None) -> None:
        if self.busy:
            return
        self.busy = True
        self._rebuild_menu()
        future = self.executor.submit(action)

        def complete(done: object) -> bool:
            self.busy = False
            try:
                result = done.result()  # type: ignore[union-attr]
                self.diagnostics.insert(0, f"{label}: succeeded")
                if success:
                    success(result)
            except TailscaleError as error:
                self.error = str(error)
                self.diagnostics.insert(0, f"{label}: {error}")
            except Exception as error:
                self.error = f"Unexpected error: {error}"
                self.diagnostics.insert(0, f"{label}: unexpected error: {error}")
            self._rebuild_menu()
            return False

        future.add_done_callback(lambda done: GLib.idle_add(complete, done))

    def _rebuild_menu(self) -> None:
        menu = Gtk.Menu()
        state = self.status.backend_state if self.status else "Checking…"
        account = (self.status.account_name or self.status.tailnet_name) if self.status else None
        self._append_label(menu, f"Tailscale: {state}" + (f" — {account}" if account else ""))
        if self.error:
            self._append_label(menu, self.error)
        menu.append(Gtk.SeparatorMenuItem())
        can_act = bool(self.status and not self.busy)

        is_running = bool(self.status and self.status.is_running)
        can_configure = can_act and is_running
        running_item = Gtk.CheckMenuItem.new_with_label("Stop Tailscale" if is_running else "Start Tailscale")
        running_item.set_active(is_running)
        running_item.set_sensitive(can_act)
        running_item.connect("toggled", self._toggle_running)
        menu.append(running_item)

        workspace = Gtk.MenuItem.new_with_label("Switch workspace…")
        workspace.set_sensitive(can_configure)
        workspace.connect("activate", self._show_profiles)
        menu.append(workspace)
        if self.status and not is_running:
            self._append_label(menu, "Start Tailscale before switching workspaces")

        dns = Gtk.CheckMenuItem.new_with_label("Accept DNS")
        dns.set_active(bool(self.status and self.status.accept_dns))
        dns.set_sensitive(can_configure and self.status is not None and self.status.accept_dns is not None)
        dns.connect("toggled", self._toggle_dns)
        menu.append(dns)
        routes = Gtk.CheckMenuItem.new_with_label("Accept routes")
        routes.set_active(bool(self.status and self.status.accept_routes))
        routes.set_sensitive(can_configure and self.status is not None and self.status.accept_routes is not None)
        routes.connect("toggled", self._toggle_routes)
        menu.append(routes)

        menu.append(Gtk.SeparatorMenuItem())
        refresh = Gtk.MenuItem.new_with_label("Refresh")
        refresh.set_sensitive(not self.busy)
        refresh.connect("activate", self.refresh)
        menu.append(refresh)
        diagnostics = Gtk.MenuItem.new_with_label("Open diagnostics")
        diagnostics.connect("activate", self._open_diagnostics)
        menu.append(diagnostics)
        setup = Gtk.MenuItem.new_with_label("Permission setup help")
        setup.connect("activate", self._open_setup_help)
        menu.append(setup)
        quit_item = Gtk.MenuItem.new_with_label("Quit")
        quit_item.connect("activate", lambda *_: Gtk.main_quit())
        menu.append(quit_item)
        menu.show_all()
        self.indicator.set_menu(menu)

        running = bool(self.status and self.status.is_running)
        self.indicator.set_icon_full("tailtray-green" if running else "tailtray-red", "TailTray")
        self.indicator.set_title(f"TailTray: {self.error or state}")

    @staticmethod
    def _append_label(menu: Gtk.Menu, label: str) -> None:
        item = Gtk.MenuItem.new_with_label(label)
        item.set_sensitive(False)
        menu.append(item)

    def _open_diagnostics(self, *_unused: object) -> None:
        self._dialog("TailTray diagnostics", "\n".join(self.diagnostics[:20]) or "No commands have run yet.")

    def _open_setup_help(self, *_unused: object) -> None:
        self._dialog("Permission setup", "TailTray does not run sudo or store passwords. To permit routine local Tailscale actions, run this once in a terminal:\n\nsudo tailscale set --operator=\"$USER\"")

    @staticmethod
    def _dialog(title: str, text: str) -> None:
        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.CLOSE, text=title)
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

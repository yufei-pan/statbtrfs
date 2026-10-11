# /proc/self/mounts lines
MOUNT_LINES_MULTI = [
    "/dev/sda1 /mnt/a btrfs rw,relatime 0 0",
    "/dev/sdb1 /mnt/b btrfs rw,relatime 0 0",
    "/dev/sdc1 /data btrfs rw,relatime 0 0",
]

MOUNT_LINES_SINGLE = [
    "/dev/sda1 /mnt/a btrfs rw,relatime 0 0",
]

SHOW_SINGLE = [
    "Label: none  uuid: 11111111-2222-3333-4444-555555555555",
    "Total devices 1 FS bytes used 12.34GiB",
    "devid    1 size 100.00GiB used 50.00GiB path /dev/sda1",
]

SHOW_MULTI_DEVICE = [
    "Label: none  uuid: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "Total devices 2 FS bytes used 1.00GiB",
    "devid    1 size 10.00GiB used 2.00GiB path /dev/nvme0n1",
    "devid    2 size 10.00GiB used 2.00GiB path /dev/nvme1n1",
]

# Label text that contains the words the old substring parser keyed on.
SHOW_TRICKY_LABEL = [
    "Label: 'backup path: Total devices uuid: x'  uuid: 11111111-2222-3333-4444-555555555555",
    "\tTotal devices 1 FS bytes used 12.34GiB",
    "\tdevid    1 size 100.00GiB used 50.00GiB path /dev/sda1",
]

# Mounted degraded: btrfs omits the unopenable device and adds a marker line.
SHOW_DEGRADED = [
    "Label: none  uuid: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "\tTotal devices 2 FS bytes used 1.00GiB",
    "\tdevid    1 size 10.00GiB used 2.00GiB path /dev/nvme0n1",
    "\t*** Some devices missing",
]

# Newer btrfs-progs list the missing device itself.
SHOW_DEGRADED_MARKED = [
    "Label: none  uuid: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "\tTotal devices 2 FS bytes used 1.00GiB",
    "\tdevid    1 size 10.00GiB used 2.00GiB path /dev/nvme0n1",
    "\tdevid    2 size 0 used 0 path <missing disk #2> MISSING",
]

SHOW_INCOMPLETE = [
    "Label: none  uuid: 11111111-2222-3333-4444-555555555555",
    "Total devices 1 FS bytes used 1.00GiB",
]

STATS_ZERO = [
    "[/dev/sda1].write_io_errs    0",
    "[/dev/sda1].read_io_errs     0",
    "[/dev/sda1].flush_io_errs    0",
    "[/dev/sda1].corruption_errs  0",
    "[/dev/sda1].generation_errs  0",
]

STATS_NONZERO = [
    "[/dev/sda1].write_io_errs    0",
    "[/dev/sda1].read_io_errs     3",
    "[/dev/sda1].corruption_errs  12",
    "[/dev/sda1].generation_errs  1",
    "not-a-stat-line",
]

# Errors on the first device, last device mostly clean: a last-line-wins parser reports ~0.
STATS_MULTI_DEVICE = [
    "[/dev/nvme0n1].write_io_errs    7",
    "[/dev/nvme0n1].read_io_errs     0",
    "[/dev/nvme0n1].flush_io_errs    2",
    "[/dev/nvme0n1].corruption_errs  40",
    "[/dev/nvme0n1].generation_errs  0",
    "[/dev/nvme1n1].write_io_errs    0",
    "[/dev/nvme1n1].read_io_errs     1",
    "[/dev/nvme1n1].flush_io_errs    0",
    "[/dev/nvme1n1].corruption_errs  2",
    "[/dev/nvme1n1].generation_errs  0",
]

SCRUB_NEVER = [
    "scrub status for 11111111-2222-3333-4444-555555555555",
    "no stats available",
]

SCRUB_FINISHED_OK = [
    "scrub status for 11111111-2222-3333-4444-555555555555",
    "Scrub started:    Thu May  2 09:56:55 2024",
    "Status:           finished",
    "Duration:         0:10:00",
    "Total to scrub:   10.00GiB",
    "Rate:             17.00MiB/s",
    "Error summary:    no errors found",
]

SCRUB_RUNNING = [
    "scrub status for 11111111-2222-3333-4444-555555555555",
    "Scrub started:    Thu May  2 09:56:55 2024",
    "Status:           running",
    "Time left:        0:05:00",
    "Total to scrub:   100.00GiB",
    "Bytes scrubbed:   40.00GiB",
    "Rate:             20.00MiB/s",
    "Error summary:    no errors found",
]

SCRUB_FINISHED_ERRORS = [
    "scrub status for 11111111-2222-3333-4444-555555555555",
    "Scrub started:    Thu May  2 09:56:55 2024",
    "Status:           finished",
    "Duration:         0:10:00",
    "Total to scrub:   10.00GiB",
    "Rate:             17.00MiB/s",
    "Error summary:    csum=3",
    "  Corrected:      0",
    "  Uncorrectable:  3",
    "  Unverified:     0",
]

SCRUB_TIME_BASIC = "Thu May  2 09:56:55 2024"
SCRUB_TIME_ISO = "2024-05-02 09:56:55"


def uuid_for(n):
    return f"{n:08x}-0000-0000-0000-000000000000"


def make_show(uuid, *devices, used="1.00GiB"):
    """`btrfs filesystem show` output for one filesystem."""
    devices = devices or ("/dev/sda1",)
    lines = [f"Label: none  uuid: {uuid}", f"\tTotal devices {len(devices)} FS bytes used {used}"]
    lines += [f"\tdevid {i:4d} size 10.00GiB used 2.00GiB path {dev}" for i, dev in enumerate(devices, 1)]
    return lines


# One system disk with three subvolume mounts, plus a separate data pool.
SUBVOL_MOUNT_LINES = [
    "/dev/sda2 / btrfs rw,subvol=/@ 0 0",
    "/dev/sda2 /home btrfs rw,subvol=/@home 0 0",
    "/dev/sdb /mnt/pool btrfs rw 0 0",
    "/dev/sda2 /var/log btrfs rw,subvol=/@log 0 0",
]
SUBVOL_SHOWS = {
    "/": make_show(uuid_for(1), "/dev/sda2"),
    "/home": make_show(uuid_for(1), "/dev/sda2"),
    "/var/log": make_show(uuid_for(1), "/dev/sda2"),
    "/mnt/pool": make_show(uuid_for(2), "/dev/sdb", "/dev/sdc"),
}


class CommandMap:
    """Stub for execute_command / execute_commands."""

    def __init__(self, mapping=None, default=None):
        self.mapping = dict(mapping or {})
        self.default = [] if default is None else list(default)
        self.calls = []

    @staticmethod
    def _norm(command):
        cmd = tuple(command)
        if cmd and cmd[0] == "sudo":
            cmd = cmd[1:]
        return cmd

    def _lookup(self, command):
        key = self._norm(command)
        if key in self.mapping:
            return list(self.mapping[key])
        return list(self.default)

    def execute_command(self, command, wait=True):
        self.calls.append(("cmd", list(command), wait))
        return self._lookup(command)

    def execute_commands(self, commands, wait=True):
        self.calls.append(("cmds", [list(c) for c in commands], wait))
        return [self._lookup(c) for c in commands]


def install_mounts(monkeypatch, module, lines):
    """Serve ``lines`` as the contents of /proc/self/mounts."""
    monkeypatch.setattr(module, "read_proc_mounts", lambda: list(lines))


def install_status(monkeypatch, module, per_mount):
    """Serve /proc/self/mounts plus show/stats/scrub status output: {mount: (show, stats, scrub)}."""
    install_mounts(monkeypatch, module, [f"/dev/sdx {mount} btrfs rw 0 0" for mount in per_mount])
    mapping = {}
    for mount, (show, stats, scrub) in per_mount.items():
        mapping[("btrfs", "filesystem", "show", mount)] = show
        mapping[("btrfs", "device", "stats", mount)] = stats
        mapping[("btrfs", "scrub", "status", mount)] = scrub
    return install_command_map(monkeypatch, CommandMap(mapping), module)


def install_command_map(monkeypatch, command_map, module):
    monkeypatch.setattr(module, "execute_command", command_map.execute_command)
    monkeypatch.setattr(module, "execute_commands", command_map.execute_commands)
    return command_map


class FakeBtrfs:
    """Simulated filesystems for -s / -w tests.

    Each mount is its own filesystem. start_scrub() marks a mount running; a running scrub
    finishes after ``polls`` status polls (int, or {mount: int}). ``running`` mounts start out
    running (started elsewhere), ``finished`` ones start out finished. ``start_results`` overrides
    start_scrub() per mount. ``interrupt_on_sleep`` raises KeyboardInterrupt on that sleep (1-based).
    """

    def __init__(self, mounts, polls=2, running=(), finished=(), errors=(), start_results=None,
                 clock=1_000_000.0, interrupt_on_sleep=None):
        self.mounts = list(mounts)
        self.polls = polls
        self.state = {m: "never" for m in self.mounts}
        self.remaining = {}
        for m in running:
            self._run(m)
        for m in finished:
            self.state[m] = "finished"
        self.errors = set(errors)
        self.start_results = dict(start_results or {})
        self.clock = clock
        self.interrupt_on_sleep = interrupt_on_sleep
        self.sleeps = 0
        self.started = []    # (mount, clock)
        self.cancelled = []
        self.status_polls = 0

    def _run(self, mount):
        self.state[mount] = "running"
        self.remaining[mount] = self.polls[mount] if isinstance(self.polls, dict) else self.polls

    # --- patched functions ---
    def start_scrub(self, mount):
        self.started.append((mount, self.clock))
        if mount in self.start_results:
            return self.start_results[mount]
        if self.state[mount] == "running":
            return "running", "ERROR: Scrub is already running."
        self._run(mount)
        return "started", f"scrub started on {mount}"

    def execute_command(self, command, wait=True):
        if command[:3] == ["btrfs", "scrub", "cancel"]:
            self.cancelled.append(command[3])
            self.state[command[3]] = "aborted"
            return ["scrub cancelled"]
        return self.execute_commands([command])[0]

    def execute_commands(self, commands, wait=True):
        out = [self._answer(c) for c in commands]
        if any(c[:3] == ["btrfs", "scrub", "status"] for c in commands):
            self.status_polls += 1
            for m in [m for m, s in self.state.items() if s == "running"]:
                self.remaining[m] -= 1
                if self.remaining[m] <= 0:
                    self.state[m] = "finished"
        return out

    def _answer(self, command):
        mount = command[-1]
        if command[:3] == ["btrfs", "filesystem", "show"]:
            return make_show(uuid_for(self.mounts.index(mount) + 1))
        if command[:3] == ["btrfs", "device", "stats"]:
            return list(STATS_ZERO)
        if command[:3] == ["btrfs", "scrub", "status"]:
            state = self.state[mount]
            if state == "running":
                return list(SCRUB_RUNNING)
            if state == "finished":
                return list(SCRUB_FINISHED_ERRORS if mount in self.errors else SCRUB_FINISHED_OK)
            if state == "aborted":
                return [line.replace("finished", "aborted") for line in SCRUB_FINISHED_OK]
            return list(SCRUB_NEVER)
        return []

    def time(self):
        return self.clock

    def sleep(self, seconds):
        self.sleeps += 1
        if self.sleeps == self.interrupt_on_sleep:
            raise KeyboardInterrupt
        self.clock += seconds

    def install(self, monkeypatch, module):
        install_mounts(monkeypatch, module, [f"/dev/sdx {m} btrfs rw 0 0" for m in self.mounts])
        monkeypatch.setattr(module, "start_scrub", self.start_scrub)
        monkeypatch.setattr(module, "execute_command", self.execute_command)
        monkeypatch.setattr(module, "execute_commands", self.execute_commands)
        monkeypatch.setattr(module.time, "time", self.time)
        monkeypatch.setattr(module.time, "sleep", self.sleep)
        monkeypatch.setattr(module.multiCMD, "pretty_format_table", lambda rows, header=None: "TABLE")
        return self

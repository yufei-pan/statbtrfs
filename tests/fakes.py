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


def install_command_map(monkeypatch, command_map, module):
    monkeypatch.setattr(module, "execute_command", command_map.execute_command)
    monkeypatch.setattr(module, "execute_commands", command_map.execute_commands)
    return command_map

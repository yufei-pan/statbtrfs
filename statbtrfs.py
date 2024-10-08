#!/usr/bin/env python3

import subprocess
from prettytable import PrettyTable
import argparse
import time
import os
import sys
import threading
import fnmatch

# ANSI color codes for coloring output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def execute_command(cmd, timeout=120,wait=True):
    try:
        columns, _ = os.get_terminal_size()
    except :
        columns = 80
    def subprocess_execution():
        nonlocal stdOut, stderr, returncode, process, process_killed
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc: 
            process = proc
            while not process_killed:
                line = process.stdout.readline()
                if not line: break
                stdOut.append(line)
                # if wait:
                #     ctrLine = '\r' + line.decode('utf-8').strip()
                #     sys.stdout.write(ctrLine.ljust(columns)[:columns])
                #     sys.stdout.flush()
            if not process_killed:
                # if wait:
                #     sys.stdout.write('\r'+' '*(columns-1))
                pass
            else:
                process.terminate()
                process.kill()
                returncode = 1
                #raise Exception('Process killed')
            _, stderr = process.communicate()
            returncode = process.returncode

    stdOut, stderr, returncode, process, startTime = [], None, None, None, time.perf_counter()
    process_killed = False
    execution_thread = threading.Thread(target=subprocess_execution)
    execution_thread.start()
    if wait:
        execution_thread.join(timeout)
    elapseTime = time.perf_counter() - startTime

    if not wait:
        returnDic = {'stdout': b'Not waiting', 'stderr': stderr, 'returncode': returncode}
    elif execution_thread.is_alive():
        process.terminate()
        process_killed = True
        execution_thread.join(1)  # Give the process some time to terminate gracefully
        if execution_thread.is_alive():
            process_killed = True
            process.kill()
            execution_thread.join(1)  # To ensure the thread is cleaned up
            
        returnDic = {'stdout': b''.join(stdOut), 'stderr': stderr, 'returncode': 1}
        returnDic['stdout'] = (returnDic['stdout'] or b'') + b'\nTimeout'
        returnDic['stderr'] = (returnDic['stderr'] or b'') + b'\nTimeout'
    else:
        returnDic = {'stdout': b''.join(stdOut), 'stderr': stderr, 'returncode': returncode}
    returnDic['elapsedTime'] = elapseTime
    return returnDic


def find_btrfs_mounts(filters):
    mounts = execute_command(["mount", "-t", "btrfs"])['stdout'].decode('utf-8').strip()
    btrfs_mounts = set()
    if mounts:
        if filters:
            filters = [f'*{filter}*' for filter in filters]
            mount_list = [line.split()[2] for line in mounts.split("\n")]
            for filter in filters:
                btrfs_mounts.update(fnmatch.filter(mount_list,filter))
        else:
            btrfs_mounts.update([line.split()[2] for line in mounts.split("\n")])
    return btrfs_mounts

def parse_show_info(info):
    fs_used = None
    device_path = None
    uuid = None
    for line in info.split("\n"):
        if "uuid:" in line:
            uuid = line.split("uuid:")[1].split()[0].strip()
        if "Total devices" in line:
            fs_used = line.split("FS bytes used")[1].strip()
        if "path" in line:
            device_path = line.split("path")[1].strip()
    if fs_used is None or device_path is None or uuid is None:
        print(f"{RED}Could not parse btrfs show info.{RESET}")
        print(f"Output from btrfs filesystem show was:\n{info}")
    return uuid, fs_used, device_path

def parse_device_stats(stats):
    err_dict = {}
    for line in stats.split("\n"):
        key, val = line.split()
        err_dict[key.split(".")[-1]] = val
    return err_dict

def color_error_count(error_count):
    if int(error_count) == 0:
        return f"{GREEN}{error_count}{RESET}"
    elif int(error_count) < 10:
        return f"{YELLOW}{error_count}{RESET}"
    else:
        return f"{RED}{error_count}{RESET}"

def parse_scrub_status(output):
    scrub_data = {}
    lines = output.strip().split("\n")
    if "no stats available" in output:
        scrub_data = {
            "scrub_status": "Never",
            "scrub_time": "N/A",
            "scrub_rate": "N/A",
            "scrubbed_data": "N/A",
            "error_summary": "N/A"
        }
    else:
        for line in lines:
            if "Status:" in line:
                scrub_data["scrub_status"] = line.split(":")[1].strip()
            elif "Scrub started:" in line:
                scrub_data["scrub_time"] = line.split(":")[1].strip()
            elif "Rate:" in line:
                scrub_data["scrub_rate"] = line.split(":")[1].strip()
            elif "Total to scrub:" in line and scrub_data.get("scrub_status") != "running":
                scrub_data["scrubbed_data"] = line.split(":")[1].strip()
            elif "Bytes scrubbed:" in line and scrub_data.get("scrub_status") == "running":
                scrub_data["scrubbed_data"] = line.split(":")[1].strip()
            elif "Error summary:" in line:
                err_idx = lines.index(line)
                error_text = "\n".join(lines[err_idx:])
                if "no errors found" in error_text.lower():
                    scrub_data["error_summary"] = f"{GREEN}OK{RESET}"  # Green-colored OK
                else:
                    scrub_data["error_summary"] = F"{RED}{error_text}{RESET}"

    return scrub_data

def issue_scrub_command(mounts):
    # print(f"{YELLOW}Issuing scrub on {mount}{RESET}")
    # execute_command(['bash','-c',f"btrfs scrub start {mount}"],wait=False)
    # limit the number of mounts to scrub to max_scrub_count
    scrubed_mounts = []
    for mount in mounts:
        print(f"{YELLOW}Issuing scrub on {mount}{RESET}")
        execute_command(['bash','-c',f"btrfs scrub start {mount}"],wait=False)
        scrubed_mounts.append(mount)
        yield scrubed_mounts
    return scrubed_mounts


def main():
    parser = argparse.ArgumentParser(description="Check Btrfs filesystem status.")
    parser.add_argument("-s", "--scrub", help="Issue scrub to all pools", action="store_true")
    parser.add_argument("-i", "--interval", help="Interval for status check in seconds", default=2, type=int)
    parser.add_argument("-m", "--max_scrub_count", help="Maximum number of scrubs to issue at the same time", default=32, type=int)
    parser.add_argument("--scrub_command_lockout", help="Lockout for scrub command. Used to block two commands sent quickly.", default=10, type=int)
    parser.add_argument('pattern',nargs='*',help='Patterns to filter btrfs moutns. Default="*"')
    parser.add_argument('-V', '--version', action='version', version="%(prog)s 0.16 stat btrfs by pan@zopyr.us")
    args = parser.parse_args()

    btrfs_mounts = set(find_btrfs_mounts(args.pattern))

    # If the scrub flag is enabled, issue the scrub command to all mounts
    if args.scrub:
        if args.max_scrub_count < 1:
            scrub_count = os.cpu_count()
        else:
            scrub_count = args.max_scrub_count
        if scrub_count > len(btrfs_mounts):
            scrub_count = len(btrfs_mounts)
        scrubber = issue_scrub_command(btrfs_mounts)
        for i in range(scrub_count):
            scrubed_mounts = next(scrubber)
        print(f'Issued scrub to {GREEN}{scrubed_mounts}{RESET} mounts')
        scrub_start_time = time.time()
        #print(f'{GREEN}Scrub all issued!{RESET}')
        time.sleep(args.interval)

    
    while True: 
        table = PrettyTable()

        table.field_names = ["Mount", "Path", "FS Used", "w_err", "r_err", "bit_rot", "gen_err",
                            "scrub_status", "scrub_time", "scrub_rate", "scrubbed_data", "error_summary"]

        if not btrfs_mounts:
            print(f"{RED}No Btrfs mounts found.{RESET}")
            return

        for mount in btrfs_mounts:
            mount_dir_name = mount.split("/")[-1]
            
            filesystem_show = execute_command(["btrfs", "filesystem", "show", mount])['stdout'].decode('utf-8').strip()
            uuid, fs_used, device_path = parse_show_info(filesystem_show)

            if uuid is None or fs_used is None or device_path is None:
                print(f"{RED}Could not fetch complete info for {mount}. Skipping...{RESET}")
                continue

            device_stats = execute_command(["btrfs", "device", "stats", mount])['stdout'].decode('utf-8').strip()
            err_dict = parse_device_stats(device_stats)

            scrub_output = execute_command(["btrfs", "scrub", "status", device_path])['stdout'].decode('utf-8').strip()
            scrub_data = parse_scrub_status(scrub_output)

            table.add_row([
                mount_dir_name,
                device_path,
                fs_used,
                color_error_count(err_dict['write_io_errs']),
                color_error_count(err_dict['read_io_errs']),
                color_error_count(err_dict['corruption_errs']),
                color_error_count(err_dict['generation_errs']),
                scrub_data["scrub_status"],
                scrub_data["scrub_time"],
                scrub_data["scrub_rate"],
                scrub_data["scrubbed_data"],
                scrub_data["error_summary"]
            ])

        print(table)


        if not args.scrub:
            break

        # Check if all scrubs are finished.
        scrub_status_idx = table.field_names.index("scrub_status")
        running_scrubs = [row[scrub_status_idx] == "running" for row in table._rows]
        # issue scrub command to next mount if there are less than max_scrub_count scrubs running
        if sum(running_scrubs) < scrub_count and time.time() - scrub_start_time > args.scrub_command_lockout and len(scrubed_mounts) < len(btrfs_mounts):
            scrubed_mounts = next(scrubber)
            # print(f'Issued scrub to {GREEN}{scrubed_mounts}{RESET} mounts')
            print(f"{GREEN}Scrubed issued to {scrubed_mounts}.{RESET}")
            scrub_start_time = time.time()

        if sum(running_scrubs) == 0 and time.time() - scrub_start_time > args.scrub_command_lockout:
            print(f"{GREEN}All Scrubs finished.{RESET}")
            break

        time.sleep(args.interval)

if __name__ == "__main__":
    main()

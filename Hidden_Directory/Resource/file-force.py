#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from typing import List, Set
from urllib.parse import urljoin

import requests

DEFAULT_BASE_URL = "http://x.x.x.x/.hidden/"

MIN_FLAG_LENGTH = 20

README_CANDIDATES = ("readme", "readme.txt", "readme.md")


class DirectoryIndexParser(HTMLParser):
    """Apache/Nginx auto-index çıktısından bağlantıları toplar."""

    def __init__(self) -> None:
        super().__init__()
        self.links: List[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def is_readme(href: str) -> bool:
    """Bağlantının README dosyasına işaret edip etmediğini kontrol eder."""
    lowered = href.lower().strip("/")
    return any(lowered == candidate for candidate in README_CANDIDATES)


def is_directory(href: str) -> bool:
    """Apache listing'inde klasörler genelde slash ile biter."""
    return href.endswith("/")


def should_skip(href: str) -> bool:
    """Gereksiz bağlantıları (üst dizin vb.) ele."""
    return (
        href.startswith("?")
        or href.startswith("#")
        or href in ("/", "../", "./")
        or "?" in href
    )


def fetch_links(url: str) -> List[str]:
    """Bir dizin sayfasındaki href'leri döndürür."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"[WARN] {url} alınamadı: {exc}")
        return []

    parser = DirectoryIndexParser()
    parser.feed(resp.text)
    return parser.links


def fetch_flag(url: str, min_length: int) -> str | None:
    """README dosyasını indirip flag pattern'i arar."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"[WARN] README indirilemedi ({url}): {exc}")
        return None

    text = resp.text
    flag_regex = re.compile(rf"[A-Za-z0-9_{{}}-]{{{min_length},}}")
    match = flag_regex.search(text)
    if match:
        return match.group()
    return None


def crawl_hidden(base_url: str, min_length: int) -> tuple[str, str] | None:
    """`.hidden` ağacında README arar, flag bulursa (flag, url) tuple'ı döner."""
    stack: List[str] = []
    seen: Set[str] = set()

    normalized_base = base_url if base_url.endswith("/") else base_url + "/"
    stack.append(normalized_base)

    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)

        links = fetch_links(current)
        if not links:
            continue

        for href in links:
            if should_skip(href):
                continue

            absolute = urljoin(current, href)

            if is_readme(href):
                print(f"[+] README bulundu: {absolute}")
                flag = fetch_flag(absolute, min_length)
                if flag:
                    return (flag, absolute)
            elif is_directory(href):
                stack.append(absolute)

    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="`.hidden/` altındaki README dosyalarını tarar ve flag bulursa brute force'u durdurur."
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Taranacak temel URL (varsayılan: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--min-length",
        type=int,
        default=MIN_FLAG_LENGTH,
        help=f"Flag olarak kabul edilecek minimum uzunluk (varsayılan: {MIN_FLAG_LENGTH})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    min_length = max(args.min_length, 1)

    print(f"[*] Taramaya başlanıyor: {args.base_url}")
    print(f"[*] Minimum flag uzunluğu: {min_length}")

    result = crawl_hidden(args.base_url, min_length)
    if result:
        flag, file_url = result
        print("\n[!] FLAG BULUNDU!")
        print(f"    Dosya yolu: {file_url}")
        print(f"    Flag: {flag}")
        print("[-] Brute force işlemini durdurabilirsiniz.")
        return 0

    print("\n[×] Flag bulunamadı, brute force devam edebilir.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
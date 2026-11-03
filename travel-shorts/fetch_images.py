#!/usr/bin/env python3
"""spec.json 의 "images" 항목을 내려받아 <project>/images/ 에 저장하고 credits.json 을 만든다.

지원하는 이미지 소스
  {"commons": "File:Some photo.jpg"}   위키미디어 공용(CC 라이선스) — 저작자/라이선스 자동 기록
  {"url": "https://..."}               직접 URL (본인에게 사용 권한이 있는 사진만!)
  {"path": "my_photos/room.jpg"}       로컬 파일 (프로젝트 폴더 기준 상대경로)
"""
import json
import shutil
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "TravelShortsBuilder/1.0 (https://github.com/mr6200/ai-idea)"
API = "https://en.wikipedia.org/w/api.php"  # 공용(commons) 파일도 조회됨
THUMB_WIDTH = 3840  # 위키미디어 표준 썸네일 크기(비표준 크기는 429 차단)


def http_get(url, retries=8):
    delay = 10
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < retries - 1:
                print(f"  rate limited, {delay}s 후 재시도")
                time.sleep(min(delay, 120))
                delay *= 2
                continue
            raise


def save_resized(data, dest, max_side=3840):
    """원본을 받아 긴 변 max_side 이하 JPEG 로 저장 (EXIF 회전 반영)."""
    import io
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(dest, "JPEG", quality=92)


def strip_html(s):
    import re
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def commons_info(titles):
    out = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "imageinfo",
            "titles": "|".join(chunk), "iiprop": "url|size|extmetadata",
            "iiurlwidth": THUMB_WIDTH,
            "iiextmetadatafilter": "LicenseShortName|Artist|LicenseUrl",
        })
        data = json.loads(http_get(f"{API}?{q}"))
        norm = {n["to"]: n["from"] for n in data["query"].get("normalized", [])}
        for p in data["query"]["pages"].values():
            if "imageinfo" not in p:
                print(f"  ! 찾을 수 없음: {p['title']}")
                continue
            ii = p["imageinfo"][0]
            m = ii.get("extmetadata", {})
            out[norm.get(p["title"], p["title"])] = {
                "url": ii["url"],  # 원본 (썸네일 생성 요청은 rate limit 이 엄격함)
                "page": ii["descriptionurl"],
                "artist": strip_html(m.get("Artist", {}).get("value")),
                "license": m.get("LicenseShortName", {}).get("value", ""),
                "license_url": m.get("LicenseUrl", {}).get("value", ""),
            }
    return out


def main(project_dir):
    proj = Path(project_dir)
    spec = json.loads((proj / "spec.json").read_text(encoding="utf-8"))
    img_dir = proj / "images"
    img_dir.mkdir(exist_ok=True)
    images = spec["images"]

    commons = [v["commons"] for v in images.values() if "commons" in v]
    info = commons_info(commons) if commons else {}

    credits = []
    for key, src in images.items():
        dest = img_dir / f"{key}.jpg"
        if "commons" in src:
            meta = info.get(src["commons"])
            if not meta:
                continue
            credits.append({"key": key, "title": src["commons"][5:], **meta})
            url = meta["url"]
        elif "url" in src:
            url = src["url"]
            credits.append({"key": key, "title": key, "page": url,
                            "artist": src.get("credit", ""), "license": src.get("license", "")})
        else:
            shutil.copy(proj / src["path"], dest)
            if src.get("credit"):
                credits.append({"key": key, "title": key, "artist": src["credit"],
                                "license": src.get("license", ""), "page": ""})
            print(f"  copied {key}")
            continue
        if dest.exists() and dest.stat().st_size > 0:
            print(f"  cached {key}")
            continue
        save_resized(http_get(url), dest)
        print(f"  downloaded {key}")
        time.sleep(2)

    (proj / "credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"완료: {len(images)}장, credits.json 저장")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python fetch_images.py projects/<name>")
    main(sys.argv[1])

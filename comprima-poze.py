#!/usr/bin/env python3
"""
Comprimă toate pozele din img/ — păstrează originalele în img/backup-original/
JPG: redus la max 1200px lățime, calitate 82
PNG: convertit la JPG dacă nu are transparență, altfel optimizat
"""
import os
import shutil
from pathlib import Path
from PIL import Image

IMG_DIR = Path(__file__).parent / "img"
BACKUP_DIR = IMG_DIR / "backup-original"
MAX_WIDTH = 1200   # pixeli
JPEG_QUALITY = 82  # 0-100

BACKUP_DIR.mkdir(exist_ok=True)

extensions = {".jpg", ".jpeg", ".png", ".webp"}
files = sorted([f for f in IMG_DIR.iterdir() if f.suffix.lower() in extensions and f.is_file()])

total_before = 0
total_after = 0
processed = 0
skipped = 0

print(f"\nGasit {len(files)} imagini in img/\n")
print(f"{'Fisier':<55} {'Inainte':>8} {'Dupa':>8} {'Reducere':>9}")
print("-" * 85)

for f in files:
    size_before = f.stat().st_size
    total_before += size_before

    # Backup original
    backup_path = BACKUP_DIR / f.name
    if not backup_path.exists():
        shutil.copy2(f, backup_path)

    try:
        img = Image.open(f)
        orig_format = img.format
        orig_mode = img.mode

        # Redimensionare daca e prea lata
        w, h = img.size
        if w > MAX_WIDTH:
            ratio = MAX_WIDTH / w
            new_h = int(h * ratio)
            img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

        # Salveaza
        if f.suffix.lower() == ".png":
            # Verifica transparenta
            has_alpha = (orig_mode in ("RGBA", "LA") or
                        (orig_mode == "P" and "transparency" in img.info))
            if has_alpha:
                # Pastreaza PNG dar optimizat
                img.save(f, "PNG", optimize=True)
            else:
                # Converteste la JPG
                if img.mode != "RGB":
                    img = img.convert("RGB")
                new_path = f.with_suffix(".jpg")
                img.save(new_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
                if new_path != f:
                    f.unlink()  # sterge PNG-ul vechi
                    f = new_path
        else:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(f, "JPEG", quality=JPEG_QUALITY, optimize=True)

        size_after = f.stat().st_size
        total_after += size_after
        reducere = (1 - size_after / size_before) * 100
        print(f"{f.name:<55} {size_before/1024:>6.0f}KB {size_after/1024:>6.0f}KB {reducere:>8.0f}%")
        processed += 1

    except Exception as e:
        print(f"{f.name:<55} EROARE: {e}")
        skipped += 1

print("-" * 85)
print(f"\n✅ Procesate: {processed} | Sarite: {skipped}")
print(f"📦 Total inainte:  {total_before/1024/1024:.1f} MB")
print(f"📦 Total dupa:     {total_after/1024/1024:.1f} MB")
print(f"💾 Spatiu eliberat: {(total_before-total_after)/1024/1024:.1f} MB ({(1-total_after/total_before)*100:.0f}% reducere)")
print(f"\n📁 Originalele sunt salvate in: img/backup-original/")
print("   Sterge acel folder dupa ce verifici ca totul arata bine pe site.\n")

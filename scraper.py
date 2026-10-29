import json
from pathlib import Path

import yt_dlp

channel = "https://www.youtube.com/@RightMoveRX/videos"

def get_channel_videos(channel_url):
    """
    Scrape video details from a YouTube channel.

    Args:
        channel_url (str): YouTube channel URL

    Returns:
        list: Videos with id, name, link, description, and tags fields
    """

    # Make sure we're looking at the Videos tab
    if not channel_url.endswith("/videos"):
        channel_url = channel_url.rstrip("/") + "/videos"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "skip_download": True,
    }

    videos = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Scraping channel:")
        print(channel_url)
        print()

        info = ydl.extract_info(channel_url, download=False)

        if not info:
            print("Could not retrieve channel information.")
            return []

        entries = info.get("entries", [])

        for entry in entries:
            if not entry:
                continue

            video_id = entry.get("id")

            if video_id:
                videos.append({
                    "id": len(videos),
                    "name": entry.get("title") or video_id,
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                    "description": entry.get("description") or "",
                    "tags": entry.get("tags") or [],
                })

    return videos


if __name__ == "__main__":

    # GitHub Actions can override this setting.
    channel_url = os.getenv(
        "YOUTUBE_CHANNEL_URL",
        "https://www.youtube.com/@RightMoveRX/videos"
    )

    videos = get_channel_videos(channel_url)
    output_path = Path(__file__).with_name("videos.json")

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(videos, output_file, indent=4, ensure_ascii=False)

    print()
    print(f"Found {len(videos)} videos")
    print(f"Saved to {output_path}")
    print("=" * 60)

    for video in videos:
        print(video["link"])

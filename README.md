# 📥 Facebook Video & Audio Downloader Tool (Termux Version)

A powerful and user-friendly terminal-based tool for downloading videos, audio, and metadata from Facebook using `yt-dlp`. This tool is optimized for **Termux** and includes interactive features, support for multi-links, and filename sanitization to avoid long filename errors.

---

## 🔧 Features

✅ Download HD video with merged audio  
✅ Extract and save video title or description separately  
✅ Download only the audio in MP3 format  
✅ Process multiple links at once  
✅ Automatically sanitize filenames to avoid file system errors  
✅ Interactive format selection for Facebook  
✅ Text-based UI with clear instructions

---

## 🚀 Getting Started

### 📥 Installation (Termux)

```bash
pkg update && pkg install python git ffmpeg yt-dlp -y
git clone https://github.com/MasHunterOfficial/fb
cd fb
chmod +x fb.py
mv fb.py fb
mv fb /data/data/com.termux/files/usr/bin/
````

### ✅ Usage

Once installed, simply run the tool from anywhere in Termux:

```bash
fb
```

Follow the on-screen instructions to:

* Enter one or more Facebook video links
* Choose to download video, audio, or just metadata
* Select specific format combinations if needed (e.g., `hd+videoidv`)

---

## 📂 Output Files

Downloaded files will be saved with:

* Sanitized titles (to avoid file name too long errors)
* `.mp4` extension for videos
* `.mp3` for audio-only files
* `_title.txt`, `_desc.txt`, or `_info.txt` for metadata

---

## 🛠️ Dependencies

Ensure these packages are installed in your Termux:

```bash
pkg install ffmpeg yt-dlp python -y
```

---

## ❗ Important Notes

* Works best with public Facebook videos.
* Make sure your Termux has permission to access storage if you're saving files outside.
* For format selection, use combinations like: `hd+1246662600449605v`
* Avoid Facebook's private/group video links due to limited support.

---

## 📌 Example

```
Enter Facebook link(s) separated by commas:
https://m.facebook.com/story.php?story_fbid=123456&id=78910

Available formats:

Note: For Facebook videos, combine video ID (ends with 'v') with audio ID (ends with 'a')
Example: hd+1029575365767579a

Enter format combination:
hd+1029575365767579a
```

---

## 🤝 Author

**Tool by:** [MasHunterOfficial](https://github.com/MasHunterOfficial)
📁 Repository: [https://github.com/MasHunterOfficial/fb](https://github.com/MasHunterOfficial/fb)

---

## 📜 License

This project is licensed under the MIT License.

```

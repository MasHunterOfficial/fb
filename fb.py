import re
import subprocess
import json
import os
from typing import List, Optional

class FacebookDownloader:
    @staticmethod
    def get_links() -> List[str]:
        """Get and validate Facebook links from user input."""
        while True:
            links = input("\nEnter Facebook link(s) separated by commas: ").split(',')
            valid_links = [
                link.strip() for link in links 
                if re.match(r'https?://(www\.|m\.|web\.)?facebook\.com/', link.strip())
            ]
            if valid_links:
                return valid_links
            print("Error: No valid Facebook links found. Please enter valid URLs starting with http:// or https://")

    @staticmethod
    def sanitize_filename(text: str, max_length: int = 80) -> str:
        """Sanitize text to be used as a filename."""
        # Replace special characters and truncate
        text = re.sub(r'[\\/*?:"<>|]', "_", text)
        text = re.sub(r'\s+', ' ', text).strip()
        # Ensure the filename isn't empty after sanitization
        if not text:
            text = "facebook_video"
        return text[:max_length]

    def get_video_info(self, url: str) -> Optional[dict]:
        """Get video metadata using yt-dlp."""
        cmd = [
            'yt-dlp', 
            '--dump-json',
            '--no-warnings',
            '--no-check-certificates',
            url
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"\nError getting video info: {e.stderr}")
            return None
        except json.JSONDecodeError:
            print("\nError: Failed to parse video information")
            return None
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
            return None

    def download_video_audio(self, url: str) -> None:
        """Download Facebook video with combined audio."""
        print(f"\n[Downloading video with audio] => {url}")
        
        # Get available formats
        print("\nAvailable formats:\n")
        subprocess.run(["yt-dlp", "-F", url], check=False)
        
        print("\nNote: For Facebook videos, combine video ID (ends with 'v') with audio ID (ends with 'a')")
        print("Example: 'hd+1029575365767579a'")
        
        selected_format = input("\nEnter format combination: ").strip()
        
        try:
            info = self.get_video_info(url)
            if not info:
                return

            title = self.sanitize_filename(info.get('title', 'facebook_video'))
            output_template = f"{title}.%(ext)s"
            
            subprocess.run([
                "yt-dlp",
                "-f", selected_format,
                "--no-check-certificates",
                "--console-title",
                "--merge-output-format", "mp4",
                "-o", output_template,
                url
            ], check=True)
            print("\nDownload completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"\nError downloading video: {e.stderr}")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")

    def save_title_to_file(self, title: str, url: str) -> None:
        """Save title to a text file."""
        filename = self.sanitize_filename(title[:50]) + "_title.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n")
                f.write(f"URL: {url}\n")
            print(f"\nTitle saved successfully as: {filename}")
        except Exception as e:
            print(f"\nError saving title: {str(e)}")

    def save_description_to_file(self, description: str, url: str) -> None:
        """Save description to a text file."""
        filename = self.sanitize_filename(description[:30].strip() if description else "no_description") + "_desc.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n\n")
                f.write("Description:\n")
                f.write(description or "No description available")
            print(f"\nDescription saved successfully as: {filename}")
        except Exception as e:
            print(f"\nError saving description: {str(e)}")

    def download_title_description(self, url: str) -> None:
        """Download video title and description to a text file."""
        info = self.get_video_info(url)
        if not info:
            return

        title = info.get('title', 'no_title')
        description = info.get('description', 'No description available')
        
        filename = self.sanitize_filename(title[:50]) + "_info.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n")
                f.write(f"URL: {url}\n")
                f.write("\nDescription:\n")
                f.write(description)
            print(f"\nSaved title and description to: {filename}")
        except Exception as e:
            print(f"\nError saving file: {str(e)}")

    def download_audio(self, url: str) -> None:
        """Download only audio from Facebook video."""
        print(f"\n[Downloading audio only] => {url}")
        
        try:
            info = self.get_video_info(url)
            if not info:
                return

            title = self.sanitize_filename(info.get('title', 'facebook_audio'))
            output_template = f"{title}.%(ext)s"
            
            subprocess.run([
                "yt-dlp",
                "-f", "bestaudio",
                "-x",
                "--audio-format", "mp3",
                "--no-check-certificates",
                "--console-title",
                "-o", output_template,
                url
            ], check=True)
            print("\nAudio download completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"\nError downloading audio: {e.stderr}")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")

    def multi_download(self, urls: List[str], download_type: str) -> None:
        """Handle multiple links download based on type."""
        for i, url in enumerate(urls, 1):
            print(f"\nProcessing ({i}/{len(urls)}): {url}")
            try:
                if download_type == "video":
                    self.download_video_audio(url)
                elif download_type == "title":
                    info = self.get_video_info(url)
                    if info:
                        title = info.get('title', 'No title available')
                        print(f"\nTitle: {title}")
                        self.save_title_to_file(title, url)
                elif download_type == "description":
                    info = self.get_video_info(url)
                    if info:
                        description = info.get('description', 'No description available')
                        print(f"\nDescription: {description[:200]}...")  # Show preview
                        self.save_description_to_file(description, url)
                elif download_type == "audio":
                    self.download_audio(url)
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                continue

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    downloader = FacebookDownloader()
    
    while True:
        clear_screen()
        print("\n" + "="*40)
        print("Facebook Downloader Tool")
        print("="*40)
        print("Combo:")
        print(" 1. Download video with audio")
        print(" 2. Download title + description")
        print("Single:")
        print(" 3. Only title (save to file)")
        print(" 4. Only audio")
        print(" 5. Only description (save to file)")
        print("Multi:")
        print(" 6. Multi-link video+audio download")
        print(" 7. Multi-link only titles (save to files)")
        print(" 8. Multi-link only descriptions (save to files)")
        print(" 9. Multi-link only audio")
        print("="*40)
        print(" 0. Exit")
        print("="*40)
        
        try:
            choice = input("Enter your choice (0-9): ").strip()
            if choice == '0':
                print("\nExiting program...")
                break
                
            choice = int(choice)
            if choice not in range(1, 10):
                raise ValueError
        except ValueError:
            input("\nInvalid choice! Please enter a number between 0-9\nPress Enter to continue...")
            continue
        
        try:
            if choice in [1, 2, 3, 4, 5]:
                links = downloader.get_links()
                if not links:
                    continue
                    
                if choice == 1:
                    downloader.download_video_audio(links[0])
                elif choice == 2:
                    downloader.download_title_description(links[0])
                elif choice == 3:
                    info = downloader.get_video_info(links[0])
                    if info:
                        title = info.get('title', 'No title available')
                        print(f"\nTitle: {title}")
                        downloader.save_title_to_file(title, links[0])
                elif choice == 4:
                    downloader.download_audio(links[0])
                elif choice == 5:
                    info = downloader.get_video_info(links[0])
                    if info:
                        description = info.get('description', 'No description available')
                        print(f"\nDescription: {description[:200]}...")  # Show preview
                        downloader.save_description_to_file(description, links[0])
                    
            elif choice in [6, 7, 8, 9]:
                links = downloader.get_links()
                if not links:
                    continue
                    
                if choice == 6:
                    downloader.multi_download(links, "video")
                elif choice == 7:
                    downloader.multi_download(links, "title")
                elif choice == 8:
                    downloader.multi_download(links, "description")
                elif choice == 9:
                    downloader.multi_download(links, "audio")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

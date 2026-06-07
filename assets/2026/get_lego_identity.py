#!/usr/bin/env python3
"""
Create a screen recording of the Lego website age picker.

Used in https://alexwlchan.net/2026/record-browser-video/
"""

import base64
import time

from playwright.sync_api import sync_playwright


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            ignore_default_args=["--mute-audio"],
        )

        context = browser.new_context(
            viewport={"width": 760, "height": 700}, device_scale_factor=2
        )

        page = context.new_page()
        page.goto("https://identity.lego.com/en-GB/age")

        # Click the page once to grant "user activation" required by media APIs
        page.click("body")

        page.evaluate("""
            async () => {
                window.captureStream = await navigator.mediaDevices.getDisplayMedia({
                    video: {displaySurface: "browser"},
                    audio: true,
                    preferCurrentTab: true
                });
                
                window.mediaRecorder = new MediaRecorder(window.captureStream, { 
                    mimeType: 'video/mp4' 
                });
                
                window.videoChunks = [];
                window.mediaRecorder.ondataavailable = (e) => {
                    if (e.data.size > 0) window.videoChunks.push(e.data);
                };
                
                window.mediaRecorder.start();
            }
        """)
        time.sleep(5)

        page.keyboard.press("1")
        time.sleep(2)
        page.keyboard.press("Backspace")

        time.sleep(2)

        for charseq in (
            "1932",
            "1947",
            "1958",
            "2026",
        ):
            page.keyboard.press(charseq[0])
            time.sleep(0.5)
            page.keyboard.press(charseq[1])
            time.sleep(0.5)
            page.keyboard.press(charseq[2])
            time.sleep(0.5)
            page.keyboard.press(charseq[3])

            time.sleep(2)

            for _ in range(4):
                page.keyboard.press("Backspace")
                time.sleep(0.25)

        base64_video_data = page.evaluate("""
            async () => {
                return new Promise((resolve) => {
                    window.mediaRecorder.onstop = () => {
                        const blob = new Blob(
                            window.videoChunks, { type: 'video/mp4' });
                        const reader = new FileReader();
                        reader.readAsDataURL(blob);
                        reader.onloadend = () => {
                            // Strip out the "data:video/mp4;base64," prefix
                            resolve(reader.result.split(',')[1]);
                        };
                    };
        
                    window.mediaRecorder.stop();
                    window.captureStream.getTracks().forEach(track => track.stop());
                });
            }
        """)

        with open("lego.mp4", "wb") as f:
            f.write(base64.b64decode(base64_video_data))

        context.close()
        browser.close()

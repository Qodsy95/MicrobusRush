# ميكروباص راش — Microbus Rush (Android)

The full game runs offline inside the app. GitHub builds the APK for you automatically — no Android Studio needed.

## Get the APK (about 10 minutes, once)

1. **Make a free GitHub account** at github.com (skip if you have one).
2. **Create a repository**: click **+ → New repository**, name it `MicrobusRush`, choose **Public**, then **Create repository**.
3. **Upload the project**: on the new repo page click **uploading an existing file**, then drag **everything inside** the unzipped `MicrobusRush` folder into the page (the `app` and `.github` folders plus `build.gradle`, `settings.gradle`, `gradle.properties` and `README.md`). Click **Commit changes**.
   - ⚠️ The `.github` folder is hidden on some computers. If it doesn't upload, click **Add file → Create new file**, type the name `.github/workflows/build-apk.yml`, paste in the contents of that file from the zip, and click **Commit changes**.
4. **Wait for the build**: open the **Actions** tab — "Build Android APK" runs by itself (≈ 5 minutes). A green ✓ means it's done.
5. **Your download link** is now ready and never changes:

   `https://github.com/YOUR-USERNAME/MicrobusRush/releases/latest/download/MicrobusRush.apk`

   (You'll also find it under **Releases** on the right side of the repo page.)

## Install on the phone

1. Open the link on your Android phone and download `MicrobusRush.apk`.
2. Tap the downloaded file. If Android asks, allow **Install unknown apps** for your browser.
3. Tap **Install** → the "ميكروباص راش" icon appears on your home screen.

> Android may show a "Play Protect" warning because the app isn't from the Play Store — tap **Install anyway**.

## Updating the game later

Replace `app/src/main/assets/index.html` in the repo with the new game file (Add file → Upload files) and commit. GitHub builds a new APK automatically, and the same download link always gives the latest version. Before uploading an update, raise `versionCode` in `app/build.gradle` (1 → 2 → 3 …) so phones install it over the old one.

## What's inside

| Path | What it is |
|---|---|
| `app/src/main/assets/index.html` | The game itself |
| `app/src/main/java/.../MainActivity.java` | Full-screen, portrait WebView that runs the game (sound on, screen stays awake, auto-pause in background) |
| `app/src/main/res/mipmap-*/ic_launcher.png` | App icon |
| `.github/workflows/build-apk.yml` | Builds the APK on GitHub and publishes the download link |

Package name `com.microbusrush.game` · Android 7.0+ · The APK is signed with a standard debug key, which is fine for sharing with friends. Publishing on Google Play needs your own signing key and an Android App Bundle (`gradle bundleRelease`).

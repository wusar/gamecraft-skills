# Production reference — gamecraft-video

Operational detail for trailers, skill explainers, and short videos. Scoped to making video; not watching or building the game.

## 1. Brief template (fill fast, default hard)

| Field | Known / assumed | Default if unknown |
|---|---|---|
| Objective | | explain one mechanic clearly |
| Audience | | new players |
| Aspect ratio | | 9:16 short, 16:9 trailer |
| Duration | | 30–60 s |
| Language | | user's language |
| CTA | | follow / wishlist / try demo |
| Route per shot | | route 2 (motion graphics) |

Keep the shot list to 3–8 entries for a short. One line per shot: id, route, seconds, subject, action, camera, on-screen text.

## 2. Route selection

- **Route 1 — actual gameplay capture.** Needs the running game. Record at target fps/resolution; avoid HUD overlap with captions. If you composite, re-time, or fake frames, disclose it.
- **Route 2 — deterministic motion graphics + TTS.** A suitable default for explainers. Built in code/editor from frame or time. Reproducible. Explicit gameplay/model-video requests retain their requested route until the user chooses otherwise.
- **Route 3 — model-generated shots.** Only after verifying a model is available and its current limits from official docs (they change). Generated = illustration, not gameplay. One subject/action/camera per shot; short takes.

Record the route in the manifest per shot. Generated shots must not be presented as gameplay anywhere.

## 3. Visual consistency kit

- Palette tokens (hex), one display font + one body font (licence-checked).
- Logo/wordmark with min clear space.
- HUD/UI style sheet if gameplay UI appears.
- Character reference sheet: front/side, key colour, silhouette, scale. Re-check identity per shot when a model is involved.
- Store refs under a `refs/` folder with exact paths.

## 4. Compose text in the renderer

Render titles, captions, and any exact UI (buttons, menus, damage numbers) in the editor/renderer with real fonts. Do not rely on a video model's text rendering — it warps, misspells, and cannot guarantee UI fidelity.

## 5. Audio

- Narration foreground; music ducked ~6–12 dB under speech; SFX spot hits.
- Normalise loudness (target roughly −14 LUFS integrated for web; confirm to the platform's current spec).
- Synthetic TTS: pick a stock voice, disclose it as synthetic where it could be mistaken for a human. **Do not clone a voice without explicit recorded consent.**

## 6. Captions

- Burn-in or sidecar (SRT/VTT) matching the manifest timings.
- Safe margins: keep text within ~8–10% from edges; avoid the platform's bottom UI and right-side action rail on vertical video.
- High contrast, min ~28 px cap height at 1080-wide; test on a phone-size preview.

## 7. Renderers — reuse, don't install

Use whatever the host already has. Verify before assuming; do not install a whole stack.

- **Canvas / FFmpeg** — draw frames or filter graphs, mux audio, encode. Good for low-dependency motion graphics.
- **Remotion** — React/TS frame-driven video, deterministic by frame. Official docs routes for AI coding agents: https://www.remotion.dev/docs/ai/coding-agents and https://www.remotion.dev/docs/ai/skills — cite as reference only; these link to docs, they are **not** evidence a local Remotion install exists.
- **Existing editor** (user's NLE) — assemble takes there; export and validate.

Determinism: seed any randomness; drive all motion from frame index or timestamp.

## 8. Manifest schema (JSON)

```json
{
  "project": "skill-explain-health-regen",
  "route_summary": "route2",
  "aspect_ratio": "9:16",
  "resolution": [1080, 1920],
  "fps": 30,
  "duration_s": 42.0,
  "voice": {"type": "tts", "name": "stock-voice-A", "cloned": false, "consent": "n/a"},
  "shots": [
    {"id": "s1", "route": "route2", "start_s": 0.0, "end_s": 6.0,
     "subject": "heal icon", "action": "pulses", "camera": "static",
     "assets": ["refs/palette.json", "assets/icons/heal.svg"],
     "caption": "Health regenerates out of combat."},
    {"id": "s2", "route": "route1", "start_s": 6.0, "end_s": 14.0,
     "subject": "gameplay clip", "assets": ["captures/clip_heal_01.mp4"],
     "caption": "In-game: regen after 5s."}
  ],
  "cta": {"text": "Wishlist on store page", "start_s": 38.0, "end_s": 42.0},
  "licenses": [{"asset": "assets/music/loop.mp3", "license": "CC-BY-4.0", "source": "..."}]
}
```

Every asset path is exact and relative to the project root for reproducibility.

## 9. Validation commands (adapt to host)

- Probe: `ffprobe -v error -show_entries format=duration,size:stream=codec_type,width,height,r_frame_rate -of json out.mp4`
- Full decode: `ffmpeg -v error -i out.mp4 -f null -` (must exit clean).
- Audio present: check for an audio stream and measure loudness (`ffmpeg -i out.mp4 -af loudnorm=print_format=summary -f null -`).
- Frame grabs: export frames at start, middle, end and inspect visually.
- Compare manifest duration/resolution to probe output.

Checklist: duration, resolution, audio present, full decode clean, start/middle/end frames, captions in safe zone and correctly timed, closing CTA readable, route disclosure and licences recorded.

## 10. Licences and integrity

- Music, SFX, fonts, images, footage: record licence + source per asset.
- Do not mirror third-party full videos; use only licensed or owned material.
- Do not misrepresent generated or stock footage as gameplay.
- No misleading benchmark or cost claims in narration or copy.

## 11. Known vs assumed at handoff

State which fields were defaults you picked, which assets exist, which model (if any) was actually available, and the honest label of the actual deliverable. For this repository's intro: "AI-assisted code-animation + synthetic-narration explainer."

## 12. Pitfalls

- Long single generation instead of short takes → drifts and low control.
- Baked-in model text → typos and wrong UI; compose text in renderer.
- Assuming Remotion or a video model is installed → verify first.
- Cloned voice without recorded consent → do not.
- Captions under the platform UI → unreadable.
- Claiming text-to-video success when none was used → dishonest. For a suitable explainer brief use the labelled graphics route; for an explicit text-to-video request preserve the target and resolve the missing service or input.

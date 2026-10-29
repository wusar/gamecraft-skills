# Engines reference — gamecraft-video

Purpose: verify and choose a renderer without inventing or installing tools. Reuse what the host has.

## 1. Availability probe (do first)

Check for anything already present before planning a pipeline:

- `ffmpeg -version` / `ffprobe -version`
- Node version and existing package.json/lockfile for Remotion; avoid npx probes that may download a missing package.
- Local editor presence (DaVinci, Premiere, etc.) — ask or inspect, don't assume
- Image/video model access: verify an endpoint/CLI/session actually exists; read current official limits (change often) from the vendor's own docs.

If a component is missing, do not silently install. Either adapt to what exists or report the gap.

## 2. Engine comparison

| Engine | Determinism | Fit | Notes |
|---|---|---|---|
| Canvas + FFmpeg | High (frame/time) | Motion graphics, captions, mux | Low dependency; manual layout |
| Remotion | High (frame index) | React-driven scenes, data-driven shots | Official agent routes: https://www.remotion.dev/docs/ai/coding-agents , https://www.remotion.dev/docs/ai/skills — docs pointers only, not proof of local install |
| Existing NLE | Manual | Assemble takes, final mix/export | Reproducibility depends on project discipline; keep manifest |
| Image/video model | Low | Route 3 illustration shots | Verify access + current limits; label generated |

## 3. Choosing by route

- Route 1 gameplay: capture tool → NLE or FFmpeg assembly; disclose composites.
- Route 2 explainer: Canvas/FFmpeg or Remotion; TTS to WAV/MP3; captions from manifest.
- Route 3 model shots: keep short, one action each; assemble in NLE/FFmpeg; mark as generated; never label gameplay.

## 4. Determinism rules

- Drive motion by frame index or timestamp, never wall-clock randomness; seed any RNG.
- Pin fps, resolution, duration in the manifest; assert against probe output.
- Reference assets by exact relative paths.

## 5. Guardrails

- No installing a full stack when one component suffices.
- Cite official docs to check current limits; do not fabricate capabilities.
- No benchmark or cost claims without a cited, measured source.
- If only Route 2 is available, use it for suitable explainer requests and disclose it. If the user explicitly requested gameplay capture or model video, preserve that target; prepare independent storyboard/project work and obtain the missing input instead of silently substituting.

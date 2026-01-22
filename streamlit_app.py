import os
import shutil
import subprocess
from pathlib import Path

import streamlit as st
import sys

# Use wide layout to reduce side margins
st.set_page_config(page_title="ppt-auto-vo", layout="wide")


ROOT = Path(__file__).parent
INPUT_DIR = ROOT / "input"
OUTPUT_DIR = ROOT / "output"
TEMP_DIR = ROOT / "temp"


def ensure_dirs():
    for d in (INPUT_DIR, OUTPUT_DIR, TEMP_DIR):
        d.mkdir(parents=True, exist_ok=True)


def list_input_files():
    return [f.name for f in sorted(INPUT_DIR.glob("*.*")) if f.suffix.lower() in (".pdf", ".pptx")]


def save_uploaded(uploaded_file):
    dest = INPUT_DIR / uploaded_file.name
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return dest.name


def run_pipeline(filename: str, language: str, clean: bool):
    cmd = [sys.executable, "-u", str(ROOT / "pptx_to_video.py"), "--file", filename, "--output", "output", "--language", language]
    if clean:
        cmd.append("--clean")

    # Run process and capture output (non-streaming fallback)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = proc.stdout or ""
    err = proc.stderr or ""
    return proc.returncode, out, err


def main():
    # add margin for entire page
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("pptvo: Automated Voiceover Video from PPTX/PDF")

    ensure_dirs()

    # Input area (placed above script)
    st.subheader("Input")
    uploaded = st.file_uploader("Upload PPTX or PDF", type=["pdf", "pptx"], key="upload_presentation")
    if uploaded is not None:
        saved_name = save_uploaded(uploaded)
        st.success(f"Saved to input/{saved_name}")

    files = list_input_files()
    if not files:
        st.warning("No input files found in the `input/` directory. Upload one or add files to input/.")
        st.stop()

    selected = st.selectbox("Choose input file", files)

    language = st.text_input("TTS language code (e.g. en, id)", value="id")
    clean = st.checkbox("Clean temp before run", value=True)

    # Run pipeline button (main area)
    if st.button("Run Pipeline", key="run_pipeline_btn"):
        st.info(f"Running pipeline on {selected} (lang={language})")
        log_box = st.empty()
        progress = st.empty()
        with st.spinner("Processing... this may take a while"):
            # Stream subprocess output live
            cmd = [sys.executable, "-u", str(ROOT / "pptx_to_video.py"), "--file", selected, "--output", "output", "--language", language]
            if clean:
                cmd.append("--clean")

            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            lines = []
            try:
                for raw in proc.stdout:
                    line = raw.rstrip()
                    lines.append(line)
                    # Keep last N lines to avoid huge UI
                    last = "\n".join(lines[-1000:])
                    log_box.code(last)
            except Exception as e:
                lines.append(f"[streaming error] {e}")
                log_box.code("\n".join(lines[-1000:]))
            proc.wait()
            code = proc.returncode
            out = "\n".join(lines)
            err = ""

        st.subheader("Process Output")
        if out:
            st.code(out)
        if err:
            st.error("Errors:")
            st.code(err)

        if code == 0:
            st.success("Pipeline finished successfully.")
        else:
            st.error(f"Pipeline exited with code {code}")

        final_video = OUTPUT_DIR / "output.mp4"
        if final_video.exists():
            st.video(str(final_video))
            with open(final_video, "rb") as f:
                btn = st.download_button(label="Download final video", data=f, file_name=final_video.name)
        else:
            st.info("Final video not found in `output/output.mp4`. Check logs above.")

    # --- Script input UI (adaptive, centered) ---
    st.subheader("Voiceover Script (optional)")
    # Allow uploading a script.txt file
    script_upload = st.file_uploader("Upload script.txt", type=["txt"], key="script_upload")
    if script_upload is not None:
        dest = INPUT_DIR / "script.txt"
        with open(dest, "wb") as f:
            f.write(script_upload.getbuffer())
        st.success("Saved script to input/script.txt")

    # Load existing script.txt if present
    script_path = INPUT_DIR / "script.txt"
    existing_script = ""
    if script_path.exists():
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                existing_script = f.read()
        except Exception:
            existing_script = ""

    # Adaptive textarea height based on content lines
    def _textarea_height_for(text: str):
        lines = max(3, text.count("\n") + 1)
        # 22 px per line approx, clamp between 150 and 800
        h = min(800, max(150, lines * 22))
        return h

    script_text = st.text_area("Edit or paste voiceover script (use [SLIDE n] tags if desired)", value=existing_script, height=_textarea_height_for(existing_script))
    if st.button("Save script to input/script.txt", key="save_script_btn"):
        try:
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_text)
            st.success("Saved script to input/script.txt")
        except Exception as e:
            st.error(f"Failed to save script: {e}")

if __name__ == "__main__":
    main()

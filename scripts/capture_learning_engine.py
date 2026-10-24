"""Capture the unchanged public SC-900 Tk app with an original example bank.

The screenshot is a real Linux/Tk rendering, not a Windows package test or an
exam-content reproduction. All learner files live in a temporary directory.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main() -> None:
    repo, output = (Path(value).resolve() for value in sys.argv[1:3])
    output.mkdir(parents=True, exist_ok=True)
    revision = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    expected = "250e55565582f9e6dc1f5608f7701aea5e9e953f"
    if revision != expected:
        raise ValueError("Capture requires the reviewed source revision")
    sys.path.insert(0, str(repo))
    import app
    from PIL import ImageGrab

    examples = [
        ("Which control asks for another proof of identity after a password?", "Multi-factor authentication", "A public username"),
        ("Which access policy gives a service only the permissions it needs?", "Least privilege", "Unrestricted access"),
        ("Which record helps an analyst review a sign-in event?", "An authentication log", "A desktop wallpaper"),
        ("What should accompany an investigation conclusion?", "Supporting evidence and its limits", "An unsupported guess"),
        ("What should happen before a consequential automated action?", "Check the required authorization", "Assume a recommendation is permission"),
    ]
    questions = []
    for number, (prompt, correct, wrong) in enumerate(examples, 1):
        questions.append({
            "id": f"portfolio-example-{number}", "question_number": number,
            "prompt": prompt, "choices": {"A": correct, "B": wrong}, "correct": ["A"],
            "general_explanation": "This original example illustrates a basic defensive security practice.",
            "choice_explanations": {"A": "Matches the security practice in the question.", "B": "Does not provide the requested control or evidence."},
            "domain": "Security fundamentals", "domain_code": "1", "chapter": "Portfolio examples",
            "topics": ["Defensive security"], "objective_code": "1.1", "question_type": "multiple_choice",
            "source_name": "Original portfolio examples", "study_focus": "Core", "flagged_issues": [],
        })
    with tempfile.TemporaryDirectory(prefix="portfolio-engine-") as folder:
        root_dir = Path(folder)
        bank = root_dir / "portfolio_examples.json"
        bank.write_text(json.dumps({"title": "Original portfolio examples", "version": "1", "questions": questions}), encoding="utf-8")
        app.APP_DIR = root_dir
        app.USER_DATA_DIR = root_dir / "user_data"
        app.CHECKPOINT_DIR = app.USER_DATA_DIR / "checkpoints"
        app.BACKUP_DIR = app.USER_DATA_DIR / "backups"
        app.CONFIG_PATH = app.USER_DATA_DIR / "config.json"
        app.DEFAULT_BANK = bank
        window = app.tk.Tk()
        try:
            engine = app.TestingEngineApp(window)
            window.geometry("1240x620+0+0")
            engine.session_mode_var.set(app.MODE_PRACTICE)
            engine.session_count_var.set("5")
            engine.session_random_var.set(False)
            engine.start_custom_session()
            if len(engine.questions) != 5:
                raise ValueError("The real app did not start the five-question example session")
            window.update_idletasks()
            window.update()
            image = ImageGrab.grab(bbox=(0, 0, 1240, 620))
            image.save(output / "sc900-practice-linux.png")
            report = {
                "status": "PASS", "source_repository": "IXI-2773/Microsoft_SC-900_Test_Learning_Engine",
                "source_commit": revision, "platform": "Linux / Tk / Xvfb",
                "fixture": "Five original portfolio example questions; no learner history",
                "bank_sha256": hashlib.sha256(bank.read_bytes()).hexdigest(),
                "screenshot_sha256": hashlib.sha256((output / "sc900-practice-linux.png").read_bytes()).hexdigest(),
                "image_size": list(image.size), "runtime_session_questions": len(engine.questions),
                "scope": "Real practice UI only; no Windows executable or learning-outcome verification",
            }
            (output / "capture-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(report, indent=2))
        finally:
            window.destroy()


if __name__ == "__main__":
    main()

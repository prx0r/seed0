"""gitnotes tests: attach/read roundtrip, absence, tags."""
import json
import subprocess as sp

from gitnotes import attach, read, tag


def _repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    for a in (["init", "-q"], ["config", "user.email", "t@t"],
              ["config", "user.name", "t"], ["branch", "-M", "main"]):
        sp.run(["git", *a], cwd=r, check=True, capture_output=True)
    (r / "f.txt").write_text("x\n")
    sp.run(["git", "add", "."], cwd=r, check=True, capture_output=True)
    sp.run(["git", "commit", "-qm", "init"], cwd=r, check=True, capture_output=True)
    return r


def test_attach_read_roundtrip(tmp_path):
    r = _repo(tmp_path)
    sha = attach(str(r), "HEAD", "scores", {"verdict": "promote", "n": 3})
    assert len(sha) >= 7
    assert read(str(r), "HEAD", "scores") == {"verdict": "promote", "n": 3}
    assert read(str(r), "HEAD", "nope") is None
    assert tag(str(r), "success_demo", "HEAD")
    tags = sp.run(["git", "tag", "-l"], capture_output=True, text=True, cwd=r)
    assert "success_demo" in tags.stdout

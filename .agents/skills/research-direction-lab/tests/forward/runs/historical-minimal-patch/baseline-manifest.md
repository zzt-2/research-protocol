# Reproducible RED baseline manifest

- Git object: `53085bb5d1b7cc3e759e62af5c55397979402acc`
- Tree root: `.agents/skills/research-direction-lab/`
- Exclusions: paths containing `/__pycache__/`; suffixes `.pyc` and `.pyo`
- Sorted non-cache file count: `60`
- File digest: SHA256 of each Git blob's exact bytes
- Bundle serialization: for every path sorted by relative POSIX path, UTF-8 encode `<file_sha256><two ASCII spaces><relative_path><LF>`; concatenate all lines without a header
- Reproducible bundle SHA256: `fbd44ac762114e54f2f6fae90226487ff0748a43c1fa6e8ba57ff9b521274a87`

The earlier pre-patch capture `91f306ef72b54dc883b52a9683629b4dff54a0f6ce985d22bd34c33e3822f1ab` is retained in the original raw outputs as historical evidence, but its ad-hoc bundle serialization was not recorded. It is not the audit identity. The immutable Git object plus the algorithm above is the authoritative RED baseline and can be independently recomputed without trusting the working tree.

Reference implementation:

```python
import hashlib
import subprocess

commit = "53085bb5d1b7cc3e759e62af5c55397979402acc"
root = ".agents/skills/research-direction-lab/"
paths = subprocess.check_output(
    ["git", "ls-tree", "-r", "--name-only", commit, "--", root],
    text=True,
    encoding="utf-8",
).splitlines()
paths = sorted(
    path for path in paths
    if "/__pycache__/" not in path and not path.endswith((".pyc", ".pyo"))
)
lines = []
for path in paths:
    blob = subprocess.check_output(["git", "show", f"{commit}:{path}"])
    relative = path[len(root):]
    lines.append(f"{hashlib.sha256(blob).hexdigest()}  {relative}\n")
bundle = hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()
assert len(paths) == 60
assert bundle == "fbd44ac762114e54f2f6fae90226487ff0748a43c1fa6e8ba57ff9b521274a87"
```

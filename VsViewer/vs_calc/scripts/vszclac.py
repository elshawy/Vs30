from pathlib import Path
from vs_calc import VsProfile

examples_dir = Path(__file__).parent.resolve()
vsf_ffp = examples_dir / "SCPT_188664_Raw01.csv"
cpt = VsProfile.from_byte_stream(str(vsf_ffp))
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.core.team.recorder import Recorder
from apps.core.steps.tester import Tester

if __name__ == "__main__":
    input_memo_path = "C:\\Users\\user\\Documents\\projects\\SomeDocuments\\Note\\experiment\\memo.md"
    input_img_path = "C:\\Users\\user\\Documents\\projects\\SomeDocuments\\Note\\experiment\\img"
    output_note_path = "C:\\Users\\user\\Documents\\projects\\SomeDocuments\\Note\\experiment\\note.md"
    tester = Tester()
    tester.initialize()
    tester.run()
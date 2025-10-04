import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.adapters.yaml_adapter import YamlAdapter

from apps.core.team.recorder import Recorder

if __name__ == "__main__":
    input_memo_path = "C:\\Users\\user\\Documents\\projects\\SomeDocuments\\Note\\experiment\\memo.md"
    input_img_path = "C:\\Users\\user\\Documents\\projects\\SomeDocuments\\Note\\experiment\\img"
    output_note_path = "C:\\Users\\user\\Documents\\projects\\SomeDocuments\\Note\\experiment\\note.md"

    recorder = Recorder(input_memo_path, input_img_path, output_note_path)
    recorder.initialize()
    recorder.run()
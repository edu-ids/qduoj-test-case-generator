import os
import json
import hashlib
import shutil

def generate_info(folder_in, folder_out):
  test_cases = {}
  for filename in os.listdir(folder_in):
    if filename.endswith('.in'):
      base_name = os.path.splitext(filename)[0]
      input_name = filename
      output_name = base_name + '.out'
      input_size = os.path.getsize(os.path.join(folder_in, input_name))
      output_path = os.path.join(folder_out, output_name)
      with open(output_path, 'r') as f:
        output_content = f.read()
      output_size = len(output_content)
      stripped_output_md5 = hashlib.md5(output_content.strip().encode()).hexdigest()
      test_cases[base_name] = {
        'input_name': input_name,
        'input_size': input_size,
        'output_name': output_name,
        'output_size': output_size,
        'stripped_output_md5': stripped_output_md5
      }
  info = {
    'spj': False,
    'test_cases': test_cases
  }
  return info

def create_output_folder(output_folder):
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)
  for filename in os.listdir('in'):
    source_path = os.path.join('in', filename)
    destination_path = os.path.join(output_folder, filename)
    shutil.copy(source_path, destination_path)
  for filename in os.listdir('out'):
    source_path = os.path.join('out', filename)
    destination_path = os.path.join(output_folder, filename)
    shutil.copy(source_path, destination_path)

def zip_output_folder(output_folder, zip_filename):
  shutil.make_archive(zip_filename, 'zip', output_folder)

if __name__ == '__main__':
  info = generate_info('in', 'out')
  with open('info', 'w') as f:
    json.dump(info, f, indent=4)
  output_folder = 'output'
  create_output_folder(output_folder)
  info_path = os.path.join(output_folder, 'info')
  shutil.copy('info', info_path)
  zip_filename = 'output'
  zip_output_folder(output_folder, zip_filename)
  shutil.rmtree(output_folder)
  os.remove('info')
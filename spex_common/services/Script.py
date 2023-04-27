from glob import glob
import json
import os


def get_order(script_folder):
    manifest_path = os.path.join(script_folder, 'manifest.json')
    if not os.path.isfile(manifest_path):
        return 999

    with open(manifest_path, 'r') as manifest:
        data = json.load(manifest)

    return data.get('order', 999)


def scripts_list():
    folder = os.path.join(os.getenv('DATA_STORAGE'), 'Scripts', '*', '')
    scripts = [
        os.path.dirname(script) for script in glob(folder)
        if os.path.isfile(os.path.join(script, 'manifest.json'))
    ]
    return [
        os.path.basename(script) for script in sorted(scripts, key=get_order)
    ]


def get_script_structure(script_name: str = None):
    folder = os.path.join(os.getenv('DATA_STORAGE'), 'Scripts', script_name, '')

    pattern = f'{folder}manifest.json'

    if not os.path.isfile(pattern):
        return {}

    with open(pattern, 'r') as manifest:
        data = json.load(manifest)

    if data is None or len(data.items()) < 1:
        return {}

    result = data

    result.update(key=script_name)

    stages = result.get('stages')

    if stages is None or len(stages) < 1:
        return result

    stages = [{'name': stage, 'scripts': []} for stage in stages]

    pattern = os.path.join(folder, '*', 'manifest.json')

    for script_manifest in glob(pattern):
        if not os.path.isfile(script_manifest):
            continue

        with open(script_manifest, 'r') as manifest:
            data = json.load(manifest)
            stage = data.get('stage')

            if stage is None:
                continue

            stage = int(stage) - 1

            if stage >= len(stages[stage]):
                for index in range(stage - len(stages) + 1):
                    stages.append({'name': f'{len(stages)}', 'scripts': []})

            stages[stage]['scripts'].append(data)

    result.update({'stages': stages})

    return result

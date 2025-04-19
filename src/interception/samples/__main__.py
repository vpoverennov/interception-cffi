from pathlib import Path

samples_dir = Path(__file__).parent

print('Interception samples:')
for sample in samples_dir.glob('**/*.py'):
    if sample.name.startswith('_'):
        continue
    print(f'python -m interception.samples.{sample.stem}')

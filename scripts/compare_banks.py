from datetime import datetime

import requests
from clabe.banks import BANK_NAMES


def fetch_banxico_data():
    current_date = datetime.now().strftime('%d-%m-%Y')
    url = f'https://www.banxico.org.mx/cep/instituciones.do?fecha={current_date}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return dict(data.get('instituciones', []))
    except Exception as e:
        print(f'Error fetching data from Banxico: {e}')
        return {}


def compare_bank_data():
    current_banks = dict(BANK_NAMES)
    banxico_banks = fetch_banxico_data()

    differences = {'additions': {}, 'removals': {}, 'changes': {}}

    print('Comparing bank data...\n')

    # Check for additions (in Banxico but not in package)
    additions = {
        code: name for code, name in banxico_banks.items() if code not in current_banks
    }
    differences['additions'] = additions
    if additions:
        print('=== ADDITIONS (in Banxico but not in package) ===')
        for code, name in sorted(additions.items()):
            print(f'  {code}: {name}')
        print()

    # Check for removals (in package but not in Banxico)
    removals = {
        code: name for code, name in current_banks.items() if code not in banxico_banks
    }
    differences['removals'] = removals
    if removals:
        print('=== REMOVALS (in package but not in Banxico) ===')
        for code, name in sorted(removals.items()):
            print(f'  {code}: {name}')
        print()

    # Check for changes (different names for the same code)
    changes = {
        code: (current_banks[code], banxico_banks[code])
        for code in set(current_banks) & set(banxico_banks)
        if current_banks[code].upper() != banxico_banks[code].upper()
    }
    differences['changes'] = changes
    if changes:
        print('=== CHANGES (different names for the same code): Package -> Banxico ===')
        for code, (current_name, banxico_name) in sorted(changes.items()):
            print(f'  {code}: {current_name} -> {banxico_name}')
        print()

    if not additions and not removals and not changes:
        print('No differences found. The data is in sync.')

    return differences


if __name__ == '__main__':
    differences = compare_bank_data()

import argparse
import json

def parse_mt103(file_path):
    data = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith(":20:"):
            data['Transaction Reference'] = line[4:].strip()
        elif line.startswith(":32A:"):
            data['Value Date_Currency_Amount'] = line[5:].strip()
        elif line.startswith(":50K:"):
            data['Ordering Customer'] = line[5:].strip()
        elif line.startswith(":59:"):
            data['Beneficiary Customer'] = line[4:].strip()
        elif line.startswith(":71A:"):
            data['Details of Charges'] = line[5:].strip()
    return data

def convert_to_crypto_format(mt103_data, crypto):
    # Contoh format sederhana, bisa dikembangkan sesuai kebutuhan
    crypto_tx = {
        "tx_reference": mt103_data.get("Transaction Reference", ""),
        "amount": mt103_data.get("Value Date_Currency_Amount", ""),
        "from": mt103_data.get("Ordering Customer", ""),
        "to": mt103_data.get("Beneficiary Customer", ""),
        "charges": mt103_data.get("Details of Charges", ""),
        "crypto": crypto,
        "crypto_address": "example_crypto_address_here"
    }
    return crypto_tx

def main():
    parser = argparse.ArgumentParser(description="MT103 to Crypto converter")
    parser.add_argument("input_file", help="Path to MT103 text file")
    parser.add_argument("--output", choices=["json", "txt"], default="json", help="Output format")
    parser.add_argument("--crypto", choices=["bitcoin", "ethereum"], default="bitcoin", help="Crypto type")

    args = parser.parse_args()
    mt103_data = parse_mt103(args.input_file)
    crypto_tx = convert_to_crypto_format(mt103_data, args.crypto)

    if args.output == "json":
        print(json.dumps(crypto_tx, indent=4))
        with open("converted_transaction.json", "w") as f:
            json.dump(crypto_tx, f, indent=4)
    else:
        with open("converted_transaction.txt", "w") as f:
            for k, v in crypto_tx.items():
                f.write(f"{k}: {v}\n")
        print("Converted transaction saved to converted_transaction.txt")

if __name__ == "__main__":
    main()

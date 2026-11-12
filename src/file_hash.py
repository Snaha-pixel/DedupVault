
import hashlib

def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(4096)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    except FileNotFoundError:
        print("File not found!")
        return None


if __name__ == "__main__":
   path = input("Enter file path: ").strip().strip('"').strip("'")

    file_hash = calculate_file_hash(path)

    if file_hash:
        print("SHA-256 Hash:", file_hash)

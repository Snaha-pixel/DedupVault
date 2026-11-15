

from src.duplicate_check import check_duplicate


def main():

    while True:

        print("\n" + "=" * 45)
        print("             DEDUPVAULT")
        print("    Duplicate Backup Detection System")
        print("=" * 45)

        print("\n1. Upload a file")
        print("2. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            file_path = input(
                "\nEnter file path: "
            ).strip().strip('"').strip("'")

            check_duplicate(file_path)

        elif choice == "2":

            print("\nThank you for using DedupVault!")
            break

        else:

            print("\nInvalid choice! Please select 1 or 2.")


if __name__ == "__main__":
    main()

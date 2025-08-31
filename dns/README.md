# dns

This folder has some code to manage my DNS records.
In particular I want my DNS records to be:

*   **Understandable** – I should be able to explain what each record is for, why I added it, and whether it's safe to change or remove
*   **Easy to edit** – I want to be able to make changes with impunity, knowing I can quickly roll back to a known good configuration if something goes wrong.

These are the files in this folder:

*   `save_dns_records_as_yaml.rb` is a script creates a YAML snapshot of all my DNS records, as they're being served
*   `compare_dns_records.rb` is a script which compares two YAML snapshots, to see if anything's changed
*   `dns_records.yml` is the canonical statement of my DNS records is in `dns_records.yml`.

This includes comments explaining what each record is for, and changes to my DNS config will be committed to Git in this file.

Once a day, GitHub Actions will take a snapshot of my DNS records, then compare it to the canonical statement.
This will alert me if anything changes unexpectedly.

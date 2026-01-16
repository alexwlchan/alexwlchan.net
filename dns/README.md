# dns

This folder has some code to manage my DNS records.
In particular I want my DNS records to be:

*   **Understandable** – I should be able to explain what each record is for, why I added it, and whether it's safe to change or remove
*   **Easy to edit** – I want to be able to make changes with impunity, knowing I can quickly roll back to a known good configuration if something goes wrong.

This folder contains a snapshot of my current DNS records, and a test that checks the snapshot is up-to-date.
The test runs once a day or when I change the snapshot.

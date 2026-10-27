
def email_tool(recipient, subject, message):
    """Validate and prepare an email draft without sending it."""

    if not all(
        isinstance(value, str) and value.strip()
        for value in (recipient, subject, message)
    ):
        return {
            "success": False,
            "error": "Recipient, subject and message are required."
        }

    recipient = recipient.strip()
    subject = subject.strip()
    message = message.strip()

    if "@" not in recipient:
        return {"success": False, "error": "Invalid email address."}

    local, separator, domain = recipient.rpartition("@")
    if not local or not separator or "." not in domain or domain.startswith("."):
        return {"success": False, "error": "Invalid email address."}

    return {
        "success": True,
        "status": "Draft created; not sent.",
        "recipient": recipient,
        "subject": subject,
        "message": message
    }


def display_result(result):
    print("\n" + "=" * 50)
    print("                  EMAIL DRAFT")
    print("=" * 50)

    if not result["success"]:
        print(f"  Error: {result['error']}")
    else:
        print(f"  To      : {result['recipient']}")
        print(f"  Subject : {result['subject']}")
        print("-" * 50)
        print(result["message"])
        print("-" * 50)
        print(f"  Status  : {result['status']}")

    print("=" * 50)


if __name__ == "__main__":
    result = email_tool(
        "student@example.com",
        "Daily Task Update",
        "The assigned task has been completed."
    )
    display_result(result)

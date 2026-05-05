const users_key = document.getElementById('api_key');
const copyButton = document.getElementById('copy_button');

copyButton.addEventListener("click", function() {;
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(users_key.textContent)
            .then(() => {
                alert("Copied to clipboard!");
            })
            .catch(err => {
                console.error("Clipboard copy failed:", err);
                alert("Failed to copy text.");
            });
    } else {
        const tempInput = document.createElement("textarea");
        tempInput.value = users_key.textContent;
        document.body.appendChild(tempInput);
        tempInput.select();
        try {
            document.execCommand("copy");
            alert("Copied to clipboard!");
        } catch (err) {
            console.error("Fallback copy failed:", err);
            alert("Failed to copy text.");
        }
        document.body.removeChild(tempInput);
    }
});

// static/js/copy_to_clipboard.js

document.addEventListener("DOMContentLoaded", function () {
    const copyButtons = document.querySelectorAll(".copyBtn");

    copyButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const targetId = button.getAttribute("data-copy-target");

            const copyElement = document.getElementById(targetId);

            if (copyElement) {
                const range = document.createRange();
                range.selectNodeContents(copyElement);

                const selection = window.getSelection();
                selection.removeAllRanges();

                selection.addRange(range);

                try {
                    const successful = document.execCommand('copy');
                    if (successful) {
                        document.getElementById("copyMessage").innerHTML = "Copied!";
                    } else {
                        document.getElementById("copyMessage").innerHTML = "Failed to copy!";
                    }
                } catch (err) {
                    console.error('Error copying text: ', err);
                }

                selection.removeAllRanges();
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll("pre").forEach(function (block) {

        const text = block.innerText.trim();

        if (!text) {
            return;
        }

        const button = document.createElement("button");

        button.type = "button";
        button.className = "copy-btn";
        button.innerText = "Copy";

        button.addEventListener("click", async function () {

            try {

                await navigator.clipboard.writeText(text);

                button.innerText = "Copied ✓";
                button.classList.add("copied");

                setTimeout(function () {
                    button.innerText = "Copy";
                    button.classList.remove("copied");
                }, 1500);

            } catch (error) {

                button.innerText = "Copy failed";

            }

        });

        block.insertAdjacentElement("afterend", button);

    });

});
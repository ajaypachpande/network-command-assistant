document.addEventListener("DOMContentLoaded", function () {

    // ======================================================
    // THEME
    // ======================================================

    const savedTheme =
        localStorage.getItem("network-assistant-theme") || "system";

    const root = document.documentElement;

    function applyTheme(theme) {

        if (theme === "system") {
            root.setAttribute("data-theme", "system");
        } else {
            root.setAttribute("data-theme", theme);
        }

        localStorage.setItem(
            "network-assistant-theme",
            theme
        );
    }


    applyTheme(savedTheme);


    const themeSelect =
        document.getElementById("theme-select");


    if (themeSelect) {

        themeSelect.value = savedTheme;

        themeSelect.addEventListener(
            "change",
            function () {

                applyTheme(
                    themeSelect.value
                );

            }
        );
    }


    // ======================================================
    // COPY COMMAND BUTTONS
    // ======================================================

    document
        .querySelectorAll("pre")
        .forEach(function (block) {

            const text =
                block.innerText.trim();


            if (!text) {
                return;
            }


            // Avoid adding Copy to large diagrams / flows
            const looksLikeDiagram =
                text.includes("↓") ||
                text.includes("┌") ||
                text.includes("└") ||
                text.includes("├") ||
                text.includes("│") ||
                text.split("\n").length > 9;


            if (looksLikeDiagram) {
                return;
            }


            const button =
                document.createElement("button");


            button.type =
                "button";


            button.className =
                "copy-btn";


            button.innerText =
                "COPY CLI";


            button.addEventListener(
                "click",
                async function () {

                    try {

                        await navigator.clipboard.writeText(
                            text
                        );


                        button.innerText =
                            "COPIED ✓";


                        button.classList.add(
                            "copied"
                        );


                        setTimeout(
                            function () {

                                button.innerText =
                                    "COPY CLI";


                                button.classList.remove(
                                    "copied"
                                );

                            },
                            1500
                        );

                    } catch (error) {

                        button.innerText =
                            "COPY FAILED";

                    }

                }
            );


            block.insertAdjacentElement(
                "afterend",
                button
            );

        });

});
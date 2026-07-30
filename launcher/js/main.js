document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("form");

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const data = new FormData(form);

        await fetch("/play", {
            method: "POST",
            body: data
        });

        // Fecha a janela do navegador após salvar as configurações
        window.close();

    });

});
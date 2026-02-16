const logoutTrigger = document.getElementById("ModalLogout");
const logoutModal = document.getElementById("logoutModal");
const cancelLogoutBtn = document.getElementById("Cancel");

logoutTrigger.addEventListener("click", () => {
    logoutModal.style.display = "flex";
});

cancelLogoutBtn.addEventListener("click", () => {
    logoutModal.style.display = "none";
});

window.addEventListener("click", (e) => {
    if (e.target === logoutModal) {
        logoutModal.style.display = "none";
    }
});
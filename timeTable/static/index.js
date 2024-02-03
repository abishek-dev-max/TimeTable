function resetForm() {
  document.getElementById("form").reset();
}
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form");
  const submitBtn = document.getElementById("submitBtn");

  form.addEventListener("input", function () {
    const requiredFields = form.querySelectorAll("[required]");
    const allFilled = [...requiredFields].every(
      (field) => field.value.trim() !== ""
    );

    submitBtn.disabled = !allFilled;
  });
});

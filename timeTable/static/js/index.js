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

document.addEventListener("DOMContentLoaded", function () {
  var departmentDropdown = document.getElementById("department");
  var staffNameDropdown = document.getElementById("staffName");

  var departmentToStaffMap = departmentToStaff;
  function updateStaffNames() {
    staffNameDropdown.innerHTML = "";

    var selectedDepartment = departmentDropdown.value;

    if (selectedDepartment in departmentToStaffMap) {
      var uniqueStaffNames = new Set(departmentToStaffMap[selectedDepartment]);
      var sortedStaffNames = Array.from(uniqueStaffNames).sort();
      sortedStaffNames.forEach(function (staffName) {
        var option = document.createElement("option");
        option.value = staffName;
        option.text = staffName;
        staffNameDropdown.add(option);
      });
    }
  }

  departmentDropdown.addEventListener("change", updateStaffNames);

  updateStaffNames();
});
